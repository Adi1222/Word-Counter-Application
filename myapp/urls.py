from django.urls import path
from . import views

urlpatterns = [
    path('frequency', views.homepage, name='homepage'),
    path('result', views.result, name='result'),
]