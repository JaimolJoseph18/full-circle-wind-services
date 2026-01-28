from datetime import datetime, date, timedelta
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload
from backend.api import schema
from backend.shared import models
from backend.shared.database import Session as SessionLocal


router = APIRouter()
THRESHOLD_VALUE = 90


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/aggregates", response_model=schema.DataReadingStats)
def get_stats(db: Session = Depends(get_db)):
    # Latest record
    recent_window = datetime.utcnow() - timedelta(minutes=1)
    latest = (
        db.query(models.DataReading)
        .filter(models.DataReading.created_at >= recent_window)
        .order_by(models.DataReading.created_at.desc())
        .first()
    )
    if not latest:
        latest = (
            db.query(models.DataReading)
            .order_by(models.DataReading.created_at.desc())
            .first()
        )

    avg_value, min_value, max_value, threshold_exceeded_count, total_count = db.query(
        func.avg(models.DataReading.value),
        func.min(models.DataReading.value),
        func.max(models.DataReading.value),
        func.count().filter(models.DataReading.value > THRESHOLD_VALUE),
        func.count(models.DataReading.id),
    ).one()

    return {
        "latest_value": latest.value if latest else None,
        "latest_timestamp": latest.created_at if latest else None,
        "average_value": avg_value,
        "min_value": min_value,
        "max_value": max_value,
        "threshold_exceeded_count": threshold_exceeded_count,
        "total_count": total_count,
    }


@router.get("/readings/today", response_model=List[schema.DataReading])
def get_readings_for_current_day(db: Session = Depends(get_db)):
    start = datetime.combine(date.today(), datetime.min.time())
    stmt = (
        select(
            models.DataReading.id,
            models.DataReading.value,
            models.DataReading.created_at,
        )
        .where(models.DataReading.created_at >= start)
        .order_by(models.DataReading.created_at.desc())
    )
    result = db.execute(stmt).all()
    return [
        schema.DataReading(id=r.id, value=r.value, timestamp=r.created_at)
        for r in result
    ]


@router.get("/history", response_model=List[schema.DataReadingWithApiLog])
def get_all_readings(offset: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    stmt = (
        select(models.DataReading)
        .options(
            selectinload(models.DataReading.api_logs),
            selectinload(models.DataReading.email_notifications),
        )
        .order_by(models.DataReading.created_at.desc())
        .offset(offset)
        .limit(limit)
    )
    result = db.execute(stmt).scalars().all()
    return [
        schema.DataReadingWithApiLog(
            id=r.id,
            value=r.value,
            timestamp=r.created_at,
            api_endpoint=r.api_logs[0].endpoint_url if r.api_logs else None,
            api_status=r.api_logs[0].status_code.value if r.api_logs else None,
            api_message=r.api_logs[0].message.value if r.api_logs else None,
            email_sent=bool(r.email_notifications),
        )
        for r in result
    ]
