from django.forms import ModelForm, TextInput

import datetime


from .models import Ticket, Location, Category, User


class OpenForm(ModelForm):

    class Meta:
        model = Ticket
        fields = ["name", "description", "category", "location", "ipAddress"]

