from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from oauth2client.contrib.django_util.storage import DjangoORMStorage
from autoriza.models import CredentialsModel

from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect

def get_agenda(service):
    AGENDA = []
    results = service.people().connections().list(
        resourceName='people/me',
        pageSize=2000,
        personFields='phoneNumbers').execute()

    while 'nextPageToken' in results:
        for person in results['connections']:
            if 'phoneNumbers' in person:
                for number in person['phoneNumbers']:
                    AGENDA.append(number['value'])

        results = service.people().connections().list(
            resourceName='people/me',
            pageSize=2000,
            pageToken=results['nextPageToken'],
            personFields='phoneNumbers').execute()

        for person in results['connections']:
            if 'phoneNumbers' in person:
                for number in person['phoneNumbers']:
                    AGENDA.append(number['value'])
    return AGENDA

def update_contacts(modeladmin, request, queryset):

    storage = DjangoORMStorage(CredentialsModel, 'id', request.user.id, 'credential')
    creds = storage.get()
    if creds is None or creds.invalid == True:
        return redirect('authorize')


    service = build('people', 'v1', credentials=creds)

    agenda = get_agenda(service)
    resultado = []

    for p in queryset.all():
        if not p.telefone in agenda:

            contato = {
        	    "names": [
        	        {
        	            "givenName": p.nome
        	        }
        	    ],
        	    "phoneNumbers": [
        	        {
        	            'value': p.telefone
        	        }
        	    ],
                "emailAddresses": [
                    {
                        'value': p.email
                    }],
                "organizations": [
                    {
                        "name" : "Teste de importação"
                    }
                ],
                "userDefined" : [
                    {
                        "key" : "obs",
                        "value": ""
                    }
                ]
            }

            if p.obs:
                contato['userDefined'][0]['value'] = p.obs

            for o in p.engajamento.all():
                contato['organizations'].append({ "name" : o.nome})

            c = service.people().createContact(parent='people/me', body=contato).execute()

            resultado.append(contato)

    modeladmin.message_user(request, '{} contatos atualizados.'.format(len(resultado)))

update_contacts.short_description = "Atualizar contatos no Google Contacts"