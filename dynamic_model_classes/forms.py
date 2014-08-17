from django.forms import ModelForm, BaseForm, BaseModelForm
from django.forms.models import ErrorList
from django.forms.models import fields_for_model

__author__ = 'boo'

class DynamicForm(BaseModelForm):

    class _meta:
        exclude = ['id', ]

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=None,
                 empty_permitted=False, instance=None):
        # use object instead class

        setattr(self._meta, 'model', instance)
        fl = fields_for_model(
            model=instance,
            fields=[f.name for f in instance._meta.fields],
            labels={f.name: hasattr(f,'label') and f.label or f.name for f in instance._meta.fields}
        )

        setattr(self._meta, 'fields', fl)
        self.base_fields = fl

        super(DynamicForm, self).__init__(data=data, files=files, auto_id=auto_id, prefix=prefix,
                 initial=initial, error_class=error_class, label_suffix=label_suffix,
                 empty_permitted=empty_permitted, instance=instance)

