import os
from typing import List

from dotenv import load_dotenv
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema
from pydantic import EmailStr

load_dotenv()

conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_FROM"),
    MAIL_PORT=int(os.getenv("MAIL_PORT", 587)),
    MAIL_SERVER=os.getenv("MAIL_SERVER"),
    MAIL_STARTTLS=True,  # upgrading an existing insecure connection to a secure one using TLS
    MAIL_SSL_TLS=False,  # 의미가 secure to secure라 끈다. -> less secure to more secure가 가능해짐.
    USE_CREDENTIALS=True,  # username과 password 사용
    VALIDATE_CERTS=True,  # validate SSL certificates
)


async def send_email_async(subject: str, recipients: List[EmailStr], body_text: str):
    html = f"""
    <h2> {subject} </h2>
    </br>
    <p> {body_text} </p>
    </br>
    </br>
    """
    message = MessageSchema(
        subject=subject,
        recipients=recipients,
        body=html,
        subtype="html",
    )

    fm = FastMail(conf)
    await fm.send_message(message)
