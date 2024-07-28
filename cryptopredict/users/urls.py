from django.urls import path
from . import views
urlpatterns=[ 
    path('',views.index,name="index"),
    path('account',views.account,name='account'),
    path('signout',views.signout,name='signout'),
    path('homes',views.homes,name='homes'),
    ]