from django.shortcuts import render
from django.http import HttpResponse

from .models import User,Issue,Vote,Comment
from .forms import SignupForm

# Create your views here.

def home(request):
    issues = Issue.objects.all().order_by('-create_time')

    items = []
    for issue in issues:
        item = {}
        item['issue_id'] = issue.id
        item['title'] = issue.title
        item['user'] = issue.create_by.name
        item['create_time'] =  issue.create_time.strftime('%Y-%m-%d %H:%M:%S');
        item['reply'] = Comment.objects.filter(issue_id=issue.id).count()
        item['agree'] = Vote.objects.filter(issue_id=issue.id,agree=True).count()
        item['disagree'] = Vote.objects.filter(issue_id=issue.id,agree=False).count()
        items.append(item)

    return render(request, 'index.html', {'items': items})



def issue(request, n):
    issue = Issue.objects.get(id=n)

    item = {}
    item['title'] = issue.title
    item['content'] = issue.content
    item['user'] = issue.create_by.name
    item['create_time'] = issue.create_time.strftime('%Y-%m-%d %H:%M:%S');
    item['reply'] = Comment.objects.filter(issue_id=n).count() or 0
    item['agree'] = Vote.objects.filter(issue_id=n,agree=True).count()
    item['disagree'] = Vote.objects.filter(issue_id=n,agree=False).count()

    objects = Comment.objects.filter(issue_id=n)
    comments = []
    for o in objects:
        comment = {}
        comment['content'] = o.content
        comment['user'] = o.create_by.name
        comment['create_time'] = o.create_time.strftime('%Y-%m-%d %H:%M:%S');
        comments.append(comment)

    return render(request, 'issue.html', {'item': item, 'comments': comments})



def login(request):
    return render(request, 'login.html') 



def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
         
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            return HttpResponse("%s, %s" % (username, password))
     
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


