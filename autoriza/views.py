from django.conf import settings
from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.http import HttpResponseBadRequest

from oauth2client.client import flow_from_clientsecrets, OAuth2WebServerFlow
from oauth2client.contrib import xsrfutil
from oauth2client.contrib.django_util.storage import DjangoORMStorage
from .models import CredentialsModel

# [...]
flow = flow_from_clientsecrets(
    settings.GOOGLE_OAUTH2_CLIENT_SECRETS_JSON,
    scope=settings.GOOGLE_SCOPES,
    redirect_uri=settings.DOMAIN+'/autoriza/oauth2callback/',
    prompt='consent')

class AuthorizeView(View):
    def get(self, request, *args, **kwargs):
        storage = DjangoORMStorage(
            CredentialsModel, 'id', request.user.id, 'credential')
        credential = storage.get()

        if credential is None or credential.invalid == True:
            flow.params['state'] = xsrfutil.generate_token(
                settings.SECRET_KEY, request.user)
            authorize_url = flow.step1_get_authorize_url()
            return redirect(authorize_url)
        return redirect('/')

class Oauth2CallbackView(View):
    def get(self, request, *args, **kwargs):
        if not xsrfutil.validate_token(
            settings.SECRET_KEY, request.GET.get('state').encode(),
            request.user):
                return HttpResponseBadRequest()
        credential = flow.step2_exchange(request.GET)
        storage = DjangoORMStorage(
            CredentialsModel, 'id', request.user.id, 'credential')
        storage.put(credential)
        return redirect('/')
