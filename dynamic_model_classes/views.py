# -*- coding: utf-8 -*-
import json

from django.views.decorators.csrf import csrf_exempt
from annoying.decorators import render_to
from django_ajax.decorators import ajax
from models import get_model, DynamicModel



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
def model_content_view(request, model_name=None, object_id=None):
    '''
        object_id  - action is no matter if not set
        model_name - name of the viewed model object, must be set
    '''
    if not model_name:
        raise Exception('Model name not defined')

    model = get_model(model_name)
    if not model:
        raise Exception("Can't get model by name '%s'" % model_name)

    if object_id:
        objs = model.objects.get(id=object_id)
    else:
        objs = model.objects.all()

    return {
        'model': model._meta.fields[:-1],
        'objs': objs,
        'data': get_models(),
        'model_name': model_name,
        }


@csrf_exempt
@ajax
def sync(request, model_name=None):
    if request.method == 'POST':
        #TODO: check and save data
        return json.dumps({'message':'Ajax work'})

    return json.dumps({'message':'Something went wrong!'})