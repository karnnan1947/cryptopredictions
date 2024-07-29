from django.contrib import admin

# Register your models here.
from users.models import users

admin.site.register(users)
