#!/usr/bin/env python
"""Provides models for userportal app.
"""

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

__author__ = "Winston Cadwell"
__copyright__ = "Copyright 2017, Winston Cadwell"
__licence__ = "BSD 2-Clause Licence"
__version__ = "1.0"
__email__ = "wcadwell@gmail.com"


class EmailPreferences(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    new_ticket = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_email_preferences_profile(sender, instance, created, **kwargs):
    if created:
        EmailPreferences.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_email_preferences_user_profile(sender, instance, **kwargs):
    instance.emailpreferences.save()
