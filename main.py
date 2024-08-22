import glob
import os

import logzero
import typer

import settings
from lib.core import IKEAOffers
from lib.utils import init_logger

app = typer.Typer(add_completion=False)
logger = init_logger()


@app.callback()
def main(
    loglevel: str = typer.Option(
        'DEBUG', '--loglevel', '-l', help='Log level (debug, info, error)'
    ),
):
    logger.setLevel(getattr(logzero, loglevel.upper()))


@app.command()
def dispatch(
    loglevel: str = typer.Option(
        'DEBUG', '--loglevel', '-l', help='Log level (debug, info, error)'
    ),
):
    """Check for IKEA offers and notify users."""
    offers = IKEAOffers()
    offers.dispatch()


@app.command()
def clean_db():
    """Clean tracking database."""
    if typer.confirm('Are you sure to delete tracking database?'):
        for file_path in glob.glob(settings.STORAGE_PATH + '*'):
            os.remove(file_path)


@app.command()
def clean_orphan_deliveries():
    """Clean orphan deliveries."""
    offers = IKEAOffers()
    offers.clean_orphan_deliveries()


if __name__ == '__main__':
    app()
