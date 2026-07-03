from datetime import datetime, timedelta
import jwt
from app.config import security_settings
from app.core.exceptions import ExpiredTokenException

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
            },
            "exp": datetime.now() + expiry
        },
        algorithm=security_settings.JWT_ALGORITHM,
        key=security_settings.JWT_SECRET_KEY
    )
    return token