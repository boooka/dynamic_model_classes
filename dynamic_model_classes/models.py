import re
from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.db import models
from django.db.models.loading import cache
from django.forms import forms, fields, widgets
from django.utils.translation import ugettext_lazy as _

from forms import DynamicForm


__author__ = 'boo'


def create_abstract(name, fields=None, app_label='', module='', options=None, admin_opts=None):
    """
    Create specified model
    """
    class Meta:
        pass

    if app_label:
        # app_label must be set using the Meta inner class
        setattr(Meta, 'app_label', app_label)

    # Update Meta with any options that were provided
    if options is not None:
        for key, value in options.iteritems():
            setattr(Meta, key, value)

    # Set up a dictionary to simulate declarations within a class
    # also model_name attr point at func
    attrs = {'__module__': module, 'Meta': Meta}

    # Add in any fields that were provided
    if fields:
        attrs.update(fields)

    # Create the class, which automatically triggers ModelBase processing
    model = type(str(name), (DynamicModel,), attrs)

    if admin_opts is not None:
        class Admin(admin.ModelAdmin):
            pass
        for key, value in admin_opts:
            setattr(Admin, key, value)

    # Create an Admin class if admin options were provided
    admin.site.register(model)

    return model


class DynamicModel(models.Model):

    # TODO: verify why not _meta
    class Meta:
        abstract = True

    @classmethod
    def class_name(cls):
        "Returns a name for current model class"
        if hasattr(cls._meta,'model_name'):
            return cls._meta.model_name
        return _('undefined model')

    @classmethod
    def get_model(cls):
        return cls

    @classmethod
    def isdynamic(cls):
         return True

    def by_attrname(self, name=''):
        if hasattr(self, name):
            return getattr(self, name)
        return 'Undefined attribute'


    # def __unicode__(self):
    #     return u'%s: %s' % (
    #         self.model_name(),
    #         ','.join([unicode(getattr(self,f.name)) for f in self._meta.fields])
    #     )


class StoredYamlModel(models.Model):

    class Meta:
        managed = True

    id = models.AutoField(primary_key=True)
    filepath = models.FilePathField()
    filesize = models.BigIntegerField()
    def __unicode__(self):
        return u'%s' % self.id


class YamlDocsModel(models.Model):

    class Meta:
        managed = True

    id = models.AutoField(primary_key=True)
    storedby = models.ForeignKey(StoredYamlModel)
    docname = models.CharField(max_length=255)
    definition = models.TextField()

    def __unicode__(self):
        return u'%s' % self.docname

class CharField(models.CharField):
    template_type = _('text')
    max_length = 255
    def __init__(self,*args, **kwargs):
        if 'max_length' not in kwargs:
            kwargs['max_length'] = self.max_length
        super(CharField, self).__init__(*args, **kwargs)

class IntegerField(models.IntegerField):
    template_type = _('text')

class DateField(models.DateField):
    template_type = _('date')


def create_model(docname, data):
    # init mapped types
    maptypes = {
        'char': {
            'model': CharField,
            'form': fields.CharField,
        },
        'int' : {
            'model': IntegerField,
            'form': fields.IntegerField,
        },
        'date': {
            'model': DateField,
            'form': fields.DateField,
        },
    }

    prefields = dict(
        id = models.AutoField(primary_key=True)
    )
    formfields, options = dict(), dict()

    options['verbose_name'] = data.get('title')
    # check for contained fields list
    if 'fields' in data and isinstance(data.get('fields'),list):
        for field in data['fields']:
            # skip as unformated
            if not isinstance(field,dict):
                continue
            # skip without names
            if not 'id' in field:
                continue

            fieldname = field['id']
            # create fields as CharFields if type not defined
            prefields[fieldname] = maptypes[field.get('type') or 'char']['model']()
            formfields[fieldname] = maptypes[field.get('type') or 'char']['form']()

            # set label as exist title else use field name
            setattr(prefields[fieldname], 'label', field.get('title') or fieldname)
            setattr(formfields[fieldname], 'label', field.get('title') or fieldname)

    # prepare params
    params = dict(
        app_label=__package__,
        module=__name__,
        doc=docname,
        )
    # create dynamic form
    myform = type('%sForm' % str(docname), (DynamicForm,),dict(fields=formfields))

    # create dynamic model by params

    return create_abstract(
        '%(doc)s' % params,
        app_label=params['app_label'],
        fields=prefields,
        module=params['module'],
        admin_opts={},
        options=options,
    )


@models.permalink
def get_absolute_url(self):
    return (''.join([self._meta.object_name,'.views.details']), [str(self.id)])


def get_model(name=''):
    '''
    Try to get model by name or returning all exists
    :param name: model name
    :return: cached model or models
    '''

    if name:
        return cache.get_model(__package__, name)

    return [m for m in cache.get_models(cache.get_app(__package__)) if hasattr(m,'isdynamic')]

