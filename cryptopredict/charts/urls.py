from django.urls import path
from . import views
urlpatterns = [
    path('charts',views.charts,name='charts'),
]