# coding:utf-8
from __future__ import unicode_literals

from django.db import models
from django import forms
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.

@python_2_unicode_compatible
class User(models.Model):
    name = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=30)
    create_time = models.DateTimeField(auto_now_add=True)
    token = models.CharField(max_length=32, unique=True, null=True)
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


class Vote(models.Model):
    issue_id = models.ForeignKey('Issue')
    vote_by = models.ForeignKey('User')
    agree = models.NullBooleanField(blank=True)


class Comment(models.Model):
    issue_id = models.ForeignKey('Issue')
    content = models.TextField()
    create_by = models.ForeignKey('User')
    create_time = models.DateTimeField(auto_now_add=True)



class SignupForm(forms.ModelForm):
    err_1 = {
        'required': "密码不能为空",
    }

    err_2 = {
        'required': "确认密码不能为空",
    }

    password1 = forms.CharField(widget=forms.PasswordInput(), error_messages=err_1)
    password2 = forms.CharField(widget=forms.PasswordInput(), error_messages=err_2)

    class Meta:
        model = User
        fields = ('name',)
        error_messages = {
            'name': {
                'required': "用户名不能为空",
                'unique': "该用户已经存在",
            },
        }

    def clean(self):
        cleaned_data = super(SignupForm, self).clean()

        name = cleaned_data.get('name')
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("密码不相同")

        return cleaned_data


class LoginForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('name','password')
        widgets = {
            'password': forms.PasswordInput(),
        }
        error_messages = {
            'name': {
                'required': "用户名不能为空",
            },
            'password': {
                'required': "密码不能为空",
            },
        }

    def clean(self):

        name = self.cleaned_data.get('name')
        password = self.cleaned_data.get('password')

        q = User.objects.filter(name=name)
        if 0 == q.count():
            raise forms.ValidationError("用户不存在")

        if q[0].password != password:
            raise forms.ValidationError("密码错误")

        return self.cleaned_data

