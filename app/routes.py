from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from passlib.handlers.bcrypt import bcrypt

from .models import SessionLocal, User, Favorite, Product, PriceHistory
from .utils import parse_product
from .auth import create_access_token
from .dependencies import get_db, get_current_user, get_current_user_optional
from sqlalchemy.orm import Session
from datetime import datetime

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
def home(request: Request, user: User = Depends(get_current_user_optional)):
    return templates.TemplateResponse("index.html", {"request": request, "user": user})


@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request, current_user: User = Depends(get_current_user_optional)):
    return templates.TemplateResponse("login.html", {"request": request, "user": current_user})


@router.get("/register", response_class=HTMLResponse)
def register_page(request: Request, current_user: User = Depends(get_current_user_optional)):
    return templates.TemplateResponse("register.html", {"request": request, "user": current_user})


@router.post("/register")
def register(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    if db.query(User).filter_by(username=username).first():
        return templates.TemplateResponse("errors/error.html", {
            "request": request,
            "status_code": 400,
            "detail": "Имя пользователя занято"
        }, status_code=400)
    user = User(username=username, password_hash=bcrypt.hash(password))
    db.add(user)
    db.commit()
    return RedirectResponse("/", status_code=302)


@router.post("/login")
def login(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter_by(username=username).first()
    if not user or not user.verify_password(password):
        return templates.TemplateResponse("errors/error.html", {
            "request": request,
            "status_code": 400,
            "detail": "Неверные учетные данные"
        }, status_code=400)
    token = create_access_token({"sub": str(user.id)})
    response = RedirectResponse("/favorites", status_code=302)
    response.set_cookie(key="access_token", value=token, httponly=True, samesite="lax", secure=False)
    return response


@router.get("/logout")
def logout():
    response = RedirectResponse("/")
    response.delete_cookie("access_token")
    return response


@router.get("/profile", response_class=HTMLResponse)
def profile(request: Request, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse("profile.html", {"request": request, "user": current_user})


@router.post("/update_profile")
def update_profile(username: str = Form(...), password: str = Form(None),
                   telegram_username: str = Form(None), db: Session = Depends(get_db),
                   current_user: User = Depends(get_current_user)):
    current_user.username = username
    if password:
        current_user.password_hash = bcrypt.hash(password)
    current_user.telegram_username = telegram_username
    db.commit()
    return RedirectResponse("/profile", status_code=302)


@router.get("/search", response_class=HTMLResponse)
def search_page(request: Request, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse("search.html", {"request": request, "user": current_user})


@router.get("/favorites", response_class=HTMLResponse)
def list_favorites(request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    favs = db.query(Favorite).filter_by(user_id=current_user.id).all()
    for f in favs:
        f.price_history = [
            {"timestamp": ph.timestamp.strftime("%d.%m.%Y %H:%M"), "price": float(ph.price)}
            for ph in db.query(PriceHistory).filter_by(product_id=f.product.id).order_by(PriceHistory.timestamp).all()
        ]
    return templates.TemplateResponse("favorites.html", {"request": request, "favs": favs, "user": current_user})


@router.post("/add_favorite")
def add_fav(url: str = Form(...), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    name, price = parse_product(url)
    product = db.query(Product).filter_by(url=url).first()
    if not product:
        product = Product(name=name, url=url, latest_price=price, last_checked=datetime.now())
        db.add(product)
        db.commit()
    db.add(Favorite(user_id=current_user.id, product_id=product.id))
    db.commit()
    db.add(PriceHistory(product_id=product.id, timestamp=datetime.now(), price=price))
    db.commit()
    return RedirectResponse("/favorites", status_code=302)


@router.post("/remove_favorite")
def remove_fav(product_id: int = Form(...), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    fav = db.query(Favorite).filter_by(user_id=current_user.id, product_id=product_id).first()
    if not fav:
        raise HTTPException(status_code=404, detail="Товар не найден в избранном")
    db.delete(fav)
    db.commit()
    return RedirectResponse("/favorites", status_code=302)
