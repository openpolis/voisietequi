# Django settings for vsq project.
import django.conf.global_settings as DEFAULT_SETTINGS
import os

DEBUG = False
SHOW_DEBUG_TOOLBAR = False
LOCAL_DEVELOPEMENT = False
EARLYBIRD_ENABLE = False


PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
REPO_ROOT = os.path.abspath(os.path.dirname(PROJECT_ROOT))
SLUG_MAX_LENGTH = 60
ELECTION_CODE='election'
HASHTAG='voisietequi'
OP_BLOG_CATEGORY = 'piattaforme/voisietequi'
COMPUTER_URL='http://urlcomputer.dominio.it'
COMPUTER_ADDR = 'tcp://urlcomputer.dominio.it:5557'
DISQUS_FORUM = ''
# MQ_URL = 'amqp://guest:guest@localhost:5672/%2f'
# MQ_EXCHANGE = 'voisietequi'
# MQ_QUEUE = 'vsq.{election}'.format(election=ELECTION_CODE)
RESULTS_DUMP = os.path.join(REPO_ROOT, 'results.csv')
MAILBIN_URL = 'tcp://127.0.0.1:5558'
MAILBIN_SERVICE = 'xxx.voisietequi.it'

ELECTION_NAME = 'Elezioni'
PARTY_LEADER = 'Segretario'
PARTY_COALITION = 'Coalizione'

ADMINS = (
#    ('Nome Cognome', 'nome@dominio.it),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'sqlite.db',             # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

MESSAGES_STORAGE = 'django.contrib.messages.storage.session.CookieStorage'

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Rome'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'it-IT'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = False

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = '/home/vsq13/media'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = '/home/vsq13/sitestatic'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.

)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'q8vo24h1waemo)sh@54#qkm93w7%upj=ip($s7q-dm0dh0m)3x'


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

ROOT_URLCONF = 'vsq.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'vsq.wsgi.application'


# Deprecated from 1.7, see TEMPLATES DIRS below
_TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_ROOT, 'templates'),
    )

# Deprecated from 1.7, see TEMPLATES OPTIONS below
_TEMPLATE_CONTEXT_PROCESSORS = DEFAULT_SETTINGS.TEMPLATE_CONTEXT_PROCESSORS + [
    'vsq.context_processor.main_settings',
    'django.core.context_processors.request',
]

# List of callables that know how to import templates from various sources.
_TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': _TEMPLATE_DIRS,
        'OPTIONS': {
            'context_processors': _TEMPLATE_CONTEXT_PROCESSORS,
            'loaders': _TEMPLATE_LOADERS,
            'debug': DEBUG
        }
    },
]

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django_extensions',
    'django.contrib.humanize',
    'vsq',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
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
            'filename': REPO_ROOT + "/log/logfile",
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

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(REPO_ROOT, 'django-cache'),
        'TIMEOUT': 60,
        'OPTIONS': {
            'MAX_ENTRIES': 1000
        }
    }
}

#max and min values for points in the final graph
MIN_GRAPH_X=0
MIN_GRAPH_Y=0
MAX_GRAPH_X=1
MAX_GRAPH_Y=1
