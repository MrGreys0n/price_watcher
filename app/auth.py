from datetime import datetime, timedelta
from fastapi import HTTPException, Cookie, Depends
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User


SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None


def get_current_user(
    db: Session = Depends(get_db),
    token: str = Cookie(None, alias="access_token")
):
    if not token:
        raise HTTPException(status_code=401, detail="Не авторизован (токен не найден)")
    payload = decode_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(status_code=401, detail="Неверный токен")
    user = db.query(User).get(int(payload["sub"]))
    if not user:
        raise HTTPException(status_code=401, detail="Пользователь не найден")
    return user
