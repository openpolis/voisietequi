# Django settings for vsq project.
import django.conf.global_settings as DEFAULT_SETTINGS
import os
import environ

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
REPO_ROOT = os.path.abspath(os.path.dirname(PROJECT_ROOT))
CONFIG_DIR = os.path.abspath(os.path.join(PROJECT_ROOT, '../config'))

env = environ.Env()
env.read_env(os.path.join(CONFIG_DIR, '.env'))

RESOURCES_DIR = env.str('RESOURCES_DIR', default=os.path.abspath(os.path.join(BASE_DIR, '../resources')))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str('SECRET_KEY', default='52n0*2bkg-wp^#u7#9vpoj2a+ww)a2q^lun)(cwv=5q=bnjlo5')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG', default=False)
TEMPLATE_DEBUG = env.bool('TEMPLATE_DEBUG', default=False)
SHOW_DEBUG_TOOLBAR = env.bool('SHOW_DEBUG_TOOLBAR', default=False)
LOCAL_DEVELOPEMENT = env.bool('LOCAL_DEVELOPMENT', default=False)
EARLYBIRD_ENABLE = env.bool('EARLYBIRD_ENABLE', default=False)
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', [])

INTERNAL_IPS = ['127.0.0.1', ]


SLUG_MAX_LENGTH = 60
ELECTION_CODE=env.string('ELECTION_CODE', default='election')
HASHTAG='voisietequi'
OP_BLOG_CATEGORY = 'piattaforme/voisietequi'
COMPUTER_URL='http://urlcomputer.dominio.it'
COMPUTER_ADDR = 'tcp://urlcomputer.dominio.it:5557'
DISQUS_FORUM = ''

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
            'default': env.db(default='sqlite:///%s/db/db.sqlite3' % RESOURCES_DIR)
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

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

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

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_ROOT, 'templates'),
    )

TEMPLATE_CONTEXT_PROCESSORS = DEFAULT_SETTINGS.TEMPLATE_CONTEXT_PROCESSORS + (
    'vsq.context_processor.main_settings',
    'django.core.context_processors.request',
    )

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
    'south',
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
