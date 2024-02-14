from pathlib import Path

from prettyconf import config

PROJECT_DIR = Path(__file__).parent
PROJECT_NAME = PROJECT_DIR.name
SSL_CERTS_DIR = PROJECT_DIR / 'certs'

CONFIG_PATH = config('CONFIG_PATH', default='config.yaml')
STORAGE_PATH = config('STORAGE_PATH', default='tracking.dbm')

SENDGRID_APIKEY = config('SENDGRID_APIKEY', default='your-sendgrid-api-key-here')
SENDGRID_FROM_ADDR = config('SENDGRID_FROM_ADDR', default='from@example.com')
SENDGRID_FROM_NAME = config('SENDGRID_FROM_NAME', default='From Example')

LOGFILE = config('LOGFILE', default=PROJECT_DIR / (PROJECT_NAME + '.log'), cast=Path)
LOGFILE_SIZE = config('LOGFILE_SIZE', cast=float, default=1e6)
LOGFILE_BACKUP_COUNT = config('LOGFILE_BACKUP_COUNT', cast=int, default=3)


SSL_CERTS_DIR = config('SSL_CERTS_DIR', default=PROJECT_DIR / 'certs', cast=Path)
IKEA_SSL_CERT_PATH = config('IKEA_SSL_CERT_PATH', default=SSL_CERTS_DIR / 'islas-ikea-es-chain.pem')
