__author__ = 'boo'
from django.contrib import admin
from dynamic_model_classes.models import DefinitionsModel

class DefinitionsAdmin(admin.ModelAdmin):
    pass

admin.site.register(DefinitionsModel, DefinitionsAdmin)
