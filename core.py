import re
import shelve

import requests
import yaml
from bs4 import BeautifulSoup
from sendgrify import SendGrid

import settings


class Product:
    def __init__(self, product_url: str):
        self.url = product_url
        if m := re.search(r'\d+$', self.url):
            self.id = m.group()
        else:
            raise ValueError(f'Product url "{self.url}" does not include an id')

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

    def __str__(self):
        return self.name


class Tracking:
    sg = SendGrid(
        settings.SENDGRID_APIKEY,
        settings.NOTIFICATION_FROM_ADDR,
        settings.NOTIFICATION_FROM_NAME,
    )
    deliveries = shelve.open(settings.STORAGE_PATH)

    def __init__(self, user: User, product: Product):
        self.user = user
        self.product = product

    @property
    def tagline(self):
        return f'{self.user.email}:{self.product.id}'

    def load(self) -> int | None:
        return self.deliveries.get(self.tagline)

    def save(self) -> None:
        self.deliveries[self.tagline] = self.product.offer_price

    def remove(self) -> None:
        del self.deliveries[self.tagline]

    def notify(self):
        self.sg.send(
            to=self.user.email,
            subject=self.product.title,
            msg=str(self.product),
            as_markdown=True,
        )

    def dispatch(self):
        notify = False
        if self.product.is_offer:
            if notified_offer_price := self.load():
                # notified in the past
                if self.product.offer_price < notified_offer_price:
                    notify = True
            else:
                notify = True
            if notify:
                self.save()
                self.notify()
        elif self.notified:
            self.remove()

    @property
    def notified(self):
        return self.tagline in self.deliveries


class IKEAOffers:
    def __init__(self, config_path: str = settings.CONFIG_PATH):
        self.config = yaml.load(open(config_path), Loader=yaml.FullLoader)

    def run(self):
        for user_cfg in self.config['users']:
            user = User(user_cfg['name'], user_cfg['email'])
            for product_url in user_cfg['track']:
                product = Product(product_url)
                tracking = Tracking(user, product)
                tracking.dispatch()
