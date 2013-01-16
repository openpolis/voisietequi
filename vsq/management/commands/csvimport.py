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
            help='Type of import: questions|answers|parties'),
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

#        elif options['type'] == 'answers':
#            self.handle_answers(*args, **options)
#
#        elif options['type'] == 'parties':
#            self.handle_parties(*args, **options)
        else:
            self.logger.error("Wrong type %s. Select among questions|answers|parties." % options['type'])
            exit(1)

    def handle_questions(self, *args, **options):
        c = 0
        self.logger.info("Inizio import da %s" % self.csv_file)

        for r in self.unicode_reader:

        #               Totale:
        #               id,testo,approfondimento,accompagno,link
        # MODELLO
        #            slug = models.SlugField(max_length=200, unique=True,
        #                help_text="Valore suggerito, generato dal testo. Deve essere unico.")
        #    testo = models.TextField()
        #    testo_html = models.TextField(editable=False)
        #    approfondimento = models.TextField(blank=True, null=True)
        #    approfondimento_html = models.TextField(editable=False, blank=True, null=True)
        #    accompagno = models.TextField(blank=True, null=True)
        #    accompagno_html = models.TextField(editable=False, blank=True, null=True)
        #    link = models.URLField(blank=True, null=True)
        #    ordine = models.IntegerField(blank=False, null=False, choices=ORDINE_DOMANDE)

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


