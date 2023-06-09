from core import IKEAOffers
from utils import init_logger

logger = init_logger()


app = IKEAOffers()
app.run()
