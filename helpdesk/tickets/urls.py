"""helpdesk URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='tickets_index'),
    url(r'^(?P<ticket_id>[0-9]+)/$', views.details, name='detail'),
    url(r'^open/$', views.open_new, name='open_new'),
    url(r'^settings/$', views.settings, name='settings'),
    url(r'^settings/location/(?P<pk>[0-9]+)/$', views.LocationDetailView.as_view(), name='location'),
    url(r'^settings/location/add/$', views.add_location, name='add_location'),
    url(r'^settings/category/(?P<pk>[0-9]+)/$', views.CategoryDetailView.as_view(), name='category'),
    url(r'^settings/category/add/$', views.add_category, name='add_category'),
]
