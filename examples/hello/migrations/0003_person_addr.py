# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0002_remove_person_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='addr',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
