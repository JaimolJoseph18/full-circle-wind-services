from sqlalchemy_utils import ChoiceType
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, DateTime, String, ForeignKey, Index
from sqlalchemy.sql import func
from backend.shared import enums
from sqlalchemy.orm import declarative_base
from backend.shared.database.engine import engine


Base = declarative_base()
Base.metadata.create_all(bind=engine)


class DataReading(Base):
    __tablename__ = "data_reading"

    id = Column(Integer, primary_key=True)
    value = Column(Integer, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    email_notifications = relationship(
        "EmailNotificationLog",
        back_populates="data_reading",
        lazy="selectin",
        cascade="all, delete-orphan",
    )

    api_logs = relationship(
        "DataMoniteringApiLog",
        back_populates="data_reading",
        lazy="selectin",
    )
    __table_args__ = (Index("ix_reading_time_value", "created_at", "value"),)


class DataMoniteringApiLog(Base):

    __tablename__ = "data_monitering_api_log"

    id = Column(Integer, primary_key=True)
    endpoint_url = Column(String, nullable=False)
    status_code = Column(ChoiceType(enums.ApiStatusCode, impl=String()), nullable=False)
    message = Column(ChoiceType(enums.ApiStatusMessages, impl=String()), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    data_reading_id = Column(
        Integer, ForeignKey("data_reading.id"), nullable=True, index=True
    )
    data_reading = relationship("DataReading", back_populates="api_logs")


class EmailNotificationLog(Base):
    __tablename__ = "email_notification_log"

    id = Column(Integer, primary_key=True)
    email_status = Column(ChoiceType(enums.EmailStatus, impl=String()), nullable=False)
    sent_at = Column(DateTime(timezone=True), server_default=func.now())
    data_reading_id = Column(
        Integer, ForeignKey("data_reading.id"), nullable=False, index=True
    )
    data_reading = relationship("DataReading", back_populates="email_notifications")
