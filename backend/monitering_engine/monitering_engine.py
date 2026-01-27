import time
from datetime import datetime
import asyncio
import requests
import schedule
from sqlalchemy import desc
from sqlalchemy.orm.session import Session
from requests.exceptions import RequestException
from backend.shared import models, config
from backend.shared.database import with_db_session
from backend.shared.logger.logger import get_logger
from backend.shared import enums
from .email import send_email
from .helper import log_api_call


logger = get_logger(__name__)
API_KEY = config.API_KEY
ENDPOINT = config.ENDPOINT
max_retries: int = 3
delay: float = 0.5
THRESHOLD_VALUE = 90


@with_db_session
def data_monitoring_engine(session: Session = None):
    response_status = None
    reading_id = None
    attempt: int = 0
    for attempt in range(max_retries):
        try:
            headers = {"X-API-Key": API_KEY}
            response = requests.get(ENDPOINT, headers=headers, timeout=2)
            response_status = response.status_code
            response.raise_for_status()
            response_json = response.json()
            current_value = response_json.get("value")
            timestamp = response_json.get("timestamp")
            data_reading = models.DataReading(
                value=current_value, created_at=timestamp
            )
            session.add(data_reading)
            session.flush()
            reading_id = data_reading.id
            log_api_call(
                session,
                ENDPOINT,
                response_status,
                enums.ApiStatusMessages.DATA_RECEIVED,
                data_reading.id,
            )
            logger.info("Data added to Data Reading table!")
            last_reading = (
                session.query(models.DataReading)
                .order_by(desc(models.DataReading.id))
                .offset(1)
                .first()
            )
            if current_value > THRESHOLD_VALUE:
                if not last_reading or last_reading.value <= THRESHOLD_VALUE:
                    loop = asyncio.get_running_loop()
                    loop.create_task(
                        send_email(
                            to_email=config.MAIL_TO,
                            value=response_json.get("value"),
                            timestamp=response_json["timestamp"],
                        )
                    )
                    email_log = models.EmailNotificationLog(
                        sent_at=datetime.utcnow(),
                        email_status=enums.EmailStatus.SENT,
                        data_reading_id=data_reading.id,
                    )
                    session.add(email_log)
            session.commit()
            logger.info("Data successfully saved to database")
            break
        except RequestException as e:
            logger.error(f"Exception detected: {e}")
            logger.warning(
                f"Attempt {attempt} failed for {ENDPOINT}: {e}.Retrying in {delay} seconds..."
            )
            log_api_call(
                session,
                ENDPOINT,
                response_status,
                enums.ApiStatusMessages.ERROR,
                reading_id,
            )
            time.sleep(delay)

    else:
        logger.error(f"All {max_retries} attempts failed for {ENDPOINT}")
        return


async def run_schedule():
    """
    Run the schedule in an asyncio event loop.
    """
    while True:
        schedule.run_pending()
        await asyncio.sleep(5)


async def start_data_moniterig_engine():
    """
    Start the schedule in an asyncio event loop.
    """
    schedule.every(1).seconds.do(data_monitoring_engine)
    await run_schedule()
