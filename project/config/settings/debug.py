from .base import *

# DEBUG MODE
DEBUG = True

INSTALLED_APPS += [
    'debug_toolbar',
]

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

# WSGI application
WSGI_APPLICATION = 'config.wsgi.debug.application'

# allowed hosts
ALLOWED_HOSTS = ['*']

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# static files dirs
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
