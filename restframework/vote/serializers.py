from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Issue,Vote,Comment

class UserSerializer(serializers.HyperlinkedModelSerializer):
    issues = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='issue-detail')
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups', 'issues')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class IssueSerializer(serializers.HyperlinkedModelSerializer):
    create_by = serializers.ReadOnlyField(source='create_by.username')
    class Meta:
        model = Issue
        fields = ('url', 'title', 'content', 'create_by', 'create_time')


class VoteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Vote
        fields = ('url', 'issue_id', 'vote_by', 'agree')


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Comment
        fields = ('url', 'issue_id', 'content', 'create_by', 'create_time')
