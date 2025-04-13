from datetime import datetime
from sqlalchemy.orm import Session
from .models import SessionLocal, Product, PriceHistory, Favorite
from .utils import parse_product
from .bot import bot


async def notify_price_changes():
    print(f"[{datetime.now()}] Начало обновления цен")
    db = SessionLocal()
    try:
        product_ids = db.query(Favorite.product_id).all()
        product_ids = list(set(product_ids))
        for pid, in product_ids:
            product = db.query(Product).get(pid)
            if not product:
                continue
            try:
                old_price = product.latest_price
                name, price = parse_product(product.url)

                if old_price != price:
                    product.latest_price = price
                    product.last_checked = datetime.now()
                    db.add(PriceHistory(product_id=product.id, timestamp=datetime.now(), price=price))
                    db.commit()

                    for fav in product.favorites:
                        user = fav.user
                        if user.telegram_chat_id:
                            try:
                                sticker = "📈" if price > old_price else "📉"
                                await bot.send_message(
                                    chat_id=user.telegram_chat_id,
                                    text=(f"{sticker} Цена изменилась!\n\n{product.name}\nБыло: {old_price}₽\n"
                                          f"Стало: {price}₽\nСсылка: {product.url}")
                                )
                            except Exception as e:
                                print(f"Ошибка отправки: {e}")

            except Exception as e:
                print(f"[{datetime.now()}] Ошибка обновления {product.url}: {e}")
    finally:
        print(f"[{datetime.now()}] Конец обновления цен")
        await bot.session.close()
        db.close()
