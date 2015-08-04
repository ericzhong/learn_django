from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect

from .models import User,Issue,Vote,Comment,SignupForm,LoginForm,CommentForm

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

    name = request.session.get('name', None)

    return render(request, 'index.html', {'items': items, 'username': name})



def issue(request, n):
    name = request.session.get('name', None)

    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            content = form.cleaned_data['content']
            if name is not None:
                u = User.objects.get(name=name)
                i = Issue.objects.get(id=n)
                Comment(issue_id=i, content=content, create_by=u).save()
                form = CommentForm()

    else:
        form = CommentForm()

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

    return render(request, 'issue.html', {'item': item, 'comments': comments, 'username': name, 'form': form})



def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']

            request.session['name'] = name
            return HttpResponseRedirect("/")

    else:
        if request.session.get('name', None) is not None:
            return HttpResponseRedirect("/")

        form = LoginForm()

    return render(request, 'login.html', {'form': form})


def logout(request):
    try:
        del request.session['name']
    except: pass

    return HttpResponseRedirect("/")


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            password = form.cleaned_data['password1']
            User(name=name,password=password,token=None).save()
            return HttpResponseRedirect("/login")

    else:
        if request.session.get('name', None) is not None:
            return HttpResponseRedirect("/")

        form = SignupForm()

    return render(request, 'signup.html', {'form': form})
