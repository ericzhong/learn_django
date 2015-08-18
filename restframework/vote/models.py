# coding:utf-8
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import User

# Create your models here.

@python_2_unicode_compatible
class Issue(models.Model):
    title = models.CharField(max_length=64)
    content = models.TextField(blank=True)
    create_by = models.ForeignKey(User, related_name='issues')
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Vote(models.Model):
    issue_id = models.ForeignKey('Issue')
    vote_by = models.ForeignKey(User)
    agree = models.NullBooleanField(blank=True)


class Comment(models.Model):
    issue_id = models.ForeignKey('Issue')
    content = models.TextField()
    create_by = models.ForeignKey(User)
    create_time = models.DateTimeField(auto_now_add=True)


