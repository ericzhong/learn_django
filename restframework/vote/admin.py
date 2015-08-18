from django.contrib import admin

# Register your models here.
from .models import Issue,Vote,Comment


admin.site.register(Issue)
admin.site.register(Vote)
admin.site.register(Comment)
