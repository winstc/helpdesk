#!/usr/bin/env python
"""Provides views for userportal app.
"""

from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import PermissionRequiredMixin

from  .models import User

from django.contrib.auth.models import Group

from .forms import EmailPreferencesForm, UserPreferencesForm

__author__ = "Winston Cadwell"
__copyright__ = "Copyright 2017, Winston Cadwell"
__licence__ = "BSD 2-Clause Licence"
__version__ = "1.0"
__email__ = "wcadwell@gmail.com"


def is_admin(user):
    return user.groups.filter(name='Admin').exists()


# Create your views here.
def index(request):
    """Provide a home page for the user.

        GET:
            This method does not process any POST requests.

        POST:
            This method does not process any POST requests.
        """
    template = loader.get_template('userportal/index.html')
    return HttpResponse(template.render({'content': "hello"}, request))


@login_required()
def preferences(request):
    if request.method == 'POST':
        account_form = UserPreferencesForm(request.POST, instance=request.user, prefix="account")
        form = EmailPreferencesForm(request.POST, instance=request.user.emailpreferences, prefix="email")

        if form.is_valid():
            form.save()

        if account_form.is_valid():
            account_form.save()

        return redirect('/preferences/')

    else:
        account_form = UserPreferencesForm(instance=request.user, prefix="account")
        form = EmailPreferencesForm(instance=request.user.emailpreferences, prefix="email")

    template = loader.get_template('userportal/preferences.html')

    return HttpResponse(template.render({'account_form': account_form, 'form': form}, request))


class UserManagement(PermissionRequiredMixin, ListView):
    permission_required = 'auth.user.can_change_user'
    model = User
    template_name = 'userportal/user_management.html'

    def get_context_data(self, **kwargs):
        context = super(UserManagement, self).get_context_data(**kwargs)
        return context


@permission_required('user.can_add_user')
def add_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()

    template = loader.get_template('userportal/add_user.html')

    form = UserCreationForm()

    return HttpResponse(template.render({'form': form}, request))


@permission_required('user.can_change_user')
def UserDetails(request, **kwargs):
    if request.method == "POST":

        form = UserChangeForm(request.POST, instance=User.objects.get(pk=kwargs.get('pk')), prefix="form")
        if form.is_valid():
            form.save()

        action = request.POST.get('action')
        if action == "delete":
            User.objects.filter(pk=kwargs.get('pk')).delete()
            return HttpResponse('')

        elif action == "toggle_admin":
            user = User.objects.get(pk=kwargs.get('pk'))
            group = Group.objects.get(name="Admin")
            if not user.groups.filter(name="Admin").count():
                user.groups.add(group)
            else:
                user.groups.remove(group)

            return HttpResponse('')

    else:

        form = UserChangeForm(instance=User.objects.get(pk=kwargs.get('pk')), prefix="form")

    template = loader.get_template('userportal/user_detail.html')

    return HttpResponse(template.render({'form': form}, request))
