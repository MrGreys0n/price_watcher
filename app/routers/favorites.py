from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from datetime import datetime, date
from app.database import get_db
from app.models import Product, Favorite, PriceHistory
from app.auth import get_current_user
import requests
from bs4 import BeautifulSoup


router = APIRouter()


def parse_product(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    name = soup.title.string.strip()
    price_text = soup.find(text=lambda t: t and "₽" in t)
    price = float("".join(filter(str.isdigit, price_text))) if price_text else 0
    return name, price


@router.get("/favorites", response_class=HTMLResponse)
def list_favorites(request: Request, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    favs = db.query(Favorite).filter_by(user_id=current_user.id).all()
    return request.app.state.templates.TemplateResponse("favorites.html", {"request": request, "favs": favs})


@router.post("/add_favorite")
def add_favorite(url: str = Form(...), db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    name, price = parse_product(url)
    product = db.query(Product).filter_by(url=url).first()
    if not product:
        product = Product(name=name, url=url, latest_price=price, last_checked=datetime.now())
        db.add(product)
        db.commit()
    db.add(Favorite(user_id=current_user.id, product_id=product.id))
    db.commit()
    db.add(PriceHistory(product_id=product.id, date=date.today(), price=price))
    db.commit()
    return RedirectResponse("/favorites", status_code=302)
