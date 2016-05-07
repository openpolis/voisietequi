import csv
import logging
from optparse import make_option
from django.core.management import BaseCommand
from vsq.models import Utente, Partito
from vsq.utils.utfreader import UnicodeDictWriter

__author__ = 'guglielmo'

"""
Export results in CSV format
Different kinds of results can be extracted, according to the invocation mode.
Default mode just extracts user answers.
"""

class Command(BaseCommand):

    RISPOSTE_MODE = 1
    RISPOSTE_DISTANZE_MODE = 2
    RISPOSTE_DISTANZE_COORDINATE_MODE = 3
    PARTITI_MODE = 4

    option_list = BaseCommand.option_list + (
        make_option('--csv-file',
                    dest='csvfile',
                    default='./out.csv',
                    help='Select csv file name'),
        make_option('--risposte',
                    dest='mode',
                    action='store_const',
                    const=RISPOSTE_MODE,
                    help='Extract users answers (default)',
                    default=False),
        make_option('--risposte-dist',
                    dest='mode',
                    action='store_const',
                    const=RISPOSTE_DISTANZE_MODE,
                    help='Exctract user answers and real distances from parties',
                    default=False),
        make_option('--risposte-dist-coord',
                    dest='mode',
                    action='store_const',
                    const=RISPOSTE_DISTANZE_COORDINATE_MODE,
                    help='Extract user answers, real distances, coordinates, projected distances and deltas',
                    default=False),
        make_option('--partiti',
                    dest='mode',
                    action='store_const',
                    const=PARTITI_MODE,
                    help='Only exctract partiti answers',
                    default=False),
        make_option('--headers',
                    dest='headers',
                    action='store_true', default=False,
                    help='Write headers before CSV records'),
    )
    csv_file = ''
    encoding = 'utf8'
    logger = logging.getLogger('csvimport')
    unicode_writer = None

    def handle(self, *args, **options):
        self.csv_file = options['csvfile']
        self.logger.info('CSV FILE "%s"\n' % self.csv_file )
        self.mode = options['mode']
        self.headers = options['headers']

        # parties query
        parties = Partito.objects.all()
        sigle = [p['sigla'] for p in parties.values('sigla')]
        risposte_partiti = {}
        for p in parties:
            risposte_partiti[p.sigla] = [(rp['domanda_id'], rp['risposta_int']) \
                                         for rp in p.get_answers().values('domanda_id', 'risposta_int')]

        # fieldnames definitions, according to selected mode
        if self.mode == self.PARTITI_MODE:
            fieldnames = ['coalizione', 'sigla', 'originale'] + map("r{0}".format, range(1,26))
        elif self.mode == self.RISPOSTE_DISTANZE_MODE:
            fieldnames = ['email', 'created_at', 'ip'] +\
                            map("r{0}".format, range(1,26)) + \
                             map("dr[{0}]".format, sigle)
        elif self.mode == self.RISPOSTE_DISTANZE_COORDINATE_MODE:
            fieldnames = ['email', 'created_at', 'ip'] +\
                         map("r{0}".format, range(1,26)) +\
                         map("dr[{0}]".format, sigle) +\
                         ["c[user]",] + map("c[{0}]".format, sigle) +\
                         map("dp[{0}]".format, sigle)
        else:
            fieldnames = ['email', 'created_at', 'ip'] + map("r{0}".format, range(1,26))

        # open csv file for writing
        try:
            self.unicode_writer = UnicodeDictWriter(
                open(self.csv_file, 'w'),
                dialect=csv.excel,
                encoding=self.encoding,
                fieldnames=fieldnames,
            )
        except IOError:
            self.logger.error("It was impossible to open file %s\n" % self.csv_file)
            exit(1)
        except csv.Error, e:
            self.logger.error("CSV error while writing %s: %s\n" % (self.csv_file, e.message))

        if self.mode == self.PARTITI_MODE:
            if self.headers:
                self.unicode_writer.writeheader()
            for (n,p) in enumerate(parties, start=1):
                row = {
                    'coalizione': p.coalizione.nome,
                    'sigla': p.sigla,
                    'originale': str(not p.nonorig),
                    }
                for r in risposte_partiti[p.sigla]:
                    row['r{0}'.format(r[0])] = str(r[1])

                self.unicode_writer.writerow(row)
            self.logger.info("%d records extracted" % n)

        else:
            # main users query, exclude test and debugging
            users = Utente.objects.exclude(nickname__istartswith='deletami').exclude(nickname__iexact='test')
            if self.headers:
                self.unicode_writer.writeheader()
            for (n, u) in enumerate(users, start=1):
                row = {
                    'email': u.email if u.email  else '-',
                    'created_at': str(u.created_at),
                    'ip': u.ip,
                }
                risposte_utente = [(ru['domanda_id'], ru['risposta_int']) \
                                   for ru in u.get_answers().values('domanda_id', 'risposta_int')]
                for r in risposte_utente:
                    row['r{0}'.format(r[0])] = str(r[1])

                if self.mode == self.RISPOSTE_DISTANZE_MODE or self.mode == self.RISPOSTE_DISTANZE_COORDINATE_MODE:
                    for s in sigle:
                        user_answers = [ru[1] for ru in risposte_utente]
                        party_answers = [rp[1] for rp in risposte_partiti[s]]

                        row['dr[{0}]'.format(s)] = "%.3f" % self.metric(user_answers, party_answers)


                if self.mode == self.RISPOSTE_DISTANZE_COORDINATE_MODE:
                    import json

                    # legge le coord del test di un utente da json nel DB
                    coordinate_field = json.loads(u.coord)

                    # estrae le coordinate dell'utente
                    for cu in coordinate_field:
                        if cu[0] == 'user':
                            ux = float(cu[1])
                            uy = float(cu[2])

                    # e crea due dict sulle sigle, per coordinate e distanze
                    coordinate = {}
                    distanze = {}
                    for cu in coordinate_field:
                        x = float(cu[1])
                        y = float(cu[2])

                        coordinate[cu[0]] = "%.3f;%.3f" % (x, y)

                        if cu[0] != 'user':
                            distanze[cu[0]] = ((ux - x) ** 2 + (uy - y) ** 2) ** (0.5)

                    for sigla, cu in coordinate.iteritems():
                        row['c[{0}]'.format(sigla)] = "%s" % cu

                    for sigla, d in distanze.iteritems():
                        row['dp[{0}]'.format(sigla)] = "%.3f" % d


                self.unicode_writer.writerow(row)

                if n % 1000 == 0:
                    self.logger.info("%d" % (n,))


    def metric(self, x, y):
        """
        Compute the pairwise distance between vector x and y
        """
        d = 2
        summ = []
        i = 0
        while i < len(x):
            # in this case use euclidean distance
            summ.append((x[i] - y[i])**d)
            i = i + 1
        return sum(summ) ** (1 / float(d))
