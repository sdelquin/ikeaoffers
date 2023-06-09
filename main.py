import logzero
import typer

from core import IKEAOffers
from utils import init_logger

app = typer.Typer(add_completion=False)
logger = init_logger()


@app.command()
def run(
    loglevel: str = typer.Option(
        'DEBUG', '--loglevel', '-l', help='Log level (debug, info, error)'
    ),
):
    '''
    Check for IKEA offers and notify users.
    '''

    logger.setLevel(getattr(logzero, loglevel.upper()))
    offers = IKEAOffers()
    offers.run()


if __name__ == "__main__":
    app()
