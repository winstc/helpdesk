# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-23 13:14
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ticket',
            options={'permissions': (('can_view_all', 'View all tickets'), ('can_open', 'Open a new ticket'))},
        ),
    ]
