import requests
from bs4 import BeautifulSoup


class Product:
    def __init__(self, product_url: str):
        self.url = product_url

        response = requests.get(product_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        item_info = soup.find('div', class_='itemInfo')
        if item_offer := item_info.find('p', class_='itemOfferPrice'):
            self.offer_price = int(item_offer['data-price'])
            old_value = item_info.find('span', class_='oldValue')
            self.original_price = int(old_value.contents[0])
        else:
            item_price = item_info.find('p', class_='itemNormalPrice')
            self.original_price = int(item_price.span['data-price'])
            self.offer_price = self.original_price

        item_title = item_info.find('div', class_='itemTitle')
        self.name = item_title.h6.text.strip()
        item_facts = item_info.find('div', class_='itemFacts')
        self.description = ' '.join(item_facts.stripped_strings)

    @property
    def is_offer(self) -> bool:
        return self.offer_price < self.original_price

    @property
    def abs_discount(self) -> int:
        return self.original_price - self.offer_price

    @property
    def rel_discount(self) -> float:
        return self.abs_discount / self.original_price * 100
