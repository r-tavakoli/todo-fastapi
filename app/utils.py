from datetime import datetime, timedelta
from pathlib import Path
from uuid import uuid4

import jwt
from itsdangerous import (
    BadSignature,
    SignatureExpired,
    URLSafeTimedSerializer,
)

from app.config import security_settings
from app.core.exceptions import ExpiredTokenException

APP_DIR = Path(__file__).resolve().parent
TEMPLATE_PATH = APP_DIR.joinpath("templates")
TEMPLATE_EMAIL_PATH = TEMPLATE_PATH.joinpath("email")

_serializer = URLSafeTimedSerializer(security_settings.JWT_SECRET_KEY)

def decode_access_token(token: str) -> dict | None:
    try:
        return jwt.decode(
            jwt=token,
            key=security_settings.JWT_SECRET_KEY,
            algorithms=[security_settings.JWT_ALGORITHM]
        )
    except jwt.ExpiredSignatureError:
        raise ExpiredTokenException()
    except jwt.PyJWTError:
        return None
    
    
def encode_access_token(id: int, user_name: str, expiry: timedelta) -> str:
    token = jwt.encode(
        payload={
            "user": {
                "user_name": user_name,
                "id": id,
                "jti": str(uuid4())
            },
            "exp": datetime.now() + expiry
        },
        algorithm=security_settings.JWT_ALGORITHM,
        key=security_settings.JWT_SECRET_KEY
    )
    return token


def generate_url_safe_token(data: dict, salt: str | None = None) -> str:
    return _serializer.dumps(data, salt)

def decode_url_safe_token(token: str, expiry: timedelta | None = None, salt: str | None = None) -> dict | None:
    try:
        return _serializer.loads(
            token, 
            max_age=expiry.total_seconds() if expiry else None,
            salt=salt,
        )
    except (BadSignature, SignatureExpired):
        return None