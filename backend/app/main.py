from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text

from backend.app.database import engine, Base, get_db
from backend.app.models.drug import Drug
from backend.app.models.calculation_log import CalculationLog


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables automatically on startup if database is reachable
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        print(f"[Lifespan Warning] Could not auto-create database tables on startup: {e}")
    yield


app = FastAPI(
    title="Personalised Drug Dosage Calculation API",
    description="Backend calculation engine for Narrow Therapeutic Index (NTI) drug dosage and renal clearance (Cockcroft-Gault).",
    version="1.0.0",
    lifespan=lifespan
)

# CORS setup for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "project": "Personalised Drug Dosage Calculation App",
        "version": "1.0.0",
        "status": "online",
        "docs_url": "/docs"
    }


@app.get("/health/db")
def check_db_health(db: Session = Depends(get_db)):
    """Verifies active connectivity to the configured database."""
    try:
        db.execute(text("SELECT 1"))
        return {
            "status": "healthy",
            "database": "connected"
        }
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database connection error: {str(exc)}"
        )


@app.post("/api/seed-drugs", status_code=status.HTTP_201_CREATED)
def seed_initial_drugs(db: Session = Depends(get_db)):
    """Seeds default Narrow Therapeutic Index (NTI) drugs for clinical testing."""
    existing_count = db.query(Drug).count()
    if existing_count > 0:
        return {"message": "Database already contains drug records.", "count": existing_count}

    initial_drugs = [
        Drug(
            name="Vankomisin",
            active_ingredient="Vancomycin Hydrochloride",
            standard_dose_mg=1000.0,
            therapeutic_range_min=10.0,
            therapeutic_range_max=20.0,
            renal_clearance_flag=True,
        ),
        Drug(
            name="Digoksin",
            active_ingredient="Digoxin",
            standard_dose_mg=0.25,
            therapeutic_range_min=0.8,
            therapeutic_range_max=2.0,
            renal_clearance_flag=True,
        ),
        Drug(
            name="Lityum",
            active_ingredient="Lithium Carbonate",
            standard_dose_mg=300.0,
            therapeutic_range_min=0.6,
            therapeutic_range_max=1.2,
            renal_clearance_flag=True,
        ),
    ]

    db.add_all(initial_drugs)
    db.commit()
    return {"message": "Default NTI drugs seeded successfully.", "count": len(initial_drugs)}
