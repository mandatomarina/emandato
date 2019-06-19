from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import Eixo, Evento, Participacao
# Register your models here.


class ParticipacaoAdmin(ImportExportModelAdmin):

    list_display = ('evento', 'cidadao',)
    list_filter = ['evento__nome']
    search_fields = ('cidadao__nome',)
    
admin.site.register(Eixo)
admin.site.register(Evento)
admin.site.register(Participacao, ParticipacaoAdmin)
