# -*- coding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db import connection
from django.db.utils import DatabaseError
from django.core.management.base import BaseCommand, CommandError
from decimal import Decimal
from django.template.defaultfilters import slugify
from vsq.utils.utfreader import *

from vsq.models import *
from optparse import make_option
import csv
import logging
from datetime import datetime
from django.utils import timezone
from HTMLParser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ' '.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

class Command(BaseCommand):

    help = 'Import data from CSV'

    option_list = BaseCommand.option_list + (
        make_option('--csv-file',
            dest='csvfile',
            default='./domande.csv',
            help='Select csv file'),
        make_option('--type',
            dest='type',
            default=None,
            help='Type of import: questions|panswers|parties'),
        )
    csv_file = ''
    encoding = 'utf8'
    logger = logging.getLogger('csvimport')
    unicode_reader = None


    def handle(self, *args, **options):

        self.csv_file = options['csvfile']
        self.logger.info('CSV FILE "%s"\n' % self.csv_file )

        # read first csv file
        try:
            self.unicode_reader = UnicodeDictReader(open(self.csv_file, 'r'), encoding=self.encoding)
        except IOError:
            self.logger.error("It was impossible to open file %s\n" % self.csv_file)
            exit(1)
        except csv.Error, e:
            self.logger.error("CSV error while reading %s: %s\n" % (self.csv_file, e.message))

        if options['type'] == 'questions':
            self.handle_questions(*args, **options)

        elif options['type'] == 'panswers':
            self.handle_panswers(*args, **options)

        elif options['type'] == 'parties':
            self.handle_parties(*args, **options)
        else:
            self.logger.error("Wrong type %s. Select among questions|answers|parties." % options['type'])
            exit(1)

    def handle_questions(self, *args, **options):
        c = 0
        self.logger.info("Inizio import da %s" % self.csv_file)

        for r in self.unicode_reader:

        #               Totale:
        #               id,testo,approfondimento,accompagno,link


            created = False
            self.logger.info("%s: Analizzando record: %s" % ( r['id'],r['testo']))
            domanda, created = Domanda.objects.get_or_create(
                id = r['id'],

                defaults={
                    'testo':  r['testo'],
                    'approfondimento': r['approfondimento'],
                    'accompagno': r['accompagno'],
                    'link': r['link'],
                    'ordine':r['id'],
                    }
            )

            if created:
                self.logger.info("%s: domanda inserita: %s" % ( c, domanda))
            else:
                self.logger.debug("%s: domanda trovata e non duplicata: %s" % (c, domanda))


            domanda.save()
            c += 1

    def handle_parties(self, *args, **options):
        c = 0
        self.logger.info("Inizio import da %s" % self.csv_file)

        for r in self.unicode_reader:

        #  Totale:
        #  id,denominazione,party_key,sigla,responsabile_nome,responsabile_mail,risposte_ok,risposte_data,site,ancora

            created = False
            self.logger.info("%s: Analizzando record: %s" % ( r['id'],r['denominazione']))
            partito, created = Partito.objects.get_or_create(
                id = r['id'],

                defaults={
                    'denominazione':  r['denominazione'],
                    'party_key': r['party_key'],
                    'sigla': r['sigla'],
                    'responsabile_nome': r['responsabile_nome'],
                    'responsabile_email':r['responsabile_mail'],
                    'sito':r['site'],
                    }
            )

            if created:
                self.logger.info("%s: partito inserito: %s" % ( c, partito))
            else:
                self.logger.debug("%s: partito trovato e non duplicato: %s" % (c, partito))

            partito.save()
            c += 1


    #load parties answers from file

    def handle_panswers(self, *args, **options):
        c = 0
        self.logger.info("Inizio import da %s" % self.csv_file)

        for r in self.unicode_reader:

        #  Totale:
        #  id,domanda_id,partito_id,risposta_int,risposta_txt,nonorig


            created = False
            self.logger.info("Analizzando record: %s" % ( r['id'],))

            domanda=Domanda.objects.get(id=r['domanda_id'])
            partito=Partito.objects.get(id=r['partito_id'])

            rpartito, created = RispostaPartito.objects.get_or_create(
                id=r['id'],

                defaults={
                    'domanda':  domanda,
                    'partito': partito,
                    'risposta_int': r['risposta_int'],
                    'risposta_txt': r['risposta_txt'],
                    'nonorig':r['nonorig'],
                    }
            )

            if created:
                self.logger.info("%s: risposta partito inserita: %s" % ( c, rpartito))
            else:
                self.logger.debug("%s: risposta partito trovata e non duplicato: %s" % (c, rpartito))

            partito.save()
            c += 1



