from backend.shared import enums, models
from sqlalchemy.orm.session import Session


def log_api_call(
    session: Session,
    endpoint: str,
    status_code: enums.ApiStatusCode,
    message: enums.ApiStatusMessages,
    data_reading_id: int,
):
    """
    Logs the API call into the database.
    """
    api_log = models.DataMoniteringApiLog(
        endpoint_url=endpoint,
        status_code=int(status_code),
        message=message,
        data_reading_id=data_reading_id,
    )
    session.add(api_log)
    session.commit()
