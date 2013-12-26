from django.contrib import admin
import models


__author__ = 'boo'

admin.site.register([models.YamlDocsModel, models.StoredYamlModel,])
