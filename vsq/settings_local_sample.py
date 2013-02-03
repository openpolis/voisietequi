from vsq.settings import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

SHOW_DEBUG_TOOLBAR = False

MEDIA_ROOT = '/home/vsq13/public/media'
MEDIA_URL = '/media/'

STATIC_ROOT = '/home/vsq13/public/static'
STATIC_URL = '/static/'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '{DBNAME}',
        'USER': '{DBUSER}',
        'PASSWORD': '{DBPASS}',
        'HOST': '',
        'PORT': '',
    }
}
SECRET_KEY = '{SECRET_KEY}'


if SHOW_DEBUG_TOOLBAR:
    INSTALLED_APPS = INSTALLED_APPS + ('debug_toolbar',)
    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': False,
        #    'SHOW_TOOLBAR_CALLBACK': custom_show_toolbar,
        #    'EXTRA_SIGNALS': ['myproject.signals.MySignal'],
        #    'HIDE_DJANGO_SQL': False,
        #    'TAG': 'div',
        #    'ENABLE_STACKTRACES' : True,
    }
    INTERNAL_IPS = ('127.0.0.1',)

ADMINS = (
    ('{ADMIN_NAME}', '{ADMIN_EMAIL}'),
)
