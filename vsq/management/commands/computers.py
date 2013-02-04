"""
This command execute exchange messages between this application
and computers, through rabbitMq server.
To configure this command can set:
ELECTION_CODE='politiche2013'
MQ_URL='amqp://guest:guest@localhost:5672/%2f'
MQ_EXCHANGE='voisietequi'
MQ_QUEUE='vsq.{election}'.format(election=ELECTION_CODE)

"""
from django.contrib.humanize.templatetags.humanize import naturaltime

import pika
from optparse import make_option
from datetime import datetime
from django.conf import settings
from django.core.management import BaseCommand, CommandError
try:
    import cPickle as pickle
except ImportError:
    import pickle

ELECTION_CODE = settings.ELECTION_CODE

# helper for settings
def setting(name, default=None): return getattr(settings,name) if hasattr(settings, name) and getattr(settings,name) else default

DEFAULT_URL = 'amqp://guest:guest@localhost:5672/%2f'
DEFAULT_EXCHANGE = 'voisietequi'
DEFAULT_QUEUE = 'vsq.{election}'.format(election=ELECTION_CODE)

DISCOVER_QUEUE_NAME = '{queue}.discover'.format( queue=settings.MQ_QUEUE )
CONFIGURE_QUEUE_NAME = '{queue}.configure'.format( queue=settings.MQ_QUEUE )

class Command(BaseCommand):

    help = 'Configure remote computers'

    option_list = BaseCommand.option_list + (
        make_option('-u','--url',
            dest='url',
            default=settings.MQ_URL,
            help='Broker url (es: {example})'.format(example=DEFAULT_URL)),
        make_option('-e','--exchange',
            dest='exchange',
            default=settings.MQ_EXCHANGE,
            help='Name of message queue exchange (es: {example})'.format(example=DEFAULT_EXCHANGE)),
        make_option('-q','--queue',
            dest='queue',
            default=DEFAULT_QUEUE,
            help='Name of message queue (es: {example})'.format(example=DEFAULT_QUEUE)),
        )

    def handle(self, *args, **options):
        action = args[0] if args else 'discover'
        print 'ACTION:', action
        print 'EXCHANGE: ', options['exchange']
        print 'URL: ', options['url']

        if action == 'discover':
            self.discover_handle(**options)
        elif action == 'configure':
            self.configure_handle(**options)
        elif action == 'test':
            if len(args) != 2:
                raise CommandError('Append a computer url to test it.')
            self.test_handle(args[1], **options)
        else:
            raise CommandError('Invalid action. Only "discover" and "configure" are allowed')

    def on_computer_discover(self, now):
        def callback(ch, method, properties, body):

            #print " [x] Received %r:%r" % (method.routing_key, pickle.loads(body),)
            data = pickle.loads(body)
            lag = datetime.now() - now

            last_update = naturaltime(data['last_update']) if data['last_update'] else 'NOT CONFIGURED'
            print( ' [x] {host} configured {last_update} [{ts}ms]'.format(
                host = data['host'],
                last_update = last_update,
                ts = (lag.microseconds / 1000) + (lag.seconds * 1000),
            ))
        return callback

    def discover_handle(self, **options):
        print 'QUEUE: ', DISCOVER_QUEUE_NAME
        connection = pika.BlockingConnection(pika.URLParameters(options['url']))
        channel = connection.channel()

        channel.exchange_declare(exchange=options['exchange'], exchange_type='topic')

        now = datetime.now()

        # rpc
        callback_queue = channel.queue_declare(exclusive=True).method.queue
        #channel.queue_bind(exchange=options['MQ_EXCHANGE'], queue=callback_queue)
        channel.basic_consume(self.on_computer_discover(now), no_ack=True, queue=callback_queue)
        #end rpc

        routing_key = DISCOVER_QUEUE_NAME
        channel.basic_publish(
            exchange=options['exchange'],
            routing_key=routing_key,
            body=pickle.dumps(now),
            properties=pika.BasicProperties( reply_to = callback_queue ), #rpc
        )
        print(" [*] Discover message sent: {0}".format(now))

        try:
            channel.start_consuming()
        except KeyboardInterrupt:
            channel.stop_consuming()
            connection.close()

    def configure_handle(self, **options):
        print 'QUEUE: ', CONFIGURE_QUEUE_NAME

        connection = pika.BlockingConnection( pika.URLParameters( options['url'] ) )
        print ' [*] Connect to %s' % options['url']
        channel = connection.channel()
        channel.exchange_declare(options['exchange'], exchange_type='topic')
        queue_name = CONFIGURE_QUEUE_NAME
        channel.queue_declare(queue=queue_name)
        channel.queue_bind(exchange=options['exchange'], queue=queue_name)
        channel.basic_publish(
            exchange=options['exchange'],
            routing_key=queue_name,
            body=pickle.dumps({
                'election_code': ELECTION_CODE,
                'configuration': self.extract_configuration(),
#                'configuration': {"1": {"1": 3, "2": 3, "3": -1, "4": -1, "5": 2, "6": 1, "7": 3, "8": 2, "9": -2, "10": 2, "11": 2, "12": 1, "13": 1, "14": -1, "15": 2, "16": 2, "17": 2, "18": 1, "19": 1, "20": -1, "21": -2, "22": 1, "23": 2, "24": 1, "25": 2}, "2": {"1": 2, "2": 1, "3": 1, "4": 3, "5": -1, "6": -1, "7": -3, "8": 2, "9": 3, "10": 3, "11": 2, "12": -1, "13": -3, "14": -3, "15": 3, "16": 3, "17": 1, "18": -2, "19": -3, "20": 3, "21": 1, "22": 2, "23": 2, "24": -3, "25": 2}, "3": {"1": 2, "2": 2, "3": 1, "4": 3, "5": -1, "6": -1, "7": -1, "8": -2, "9": 3, "10": 3, "11": -2, "12": 1, "13": -2, "14": -2, "15": 2, "16": 2, "17": 2, "18": -2, "19": 1, "20": 2, "21": 2, "22": 2, "23": 3, "24": 2, "25": 1}, "4": {"1": 3, "2": 3, "3": -3, "4": -1, "5": 3, "6": 3, "7": 2, "8": 3, "9": -1, "10": 3, "11": 3, "12": 3, "13": 3, "14": 3, "15": 3, "16": -3, "17": -3, "18": 2, "19": -3, "20": -3, "21": -3, "22": -3, "23": -3, "24": -1, "25": 3}, "5": {"1": 1, "2": 1, "3": 1, "4": 2, "5": -1, "6": -1, "7": 3, "8": 1, "9": 1, "10": 1, "11": -2, "12": -2, "13": -3, "14": -3, "15": 1, "16": 3, "17": 3, "18": -3, "19": 3, "20": 3, "21": 2, "22": 3, "23": 3, "24": 3, "25": -2}, "6": {"1": 1, "2": 3, "3": -1, "4": 1, "5": 1, "6": 1, "7": -2, "8": 2, "9": 1, "10": 1, "11": 1, "12": 1, "13": -2, "14": -1, "15": 1, "16": 1, "17": -1, "18": -3, "19": -3, "20": 3, "21": 3, "22": -1, "23": 3, "24": 3, "25": 1}, "7": {"1": 2, "2": 3, "3": 1, "4": 2, "5": 2, "6": 3, "7": 1, "8": 2, "9": 3, "10": 2, "11": 3, "12": 3, "13": 3, "14": 1, "15": 3, "16": -3, "17": -2, "18": 3, "19": 1, "20": -1, "21": 1, "22": 1, "23": 2, "24": 2, "25": 1}, "8": {"1": 2, "2": 3, "3": -1, "4": 3, "5": 3, "6": 3, "7": 2, "8": 3, "9": -2, "10": 3, "11": 3, "12": 2, "13": 2, "14": 3, "15": 3, "16": -2, "17": -2, "18": 1, "19": -3, "20": -2, "21": 1, "22": -2, "23": 3, "24": 2, "25": 3}, "9": {"1": 3, "2": 3, "3": -3, "4": -2, "5": 1, "6": 3, "7": 3, "8": 3, "9": 1, "10": 3, "11": 2, "12": 2, "13": 3, "14": 2, "15": 3, "16": -3, "17": -3, "18": 3, "19": -3, "20": -3, "21": -3, "22": -3, "23": -3, "24": 1, "25": 1}, "11": {"1": 2, "2": 3, "3": -3, "4": -3, "5": 3, "6": 1, "7": 3, "8": 3, "9": 1, "10": 3, "11": 2, "12": 2, "13": 3, "14": 3, "15": 2, "16": -3, "17": -3, "18": 2, "19": -3, "20": -3, "21": -3, "22": -3, "23": -3, "24": 1, "25": 1}, "14": {"1": 2, "2": 3, "3": -3, "4": 3, "5": 3, "6": 3, "7": 3, "8": 3, "9": 3, "10": 3, "11": 3, "12": 2, "13": 3, "14": 3, "15": 3, "16": -3, "17": -3, "18": 3, "19": -3, "20": -3, "21": 3, "22": -3, "23": -3, "24": 3, "25": 3}, "16": {"1": -1, "2": 3, "3": -1, "4": 1, "5": 1, "6": 1, "7": -3, "8": 1, "9": 1, "10": 1, "11": 1, "12": -1, "13": -3, "14": -1, "15": 1, "16": 1, "17": 1, "18": -3, "19": -3, "20": 3, "21": 3, "22": 2, "23": 2, "24": 3, "25": 1}}
            }))
        print " [x] Start configuration: %r" % (ELECTION_CODE,)
        connection.close()

    def extract_configuration(self):
        from vsq.models import Partito
        config = {}
        for partito in Partito.objects.all():
            config[partito.party_key] = {}
            for risposta in partito.rispostapartito_set.all().select_related('domanda'):
                config[partito.party_key][risposta.domanda.pk] = risposta.risposta_int
        return config

    def test_handle(self, computer_url, **options):
        from vsq.models import Domanda
        from random import randint
        import json


        risposte = {}
        for domanda in Domanda.objects.all().order_by('ordine'):
            risposte[domanda.pk] = randint(1,3) * (1 if randint(0,1) == 0 else -1)
            print "{0}:{1} ".format( domanda.pk, risposte[domanda.pk]),
        print

        if not computer_url.startswith('http'):
            computer_url = 'http://%s' % computer_url
        data = json.dumps({
            'election_code': ELECTION_CODE,
            'user_data': {'email': 'email@email.tld','name':'mariorossi%s' % randint(1,9999999)},
            'user_answers': risposte,
            'test': True
        })

        from urllib2 import Request, urlopen, URLError
        req = Request(computer_url, data)
        try:
            response = urlopen(req)
        except URLError as e:
            if hasattr(e, 'reason'):
                print 'We failed to reach a server.'
                print 'Reason: ', e.reason
            elif hasattr(e, 'code'):
                print 'The server couldn\'t fulfill the request.'
                print 'Error code: ', e.code
        else:
            # everything is fine
            data = response.read()
            data = json.loads(data)

            print 'execution code:', data['code']
            for party, x, y in data['results']:
                print "{0:^10}".format(party), x, y


