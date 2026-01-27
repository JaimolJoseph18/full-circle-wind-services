from sqlalchemy import create_engine

DATABASE_URL = "postgresql://postgres:lyvplatform@localhost:5432/data_monitoring"

engine = create_engine(
    DATABASE_URL,
    future=True,
    pool_pre_ping=True,
)
