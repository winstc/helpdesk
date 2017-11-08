from django.forms import ModelForm, TextInput

from .models import Ticket, File


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
