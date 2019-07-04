from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from django.http import JsonResponse

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

    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credentialsfile, SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
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
    # Call the People API
    SCOPES = ['https://www.googleapis.com/auth/contacts']
    creds = generate_credentials(SCOPES)
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
                ]
            }

            if p.engajamento:
                x['organizations'].append({ "name" : p.engajamento.nome})

            c = service.people().createContact(parent='people/me', body=contato).execute()
            resultado.append(x)

    return JsonResponse({ "results" : resultado})
