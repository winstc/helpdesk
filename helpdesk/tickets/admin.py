from django.contrib import admin

from .models import Ticket


class TicketModel(admin.ModelAdmin):
    date_hierarchy = 'date_submitted'

admin.site.register(Ticket)
