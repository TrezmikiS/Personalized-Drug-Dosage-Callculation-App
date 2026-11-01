import os
import socket
from urllib.parse import urlparse
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/dosage_db"
)

# Normalize postgresql scheme to use psycopg2 driver if not explicitly specified
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://", 1)


def is_service_listening(url: str) -> bool:
    """Quick socket probe to check if the target DB host:port is accepting connections."""
    try:
        parsed = urlparse(url)
        host = parsed.hostname or "127.0.0.1"
        port = parsed.port or 5432
        with socket.create_connection((host, port), timeout=0.4):
            return True
    except (OSError, ValueError):
        return False


def get_engine():
    """
    Connects to the database. If PostgreSQL is configured but not running / reachable,
    gracefully and immediately falls back to a local SQLite database (dosage_app.db)
    so the application works seamlessly out-of-the-box.
    """
    if "postgresql" in DATABASE_URL:
        if is_service_listening(DATABASE_URL):
            try:
                pg_engine = create_engine(
                    DATABASE_URL,
                    pool_pre_ping=True,
                    connect_args={"connect_timeout": 2}
                )
                with pg_engine.connect() as conn:
                    conn.execute(text("SELECT 1"))
                print("[Database] Connected to PostgreSQL.")
                return pg_engine
            except Exception as err:
                print(f"[Database Warning] PostgreSQL connect failed: {err}")

        print("[Database] PostgreSQL server not running locally. Using local SQLite database (dosage_app.db).")
        sqlite_url = "sqlite:///./dosage_app.db"
        return create_engine(
            sqlite_url,
            connect_args={"check_same_thread": False}
        )
    else:
        connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
        return create_engine(DATABASE_URL, connect_args=connect_args, pool_pre_ping=True)


engine = get_engine()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """FastAPI dependency for creating a scoped database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
