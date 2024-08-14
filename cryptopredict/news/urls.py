from django.urls import path
from . import views
urlpatterns=[
    path('news',views.newz,name="newz"),
]