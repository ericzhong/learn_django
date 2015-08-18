"""restframework URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

from rest_framework import routers
from quickstart import views as quick_views
from vote import views as vote_views


#quick_router = routers.DefaultRouter()
#quick_router.register(r'users', quick_views.UserViewSet)
#quick_router.register(r'groups', quick_views.GroupViewSet)

vote_router = routers.DefaultRouter()
vote_router.register(r'users', vote_views.UserViewSet)
vote_router.register(r'groups', vote_views.GroupViewSet)
vote_router.register(r'issues', vote_views.IssueViewSet)
vote_router.register(r'votes', vote_views.VoteViewSet)
vote_router.register(r'comments', vote_views.CommentViewSet)


urlpatterns = [
    #url(r'^quick-api/', include(quick_router.urls)),
    url(r'^vote-api/', include(vote_router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    url(r'^admin/', include(admin.site.urls)),
]
