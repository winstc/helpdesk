#!/usr/bin/env python
"""Provides models for tickets app.

"""

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

import django.utils.timezone

__author__ = "Winston Cadwell"
__copyright__ = "Copyright 2017, Winston Cadwell"
__licence__ = "BSD 2-Clause Licence"
__version__ = "1.0"
__email__ = "wcadwell@gmail.com"


class Location(models.Model):
    """Provides a model to store locations in.

    This model is used in Ticket to provide the user a list of
    location to select from.

    *name*
        Name of the location
    *description*
        A description of the location
    *longitude*
        Longitude of the location
    *latitude*
        Latitude of the location
    """
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    longitude = models.DecimalField(max_digits=8, decimal_places=3, null=True, blank=True)
    latitude = models.DecimalField(max_digits=8, decimal_places=3, null=True, blank=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    """Provides a model to store categories in.

    This model is used in Ticket to provide the user a list or
    categories to select from.

    *name*
        Name of the category
    *description*
        Description of the category
    """
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Ticket(models.Model):
    """Provides a model to store tickets.

    This model is used to store tickets that the user submits.

    :const:`STATUS_CHOICES`
        Tuple of Tuples containing possible choices for *status*

    *user*
        Linked to User model built into Django. Used to
        link Ticket to a specific user.
    *name*
        Used to store users name in-case it is
        different than the logged in user's.
    *description*
        A description of the problem, provided by the user.
    *status*
        Status of the ticket. This field is multiple choice, choices
        are provided by :const:`STATUS_CHOICES`.
    *priority*
        Priority value for the ticket. Can range between 1 and 5.
    *submissionDate*
        Date that the ticket was submitted.
    *location*
        :class:`Location` for the ticket.
    *category*
        :class:`Category` for the ticket.
    *ipAddress*
        Stores an IP Address associated with the ticket.
    """

    class Meta:
        permissions = (("can_view_all", "View all tickets"), ("can_open", "Open a new ticket"),
                       ("can_edit_tickets", "Has full control of tickets"))

    COMPLETE = 'C'
    WAITING = "W"
    IN_PROGRESS = "I"

    STATUS_CHOICES = (
        (COMPLETE, "Complete"),
        (IN_PROGRESS, "In Progress"),
        (WAITING, "Waiting")
    )

    user = models.ForeignKey(User, default=1)
    name = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=1,
                              choices=STATUS_CHOICES,
                              default="W")
    priority = models.IntegerField(default=1, validators=[
        MinValueValidator(5),
        MaxValueValidator(1)
    ])
    submissionDate = models.DateTimeField('date submitted', default=django.utils.timezone.now)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    ipAddress = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        return str(self.user.username + " - " + str(self.submissionDate.date()))


class Question(models.Model):
    """This model is currently unused.

    In a future release this model will be used to store
    optional question for the user.
    """
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    questionTitle = models.CharField(max_length=100)
    questionText = models.TextField()
    questionHelpText = models.TextField()
    questionType = models.CharField(max_length=15)


class File(models.Model):
    """Model to index files uploaded by the user.

    This model stores a file and some data associated with it.

    *ticket*
        :class"`Ticket` that file is linked to.
    *description*
        Description of the file.
    *file*
        Stores uploaded file.
    *timestamp*
        Stores the time of upload.
    """
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    file = models.FileField(upload_to='uploads/', null=True, blank=True)
    timestamp = models.DateTimeField(default=django.utils.timezone.now)

    def __str__(self):
        return self.file.name.split("/")[-1]
