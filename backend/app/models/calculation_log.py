from sqlalchemy import Column, Integer, String, Numeric, Boolean, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from backend.app.database import Base


class CalculationLog(Base):
    __tablename__ = "calculation_logs"

    id = Column(Integer, primary_key=True, index=True)
    patient_age = Column(Integer, nullable=False)
    patient_weight_kg = Column(Numeric(5, 2), nullable=False)
    patient_gender = Column(String(10), nullable=False)
    serum_creatinine = Column(Numeric(4, 2), nullable=False)
    calculated_crcl = Column(Numeric(6, 2), nullable=False)
    drug_id = Column(Integer, ForeignKey("drugs.id", ondelete="SET NULL"), nullable=True)
    calculated_dose_mg = Column(Numeric(8, 2), nullable=False)
    warning_flag = Column(Boolean, default=False, nullable=False)
    warning_message = Column(Text, nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    drug = relationship("Drug", back_populates="calculation_logs")
