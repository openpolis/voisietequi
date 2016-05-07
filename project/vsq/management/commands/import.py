# -*- coding: utf-8 -*-
from uuid import uuid4
from django.core.management.base import BaseCommand
from vsq.utils.utfreader import *

from vsq.models import *
from optparse import make_option
import csv
import logging


class Command(BaseCommand):

    help = 'Import user answers from CSV'

    option_list = BaseCommand.option_list + (
        make_option('--csv-file',
            dest='csvfile',
            default='./risultati.csv',
            help='Select csv file'),
        make_option('--clean',
            action='store_true',
            dest='clean',
            default=False,
            help='Clean users and their replies'),
        make_option('--offset',
            dest='offset',
            default=None,
            help='Starting line, header excluded', type=int),
        make_option('--limit',
            dest='limit',
            default=None,
            help='Max number of users', type=int),
        )
    csv_file = ''
    encoding = 'utf8'
    logger = logging.getLogger('csvimport')
    unicode_reader = None


    def handle(self, *args, **options):

        self.csv_file = options['csvfile']
        self.to_clean = options['clean']
        self.offset = options['offset']
        self.limit = options['limit']
        self.logger.info('CSV FILE "%s"\n' % self.csv_file )

        # read first csv file
        try:
            self.unicode_reader = UnicodeDictReader(open(self.csv_file, 'r'), encoding=self.encoding)
        except IOError:
            self.logger.error("It was impossible to open file %s\n" % self.csv_file)
            exit(1)
        except csv.Error, e:
            self.logger.error("CSV error while reading %s: %s\n" % (self.csv_file, e.message))

        self.handle_answers()

    def handle_answers(self):

        c = -1
        self.logger.info("Caricamento domande...")

        domande = {}
        for d in Domanda.objects.all():
            domande[d.ordine] = d

        self.logger.info("Caricate %d domande" % len(domande))

        if self.to_clean:
            self.logger.info("Pulizia utenti e risposte")

            RispostaUtente.objects.all().delete()
            Utente.objects.all().delete()

            self.logger.info("Cancellati utenti e risposte")

        self.logger.info("Inizio import da %s" % self.csv_file)

        for r in self.unicode_reader:

            c += 1

            if not self.offset is None and c < self.offset:
                if c % 100 == 0:
                    self.logger.debug("Skip %d: before offset (%d)" % (c, self.offset))
                continue
            if not self.limit is None and c - (self.offset or 0) >= self.limit:
                self.logger.debug("Break at %d: after limit (%d)" % (c, self.limit))
                break

            self.logger.info("%s: Analizzando record: %s" % (r['email'], r['ip']))
            utente = Utente.objects.create(
                nickname=r['email'] or 'unknown',
                email=r['email'],
                ip=r['ip'],
                user_key=uuid4(),
            )
            risposte = []
            try:
                for i, j in [(k, r['r%d' % k]) for k in range(1, 26)]:
                    risposte.append(RispostaUtente(
                        domanda=domande[i],
                        risposta_int=int(j),
                        utente=utente,
                    ))
            except ValueError:
                self.logger.error("Risposta non valida per l'utente %s in riga %d: %s" % (utente, c, r))
                utente.delete()
                continue

            RispostaUtente.objects.bulk_create(risposte)
            self.logger.info("Aggiungo le %d risposte dell'utente: %s" % (len(risposte), utente,))


        self.logger.info("Inseriti %d utenti con le loro risposte" % (c - (self.offset or 0)))



