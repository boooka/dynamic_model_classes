import os
import fnmatch
import yaml
import json

from django.core.management.base import BaseCommand, CommandError
from dynamic_model_classes.models import create_model, StoredYamlModel, YamlDocsModel



__author__ = 'boo'

class Command(BaseCommand):
    help = "Parse filenames, specified at the command line as a args. If they be successfully imported, as yaml formatted, then will create models."
    verbosity = 0

    def parse_yaml(self, fname):
        if not fname and self.verbosity:
            self.stderr.write('File not specified for parsing')
            return

        absfname = os.path.abspath(fname)

        if absfname and StoredYamlModel.objects.filter(filepath=absfname):
            if self.verbosity:
                self.stdout.write('File "%s" already parsed' % absfname)
            return

        f = open(absfname)
        # now try to get parsed data from yaml formated file
        for data in yaml.load_all(f.read(-1)):
            # for late use it will be saved and not loaded from structured file
            stored = StoredYamlModel(filepath=absfname)
            stored.save()

            for doc, v in data.items():
                yamldoc = YamlDocsModel(storedby=stored, docname=doc, definition=json.dumps(v))
                yamldoc.save()
                create_model(doc, v)

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