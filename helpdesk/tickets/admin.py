from django.contrib import admin

from .models import Ticket, File, Question, Location, Category


class TicketModel(admin.ModelAdmin):
    date_hierarchy = 'date_submitted'


admin.site.register(Ticket)

admin.site.register(Question)

admin.site.register(File)

admin.site.register(Location)

admin.site.register(Category)