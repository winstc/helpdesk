""" Provides a simple tool to fetch third party libraries

"""

import json
import os
import requests

from json.decoder import JSONDecodeError

from urllib.parse import urljoin

from django.conf import settings
from django.core.management.base import BaseCommand

__author__ = "Winston Cadwell"
__copyright__ = "Copyright 2018, Winston Cadwell"
__licence__ = "BSD 2-Clause Licence"
__version__ = "1.0"
__email__ = "wcadwell@gmail.com"

ROOT_DIR = os.path.dirname(settings.BASE_DIR)
FILE = os.path.join(ROOT_DIR, "third-party-libs.json")


class Command(BaseCommand):
    help = "Fetches third party css and javascript libraies. This includes bootstrap, jquery, and popper.js"

    json_data = ""

    libraries = {'bootstrap': ""}

    # loads json conf file from path
    def load_conf(self):
        if not os.path.isfile(FILE):
            raise FileNotFoundError
        else:
            try:
                with open(FILE, 'r') as f:
                    return json.loads(f.read())
            except IOError:
                self.stdout.write("Error reading file!")
                exit(1)
            except JSONDecodeError:
                self.stdout.write("Error parsing JSON. Please check syntax and try again!")
                exit(2)

    # downloads files from their sources according to conf file
    def fetch_files(self, file_list):
        for item in file_list:
            self.stdout.write(str("Package: {}".format(item[0])))
            destination_dir = os.path.abspath(os.path.join(settings.BASE_DIR, item[1]['destination']))

            for file in item[1]['files']:
                url = urljoin(item[1]['source'], file)

                if not os.path.exists(destination_dir):
                    os.makedirs(destination_dir)

                self.stdout.write(str("\tDownloading: {} from {}".format(file, url)))
                r = requests.get(url)
                dest_file = os.path.join(destination_dir, file)

                try:
                    with open(dest_file, 'wb') as f:
                        f.write(r.content)
                except FileNotFoundError:
                    self.stdout.write("Error writing file!")

    # removes existing files
    def clean_dirs(self, file_list):
        for item in file_list:
            self.stdout.write(str("Package: {}".format(item[0])))
            file_dir = os.path.abspath(os.path.join(settings.BASE_DIR, item[1]['destination']))

            for file in item[1]['files']:

                file = os.path.join(file_dir, file)

                if os.path.isfile(file):
                    self.stdout.write("Removing file: {}".format(file))
                    os.remove(file)
                else:
                    self.stdout.write("File {}: Does not exist".format(file))

    def add_arguments(self, parser):
        parser.add_argument('-c', '--clean', action='store_true', dest='clean_dirs')
        parser.add_argument('-r', '--refresh', action="store_true")
        parser.add_argument('--file', dest="file", type=str)

    def handle(self, *args, **options):
        # if user supplies file
        if options['file']:
            self.FILE = options['file']

        # load config
        self.json_data = self.load_conf()

        if options['clean_dirs']:
            self.clean_dirs(self.json_data.items())
        elif options['refresh']:
            self.clean_dirs(self.json_data.items())
            self.fetch_files(self.json_data.items())
        else:
            # download files
            self.fetch_files(self.json_data.items())
