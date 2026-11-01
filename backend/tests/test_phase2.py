"""Unit and Integration Tests for Phase 2:
- Cockcroft-Gault, Devine IBW, ABW formulas
- Narrow Therapeutic Index (NTI) drug dosage adjustments
- Pydantic schema physiological input validation
- 16 Clinical Virtual Patient Scenarios (Sanal Hasta Veri Seti)
- End-to-end API endpoints (/api/calculate, /api/calculate/logs, /api/drugs)
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from pydantic import ValidationError

from backend.app.database import Base, get_db
from backend.app.models.drug import Drug
from backend.app.models.calculation_log import CalculationLog
from backend.app.main import app
from backend.app.algorithms.renal import (
    calculate_ibw,
    calculate_abw,
    determine_weight_for_crcl,
    calculate_cockcroft_gault,
)
from backend.app.algorithms.dosage import adjust_dosage
from backend.app.schemas.dosage_schema import CalculationRequest

# Setup isolated in-memory test database for Phase 2
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(autouse=True)
def setup_database():
    app.dependency_overrides[get_db] = override_get_db
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    # Seed standard drugs for calculation tests
    db.add_all([
        Drug(
            id=1,
            name="Vankomisin",
            active_ingredient="Vancomycin Hydrochloride",
            standard_dose_mg=1000.0,
            therapeutic_range_min=10.0,
            therapeutic_range_max=20.0,
            renal_clearance_flag=True,
        ),
        Drug(
            id=2,
            name="Digoksin",
            active_ingredient="Digoxin",
            standard_dose_mg=0.25,
            therapeutic_range_min=0.8,
            therapeutic_range_max=2.0,
            renal_clearance_flag=True,
        ),
        Drug(
            id=3,
            name="Lityum",
            active_ingredient="Lithium Carbonate",
            standard_dose_mg=300.0,
            therapeutic_range_min=0.6,
            therapeutic_range_max=1.2,
            renal_clearance_flag=True,
        ),
    ])
    db.commit()
    db.close()
    yield
    Base.metadata.drop_all(bind=engine)
    app.dependency_overrides.pop(get_db, None)


# ==========================================
# 1. RENAL ALGORITHM UNIT TESTS
# ==========================================

def test_ibw_devine_formula():
    # 175 cm ~= 68.897 inches -> 8.897 inches over 60
    # Male: 50 + 2.3 * 8.897 ~= 70.46 kg
    ibw_male = calculate_ibw(height_cm=175.0, gender="male")
    assert 70.0 <= ibw_male <= 71.0

    # Female: 45.5 + 2.3 * 8.897 ~= 65.96 kg
    ibw_female = calculate_ibw(height_cm=175.0, gender="female")
    assert 65.5 <= ibw_female <= 66.5


def test_abw_for_obese_patient():
    ibw = 70.0
    actual_weight = 110.0  # > 1.2 * 70 = 84 kg -> Obese
    # ABW = 70 + 0.4 * (110 - 70) = 70 + 16 = 86.0 kg
    abw = calculate_abw(actual_weight, ibw)
    assert abw == 86.0


def test_weight_determination_underweight_and_normal():
    # Underweight: Actual < IBW -> should use Actual weight
    weight_info = determine_weight_for_crcl(actual_weight_kg=50.0, height_cm=175.0, gender="male")
    assert weight_info["weight_used_kg"] == 50.0
    assert weight_info["weight_type_used"] == "ACTUAL"
    assert weight_info["is_obese"] is False

    # Obese: Actual > 1.2 * IBW -> should use ABW
    weight_info_obese = determine_weight_for_crcl(actual_weight_kg=120.0, height_cm=175.0, gender="male")
    assert weight_info_obese["weight_type_used"] == "ABW"
    assert weight_info_obese["is_obese"] is True

    # No height provided -> defaults to Actual
    weight_info_no_height = determine_weight_for_crcl(actual_weight_kg=80.0, height_cm=None, gender="male")
    assert weight_info_no_height["weight_used_kg"] == 80.0
    assert weight_info_no_height["weight_type_used"] == "ACTUAL"


def test_cockcroft_gault_female_factor():
    # Male calculation
    res_male = calculate_cockcroft_gault(age=60, actual_weight_kg=72.0, serum_creatinine=1.0, gender="male")
    # Female calculation with exact same parameters
    res_female = calculate_cockcroft_gault(age=60, actual_weight_kg=72.0, serum_creatinine=1.0, gender="female")
    
    # CrCl male = (80 * 72) / (72 * 1) = 80.0 mL/min
    assert res_male["calculated_crcl"] == 80.0
    # CrCl female = 80.0 * 0.85 = 68.0 mL/min
    assert res_female["calculated_crcl"] == 68.0


def test_cockcroft_gault_input_validation():
    with pytest.raises(ValueError, match="strictly positive"):
        calculate_cockcroft_gault(age=50, actual_weight_kg=70.0, serum_creatinine=0.0, gender="male")

    with pytest.raises(ValueError, match="only for adults"):
        calculate_cockcroft_gault(age=15, actual_weight_kg=50.0, serum_creatinine=1.0, gender="male")


# ==========================================
# 2. DOSAGE ADJUSTMENT ALGORITHM UNIT TESTS
# ==========================================

def test_dosage_vancomycin_tiers():
    # CrCl >= 50: Normal
    res_norm = adjust_dosage("Vankomisin", standard_dose_mg=1000.0, crcl=65.0, weight_kg=75.0)
    assert res_norm.warning_level == "NORMAL"
    assert res_norm.calculated_dose_mg == 1000.0
    assert res_norm.dosing_interval_hours == 12
    assert not res_norm.warning_flag

    # 30 <= CrCl < 50: Interval extension
    res_mod1 = adjust_dosage("Vankomisin", standard_dose_mg=1000.0, crcl=40.0, weight_kg=75.0)
    assert res_mod1.warning_level == "WARNING"
    assert res_mod1.calculated_dose_mg == 1000.0
    assert res_mod1.dosing_interval_hours == 24
    assert res_mod1.warning_flag

    # 10 <= CrCl < 30: 50% dose reduction
    res_mod2 = adjust_dosage("Vankomisin", standard_dose_mg=1000.0, crcl=20.0, weight_kg=75.0)
    assert res_mod2.warning_level == "WARNING"
    assert res_mod2.calculated_dose_mg == 500.0
    assert res_mod2.dosing_interval_hours == 24
    assert res_mod2.warning_flag

    # CrCl < 10: Critical Hold
    res_crit = adjust_dosage("Vankomisin", standard_dose_mg=1000.0, crcl=8.0, weight_kg=75.0)
    assert res_crit.warning_level == "CRITICAL"
    assert res_crit.calculated_dose_mg == 0.0
    assert res_crit.warning_flag


def test_dosage_digoxin_tiers():
    # Normal: 0.25 mg
    res_norm = adjust_dosage("Digoksin", standard_dose_mg=0.25, crcl=75.0, weight_kg=70.0)
    assert res_norm.warning_level == "NORMAL"
    assert res_norm.calculated_dose_mg == 0.25

    # Moderate: 50% reduction -> 0.125 mg
    res_mod = adjust_dosage("Digoksin", standard_dose_mg=0.25, crcl=35.0, weight_kg=70.0)
    assert res_mod.warning_level == "WARNING"
    assert res_mod.calculated_dose_mg == 0.125

    # Severe: 75% reduction -> 0.0625 mg
    res_crit = adjust_dosage("Digoksin", standard_dose_mg=0.25, crcl=7.0, weight_kg=70.0)
    assert res_crit.warning_level == "CRITICAL"
    assert res_crit.calculated_dose_mg == 0.0625


def test_dosage_lithium_tiers():
    # Normal: 300 mg BID
    res_norm = adjust_dosage("Lityum", standard_dose_mg=300.0, crcl=60.0, weight_kg=80.0)
    assert res_norm.warning_level == "NORMAL"
    assert res_norm.calculated_dose_mg == 300.0

    # Moderate: 150 mg
    res_mod = adjust_dosage("Lityum", standard_dose_mg=300.0, crcl=30.0, weight_kg=80.0)
    assert res_mod.warning_level == "WARNING"
    assert res_mod.calculated_dose_mg == 150.0

    # Severe: Contraindicated -> 0.0 mg
    res_crit = adjust_dosage("Lityum", standard_dose_mg=300.0, crcl=5.0, weight_kg=80.0)
    assert res_crit.warning_level == "CRITICAL"
    assert res_crit.calculated_dose_mg == 0.0


# ==========================================
# 3. PYDANTIC SCHEMA VALIDATION TESTS
# ==========================================

def test_pydantic_adult_age_validation():
    # Age < 18 must fail validation
    with pytest.raises(ValidationError):
        CalculationRequest(
            patient_age=16,
            patient_weight_kg=60.0,
            patient_gender="male",
            serum_creatinine=1.0,
            drug_id=1
        )


def test_pydantic_creatinine_validation():
    # Serum creatinine <= 0 must fail
    with pytest.raises(ValidationError):
        CalculationRequest(
            patient_age=45,
            patient_weight_kg=70.0,
            patient_gender="female",
            serum_creatinine=0.0,
            drug_id=1
        )


def test_pydantic_gender_normalization():
    # 'erkek' should normalize to 'male'
    req1 = CalculationRequest(
        patient_age=45,
        patient_weight_kg=70.0,
        patient_gender="erkek",
        serum_creatinine=1.0,
        drug_id=1
    )
    assert req1.patient_gender.value == "male"

    # 'kadın' should normalize to 'female'
    req2 = CalculationRequest(
        patient_age=45,
        patient_weight_kg=65.0,
        patient_gender="kadın",
        serum_creatinine=1.0,
        drug_id=1
    )
    assert req2.patient_gender.value == "female"


# ==========================================
# 4. 16 VIRTUAL PATIENT SCENARIOS (SANAL HASTA SETİ)
# ==========================================

@pytest.mark.parametrize("scenario_id,age,weight,height,gender,scr,drug_id,expected_tier", [
    (1, 25, 75.0, 180.0, "male", 0.9, 1, "NORMAL"),      # Genç sağlıklı erkek (CrCl ~133 mL/min)
    (2, 28, 58.0, 165.0, "female", 0.7, 1, "NORMAL"),    # Genç sağlıklı kadın (CrCl ~109 mL/min)
    (3, 48, 125.0, 172.0, "male", 1.2, 1, "NORMAL"),     # Obez erkek (ABW uygulanmalı, CrCl ~90 mL/min)
    (4, 52, 105.0, 160.0, "female", 1.1, 1, "NORMAL"),   # Obez kadın (ABW uygulanmalı, CrCl ~71 mL/min)
    (5, 78, 45.0, 165.0, "female", 1.4, 2, "WARNING"),   # Zayıf / kaşektik geriatrik kadın (CrCl ~23 mL/min)
    (6, 68, 74.0, 175.0, "male", 1.8, 1, "WARNING"),     # Yaşlı erkek - Vankomisin orta yetmezlik (CrCl ~41 mL/min)
    (7, 84, 62.0, 168.0, "male", 2.2, 2, "WARNING"),     # Çok yaşlı erkek - Digoksin orta yetmezlik (CrCl ~21 mL/min)
    (8, 55, 70.0, 175.0, "male", 9.0, 1, "CRITICAL"),    # Akut böbrek yetmezliği / anürik (CrCl = 9.18 mL/min < 10)
    (9, 32, 65.0, 170.0, "female", 0.8, 3, "NORMAL"),    # Bipolar genç kadın - Lityum normal (CrCl ~103 mL/min)
    (10, 59, 82.0, 176.0, "male", 2.1, 3, "WARNING"),    # Bipolar erkek - Lityum orta yetmezlik (CrCl ~43 mL/min)
    (11, 72, 60.0, 160.0, "female", 6.0, 3, "CRITICAL"), # Yaşlı kadın - Lityum Kontrendike (CrCl = 8.03 mL/min < 10)
    (12, 45, 70.0, None, "male", 1.0, 1, "NORMAL"),      # Boy girilmemiş hasta (Actual weight, CrCl ~92 mL/min)
    (13, 65, 70.0, 165.0, "female", 1.5, 1, "WARNING"),  # Kadın hasta (CrCl ~36 mL/min, Sarı uyarı)
    (14, 40, 75.0, 175.0, "male", 1.4, 1, "NORMAL"),     # Normal erkek hasta (CrCl ~74 mL/min, Yeşil rozet)
    (15, 75, 70.0, 170.0, "male", 7.5, 2, "CRITICAL"),   # Son dönem yaşlı erkek (CrCl = 8.42 mL/min < 10, Kırmızı alarm)
    (16, 50, 140.0, 185.0, "male", 3.0, 1, "WARNING"),   # Ağır obez ileri yetmezlik (CrCl ~44 mL/min)
])
def test_virtual_patient_dataset(scenario_id, age, weight, height, gender, scr, drug_id, expected_tier):
    client = TestClient(app)
    payload = {
        "patient_age": age,
        "patient_weight_kg": weight,
        "patient_height_cm": height,
        "patient_gender": gender,
        "serum_creatinine": scr,
        "drug_id": drug_id
    }
    response = client.post("/api/calculate", json=payload)
    assert response.status_code == 201, f"Failed for scenario {scenario_id}: {response.text}"
    data = response.json()
    assert data["warning_level"] == expected_tier, f"Mismatch in scenario {scenario_id}: got {data['warning_level']} expected {expected_tier}"
    assert data["calculated_crcl"] > 0
    assert data["log_id"] is not None


# ==========================================
# 5. INTEGRATION & ENDPOINT TESTS
# ==========================================

def test_api_calculate_and_audit_log():
    client = TestClient(app)
    payload = {
        "patient_age": 65,
        "patient_weight_kg": 75.0,
        "patient_height_cm": 175.0,
        "patient_gender": "male",
        "serum_creatinine": 1.5,
        "drug_id": 1
    }
    response = client.post("/api/calculate", json=payload)
    assert response.status_code == 201
    result = response.json()
    assert result["drug_name"] == "Vankomisin"
    assert result["weight_type_used"] == "ACTUAL"
    assert "log_id" in result

    # Check that calculation log is readable via GET /api/calculate/logs
    logs_res = client.get("/api/calculate/logs")
    assert logs_res.status_code == 200
    logs_list = logs_res.json()
    assert len(logs_list) >= 1
    assert logs_list[0]["id"] == result["log_id"]
    assert logs_list[0]["patient_age"] == 65


def test_api_drugs_endpoints():
    client = TestClient(app)
    # Get all drugs
    res = client.get("/api/drugs")
    assert res.status_code == 200
    drugs = res.json()
    assert len(drugs) == 3
    names = [d["name"] for d in drugs]
    assert "Vankomisin" in names
    assert "Digoksin" in names
    assert "Lityum" in names

    # Get single drug
    single_res = client.get(f"/api/drugs/{drugs[0]['id']}")
    assert single_res.status_code == 200
    assert single_res.json()["name"] == drugs[0]["name"]

    # Not found drug
    not_found = client.get("/api/drugs/99999")
    assert not_found.status_code == 404


def test_api_calculate_not_found_drug():
    client = TestClient(app)
    payload = {
        "patient_age": 45,
        "patient_weight_kg": 70.0,
        "patient_gender": "male",
        "serum_creatinine": 1.0,
        "drug_id": 99999
    }
    response = client.post("/api/calculate", json=payload)
    assert response.status_code == 404
    assert "does not exist" in response.json()["detail"]
