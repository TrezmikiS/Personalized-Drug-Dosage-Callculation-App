"""API routes for drug entities and clinical parameters.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.models.drug import Drug
from backend.app.schemas.dosage_schema import DrugResponse

router = APIRouter(prefix="/api/drugs", tags=["Drugs"])


@router.get("", response_model=List[DrugResponse])
def get_all_drugs(db: Session = Depends(get_db)):
    """Retrieves all registered Narrow Therapeutic Index (NTI) drugs."""
    drugs = db.query(Drug).order_by(Drug.id).all()
    return drugs


@router.get("/{drug_id}", response_model=DrugResponse)
def get_drug_by_id(drug_id: int, db: Session = Depends(get_db)):
    """Retrieves details of a specific drug by its primary key ID."""
    drug = db.query(Drug).filter(Drug.id == drug_id).first()
    if not drug:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Drug with ID {drug_id} not found."
        )
    return drug
