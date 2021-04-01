from decouple import config as envvars_config

from promo_system.settings.base import *


SECRET_KEY = envvars_config('SECRET_KEY')

DEBUG = True

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1'
]

DATABASES = {
    'default': {
        'ENGINE':   envvars_config('DATABASE_ENGINE'),
        'NAME':     envvars_config('DATABASE_NAME'),
        'USER':     envvars_config('DATABASE_USER'),
        'PASSWORD': envvars_config('DATABASE_PASSWORD'),
        'HOST':     envvars_config('DATABASE_HOST'),
        'PORT':     envvars_config('DATABASE_PORT')
    }
}