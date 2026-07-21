from typing import Any, Dict, List
from fastapi import BackgroundTasks
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from pydantic import EmailStr
from app.config import notification_settings
from app.utils import TEMPLATE_PATH


class NotificationService:
    def __init__(self, background_tasks: BackgroundTasks):
        self.fast_mail = FastMail(
            ConnectionConfig(**notification_settings.model_dump(), 
            TEMPLATE_FOLDER = TEMPLATE_PATH
        ))
        self.background_tasks = background_tasks

    async def send_email(self, recipients: List[EmailStr], subject: str, context: Dict[str, Any], template_name: str):
        self.background_tasks.add_task(
            self.fast_mail.send_message,
            message = MessageSchema(
                recipients=recipients,
                subject=subject,
                template_body=context,
                subtype=MessageType.html,
            ),
            template_name=template_name
        )