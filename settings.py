from pathlib import Path

from prettyconf import config

PROJECT_DIR = Path(__file__).parent
PROJECT_NAME = PROJECT_DIR.name

CONFIG_PATH = config('CONFIG_PATH', default='config.yaml')
STORAGE_PATH = config('STORAGE_PATH', default='tracking.dbm')

SENDGRID_APIKEY = config('SENDGRID_APIKEY', default='your-sendgrid-api-key-here')
SENDGRID_FROM_ADDR = config('SENDGRID_FROM_ADDR', default='from@example.com')
SENDGRID_FROM_NAME = config('SENDGRID_FROM_NAME', default='From Example')

LOGFILE = config('LOGFILE', default=PROJECT_DIR / (PROJECT_NAME + '.log'), cast=Path)
LOGFILE_SIZE = config('LOGFILE_SIZE', cast=float, default=1e6)
LOGFILE_BACKUP_COUNT = config('LOGFILE_BACKUP_COUNT', cast=int, default=3)
