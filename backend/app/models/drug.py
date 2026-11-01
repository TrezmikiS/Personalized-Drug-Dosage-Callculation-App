from sqlalchemy import Column, Integer, String, Numeric, Boolean, DateTime, func
from sqlalchemy.orm import relationship
from backend.app.database import Base


class Drug(Base):
    __tablename__ = "drugs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True, index=True)
    active_ingredient = Column(String(100), nullable=False)
    standard_dose_mg = Column(Numeric(8, 2), nullable=False)
    therapeutic_range_min = Column(Numeric(8, 2), nullable=False)
    therapeutic_range_max = Column(Numeric(8, 2), nullable=False)
    renal_clearance_flag = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    calculation_logs = relationship("CalculationLog", back_populates="drug", cascade="all, delete-orphan")
