#!/usr/bin/env python
"""Provides views for userportal app.
"""

from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

__author__ = "Winston Cadwell"
__copyright__ = "Copyright 2017, Winston Cadwell"
__licence__ = "BSD 2-Clause Licence"
__version__ = "1.0"
__email__ = "wcadwell@gmail.com"


# Create your views here.
def index(request):
    """Provide a home page for the user.

        GET:
            This method does not process any POST requests.

        POST:
            This method does not process any POST requests.
        """
    template = loader.get_template('userportal/index.html')
    return HttpResponse(template.render({'content': "hello"}, request))
