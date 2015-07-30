# coding:utf-8
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.

@python_2_unicode_compatible
class User(models.Model):
    name = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=30)
    create_time = models.DateTimeField(auto_now_add=True)
    token = models.CharField(max_length=32, unique=True)
    last_login = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Issue(models.Model):
    title = models.CharField(max_length=64)
    content = models.TextField(blank=True)
    create_by = models.ForeignKey('User')
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


@python_2_unicode_compatible
class Vote(models.Model):
    issue_id = models.ForeignKey('Issue')
    vote_by = models.ForeignKey('User')
    agree = models.NullBooleanField(blank=True)

    def __str__(self):
        return self


@python_2_unicode_compatible
class Comment(models.Model):
    issue_id = models.ForeignKey('Issue')
    content = models.TextField()
    create_by = models.ForeignKey('User')
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self

