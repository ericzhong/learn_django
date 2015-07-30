# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.TextField()),
                ('create_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=64)),
                ('content', models.TextField(blank=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=30)),
                ('password', models.CharField(max_length=30)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('token', models.CharField(unique=True, max_length=32, blank=True)),
                ('last_login', models.DateTimeField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('agree', models.NullBooleanField()),
                ('issue_id', models.ForeignKey(to='vote.Issue')),
                ('vote_by', models.ForeignKey(to='vote.User')),
            ],
        ),
        migrations.AddField(
            model_name='issue',
            name='create_by',
            field=models.ForeignKey(to='vote.User'),
        ),
        migrations.AddField(
            model_name='comment',
            name='create_by',
            field=models.ForeignKey(to='vote.User'),
        ),
        migrations.AddField(
            model_name='comment',
            name='issue_id',
            field=models.ForeignKey(to='vote.Issue'),
        ),
    ]
