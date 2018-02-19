import os
import random
import string
import json

from django.core.management import BaseCommand

__author__ = "Winston Cadwell"
__copyright__ = "Copyright 2018, Winston Cadwell"
__licence__ = "BSD 2-Clause Licence"
__version__ = "1.0"
__email__ = "wcadwell@gmail.com"


class Command(BaseCommand):

    def is_valid_file(self, file):
        if not os.path.isfile(file):
            self.stdout.write("File not found or path is invalid!")
            exit(1)
        else:
            return open(file, 'r+')  # return open file handlei

    @staticmethod
    def generate_new_key():
        return ''.join([random.SystemRandom().choice(string.ascii_letters + string.digits + string.punctuation)
                        for _ in range(50)])

    def add_arguments(self, parser):
        parser.add_argument('-f', '--file', type=str, dest='file',
                            default=str(os.path.join(os.path.expanduser("~"), '.config/helpdesk/config.json')))

    def update_key(self):
        with self.file as f:
            settings = json.loads(f.read())

            settings["secret_key"] = self.generate_new_key()

            f.seek(0)
            f.write(json.dumps(settings, indent=2))
            f.truncate()

    def handle(self, *args, **options):
        self.file = self.is_valid_file(options['file'])
        self.update_key()
