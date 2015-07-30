from django.contrib import admin
from .models import User,Issue,Vote,Comment

# Register your models here.

admin.site.register(User)
admin.site.register(Issue)
admin.site.register(Vote)
admin.site.register(Comment)
