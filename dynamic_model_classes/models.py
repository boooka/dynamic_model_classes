from django.conf import settings
from django.contrib import admin
from django.db import models
from forms import MyBaseForm

import json


__author__ = 'boo'


def create_abstract(name, fields=None, app_label='', module='', options=None, admin_opts=None):
    """
    Create specified model
    """
    class Meta:
        # Using type('Meta', ...) gives a dictproxy error during model creation
        pass

    if app_label:
        # app_label must be set using the Meta inner class
        setattr(Meta, 'app_label', app_label)

    # Update Meta with any options that were provided
    if options is not None:
        for key, value in options.iteritems():
            setattr(Meta, key, value)

    # Set up a dictionary to simulate declarations within a class
    attrs = {'__module__': module, 'Meta': Meta}

    # Add in any fields that were provided
    if fields:
        attrs.update(fields)

    # Create the class, which automatically triggers ModelBase processing
    model = type(str(name), (models.Model,), attrs)

    # Create an Admin class if admin options were provided
    admin.site.register(model)

    if admin_opts is not None:
        class Admin(admin.ModelAdmin):
            pass
        for key, value in admin_opts:
            setattr(Admin, key, value)

    return model


class DefinitionsModel(models.Model):
    definition = models.TextField()
    filepath = models.FilePathField()



def create_model(data, fname=''):
    # init mapped types
    maptypes = {
        'char': models.CharField(max_length=255),
        'int' : models.IntegerField(),
        'date': models.DateField(auto_now=True),
    }
    # if model(s) loaded from file save structure for late
    if fname:
        obj = DefinitionsModel()
        obj.filepath = fname
        obj.definition = json.dumps(data)
        obj.save()

    # iterate over docs from data
    for doc, v in data.items():

        prefields, options = dict(), dict()

        options['verbose_name'] = v.get('title')
        # check for contained fields list
        if 'fields' in v and isinstance(v.get('fields'),list):
            for field in v['fields']:
                # skip as unformated
                if not isinstance(field,dict):
                    continue
                # skip without names
                if not 'id' in field:
                    continue

                fieldname = field['id']
                prefields[fieldname] = maptypes['char']
                if 'type' in field:
                    prefields[fieldname] = maptypes[field.get('type')]
                if 'title' in field:
                    setattr(prefields[fieldname], 'help_text', field.get('title'))

        # m = type(doc, (models.Model,), dict(fields=prefields, __module__='dynamic_model_classes.models'))
        params = dict(
            app_label='dynamic_model_classes',
            module='dynamic_model_classes.models',
            doc=doc,
            )

        # create dynamic model by params
        created = create_abstract(
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



