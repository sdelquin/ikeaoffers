from core import Product

URL_NO_OFFER = 'https://www.islas.ikea.es/tenerife/es/pd/teodores-silla-verde-art-00530617'
URL_OFFER = 'https://www.islas.ikea.es/tenerife/es/pd/boaxel-1-seccion-baldas-blanco-spr-09392616'

p = Product(URL_OFFER)
print(p.abs_discount)
print(p.rel_discount)
