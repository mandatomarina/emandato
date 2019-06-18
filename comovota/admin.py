from django.contrib import admin
from .models import Voto, Orgao
# Register your models here.

class VotoAdmin(admin.ModelAdmin):
    def nome(self, obj):
        if (obj.numero and obj.ano):
            return "{} {}/{}".format(obj.tipo,obj.numero, obj.ano)
        else:
            return obj.tipo

    list_display = ('nome', 'ementa_cidada', 'voto', 'justificativa', 'data', 'resultado')
    autocomplete_fields = ['materia']

admin.site.register(Voto, VotoAdmin)
admin.site.register(Orgao)
