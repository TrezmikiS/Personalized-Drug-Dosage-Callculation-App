"""Pydantic schemas for input validation and API serialization.
"""

from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, field_validator, ConfigDict


class GenderEnum(str, Enum):
    MALE = "male"
    FEMALE = "female"


class CalculationRequest(BaseModel):
    """Input payload for dosage and CrCl calculation."""
    patient_age: int = Field(
        ...,
        ge=18,
        le=120,
        description="Patient age in years. Clinically validated for adults 18 to 120."
    )
    patient_weight_kg: float = Field(
        ...,
        gt=20.0,
        le=350.0,
        description="Patient weight in kg (must be between 20.0 and 350.0 kg)."
    )
    patient_height_cm: Optional[float] = Field(
        default=None,
        ge=100.0,
        le=250.0,
        description="Patient height in cm (optional, 100.0 to 250.0 cm for IBW/ABW correction)."
    )
    patient_gender: GenderEnum = Field(
        ...,
        description="Patient biological gender ('male' or 'female')."
    )
    serum_creatinine: float = Field(
        ...,
        ge=0.1,
        le=25.0,
        description="Serum creatinine level in mg/dL (must be between 0.1 and 25.0 mg/dL)."
    )
    drug_id: int = Field(
        ...,
        gt=0,
        description="Unique identifier of the target drug from database."
    )

    @field_validator("patient_gender", mode="before")
    @classmethod
    def normalize_gender(cls, value: str) -> str:
        if isinstance(value, str):
            val = value.strip().lower()
            if val in ["male", "erkek", "m"]:
                return "male"
            if val in ["female", "kadin", "kadın", "f"]:
                return "female"
        return value

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "patient_age": 65,
                "patient_weight_kg": 78.5,
                "patient_height_cm": 175.0,
                "patient_gender": "male",
                "serum_creatinine": 1.4,
                "drug_id": 1
            }
        }
    )


class CalculationResponse(BaseModel):
    """Comprehensive calculation output response."""
    log_id: int
    drug_id: int
    drug_name: str
    active_ingredient: str
    patient_age: int
    patient_gender: str
    patient_weight_kg: float
    patient_height_cm: Optional[float]
    calculated_crcl: float
    ibw: Optional[float]
    weight_used_kg: float
    weight_type_used: str
    standard_dose_mg: float
    calculated_dose_mg: float
    dosing_interval_hours: Optional[int]
    warning_level: str  # NORMAL, WARNING, CRITICAL
    warning_flag: bool
    warning_message: str
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)


class CalculationLogResponse(BaseModel):
    """Historical audit log item."""
    id: int
    patient_age: int
    patient_weight_kg: float
    patient_gender: str
    serum_creatinine: float
    calculated_crcl: float
    drug_id: Optional[int]
    calculated_dose_mg: float
    warning_flag: bool
    warning_message: Optional[str]
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)


class DrugResponse(BaseModel):
    """Drug entity serialization schema."""
    id: int
    name: str
    active_ingredient: str
    standard_dose_mg: float
    therapeutic_range_min: float
    therapeutic_range_max: float
    renal_clearance_flag: bool
    created_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)
