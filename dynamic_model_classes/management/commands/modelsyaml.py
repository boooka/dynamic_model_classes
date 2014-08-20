import os
import fnmatch
import json

import yaml
from django.core.management.base import BaseCommand, CommandError
from django.core import management
from django.db.utils import OperationalError

from dynamic_model_classes.models import StoredYamlModel, YamlDocsModel


__author__ = 'boo'

class Command(BaseCommand):
    help = "Parse filenames, specified at the command line as a args. If they be successfully imported, as yaml formatted, then will create models."
    verbosity = 0

    def parse_yaml(self, fname, recursion=False):
        if not fname and self.verbosity:
            self.stderr.write('File not specified for parsing')
            return

        absfname = os.path.abspath(fname)
        filesize = os.path.getsize(absfname)
        # check by name and size
        stored_yaml = StoredYamlModel.objects.filter(filepath=absfname, filesize=filesize)

        # also check exists tables if absent try syncdb
        try:
            exists = stored_yaml.exists()
        except OperationalError:
            if recursion:
                # Something went wrong
                self.stdout.write('Except "%s" on "%s"' % sys.exc_info()[:2])
                return
            management.call_command('syncdb')
            # try again on synced db
            self.parse_yaml(fname, True)
            return

        if exists and self.verbosity:
            # identicaly file
            self.stdout.write('File "%s" already parsed' % absfname)
            return

        # yes, have a file with defferencies or new
        if self.verbosity:
            self.stdout.write('Parsing "%s"' % absfname)

        f = open(absfname)
        # now try to get parsed data from yaml formated file
        for data in yaml.load_all(f.read(-1)):
            # for late use it will be saved and not loaded from structured file
            stored, created = StoredYamlModel.objects.get_or_create(filepath=absfname, defaults={'filesize':filesize})
            stored.save()

            for doc, v in data.items():
                if not created:
                    # update definations
                    yamldoc = YamlDocsModel.objects.get(storedby=stored,docname=doc)
                    yamldoc.definition = json.dumps(v)
                else:
                    # new file - new records
                    yamldoc = YamlDocsModel(storedby=stored, docname=doc, definition=json.dumps(v))

                yamldoc.save()

            if self.verbosity:
                self.stdout.write('%s file and parse data' % created and 'Store' or 'Update')


    def handle(self, *args, **kwargs):

        self.verbosity = int(kwargs.get('verbosity')) > 1

        if not args:
            if self.verbosity:
                self.stderr.write('No file names specified in command args, parse all yaml in current dir')

            # find yaml files in current dir
            for file in os.listdir('.'):
                if fnmatch.fnmatch(file, '*.yaml'):
                    # also parse yaml files
                    self.parse_yaml(file)

        for fname in args:
            if not os.path.exists(fname):
                raise CommandError('File "%s" does not exist' % fname)

            self.parse_yaml(fname)

        if self.verbosity:
            self.stdout.write('Command parse all files')