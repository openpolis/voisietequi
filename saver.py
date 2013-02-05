def handle_save_message():
    # storing
    import pika
    import os

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vsq.settings_local")

    from django.conf import settings
    mq_url = settings.MQ_URL


    if not settings.configured:
        settings.configure()

    from vsq.models import Utente, RispostaUtente
    try:
        import cPickle as pickle
    except ImportError:
        import pickle

    import logging
    logging.basicConfig()

    connection = pika.BlockingConnection(pika.URLParameters(mq_url))
    channel = connection.channel()

    channel.exchange_declare(exchange=settings.MQ_EXCHANGE, exchange_type='topic')

    def callback_save(ch, method, properties, body):
        data = pickle.loads(body)
        print " [x] %r:%r" % (method.routing_key, data)
        u = Utente(
            nickname= data['user_data']['name'],
            ip= data['user_data']['ip_address'],
            email= data['user_data']['email'],
            user_key= data['code']
            # agent = data['agent'],
        )
        u.save()

        for domanda, risposta in data['user_answers'].items():
            RispostaUtente(
                domanda_id = domanda,
                risposta_int = risposta,
                utente = u
            ).save()


        ch.basic_ack(delivery_tag = method.delivery_tag)
    #channel.queue_declare(config.MQ_PREFIX+'configure')
    queue_name = channel.queue_declare(exclusive=True).method.queue
    binding_key = "{queue}.save".format(queue=settings.MQ_QUEUE)
    channel.queue_bind(
        queue= queue_name,
        exchange= settings.MQ_EXCHANGE,
        routing_key= binding_key
    )
    channel.basic_consume(
        consumer_callback=callback_save,
        queue=queue_name,
    )

    print ' [x] Ready to save computer results'

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
        connection.close()


if __name__ == '__main__':

    handle_save_message()
