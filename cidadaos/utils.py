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


def generate_credentials(SCOPES):
    """Shows basic usage of the People API.
    Prints the name of the first 10 connections.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    tokenfile = os.path.join(BASE_DIR, 'token.pickle')
    credentialsfile = os.path.join(BASE_DIR, 'credentials.json')


    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = Flow.from_client_secrets_file(credentialsfile, scopes=SCOPES, redirect_uri='urn:ietf:wg:oauth:2.0:oob')
            auth_url, _ = flow.authorization_url(prompt='consent')
        # Save the credentials for the next run
        with open(tokenfile, 'wb') as token:
            pickle.dump(creds, token)
    return creds

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
    print(creds)
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

            if p.engajamento:
                contato['organizations'].append({ "name" : p.engajamento.nome})

            c = service.people().createContact(parent='people/me', body=contato).execute()

            resultado.append(contato)

    modeladmin.message_user(request, '{} contatos atualizados.'.format(len(resultado)))
