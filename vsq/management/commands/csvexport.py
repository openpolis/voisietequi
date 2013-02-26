import csv
import logging
from optparse import make_option
from django.core.management import BaseCommand
from vsq.models import Utente
from vsq.utils.utfreader import UnicodeDictWriter

__author__ = 'guglielmo'

"""
Export results in CSV format
"""

class Command(BaseCommand):

    help = 'Export user votes into CSV'

    option_list = BaseCommand.option_list + (
        make_option('--csv-file',
                    dest='csvfile',
                    default='./risposte.csv',
                    help='Select csv file'),
    )
    csv_file = ''
    encoding = 'utf8'
    logger = logging.getLogger('csvimport')
    unicode_writer = None

    def handle(self, *args, **options):

        self.csv_file = options['csvfile']
        self.logger.info('CSV FILE "%s"\n' % self.csv_file )

        # read first csv file
        try:
            self.unicode_writer = UnicodeDictWriter(
                open(self.csv_file, 'w'),
                encoding=self.encoding,
                fieldnames=['email', 'created_at', 'ip'] + map("r{0}".format, range(1,26)),
            )
        except IOError:
            self.logger.error("It was impossible to open file %s\n" % self.csv_file)
            exit(1)
        except csv.Error, e:
            self.logger.error("CSV error while writing %s: %s\n" % (self.csv_file, e.message))

        users = Utente.objects.all()
        for (n, u) in enumerate(users, start=1):
            row = {
                'email': u.email if u.email  else '-',
                'created_at': str(u.created_at),
                'ip': u.ip,
            }
            for r in u.rispostautente_set.all():
                row['r{0}'.format(r.domanda_id)] = str(r.risposta_int)

            self.unicode_writer.writerow(row)

            if n % 1000 == 0:
                self.logger.info("%d" % (n,))


