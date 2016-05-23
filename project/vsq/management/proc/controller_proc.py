import json
import time
import zmq
from . import base

__author__ = 'joke2k'


def send_configuration(pub_addr, election_code, config):

    # setup socket
    context = zmq.Context()
    
    # addr may be 'host:port' or ('host', 'port') or ('port')
    if isinstance(pub_addr, str):
        pub_addr = pub_addr.split(':')
    host, port = pub_addr if len(pub_addr) == 2 else ('*', pub_addr[0])
    
    # bind to specified address for PUB operations
    pub_socket = context.socket(zmq.PUB)
    pub_socket.bind('tcp://%s:%s' % (host, port))

    # wait for connections (handshake, ...)
    time.sleep(0.2)

    # create and send configuration message
    pub_socket.send_json(['configure', [election_code], config])

    # close socket
    pub_socket.close()


class ControllerProcess(base.ZmqProcess):

    def __init__(self, pull_addr):
        super(ControllerProcess, self).__init__()

        self.pull_addr = pull_addr

    def setup(self):
        """Sets up PyZMQ and creates all streams."""
        print "Listening to response from configured computers"

        super(ControllerProcess, self).setup()

        # Create the stream and add the message handler
        self.pull_stream, _ = self.stream(zmq.PULL, self.pull_addr, bind=True)
        self.pull_stream.on_recv(PullStreamHandler())

        print "Controller connected:", self.pull_addr

    def run(self):
        """Sets up everything and starts the event loop."""
        print ("Run Controller process")
        self.setup()
        self.loop.start()

    def stop(self):
        """Stops the event loop."""
        print ("Stop Controller process")
        self.loop.stop()


class PullStreamHandler(base.MessageHandler):

    def computer_configured(self, *args, **kwargs):
        print "Computer responded: %s %s" % (args, kwargs)

    def save_results(self, election_code, **data):
        print "Save results: %s %s" % (election_code, data)

        from vsq.models import Utente, RispostaUtente

        u_check = Utente.objects.filter(user_key=data['code']).count()
        if u_check > 0:
            print "ERR Utente esistente: {0}".format(data)
        else:
            u = Utente(
                nickname= data['user_data']['name'],
                ip= data['user_data']['ip_address'],
                agent = data['user_data']['agent'],
                email= data['user_data']['email'],
                wants_newsletter='wants_newsletter' in data['user_data'] and data['user_data']['wants_newsletter'] == 'on',
                user_key= data['code'],
                coord = json.dumps(data['results']),
                )
            from django.db.utils import DatabaseError
            try:
                u.save()

                objs = RispostaUtente.objects.bulk_create([
                    RispostaUtente(
                        domanda_id = domanda,
                        risposta_int = risposta,
                        utente = u
                    )
                    for domanda, risposta in data['user_answers'].items()
                ])

                print "User %s has answered to %d questions" % (data['code'], len(objs))
            except DatabaseError as e:
                print "ERR: %s" % (e,)


if __name__ == '__main__':

    controller = ControllerProcess(pull_addr='*:5557')
    controller.start()

    send_configuration('test', {'foo': 'bar'})

    controller.join()