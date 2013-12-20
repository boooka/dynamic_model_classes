from django.contrib import admin
from dynamic_model_classes.models import DefinitionsModel


__author__ = 'boo'

class DefinitionsAdmin(admin.ModelAdmin):
    pass

admin.site.register(DefinitionsModel, DefinitionsAdmin)
