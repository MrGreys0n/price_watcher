import requests
from bs4 import BeautifulSoup


def parse_product(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    name = soup.title.string.strip()
    price_text = soup.find(text=lambda t: t and '₽' in t)
    price = float(''.join(filter(str.isdigit, price_text))) if price_text else 0
    return name, price
