from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('app', views.protype, name='app'),
    path('profile', views.profile, name='profile')
]
