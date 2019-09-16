from django.urls import path
from . import views


urlpatterns = [
    # [...]
    path('authorize/', views.AuthorizeView.as_view(), name='authorize'),
    path('oauth2callback/', views.Oauth2CallbackView.as_view(),
         name='oauth2callback')
]
