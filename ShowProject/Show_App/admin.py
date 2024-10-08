from django.contrib import admin
from .models import User, Show, ShowComment

# Register your models here.

admin.site.register(User)
admin.site.register(Show)
admin.site.register(ShowComment)