# -*- coding: utf-8 -*-

import os.path
import sys
from contrib.constants import *

#DEBUG = True
DEBUG = False
TEMPLATE_DEBUG = DEBUG

ROOT_PATH = os.path.dirname(__file__)

sys.path.insert(0, os.path.join(ROOT_PATH, '..'))
sys.path.insert(0, os.path.join(ROOT_PATH, '.'))
sys.path.insert(0, os.path.join(ROOT_PATH, 'lib'))

ADMINS = (
    ('Soul', 'soul@youmemory.org'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'cemetery2',                      # Or path to database file if using sqlite3.
        'USER': 'postgres',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    },
    'old': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'cemetery',                      # Or path to database file if using sqlite3.
        'USER': 'postgres',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

TIME_ZONE = 'Europe/Moscow'

LANGUAGE_CODE = 'ru-RU'

SITE_ID = 1

USE_I18N = True
USE_L10N = True

MEDIA_ROOT = os.path.join(ROOT_PATH, 'media')
MEDIA_URL = '/media/'
ADMIN_MEDIA_PREFIX = '/admin_media/'

# Make this unique, and don't share it with anybody.
#SECRET_KEY = 'b+k0d6o-g$#!pj4$ehh6^tb2glk-n=^ohp8!fb3+m5j2)5n&v1'
SECRET_KEY = '0@z465a*srqjm894!f^ek-8i5)uc^rlq)wk$^zak@@=k_=n$ai'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    #'pagination.middleware.PaginationMiddleware',
    'common.middleware.NoCacheMiddleware',
#    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    os.path.join(ROOT_PATH, 'templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    "django.contrib.messages.context_processors.messages",
    "common.context.variables",
)


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',

    'south',
    'pytils',
    'sentry',
    'sentry.client',
    'debug_toolbar',
    
    # Наши приложения
    'common',
    'persons',
    'organizations',
    'geo',
    'cemetery_app',
    'utils',
)

INTERNAL_IPS = []

LOGIN_URL = "/login/"
LOGOUT_URL = "/logout/"
LOGIN_REDIRECT_URL = "/"

PAGINATION_USER_PER_PAGE_ALLOWED = True
PAGINATION_PER_PAGE = 50

PLACE_PRODUCTTYPE_ID = "60925a32-2add-11e0-8b17-485b39c96dfe"
#BURIAL_PRODUCTTYPE_ID = 1


# Кодировка для файлов обмена.
CSV_ENCODING = "utf8"

# Настройки пэйджинации.
PAGINATION_USER_PER_PAGE_MAX = 50
PAGINATION_PER_PAGE = 5

SENTRY_TESTING = True

DEBUG_TOOLBAR_CONFIG = {'INTERCEPT_REDIRECTS': False}

SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_SAVE_EVERY_REQUEST = True

try:
    from settings_local import *
except ImportError:
    pass
