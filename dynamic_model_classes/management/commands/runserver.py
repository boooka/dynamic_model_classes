# -*- coding: utf-8 -*-
from django.core import management
from django.core.management.commands.runserver import Command as RunserverCommand
from dynamic_model_classes.models import create_model, YamlDocsModel
import json


__author__ = 'boo'

class Command(RunserverCommand):

    def setupdynamicmodels(self):

        # load already exists models
        mobjs = YamlDocsModel.objects.all()
        for mobj in mobjs:
            model_created = create_model(mobj.docname, json.loads(mobj.definition))
            if self.verbosity:
                self.stdout.write('Created model "%s"' % model_created)


    def handle(self, addrport, *args, **options):

        self.verbosity = int(options.get('verbosity')) > 1

        # all loaded models before well be saved in db and can be preloaded without source file
        self.setupdynamicmodels()

        # check models from files
        management.call_command('modelsyaml')

        # now can call sync db
        management.call_command('syncdb')

        # передаем управление методу базового класса
        super(Command, self).handle(addrport, *args, **options)

