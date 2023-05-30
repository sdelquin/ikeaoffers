import requests
import yaml
from bs4 import BeautifulSoup
from sendgrify import SendGrid

import settings


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

    @property
    def title(self) -> str:
        title_ = self.name
        if self.is_offer:
            title_ += ' en oferta'
        return title_

    @property
    def hero(self) -> str:
        return f'{self.name} ({self.description})'

    def __str__(self):
        if self.is_offer:
            return f'''**¡{self.hero} en oferta!**

- {self.original_price}€ ↘️ **{self.offer_price}€**
- {self.abs_discount}€ de descuento absoluto.
- {self.rel_discount:.2f}% de descuento relativo.
- {self.url}
'''
        else:
            return self.hero


class User:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email
        self.sg = SendGrid(
            settings.SENDGRID_APIKEY,
            settings.NOTIFICATION_FROM_ADDR,
            settings.NOTIFICATION_FROM_NAME,
        )

    def handle_product(self, product: Product):
        if product.is_offer:
            self.sg.send(to=self.email, subject=product.title, msg=str(product), as_markdown=True)


class IKEAOffers:
    def __init__(self, config_path: str = settings.CONFIG_PATH):
        self.config = yaml.load(open(config_path), Loader=yaml.FullLoader)

    def run(self):
        for user_cfg in self.config['users']:
            user = User(user_cfg['name'], user_cfg['email'])
            for product_url in user_cfg['track']:
                product = Product(product_url)
                user.handle_product(product)
