from fastapi import APIRouter, Form, Depends, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from passlib.hash import bcrypt
from app.models import User
from app.database import get_db
from app.auth import create_access_token, get_current_user


router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/register", response_class=HTMLResponse)
def show_register_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.post("/register")
def register(
        username: str = Form(...),
        password: str = Form(...),
        db: Session = Depends(get_db)
):
    if db.query(User).filter_by(username=username).first():
        return RedirectResponse("/", status_code=302)
    user = User(username=username, password_hash=bcrypt.hash(password))
    db.add(user)
    db.commit()
    return RedirectResponse("/", status_code=302)


@router.post("/login")
def login(
        username: str = Form(...),
        password: str = Form(...),
        db: Session = Depends(get_db)
):
    user = db.query(User).filter_by(username=username).first()
    if not user or not user.verify_password(password):
        return RedirectResponse("/", status_code=302)

    token = create_access_token({"sub": str(user.id)})
    response = RedirectResponse("/favorites", status_code=302)
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        samesite="lax",
        secure=False
    )
    return response


@router.get("/profile", response_class=HTMLResponse)
def profile(request: Request, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse("profile.html", {"request": request, "user": current_user})


@router.get("/logout")
def logout():
    response = RedirectResponse("/")
    response.delete_cookie("access_token")
    return response


@router.post("/update_profile")
def update_profile(
    username: str = Form(...),
    password: str = Form(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    current_user.username = username
    if password:
        current_user.password_hash = bcrypt.hash(password)
    db.commit()
    return RedirectResponse("/profile", status_code=302)

