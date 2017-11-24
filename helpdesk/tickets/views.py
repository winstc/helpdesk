#!/usr/bin/env python
"""Provides views for tickets app.
"""

from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.template.loader import render_to_string
from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import get_object_or_404
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from helpdesk.settings import EMAIL_HOST_USER

from .models import Ticket, Location, Category, File
from .forms import OpenForm, FileUploadForm

__author__ = "Winston Cadwell"
__copyright__ = "Copyright 2017, Winston Cadwell"
__licence__ = "BSD 2-Clause Licence"
__version__ = "1.0"
__email__ = "wcadwell@gmail.com"


@permission_required('tickets.can_view_all')
def index(request):
    """Provide a list view for tickets.

    This view allows the user to sort Ticket objects and
    manipulate their status and priority. It also provides a
    link for each tickets detail view.

    GET:
        This method accepts two different GET parameters
        show_completed and order_by

        *show_completed*
            Sets whether to include completed tickets or not.
        *order_by*
            Used when querying the database. Can be the name of
            any Ticket field. A '-' character
            at the beginning denotes reverse order.

    POST:
        This method does not process any POST requests.
    """
    # parse values from GET request
    order_by = request.GET.get('order_by', "name")
    show_completed = request.GET.get('show_completed', False)

    # determine whether to exclude completed tickets
    if show_completed:
        excluded = ""
    else:
        excluded = "C"

    # query the database for tickets
    ticket_list = Ticket.objects.exclude(status=excluded).order_by(order_by)
    template = loader.get_template('tickets/index.html')
    context = {
        'ticket_list': ticket_list,
    }

    # render template and return it
    return HttpResponse(template.render(context, request))


# detail view for tickets
# gives a detailed view of a specific ticket
@permission_required('tickets.can_view_all')
def details(request, ticket_id):
    """Provide a detail view for tickets.

        This view allows the user to see a detailed view of a Ticket object.
        It display all Ticket information along with associated files.

        GET:
            This method does not process any GET requests.

        POST:
            This method handles POST requests for several
            different actions.

            *action*
                The action to perform on the current ticket.
            *value*
                Used for any value associated with the action.
            *ticket_id*
                The id of the Ticket object that the action is
                to be performed on.
        """

    # process POST requests
    if request.method == "POST":

        # store POST parameters
        action = request.POST.get('action')
        value = request.POST.get('value')
        ticket_id = request.POST.get('ticket_id')

        # delete current ticket
        if action == "delete":
            Ticket.objects.filter(pk=ticket_id).delete()

            # redirect to ticket list because the
            # page for the deleted ticket will now
            # return a 404 error
            return HttpResponseRedirect('/ticket')

        # change status of current ticket
        elif action == "status":
            if value == "C":
                t = Ticket.objects.get(pk=ticket_id)
                t.status = "C"
                t.save()

                return HttpResponse(t.status)

            elif value == "I":
                t = Ticket.objects.get(pk=ticket_id)
                t.status = "I"
                t.save()

                return HttpResponse(t.status)

            elif value == "W":
                t = Ticket.objects.get(pk=ticket_id)
                t.status = "W"
                t.save()

                return HttpResponse(t.status)

        # change priority of current ticket
        elif action == "priority":
            if value.isdigit() and 1 <= int(value) <= 5:
                t = Ticket.objects.get(pk=ticket_id)
                t.priority = value
                t.save()

                return HttpResponse(t.status)

    # process non POST requests
    else:
        template = loader.get_template('tickets/details.html')
        ticket = get_object_or_404(Ticket, pk=ticket_id)

        # query database for media associated with ticket
        media = File.objects.filter(ticket=ticket)

        return HttpResponse(template.render({'ticket': ticket, 'media': media}, request))


# view for opening new tickets
@login_required
def open_new(request):
    """Provide a view for opening a new ticket.

            This view provides a view for opening a new ticket. It provides
            a simple form for the user to submit the necessary to open a new ticket.

            GET:
                This method does not process any GET requests.

            POST:
                This method handles POST requests for two forms: OpenForm and FileUploadForm
            """

    # process POST requests
    if request.method == 'POST':

        # create a form instance and populate it with data from the request:
        form = OpenForm(request.user, request.POST, prefix="openForm")
        file_form = FileUploadForm(request.POST, request.FILES, prefix="fileForm")

        # check whether it's valid:
        if form.is_valid():
            new_ticket = form.save(commit=False)
            current_user = request.user
            new_ticket.user = current_user
            new_ticket.save()

            if file_form.is_valid():
                new_file = file_form.save(commit=False)
                if new_file.file:
                    new_file.ticket = new_ticket
                    new_file.save()

            # send user a confirmation email
            # the email is rendered using the confirmation-email.html template
            # located in 'tickets/templates'
            subject = "Ticket Submission Confirmation"
            recipient = current_user.email
            from_email = EMAIL_HOST_USER
            data = {
                'user': current_user,
                'ticket': new_ticket
            }
            html_message = render_to_string('tickets/confirmation_email.html', data)
            text_message = strip_tags(html_message)

            msg = EmailMultiAlternatives(subject, text_message, from_email, [recipient])
            msg.attach_alternative(html_message, "text/html")
            msg.send()

            return HttpResponseRedirect('/')

    # process non POST requests
    else:
        # create blank forms for use in page
        form = OpenForm(request.user, prefix="openForm")
        file_form = FileUploadForm(prefix="fileForm")

    template = loader.get_template('tickets/open.html')
    locations = Location.objects.all()
    categories = Category.objects.all()

    return HttpResponse(
        template.render({"locations": locations, "categories": categories, 'form': form, 'file_form': file_form},
                        request))
