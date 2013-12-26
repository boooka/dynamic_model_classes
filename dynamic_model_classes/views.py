# -*- coding: utf-8 -*-
from annoying.decorators import render_to
from models import get_model


__author__ = 'boo'

def get_models():
    dmodels, data = get_model(), {}

    for dmodel in dmodels:
        data[dmodel] = dmodel._meta.verbose_name
    return data

@render_to('home.html')
def home(request):

    # getting all installed models and initiating var data

    return {
        'data': get_models(),
    }

@render_to('model.html')
def model_content_view(request, model=None, object_id=None):
    '''
        object_id  - action is no matter if not set
        model_name - name of the viewed model object, must be set
    '''
    if not model:
        raise Exception('Error getting "%s" model objects' % model)

    m = get_model(model)
    if not m:
        raise Exception('Cant get model by name "%s"' % model)

    if object_id:
        objs = m.objects.get(id=object_id)
    else:
        objs = m.objects.all()

    return {
        'model': m,
        'objs': objs,
        'data': get_models(),
    }