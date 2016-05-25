# Django settings for vsq project.
import django.conf.global_settings as DEFAULT_SETTINGS
import os


from sys import path
from os.path import abspath, basename, dirname, join, normpath
from environ import Env

########## PATH CONFIGURATION
PACKAGE_PATH = dirname(abspath(__file__))
PACKAGE_NAME = basename(PACKAGE_PATH)

PROJECT_PATH = dirname(PACKAGE_PATH)
PROJECT_NAME = "VoiSieteQui"
PROJECT_PACKAGE = "vsq"

REPO_PATH = dirname(PROJECT_PATH)
REPO_NAME = "voisietequi"

CONFIG_DIR = 'config'
CONFIG_PATH = join(REPO_PATH, CONFIG_DIR)

RESOURCE_DIR = 'resources'
RESOURCES_PATH = join(REPO_PATH, RESOURCE_DIR)

# Add our project to our pythonpath, this way we don't need to type our project
# name in our dotted import paths:
path.append(PROJECT_PATH)

# load environment variables
Env.read_env(normpath(join(CONFIG_PATH, '.env')))
env = Env()
########## END PATH CONFIGURATION


########## START VOISIETEQUI CONFIGURATION
# Site status
EARLYBIRD_ENABLE = env.bool('EARLYBIRD_ENABLE', default=False)
RESULTS_DUMP = normpath(join(RESOURCES_PATH, 'results.csv'))

# PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
# REPO_ROOT = os.path.abspath(os.path.dirname(PROJECT_ROOT))

ELECTION_CODE = env('ELECTION_CODE', default='election')
ELECTION_NAME = env('ELECTION_NAME', default='Elezioni')
PARTY_LEADER = env('PARTY_LEADER', default='Segretario')
PARTY_COALITION = env('PARTY_COALITION', default='Coalizione')

PARTY_TERM = env('PARTY_TERM', default='Partito')
PARTY_TERM_PLURAL = env('PARTY_TERM_PLURAL', default='Partiti')
PARTY_TERM_GENDER = env('PARTY_TERM_GENDER', default='male')
OF_PARTY_TERM_PLURAL = env('OF_PARTY_TERM_PLURAL', default='dei partiti')
THE_PARTY_TERM_PLURAL = env('THE_PARTY_TERM_PLURAL', default='i partiti')

PARTY_DESCRIPTION_TERM = env('PARTY_DESCRIPTION_TERM', default='Descrizione')
PARTY_LINKED_PARTIES_TERM = env('PARTY_LINKED_PARTIES_TERM', default='Partiti collegati')

OTHER_ELECTIONS = env.json('OTHER_ELECTIONS', default=[])
SHOW_PARTY_COALITION = env.bool('SHOW_PARTY_COALITION', default=True)

# External service configurations
HASHTAG = env('HASHTAG', default='voisietequi')
OP_BLOG_CATEGORY = env('OP_BLOG_CATEGORY', default='piattaforme/voisietequi')
DISQUS_FORUM = env('DISQUS_FORUM', default='')

# Computer configuration
COMPUTER_URL = env('COMPUTER_URL', default='http://urlcomputer.dominio.it')
PUB_ADDR = env('PUB_ADDR', default='*:5556')
PULL_ADDR = env('PULL_ADDR', default='*:5557')

# Mailbin configuration
MAILBIN_URL = env('MAILBIN_URL', default='tcp://127.0.0.1:5558')
MAILBIN_SERVICE = env('MAILBIN_SERVICE', default='xxx.voisietequi.it')

# Constraints:

# If you edit this option you have to make a migration
SLUG_MAX_LENGTH = 60

# Max and min values for points in the final graph
MIN_GRAPH_X=0
MIN_GRAPH_Y=0
MAX_GRAPH_X=1
MAX_GRAPH_Y=1

# Unused settings... to remove
# MQ_URL = 'amqp://guest:guest@localhost:5672/%2f'
# MQ_EXCHANGE = 'voisietequi'
# MQ_QUEUE = 'vsq.{election}'.format(election=ELECTION_CODE)
########## END VOISIETEQUI CONFIGURATION



########## DEBUG CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = env.bool('DEBUG', False)
########## END DEBUG CONFIGURATION


########## MANAGER CONFIGURATION
ADMIN_EMAIL = env('ADMIN_EMAIL', default='admin@%s.com' % PROJECT_NAME)
ADMIN_NAME = env('ADMIN_NAME', default=ADMIN_EMAIL.split('@')[0])

# See: https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = (
    (ADMIN_EMAIL, ADMIN_NAME),
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS

# See: https://docs.djangoproject.com/en/dev/ref/settings/#default-from-email
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL', default=ADMIN_EMAIL)

# See: https://docs.djangoproject.com/en/1.9/ref/settings/#email-backend
EMAIL_CONFIG = env.email_url(
    'EMAIL_URL', default='consolemail://')

vars().update(EMAIL_CONFIG)
########## END MANAGER CONFIGURATION


########## DATABASE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    'default': env.db(default='sqlite:///{0}'.format(normpath(join(RESOURCES_PATH, 'db', 'database.db'))))
}
########## END DATABASE CONFIGURATION


########## GENERAL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#time-zone
TIME_ZONE = 'Europe/Rome'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = 'it-IT'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = False
########## END GENERAL CONFIGURATION


########## MEDIA CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = env('MEDIA_ROOT', default=normpath(join(RESOURCES_PATH, 'media')))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = '/media/'
########## END MEDIA CONFIGURATION


########## STATIC FILE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = env('STATIC_ROOT', default=normpath(join(RESOURCES_PATH, 'static')))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = '/static/'

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = (
    normpath(join(PROJECT_PATH, 'static')),
)

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
########## END STATIC FILE CONFIGURATION


########## SECRET CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Note: This key should only be used for development and testing.
SECRET_KEY = env('SECRET_KEY')
########## END SECRET CONFIGURATION


########## SITE CONFIGURATION
# Hosts/domain names that are valid for this site
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])
########## END SITE CONFIGURATION


########## TEMPLATE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            normpath(join(PROJECT_PATH, 'templates')),
        ],
        'OPTIONS': {
            'context_processors': DEFAULT_SETTINGS.TEMPLATE_CONTEXT_PROCESSORS + [
                'vsq.context_processor.main_settings',
                'django.template.context_processors.request',
            ],
            'loaders': (
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
                # 'django.template.loaders.eggs.Loader',
            ),
            'debug': env.bool('TEMPLATE_DEBUG', default=DEBUG)
        }
    },
]
########## END TEMPLATE CONFIGURATION


########## MIDDLEWARE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#middleware-classes
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'vsq.middlewares.PrivateBetaMiddleware',
)
########## END MIDDLEWARE CONFIGURATION


########## URL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
ROOT_URLCONF = '%s.urls' % PACKAGE_NAME
########## END URL CONFIGURATION


########## APP CONFIGURATION
DJANGO_APPS = (
    # Default Django apps:
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Useful template tags:
    'django.contrib.humanize',

    # Admin panel and documentation:
    'django.contrib.admin',
    # 'django.contrib.admindocs',

    # Django helper
    'django_extensions',
    'debug_toolbar',
    'ckeditor',
)

# Apps specific for this project go here.
LOCAL_APPS = (
    'vsq',
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + LOCAL_APPS
########## END APP CONFIGURATION


########## AUTHENTICATION CONFIGURATION
AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
)
########## END AUTHENTICATION CONFIGURATION


########## LOGGING CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#logging
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
        },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'formatter': 'standard'
        },
        'logfile': {
            'level':'INFO',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': normpath(join(RESOURCES_PATH, 'logs', 'voisietequi.log')),
            'maxBytes': 10000000,
            'backupCount': 10,
            'formatter': 'standard',
            },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
            },
        'csvimport': {
            'handlers': ['console', 'logfile'],
            'level': 'DEBUG',
            'propagate': True,
            }
    }
}
########## END LOGGING CONFIGURATION


########## WSGI CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = '%s.wsgi.application' % PACKAGE_NAME
########## END WSGI CONFIGURATION


########## START CACHE CONFIGURATION
# See: https://docs.djangoproject.com/en/1.9/ref/settings/#caches
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': normpath(join(RESOURCES_PATH, 'cache')),
        'TIMEOUT': 60,
        'OPTIONS': {
            'MAX_ENTRIES': 1000
        }
    }
}
########## END CACHE CONFIGURATION


########## START MESSAGES CONFIGURATION
MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'
########## END MESSAGES CONFIGURATION


TINYMCE_DEFAULT_CONFIG = {
    'theme': "advanced",
    'custom_undo_redo_levels': 10,
}
