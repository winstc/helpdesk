#!/usr/bin/env python
"""Provides extra template tags for authentication.
"""

from django import template
from django.contrib.auth.models import Group

__author__ = "Winston Cadwell"
__copyright__ = "Copyright 2017, Winston Cadwell"
__licence__ = "BSD 2-Clause Licence"
__version__ = "1.0"
__email__ = "wcadwell@gmail.com"


register = template.Library()


@register.filter(name='has_group')
def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False
