from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import get_object_or_404

from .models import Ticket, Location, Category
from .forms import OpenForm, FileUploadForm


@permission_required('tickets.can_view_all')
def index(request):
    order_by = request.GET.get('order_by', "name")
    show_completed = request.GET.get('show_completed', False)

    if show_completed:
        excluded = ""
    else:
        excluded = "C"

    latest_ticket_list = Ticket.objects.exclude(status=excluded).order_by(order_by)
    template = loader.get_template('tickets/index.html')
    context = {
        'latest_ticket_list': latest_ticket_list,
    }
    return HttpResponse(template.render(context, request))

@permission_required('tickets.can_view_all')
def details(request, ticket_id):
    template = loader.get_template('tickets/details.html')
    ticket = get_object_or_404(Ticket, pk=ticket_id)

    return HttpResponse(template.render({'ticket': ticket}, request))


def status(request, ticket_id):
    return HttpResponse("You're looking at the status of ticket %s" % ticket_id)


@login_required
def open_new(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:

        form = OpenForm(request.user, request.POST)
        file_form = FileUploadForm(request.POST, request.FILES)

        # check whether it's valid:
        if form.is_valid():
            new_ticket = form.save(commit=False)
            current_user = request.user
            new_ticket.user = current_user
            new_ticket.save()

            if file_form.is_valid():
                new_file = file_form.save(commit=False)
                new_file.ticket = new_ticket
                new_file.save()

            return HttpResponseRedirect('/')

            # if a GET (or any other method) we'll create a blank form
    else:
        form = OpenForm(request.user)
        file_form = FileUploadForm()

    template = loader.get_template('tickets/open.html')
    locations = Location.objects.all()
    categories = Category.objects.all()

    return HttpResponse(
        template.render({"locations": locations, "categories": categories, 'form': form, 'file_form': file_form},
                        request))
