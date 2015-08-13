# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def load_data(apps, schema_editor):
    Person = apps.get_model("hello", "Person")
    db_alias = schema_editor.connection.alias
    Person.objects.using(db_alias).bulk_create([
        Person(first_name="Michael", last_name="Jordan"),
        Person(first_name="Kobe", last_name="Bryant"),
        Person(first_name="LeBron", last_name="James"),
    ])

class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0003_person_addr'),
    ]

    operations = [
        migrations.RunPython(
            load_data,
        ),
    ]
