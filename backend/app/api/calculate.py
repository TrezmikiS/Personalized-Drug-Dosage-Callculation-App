"""API routes for dosage calculations and audit logging.
"""

from datetime import datetime, timezone
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.models.drug import Drug
from backend.app.models.calculation_log import CalculationLog
from backend.app.schemas.dosage_schema import (
    CalculationRequest,
    CalculationResponse,
    CalculationLogResponse,
)
from backend.app.algorithms.renal import calculate_cockcroft_gault
from backend.app.algorithms.dosage import adjust_dosage

router = APIRouter(prefix="/api/calculate", tags=["Calculations"])


@router.post("", response_model=CalculationResponse, status_code=status.HTTP_201_CREATED)
def perform_dosage_calculation(
    payload: CalculationRequest,
    db: Session = Depends(get_db)
):
    """Calculates patient renal clearance (CrCl) and personalized drug dosage.

    Steps:
      1. Validates patient physiological parameters via Pydantic.
      2. Fetches target drug parameters from PostgreSQL.
      3. Computes Cockcroft-Gault CrCl (with IBW/ABW correction if height provided).
      4. Adjusts dosage and dosing interval according to clinical guidelines.
      5. Commits an immutable audit trail to calculation_logs table.
      6. Returns structured clinical recommendations with risk badges.
    """
    drug = db.query(Drug).filter(Drug.id == payload.drug_id).first()
    if not drug:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Drug with ID {payload.drug_id} does not exist in database."
        )

    # 1. Calculate Cockcroft-Gault Creatinine Clearance
    renal_res = calculate_cockcroft_gault(
        age=payload.patient_age,
        actual_weight_kg=payload.patient_weight_kg,
        serum_creatinine=payload.serum_creatinine,
        gender=payload.patient_gender.value,
        height_cm=payload.patient_height_cm
    )

    # 2. Compute personalized dosage adjustment and clinical warnings
    dosage_res = adjust_dosage(
        drug_name=drug.name,
        standard_dose_mg=float(drug.standard_dose_mg),
        crcl=renal_res["calculated_crcl"],
        weight_kg=renal_res["weight_used_kg"]
    )

    # 3. Create persistent audit log
    log_entry = CalculationLog(
        patient_age=payload.patient_age,
        patient_weight_kg=payload.patient_weight_kg,
        patient_gender=payload.patient_gender.value,
        serum_creatinine=payload.serum_creatinine,
        calculated_crcl=renal_res["calculated_crcl"],
        drug_id=drug.id,
        calculated_dose_mg=dosage_res.calculated_dose_mg,
        warning_flag=dosage_res.warning_flag,
        warning_message=dosage_res.warning_message
    )

    db.add(log_entry)
    db.commit()
    db.refresh(log_entry)

    # 4. Construct comprehensive response
    return CalculationResponse(
        log_id=log_entry.id,
        drug_id=drug.id,
        drug_name=drug.name,
        active_ingredient=drug.active_ingredient,
        patient_age=payload.patient_age,
        patient_gender=payload.patient_gender.value,
        patient_weight_kg=payload.patient_weight_kg,
        patient_height_cm=payload.patient_height_cm,
        calculated_crcl=renal_res["calculated_crcl"],
        ibw=renal_res["ibw"],
        weight_used_kg=renal_res["weight_used_kg"],
        weight_type_used=renal_res["weight_type_used"],
        standard_dose_mg=float(drug.standard_dose_mg),
        calculated_dose_mg=dosage_res.calculated_dose_mg,
        dosing_interval_hours=dosage_res.dosing_interval_hours,
        warning_level=dosage_res.warning_level,
        warning_flag=dosage_res.warning_flag,
        warning_message=dosage_res.warning_message,
        timestamp=log_entry.timestamp or datetime.now(timezone.utc)
    )


@router.get("/logs", response_model=List[CalculationLogResponse])
def get_calculation_logs(
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """Retrieves recent clinical dosage calculation audit logs."""
    logs = (
        db.query(CalculationLog)
        .order_by(CalculationLog.timestamp.desc())
        .limit(limit)
        .all()
    )
    return logs
