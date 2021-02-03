from django.contrib import admin
from .models import RamblerComment, RamblerPost, RamblerSub

# Register your models here.
admin.site.register([RamblerComment, RamblerPost, RamblerSub])
