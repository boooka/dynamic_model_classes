import os
import yaml

from django.core.management.base import BaseCommand, CommandError
from django.db import models
from dynamic_model_classes.models import create_abstract

__author__ = 'boo'

class Command(BaseCommand):
    help = "Parse filenames, specified at the command line as a args. If they be successfully imported, as yaml formatted, then will create models."


    def handle(self, *args, **kwargs):

        verbosity = int(kwargs.get('verbosity')) > 1

        if not args and verbosity:
            self.stderr.write('No file names specified in command args')

        for fname in args:
            if not os.path.exists(fname):
                raise CommandError('File "%s" does not exist' % fname)

            f = open(fname)

            # init mapped types
            maptypes = {
                        'char': models.CharField(max_length=255),
                        'int' : models.IntegerField(),
                        'date': models.DateField(auto_now=True),
                        }

            # now try to get parsed data from yaml formated file
            for data in yaml.load_all(f.read(-1)):
                for doc, v in data.items():
                    prefields = dict()

                    # check for contained fields list
                    if 'fields' in v and isinstance(v.get('fields'),list):
                        for field in v['fields']:
                            # skip as unformated
                            if not isinstance(field,dict):
                                continue
                            # skip without names
                            if not 'id' in field:
                                continue

                            fieldname = field['id']
                            prefields[fieldname] = maptypes['char']
                            if 'type' in field:
                                prefields[fieldname] = maptypes[field.get('type')]
                            if 'title' in field:
                                setattr(prefields[fieldname], 'help_text', field.get('title'))

                    m = create_abstract(doc, fields=prefields)


            if verbosity:
                self.stdout.write('Successfully parse file "%s"' % fname)