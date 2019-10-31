from mailchimp3 import MailChimp
from mailchimp3.helpers import get_subscriber_hash
from django.conf import settings


def return_empty(metadata):
    return {k: v for k, v in metadata.items() if v is not None}

def update_mailchimp(modeladmin, request, queryset):
    
    valid_contacts = queryset.filter(email__isnull=False)

    client = MailChimp(mc_api=settings.MAILCHIMP_API, mc_user=settings.MAILCHIMP_USER)

    listas = client.lists.all(get_all=True, fields="lists.name,lists.id")
    lista = listas['lists'][0]['id']

    for p in valid_contacts:
        user_hash = get_subscriber_hash(p.email)

        contact = {
            'email_address': p.email,
            'status_if_new': 'subscribed',
            'merge_fields': {
                'FNAME': p.nome,
                'LNAME': p.sobrenome,
                'CITY' : p.cidade,
                'STATE' : p.estado,
                'ORG' : p.entidade.first().nome if p.entidade.first() else '',
                'SENSIBLE' : p.engajamento.nome if p.engajamento else '',
                'EVENTS' : '',
                'PHONE' : p.telefone,
                'ADDRESS' : p.endereco,
                'GENDER' :  p.sexo.nome,
                'AGE' : p.idade()
            },
            'tags' : [],
        }

        contact['merge_fields'] = return_empty(contact['merge_fields'])

        resultado = client.lists.members.create_or_update(lista, user_hash, return_empty(contact))
    modeladmin.message_user(request, '{} contatos atualizados.'.format(valid_contacts.count()))


update_mailchimp.short_description = "Atualizar contatos no Mailchimp"