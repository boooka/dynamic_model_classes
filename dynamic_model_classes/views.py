# -*- coding: utf-8 -*-
__author__ = 'boo'

from annoying.decorators import render_to
from django.db.models.loading import cache
import models

@render_to('home.html')
def home(request):

    dynamicmodels = set(cache.get_models(models)) - set([models.DefinitionsModel])
    data = {}
    for dmodel in dynamicmodels:
        data[dmodel._meta.model_name] = dmodel._meta.verbose_name

    return {
        'data': data,
    }