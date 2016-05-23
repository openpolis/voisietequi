"""
This command execute exchange messages between this application
and computers, through ZMQ 
"""
from optparse import make_option
from django.conf import settings
from django.core.management import BaseCommand, CommandError
from vsq.management.proc import controller_proc
from vsq.models import Partito


# helper for settings
def setting(name, default=None): return getattr(settings,name) if hasattr(settings, name) and getattr(settings,name) else default


class Command(BaseCommand):

    help = """Send command to remote computers, or listen to their communication. 
    <action> can be 'saver', 'partiti', 'configure' or 'test <computation_url>'
    """
    args = '<action>'

    def handle(self, *args, **options):
        action = args[0] if args else 'discover'

        if action == 'saver':
            self.saver_handle(**options)
        elif action == 'configure':
            self.configure_handle(**options)
        elif action == 'partiti':
            self.partiti_handle(**options)
        elif action == 'test':
            if len(args) != 2:
                raise CommandError('Append a computer url to test it.')
            self.test_handle(args[1], **options)
        else:
            raise CommandError('Invalid action. Only "discover", "configure", "partiti" or "test" are allowed')

    def saver_handle(self, **options):
        """
        Starts a saver daemon that listens on the specified pull address
        and 
        """

        controller = controller_proc.ControllerProcess(settings.PULL_ADDR)
        controller.start()
        controller.join()

    def configure_handle(self, **options):

        controller = controller_proc.ControllerProcess(settings.PULL_ADDR)
        controller.start()

        new_config = self.extract_configuration()

        controller_proc.send_configuration(settings.PUB_ADDR, settings.ELECTION_CODE, new_config)

        print " [x] Start configuration: %s %s (pub_addr: %s)" % (settings.ELECTION_CODE, new_config, settings.PUB_ADDR)

        try:
            controller.join()
        except KeyboardInterrupt:
            controller.stop()
            print "EXIT"

    def extract_configuration(self):
        from vsq.models import Partito
        import collections
        config = collections.defaultdict(dict)
        for partito in Partito.objects.all():
            # config[partito.sigla] = {}
            for risposta in partito.rispostapartito_set.all().select_related('domanda'):
                config[partito.sigla][risposta.domanda.pk] = risposta.risposta_int
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
            'election_code': settings.ELECTION_CODE,
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

    def partiti_handle(self, **options):
        """
        Get all parties positions from computer,
        whithout user
        """
        import json


        computer_url = "http://{0}.voisietequi.it/coordinate_partiti/{0}" .format(settings.ELECTION_CODE)
        print "looking up {0}".format(computer_url)

        from urllib2 import Request, urlopen, URLError
        req = Request(computer_url)
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

            for party, x, y in data:
                p = Partito.objects.get(sigla=party)
                p.coord_x = x
                p.coord_y = y
                p.save()
                print "{0:^10}".format(party), x, y

