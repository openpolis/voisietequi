# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Count
import cStringIO
import codecs
import csv
from vsq.models import Domanda, RispostaUtente


class DictUnicodeWriter(object):

    def __init__(self, f, fieldnames, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.DictWriter(self.queue, fieldnames, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, D):
        #self.writer.writerow({k:v.encode("utf-8") for k,v in D.items()})
        self.writer.writerow(dict([(k, v.encode("utf-8")) for k, v in D.items()]))
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for D in rows:
            self.writerow(D)

    def writeheader(self):
        self.writer.writerow(dict((fn, fn) for fn in self.writer.fieldnames))
        #self.writer.writeheader()


class Command(BaseCommand):

    help = 'Export results'

    def handle(self, *args, **options):

        risposte = [-3, -2, -1, 1, 2, 3]
        headers = [
            'Ordine',
            'Domanda',
            'Molto Contrari',
            'Contrari',
            'Tendenzialmente Contrari',
            'Tendenzialmente Favorevoli',
            'Favorevoli',
            'Molto Favorevoli'
        ]
        results = []

        f = cStringIO.StringIO()
        w = DictUnicodeWriter(f, headers)
        w.writeheader()

        for domanda in Domanda.objects.all():

            row = [str(domanda.ordine), domanda.testo, ]

            conteggi = dict(zip(risposte, [0] * len(risposte)))

            for posizione in RispostaUtente.objects.filter(domanda=domanda).values('risposta_int').annotate(nr=Count('risposta_int')):

                conteggi[posizione['risposta_int']] = posizione['nr']

            row += [str(conteggi[x]) for x in risposte]

            results.append(dict(zip(headers, row)))

        w.writerows(results)
        result = f.getvalue()
        f.close()

        return result







