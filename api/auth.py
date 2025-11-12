from datetime import datetime, timedelta, timezone
import jwt
from django.conf import settings

JWT_ALGORITHM = "HS256"
JWT_EXPIRE_HOURS = 24


def create_jwt(member_id: int) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(member_id),
        "m": member_id,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(hours=JWT_EXPIRE_HOURS)).timestamp()),
        "iss": "easyapp",
        "typ": "access",
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=JWT_ALGORITHM)
    return token


def verify_jwt(token: str) -> dict | None:
    try:
        data = jwt.decode(token, settings.SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return data
    except Exception:
        return None
