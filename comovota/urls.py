from django.urls import path

from . import views

urlpatterns = [
    path('', views.votos_list, name='votos_list')
]
