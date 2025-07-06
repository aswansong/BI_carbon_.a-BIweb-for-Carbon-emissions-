from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = False

ALLOWED_HOSTS = ['39.103.187.86']

SECRET_KEY = 'django-insecure-4^1ukjc601l^m+3z5k0+h=b3hzban)kbl)*5aw=1qy3n=)k2hl'

ALLOWED_HOSTS = ['39.103.187.86']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

Q_CLUSTER = {
    'workers':2,
    'timeout':600,
    'retry':1200,
    'orm':'default',

}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'my_cache_table',
    }
}
