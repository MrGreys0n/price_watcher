import os

from sqlalchemy import create_engine, Column, Integer, String, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from passlib.hash import bcrypt

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password_hash = Column(String)
    favorites = relationship("Favorite", back_populates="user")
    telegram_username = Column(String, nullable=True)
    telegram_chat_id = Column(String, nullable=True)

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
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    timestamp = Column(DateTime)
    price = Column(Numeric)
    product = relationship("Product", back_populates="history")


Base.metadata.create_all(bind=engine)
