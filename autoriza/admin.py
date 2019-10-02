from django.contrib import admin

from cidadaos.admin import CidadaoAdmin
from .utils import update_contacts


# Register your models here.

CidadaoAdmin.update_contacts.short_description = "Atualizar contatos no Google Contacts"
CidadaoAdmin.actions = [update_contacts]