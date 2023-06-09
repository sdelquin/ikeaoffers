import glob
import os

import logzero
import typer

import settings
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
    '''Check for IKEA offers and notify users.'''

    logger.setLevel(getattr(logzero, loglevel.upper()))
    offers = IKEAOffers()
    offers.run()


@app.command()
def clear():
    '''Clear tracking database.'''
    if typer.confirm('Are you sure to delete tracking database?'):
        for file_path in glob.glob(settings.STORAGE_PATH + '*'):
            os.remove(file_path)


if __name__ == "__main__":
    app()
