#!/usr/bin/env python
"""Provides forms for userportal app.
"""

from django.forms import ModelForm, TextInput

from .models import User, EmailPreferences

__author__ = "Winston Cadwell"
__copyright__ = "Copyright 2017, Winston Cadwell"
__licence__ = "BSD 2-Clause Licence"
__version__ = "1.0"
__email__ = "wcadwell@gmail.com"


class EmailPreferencesForm(ModelForm):

    class Meta:
        model = EmailPreferences
        fields = ["new_ticket"]

        labels = {
            'new_ticket': "New Ticket Emails"
        }

        help_texts = {
            'new_ticket': "Send me an email when I open a new ticket"
        }


class UserPreferencesForm(ModelForm):

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]
