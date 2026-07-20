import asyncio
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from config import notification_settings

# print(notification_settings)

fast_mail = FastMail(
    ConnectionConfig(
        **notification_settings.model_dump()
    )
)

async def send_email_msg():
    await fast_mail.send_message(MessageSchema(
        recipients=["rah_tav@yahoo.com"],
        subject="todo fastapi test email",
        body="""
            hi there,
            this is a test email...
            do what u can do and dont what u cant!
            the end
            bye
        """,
        subtype=MessageType.plain
    ))


asyncio.run(send_email_msg())