from typing import Union
from datetime import datetime
from pydantic import BaseModel


class DataReadingBase(BaseModel):
    id: int
    value: int
    timestamp: datetime

    class Config:
        from_attributes = True


class DataReading(DataReadingBase):
    pass


class DataReadingWithApiLog(DataReadingBase):
    api_endpoint: str
    api_status: Union[int, str]
    api_message: str
    email_sent: bool


class DataReadingStats(BaseModel):
    latest_value: int
    latest_timestamp: datetime
    average_value: float
    min_value: int
    max_value: int
    threshold_exceeded_count: int
    total_count: int
