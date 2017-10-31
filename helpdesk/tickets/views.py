from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth.decorators import permission_required, login_required

from .models import Ticket, Location, Category
from .forms import OpenForm

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


@login_required
def open_new(request):

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:

        form = OpenForm(request.POST)

        # check whether it's valid:
        if form.is_valid():
                new_ticket = form.save(commit=False)
                current_user = request.user
                print(request.user)
                new_ticket.user = current_user
                print(current_user.id)
                new_ticket.save()

                return HttpResponseRedirect('/')

            # if a GET (or any other method) we'll create a blank form
    else:
        form = OpenForm()

    template = loader.get_template('tickets/open.html')
    locations = Location.objects.all()
    categories = Category.objects.all()

    return HttpResponse(template.render({"locations": locations, "categories": categories, 'form': form}, request))


