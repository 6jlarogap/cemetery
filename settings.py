# -*- coding: utf-8 -*-

import os.path
from contrib.constants import *

DEBUG = True
#DEBUG = False
TEMPLATE_DEBUG = DEBUG

ROOT_PATH = os.path.dirname(__file__)

ADMINS = (
    ('Soul', 'soul@youmemory.org'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'cemetery',                      # Or path to database file if using sqlite3.
        'USER': 'postgres',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
#TIME_ZONE = 'Europe/Moscow'
#TIME_ZONE = 'Europe/Minsk'
TIME_ZONE = None

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'ru-RU'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(ROOT_PATH, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
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
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

ROOT_URLCONF = 'cemetery.urls'

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
    'django_extensions',
    'annoying',
    'simplepagination',
    'pytils',
    'sentry',
    'sentry.client',
    'debug_toolbar',
    
    # Наши приложения
    'common',

)

INTERNAL_IPS = ['127.0.0.1',] + ['80.70.236.%s' % i for i in range(1, 255)]

LOGIN_URL = "/login/"
LOGOUT_URL = "/logout/"
LOGIN_REDIRECT_URL = "/"

PAGINATION_USER_PER_PAGE_ALLOWED = True


PLACE_PRODUCTTYPE_ID = "60925a32-2add-11e0-8b17-485b39c96dfe"
#BURIAL_PRODUCTTYPE_ID = 1


# Операции.
OPER_1 = "7d58e9ec-2add-11e0-8b17-485b39c96dfe"  # Захоронение
OPER_2 = "0df73c7a-a1a5-43d5-a31f-b4fee8c5e50b"  # Почетное захоронение
OPER_3 = "78672a34-2add-11e0-8b17-485b39c96dfe"  # Захоронение в существующую
OPER_4 = "732795d6-2add-11e0-8b17-485b39c96dfe"  # Подзахоронение к существующей
OPER_5 = "6e0492ac-2add-11e0-8b17-485b39c96dfe"  # Урна
OPER_6 = "c9b7a6b5-12a5-4da5-8242-b9e556bcc6e3"  # Захоронение детское

# Кодировка для файлов обмена.
CSV_ENCODING = "utf8"

# Настройки пэйджинации.
PAGINATION_USER_PER_PAGE_MAX = 50
PAGINATION_PER_PAGE = 5

SENTRY_TESTING = True

DEBUG_TOOLBAR_CONFIG = {'INTERCEPT_REDIRECTS': False}

try:
    from settings_local import *
except ImportError:
    pass