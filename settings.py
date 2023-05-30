from prettyconf import config

CONFIG_PATH = config('CONFIG_PATH', default='config.yaml')
SENDGRID_APIKEY = config('SENDGRID_APIKEY', default='your-sendgrid-api-key-here')
NOTIFICATION_FROM_ADDR = config('NOTIFICATION_FROM_ADDR', default='from@example.com')
NOTIFICATION_FROM_NAME = config('NOTIFICATION_FROM_NAME', default='From Example')
