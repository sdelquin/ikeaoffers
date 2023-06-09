import re
import shelve

import requests
import yaml
from bs4 import BeautifulSoup
from logzero import logger
from sendgrify import SendGrid

import settings


class Product:
    def __init__(self, product_url: str):
        logger.info(f'📦 Building product from: {product_url}')
        self.url = product_url
        if m := re.search(r'\d+$', self.url):
            self.id = m.group()
            logger.debug(f'Extracting product id from url: {self.id}')
        else:
            logger.error(f'Product url "{self.url}" does not include an id')

        logger.debug('Requesting data from url')
        response = requests.get(product_url)
        soup = BeautifulSoup(response.content, 'html.parser')

        item_info = soup.find('div', class_='itemInfo')
        item_title = item_info.find('div', class_='itemTitle')
        self.name = item_title.h6.text.strip()
        item_facts = item_info.find('div', class_='itemFacts')
        self.description = ' '.join(item_facts.stripped_strings)

        if item_offer := item_info.find('p', class_='itemOfferPrice'):
            logger.info(f'✨ Product {self.name} includes an offer!')
            self.offer_price = float(item_offer['data-price'])
            old_value = item_info.find('span', class_='oldValue')
            self.original_price = float(old_value.contents[0])
        else:
            logger.info('== Product normal price')
            item_price = item_info.find('p', class_='itemPrice')
            self.original_price = float(item_price.span.contents[0])
            self.offer_price = self.original_price

    @property
    def is_offer(self) -> bool:
        return self.offer_price < self.original_price

    @property
    def abs_discount(self) -> float:
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
        return self.hero

    @property
    def template(self):
        if self.is_offer:
            return f'''**¡{self.hero} en oferta!**

- {self.original_price:.02f}€ ↘️ **{self.offer_price}€**
- {self.abs_discount:.02f}€ de descuento absoluto.
- {self.rel_discount:.0f}% aprox. de descuento relativo.
- {self.url}
'''
        else:
            return f'{self.hero} a precio normal'


class User:
    def __init__(self, name: str, email: str):
        logger.info(f'👤 Building user: {name}')
        self.name = name
        self.email = email

    def __str__(self):
        return f'{self.name} ({self.email})'


class Tracking:
    sg = SendGrid(
        settings.SENDGRID_APIKEY,
        settings.SENDGRID_FROM_ADDR,
        settings.SENDGRID_FROM_NAME,
    )
    deliveries = shelve.open(settings.STORAGE_PATH)

    def __init__(self, user: User, product: Product):
        logger.debug('Building Tracking object')
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
        logger.info(f'Notifying {self}')
        self.sg.send(
            to=self.user.email,
            subject=self.product.title,
            msg=self.product.template,
            as_markdown=True,
        )

    def dispatch(self):
        logger.info(f'Dispatching tracking {self}')
        notify = False
        if self.product.is_offer:
            if notified_offer_price := self.load():
                # notified in the past
                logger.debug(f'{self.user} was already notified for: {self.product}')
                if self.product.offer_price < notified_offer_price:
                    logger.debug(f'{self.user} will be notified for a better offer')
                    notify = True
            else:
                notify = True
            if notify:
                self.save()
                self.notify()
        elif self.notified:
            logger.debug('Product {self.product} does not include an offer')
            self.remove()

    @property
    def notified(self):
        return self.tagline in self.deliveries

    def __str__(self):
        return f'[{self.user.name} - {self.product.name}]'


class IKEAOffers:
    def __init__(self, config_path: str = settings.CONFIG_PATH):
        self.config = yaml.load(open(config_path), Loader=yaml.FullLoader)

    def run(self):
        for user_cfg in self.config['users']:
            user = User(user_cfg['name'], user_cfg['email'])
            for product_url in user_cfg['track']:
                try:
                    product = Product(product_url)
                    tracking = Tracking(user, product)
                except Exception as err:
                    logger.error(err)
                else:
                    tracking.dispatch()
