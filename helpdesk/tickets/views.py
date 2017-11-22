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


# index view for tickets
# gives a sortable overview of tickets
@permission_required('tickets.can_view_all')
def index(request):
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
