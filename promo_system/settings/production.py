from promo_system.settings.base import *


DEBUG = True

SECRET_KEY = os.environ.get('SECRET_KEY')

ALLOWED_HOSTS = [
    'promo-system.herokuapp.com',
]

DATABASES = {}

import dj_database_url
DATABASES['default'] = dj_database_url.config(conn_max_age=600, ssl_require=True)