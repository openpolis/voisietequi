from vsq.settings import *

DEBUG = True
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG
EARLYBIRD_ENABLE = False

ELECTION_CODE = 'europee2014'
COMPUTER_ADDR = 'tcp://local.computer.vsq.it:5557'
COMPUTER_URL='http://local.computer.vsq.it:8001'
DISQUS_FORUM = ''
MAILBIN_URL = 'tcp://127.0.0.1:5558'
MAILBIN_SERVICE = 'service.dominio.it'

ELECTION_NAME = 'Europee 2014'
PARTY_LEADER = 'Candidato alla Presidenza del Consiglio Europeo'
PARTY_COALITION = 'Gruppo al Parlamento Europeo'

SHOW_DEBUG_TOOLBAR = False

MEDIA_ROOT = '/workspace/projects/op/vsq/voisietequi/public/media'
MEDIA_URL = '/media/'

STATIC_ROOT = '/workspace/projects/op/vsq/voisietequi/public/static'
STATIC_URL = '/static/'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'database.db',
        'USER': '',
        'PASSWORD': '',
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
