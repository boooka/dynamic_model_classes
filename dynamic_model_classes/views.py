# -*- coding: utf-8 -*-
import json

from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from annoying.decorators import render_to
from django_ajax.decorators import ajax
from models import get_model, DynamicModel
from forms import DynamicForm


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
        'models': get_models(),
    }



@render_to('model.html')
@csrf_exempt
def model_content_view(request, model_name=None, object_id=None):
    '''
        object_id  - action is no matter if not set
        model_name - name of the viewed model object, must be set
    '''
    if not model_name:
        raise Exception('Model name is not defined')

    model = get_model(model_name)

    # if get multiple models or not get model by name
    assert model is not None and type(model) is not type(list), "Can't get model by name '%s'" % model_name

    if request.method == 'POST':
        form = DynamicForm(request.POST, instance=model())
        if form.is_valid() and u'save' in request.POST:
            obj = form.save()
    else:
        if object_id:
            objs = model.objects.get(id=object_id)
            form = DynamicForm(instance=objs)
        else:
            objs = model.objects.all()
            form = DynamicForm(instance=model())



    model_fields = [{
                'field': f,
                'field_type': u'%s' % f.template_type,
                'field_index': model._meta.fields.index(f),
                } for f in model._meta.fields[:-1]]
    model_name = model.model_name()

    return {
        'model_fields': model_fields,
        'model_name': model_name,
        'objs': model.objects.all(),
        'models': get_models,
        'form': form,
    }



# task do not require this check, her will be skipped
@csrf_exempt
@ajax
def sync(request, model_name=None):
    '''
    Ajax view

    :param request: contain modified data
    :param model_name: indicate modified model
    :return: status and new data from model
    '''

    if not model_name:
        raise Exception('Model name is not defined ')

    model = get_model(model_name)

    assert not isinstance(model,dict), "Multiple models assertion error"


    if request.method == 'POST':
        #TODO: check and save data
        pk = u'pk' in request.POST and request.POST['pk']
        obj = model.objects.get(pk=pk)
        initial_data = model_to_dict(obj)
        changed_data = initial_data.copy()
        changed_data.update({request.POST['name']: request.POST['value']})

        form = DynamicForm(changed_data, initial=model_to_dict(obj), instance=obj)

        if form.is_valid() and pk:

            form.save()
            return json.dumps({'message':'Update record %s id field %s' % (pk, request.POST['name'])})

    return json.dumps({'message':'Something went wrong!'})