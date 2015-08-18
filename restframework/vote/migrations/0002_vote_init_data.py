# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.contrib.auth.models import User

def load_data(apps, schema_editor):
    Issue = apps.get_model("vote", "Issue")
    Vote = apps.get_model("vote", "Vote")
    Comment = apps.get_model("vote", "Comment")

    db_alias = schema_editor.connection.alias

    u = User(username="admin", is_superuser=True, is_active=True, is_staff=True)
    u.set_password("admin")
    u.save()

    u = User(username="test", is_superuser=False, is_active=True, is_staff=True)
    u.set_password("test")
    u.save()


    Issue.objects.using(db_alias).bulk_create([
        Issue(title="aaaaaaaaaa", content="...............", create_by_id=1),
        Issue(title="bbbbbbbbbb", content="...............", create_by_id=1),
        Issue(title="cccccccccc", content="...............", create_by_id=1),
        Issue(title="dddddddddd", content="...............", create_by_id=1),
    ])

    Comment.objects.using(db_alias).bulk_create([
        Comment(issue_id_id=1, content="comment.........", create_by_id=1),
        Comment(issue_id_id=2, content="comment.........", create_by_id=1),
        Comment(issue_id_id=3, content="comment.........", create_by_id=1),
        Comment(issue_id_id=4, content="comment.........", create_by_id=1),
    ])

    Vote.objects.using(db_alias).bulk_create([
        Vote(issue_id_id=1, vote_by_id=1, agree=True),
        Vote(issue_id_id=2, vote_by_id=1, agree=False),
        Vote(issue_id_id=3, vote_by_id=1, agree=True),
        Vote(issue_id_id=4, vote_by_id=1, agree=False),
    ])


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(
            load_data,
        ),
    ]
