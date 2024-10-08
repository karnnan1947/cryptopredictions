from django.urls import path
from . import views

urlpatterns=[
    path('predicts/',views.predicts,name='predicts'),
]