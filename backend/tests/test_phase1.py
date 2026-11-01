import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.app.database import Base, get_db
from backend.app.models.drug import Drug
from backend.app.models.calculation_log import CalculationLog
from backend.app.main import app

from sqlalchemy.pool import StaticPool

# Setup in-memory SQLite database with StaticPool for unit tests
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


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_root_endpoint():
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    assert "version" in data


def test_db_health_endpoint():
    client = TestClient(app)
    response = client.get("/health/db")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "database": "connected"}


def test_seed_drugs_endpoint():
    client = TestClient(app)
    response = client.post("/api/seed-drugs")
    assert response.status_code == 201
    assert response.json()["count"] == 3

    # Seed again should not duplicate
    response_again = client.post("/api/seed-drugs")
    assert response_again.status_code == 201
    assert "already contains" in response_again.json()["message"]


def test_drug_and_calculation_log_orm():
    db = TestingSessionLocal()
    drug = Drug(
        name="Vankomisin",
        active_ingredient="Vancomycin HCl",
        standard_dose_mg=1000.0,
        therapeutic_range_min=10.0,
        therapeutic_range_max=20.0,
        renal_clearance_flag=True,
    )
    db.add(drug)
    db.commit()
    db.refresh(drug)

    assert drug.id is not None

    log = CalculationLog(
        patient_age=70,
        patient_weight_kg=68.0,
        patient_gender="erkek",
        serum_creatinine=1.5,
        calculated_crcl=42.5,
        drug_id=drug.id,
        calculated_dose_mg=500.0,
        warning_flag=True,
        warning_message="Orta derece böbrek yetmezliği. Doz azaltıldı.",
    )
    db.add(log)
    db.commit()
    db.refresh(log)

    assert log.id is not None
    assert log.drug.name == "Vankomisin"
    assert len(drug.calculation_logs) == 1
    db.close()
