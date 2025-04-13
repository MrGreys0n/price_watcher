from fastapi import Depends, Cookie, HTTPException, status
from sqlalchemy.orm import Session
from .models import SessionLocal, User
from .auth import decode_token


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class AuthDependency:
    def __call__(self, db: Session = Depends(get_db), token: str = Cookie(None, alias="access_token")):
        if not token:
            raise HTTPException(status_code=status.HTTP_307_TEMPORARY_REDIRECT, headers={"Location": "/"})
        payload = decode_token(token)
        if not payload or "sub" not in payload:
            raise HTTPException(status_code=status.HTTP_307_TEMPORARY_REDIRECT, headers={"Location": "/"})
        user_id = int(payload["sub"])
        user = db.query(User).get(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_307_TEMPORARY_REDIRECT, headers={"Location": "/"})
        return user


get_current_user = AuthDependency()


def get_current_user_optional(token: str = Cookie(None, alias="access_token"), db: Session = Depends(get_db)):
    if token:
        payload = decode_token(token)
        if payload and "sub" in payload:
            return db.query(User).get(int(payload["sub"]))
    return None
