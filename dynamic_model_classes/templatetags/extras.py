# -*- coding: utf-8 -*-
from django import template

import calendar

register = template.Library()


@register.filter
def by_attrname(obj, name):

    assert hasattr(obj, name) is True, "Invalid field '%s'" % name

    return getattr(obj, name)


@register.filter
def day_name(weekday):
    return calendar.day_name[int(weekday)]
