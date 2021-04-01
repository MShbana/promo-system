from promo_system.settings.base import *


DEBUG = True

SECRET_KEY = os.environ.get('SECRET_KEY')

ALLOWED_HOSTS = [
    'promo-system.herokuapp.com',
]

DATABASES = {
    'default': {
        'ENGINE':   os.environ.get('DATABASE_ENGINE'),
        'NAME':     os.environ.get('DATABASE_NAME'),
        'USER':     os.environ.get('DATABASE_USER'),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD'),
        'HOST':     os.environ.get('DATABASE_HOST'),
        'PORT':     os.environ.get('DATABASE_PORT')
    }
}


import dj_database_url
DATABASES['default'] = dj_database_url.config(conn_max_age=600, ssl_require=True)