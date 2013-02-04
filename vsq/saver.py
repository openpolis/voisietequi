def handle_save_message():
    # storing
    import pika
    import multiprocessing
    from django.conf import settings
    from vsq.models import Utente, RispostaUtente
    try:
        import cPickle as pickle
    except ImportError:
        import pickle
    import logging
    logging.basicConfig()

    connection = pika.BlockingConnection(pika.URLParameters(settings.MQ_URL))
    channel = connection.channel()

    channel.exchange_declare(exchange=settings.MQ_EXCHANGE, exchange_type='topic')

    def callback_configure(ch, method, properties, body):
        data = pickle.loads(body)
        #print " [x] %r:%r" % (method.routing_key, data)
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
        consumer_callback=callback_configure,
        queue=queue_name,
    )

    def f():
        try:
            channel.start_consuming()
        except KeyboardInterrupt:
            channel.stop_consuming()
            connection.close()

    multiprocessing.Process(target=f).start()