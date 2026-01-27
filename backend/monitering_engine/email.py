import os
from string import Template
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from backend.shared import config
from backend.shared.logger.logger import get_logger


logger = get_logger(__name__)

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
EMAIL_TEMPLATE_PATH = os.path.join(BASE_DIR, "email_templates", "alert_email.html")

conf = ConnectionConfig(
    MAIL_USERNAME=config.MAIL_USERNAME,
    MAIL_PASSWORD=config.MAIL_PASSWORD,
    MAIL_FROM=config.MAIL_FROM,
    MAIL_PORT=587,  # check if port is 587 tls or ssl to be used
    MAIL_SERVER=config.MAIL_SERVER,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
)


async def send_email(to_email: str, value: int, timestamp: str):
    with open(EMAIL_TEMPLATE_PATH, "r", encoding="utf-8") as f:
        template = Template(f.read())

    html_content = template.safe_substitute(value=value, timestamp=timestamp)

    message = MessageSchema(
        subject="Critical Value Alert",
        recipients=[to_email],
        body=html_content,
        subtype=MessageType.html,
    )

    fm = FastMail(conf)
    await fm.send_message(message)
    logger.info(f"Email sent to {to_email} for value {value}")
