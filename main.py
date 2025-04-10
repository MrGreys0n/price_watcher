from fastapi import FastAPI, Depends, HTTPException, Request, Form, Cookie, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from jinja2 import pass_environment
from sqlalchemy import create_engine, Column, Integer, String, Numeric, Date, ForeignKey, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base, relationship, Session
from passlib.hash import bcrypt
from datetime import datetime, date, timedelta
from jose import JWTError, jwt
import requests
from bs4 import BeautifulSoup
import uvicorn
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import atexit

# === CONFIG ===
DATABASE_URL = "postgresql://postgres:1080@localhost/price_finder"
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# === INIT ===
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# === MODELS ===
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password_hash = Column(String)
    favorites = relationship("Favorite", back_populates="user")

    def verify_password(self, password):
        return bcrypt.verify(password, self.password_hash)


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    url = Column(String)
    latest_price = Column(Numeric)
    last_checked = Column(DateTime)
    history = relationship("PriceHistory", back_populates="product")
    favorites = relationship("Favorite", back_populates="product")


class Favorite(Base):
    __tablename__ = "favorites"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    user = relationship("User", back_populates="favorites")
    product = relationship("Product", back_populates="favorites")


class PriceHistory(Base):
    __tablename__ = "price_history"
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    timestamp = Column(DateTime)
    price = Column(Numeric)
    product = relationship("Product", back_populates="history")


Base.metadata.create_all(bind=engine)

# === JWT UTILS ===
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


# === DEPENDENCIES ===
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


# === ROUTES ===
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/register")
def register(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    if db.query(User).filter_by(username=username).first():
        raise HTTPException(status_code=400, detail="Username taken")
    user = User(username=username, password_hash=bcrypt.hash(password))
    db.add(user)
    db.commit()
    return RedirectResponse("/", status_code=302)


@app.post("/login")
def login(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter_by(username=username).first()
    if not user or not user.verify_password(password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = create_access_token({"sub": str(user.id)})
    response = RedirectResponse("/favorites", status_code=302)
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        samesite="lax",  # <= попробуй lax
        secure=False  # <= важно! False для localhost
    )
    return response


@app.get("/logout")
def logout():
    response = RedirectResponse("/")
    response.delete_cookie("access_token")
    return response


@app.get("/profile", response_class=HTMLResponse)
def profile(request: Request, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse("profile.html", {
        "request": request,
        "user": current_user
    })


@app.post("/update_profile")
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



@app.get("/search", response_class=HTMLResponse)
def search_page(request: Request):
    return templates.TemplateResponse("search.html", {"request": request})



@app.get("/favorites", response_class=HTMLResponse)
def list_favorites(request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    favs = db.query(Favorite).filter_by(user_id=current_user.id).all()

    # Подгружаем историю цен для каждого продукта
    for f in favs:
        f.price_history = [
            {"timestamp": ph.timestamp.strftime("%d.%m.%Y %H:%M"), "price": float(ph.price)}
            for ph in db.query(PriceHistory)
            .filter_by(product_id=f.product.id)
            .order_by(PriceHistory.timestamp)
            .all()
        ]
    return templates.TemplateResponse("favorites.html", {
        "request": request,
        "favs": favs
    })



@app.post("/add_favorite")
def add_fav(url: str = Form(...), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
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


@app.post("/remove_favorite")
def remove_fav(product_id: int = Form(...), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    fav = db.query(Favorite).filter_by(user_id=current_user.id, product_id=product_id).first()
    if not fav:
        raise HTTPException(status_code=404, detail="Товар не найден в избранном")
    db.delete(fav)
    db.commit()
    return RedirectResponse("/favorites", status_code=302)


# === UTILS ===
def parse_product(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    name = soup.title.string.strip()
    price_text = soup.find(text=lambda t: t and '₽' in t)
    price = float(''.join(filter(str.isdigit, price_text))) if price_text else 0
    return name, price


def update_favorite_prices():
    print(f"[{datetime.now()}] Начало обновления цен")
    db = SessionLocal()
    try:
        product_ids = db.query(Favorite.product_id).distinct()
        for pid, in product_ids:
            product = db.query(Product).get(pid)
            if not product:
                continue
            try:
                name, price = parse_product(product.url)
                product.latest_price = price
                product.last_checked = datetime.now()
                db.add(PriceHistory(product_id=product.id, timestamp=datetime.now(), price=price))
                db.commit()
                print(f"[{datetime.now()}] Обновлена цена для {product.name}: {price} RUB")
            except Exception as e:
                print(f"[{datetime.now()}] Ошибка обновления {product.url}: {e}")
    except Exception as e:
        print(f"[{datetime.now()}] Ошибка обновления: {e}")
    finally:
        db.close()


scheduler = BackgroundScheduler()
scheduler.add_job(update_favorite_prices, IntervalTrigger(minutes=20))
scheduler.start()
atexit.register(lambda: scheduler.shutdown())
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
