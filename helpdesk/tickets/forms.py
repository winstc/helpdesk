#!/usr/bin/env python
"""Provides views for tickets app.
"""

from django.forms import ModelForm, TextInput

from .models import Ticket, File, Location, Category

__author__ = "Winston Cadwell"
__copyright__ = "Copyright 2017, Winston Cadwell"
__licence__ = "BSD 2-Clause Licence"
__version__ = "1.0"
__email__ = "wcadwell@gmail.com"


class OpenForm(ModelForm):

    def __init__(self, user, *args, **kwargs):
        super(OpenForm, self).__init__(*args, **kwargs)
        self.user = user
        self.fields['name'].widget = TextInput(attrs={'value': self.user.first_name})

    class Meta:
        model = Ticket
        fields = ["name", "description", "category", "location", "ipAddress"]

        labels = {
            'ipAddress': "IP Address"
        }


class FileUploadForm(ModelForm):

    class Meta:
        model = File
        fields = ["file", "description"]

        help_texts = {
            'description': "Give a brief description of what the file is"
        }


class AddLocationForm(ModelForm):

    class Meta:
        model = Location
        fields = ["name", "description", "longitude", "latitude"]


class AddCategoryForm(ModelForm):

    class Meta:
        model = Category
        fields = ["name", "description"]
