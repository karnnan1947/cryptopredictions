from django.contrib import admin

# Register your models here.
from users.models import users,Feedback

admin.site.register(users)
admin.site.register(Feedback)
