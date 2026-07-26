from typing import Any

from asgiref.sync import async_to_sync
from celery import Celery
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from pydantic import EmailStr

from app.config import db_settings, notification_settings
from app.utils import TEMPLATE_EMAIL_PATH

fast_mail = FastMail(
            ConnectionConfig(
                **notification_settings.model_dump(), 
                TEMPLATE_FOLDER=TEMPLATE_EMAIL_PATH
            )
        )

send_message = async_to_sync(fast_mail.send_message)


app = Celery(
    main="api_tasks",
    broker=db_settings.REDIS_URL,
    backend=db_settings.REDIS_URL,
)

@app.task(name="send_email_through_celery")
def send_email_through_celery(
    recipients: list[EmailStr],
    subject: str,
    context: dict[str, Any],
    template_name: str,
):
    send_message(
        message=MessageSchema(
            recipients=recipients,
            subject=subject,
            template_body=context,
            subtype=MessageType.html,
        ),
        template_name=template_name,
    )
    
    

# send_email.delay(
#     recipients=["rah_tav@yahoo.com"],
#     subject="celery celery",
#     body="this is a test to run background tasks in celery",    
# )
