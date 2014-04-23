from vsq.settings import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG
EARLYBIRD_ENABLE = False

# rabbitmq settings
# typically MQ_URL resembles:
# amqp://guest:guest@localhost:5672/%2f
ELECTION_CODE='{ELECTIONCODE}'
MQ_URL = '{MQ_URL}'
MQ_EXCHANGE = '{MQ_EXCHANGE}'
MQ_QUEUE = 'vsq.{election}'.format(election=ELECTION_CODE)
COMPUTER_URL='http://urlcomputer.dominio.it'
DISQUS_FORUM = ''
MAILBIN_URL = 'tcp://127.0.0.1:5558'
MAILBIN_SERVICE = 'service.dominio.it'

# nome mostrato sul sito
ELECTION_NAME = 'Europee 2014'
# voci mostrate dentro la scheda del partito
# PARTY_LEADER = 'Segretario'
# PARTY_COALITION = 'Coalizione'

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
