from django.shortcuts import render
from django.http import HttpResponse

from .models import User,Issue,Vote,Comment

# Create your views here.

def home(request):
    issues = Issue.objects.all().order_by('-create_time')
    items = []
    for issue in issues:
        item = {}
        item['title'] = issue.title
        item['user'] = issue.create_by.name
        item['create_time'] =  issue.create_time.strftime('%Y-%m-%d %H:%M:%S');
        item['reply'] =  Comment.objects.filter(issue_id=issue.id).count()
        item['agree'] = Vote.objects.filter(issue_id=issue.id,agree=True).count()
        item['disagree'] = Vote.objects.filter(issue_id=issue.id,agree=False).count()
        items.append(item)

    return render(request, 'index.html', {'items': items})
