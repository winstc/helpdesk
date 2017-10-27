from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import permission_required

from .models import Ticket

# Create your views here.


@permission_required('tickets.can_view_all')
def index(request):
    latest_ticket_list = Ticket.objects.order_by('-submissionDate')[:5]
    template = loader.get_template('tickets/index.html')
    context = {
        'latest_ticket_list': latest_ticket_list,
    }
    return HttpResponse(template.render(context, request))


def details(request, ticket_id):
    return HttpResponse("You're looking at ticket %s" % ticket_id)


def status(request, ticket_id):
    return HttpResponse("You're looking at the status of ticket %s" % ticket_id)


def open_new(request):
    template = loader.get_template('tickets/open.html')
    return HttpResponse(template.render({}, request))

