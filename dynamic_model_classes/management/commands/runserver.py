# -*- coding: utf-8 -*-
from django.core import management
from django.core.management.commands.runserver import Command as RunserverCommand
from dynamic_model_classes.models import create_model, DefinitionsModel
import json


__author__ = 'boo'

class Command(RunserverCommand):

    def setupdynamicmodels(self):

        # load already exists models
        mobjs = DefinitionsModel.objects.all()
        for mobj in mobjs:
            data = json.loads(mobj.definition)
            create_model(data)

            #     from django.db.models.loading import cache
            #     cache.register_models('', *reg_models)


    def handle(self, addrport, *args, **options):

        self.setupdynamicmodels()

        # check models from files
        management.call_command('modelsyaml')

        # now can call sync db
        management.call_command('syncdb')

        # передаем управление методу базового класса
        super(Command, self).handle(addrport, *args, **options)