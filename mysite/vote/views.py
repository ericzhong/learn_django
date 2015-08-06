from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.core.urlresolvers import reverse

from .models import User,Issue,Vote,Comment,SignupForm,LoginForm,CommentForm,NewIssueForm,PasswordForm

# Create your views here.

def _logout(request):
    try:
        del request.session['name']
    except: pass


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
        agree = request.GET.get('agree', None)
        if agree is not None:
            if '0' == agree:
                agree = False
            elif '1' == agree:
                agree = True
            else:
                return HttpResponseRedirect(reverse('issue', args=[n]))

            if name is not None:
                if 0 != Vote.objects.filter(vote_by=User.objects.get(name=name),
                                            issue_id=Issue.objects.get(id=n)).count():
                    return HttpResponseRedirect(reverse('issue', args=[n]))

                Vote(issue_id=Issue.objects.get(id=n),
                    vote_by=User.objects.get(name=name),
                    agree=agree).save()

        form = CommentForm()

    issue = Issue.objects.get(id=n)

    item = {}
    item['id'] = n
    item['title'] = issue.title
    item['content'] = issue.content
    item['user'] = issue.create_by.name
    item['create_time'] = issue.create_time.strftime('%Y-%m-%d %H:%M:%S');
    item['reply'] = Comment.objects.filter(issue_id=n).count() or 0
    item['agree'] = Vote.objects.filter(issue_id=n,agree=True).count()
    item['disagree'] = Vote.objects.filter(issue_id=n,agree=False).count()
    item['votable'] = False if Vote.objects.filter(vote_by=User.objects.get(name=name),
                                  issue_id=Issue.objects.get(id=n)).count() !=0 else True

    objects = Comment.objects.filter(issue_id=n)
    comments = []
    for o in objects:
        comment = {}
        comment['content'] = o.content
        comment['user'] = o.create_by.name
        comment['create_time'] = o.create_time.strftime('%Y-%m-%d %H:%M:%S');
        comments.append(comment)

    return render(request, 'issue.html', {'item': item, 'comments': comments, 'username': name, 'form': form})


def new_issue(request):
    name = request.session.get('name', None)

    if request.method == 'POST':
        form = NewIssueForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            if name is not None:
                u = User.objects.get(name=name)
                Issue(title=title, content=content, create_by=u).save()
                return HttpResponseRedirect(reverse('home'))

    else:
        if name is None:
            return HttpResponseRedirect(reverse('home'))
        form = NewIssueForm()

    return render(request, 'new.html', {'username': name, 'form': form})



def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']

            request.session['name'] = name
            return HttpResponseRedirect(reverse('home'))

    else:
        if request.session.get('name', None) is not None:
            return HttpResponseRedirect(reverse('home'))

        form = LoginForm()

    return render(request, 'login.html', {'form': form})


def logout(request):
    _logout(request)
    return HttpResponseRedirect(reverse('home'))


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            password = form.cleaned_data['password1']
            User(name=name,password=password,token=None).save()
            return HttpResponseRedirect(reverse('login'))

    else:
        if request.session.get('name', None) is not None:
            return HttpResponseRedirect(reverse('home'))

        form = SignupForm()

    return render(request, 'signup.html', {'form': form})


def password(request):
    name = request.session.get('name', None)

    if request.session.get('name', None) is None:
        return HttpResponseRedirect(reverse('home'))

    if request.method == 'POST':
        form = PasswordForm(request.POST,username=name)

        if form.is_valid():
            password = form.cleaned_data['password1']
            User.objects.filter(name=name).update(password=password)
            _logout(request)
            return HttpResponseRedirect(reverse('login'))

    else:
        form = PasswordForm()

    return render(request, 'password.html', {'username': name, 'form': form})
