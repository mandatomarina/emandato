from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from cidadaos.admin import M2MField, M2MCreateWithForeignKey
from .models import Emenda, Orgao, Fase, Territorio
# Register your models here.

class EmendaResource(resources.ModelResource):
    tema = M2MField(attribute="tema",column_name='tema',widget=M2MCreateWithForeignKey(Tema,',', 'nome', create=True))

    class Meta:
        model = Emenda
        import_id_fields = ('projeto',)
        #fields = ('nome', 'sobrenome', 'email', 'telefone', 'endereco', 'cidade', 'estado', 'sexo', 'raca', 'cargo', 'entidade', 'tema', 'engajamento', 'aniversario')#, 'engajamento')
        #export_order = ('nome', 'sobrenome', 'email', 'telefone', 'endereco', 'cidade', 'estado', 'sexo', 'raca', 'cargo', 'entidade', 'tema', 'engajamento', 'aniversario')#, 'engajamento')

class EmendaAdmin(ImportExportModelAdmin):
        resource_class = EmendaResource


admin.site.register(Emenda, EmendaAdmin)
admin.site.register(Orgao)
admin.site.register(Fase)
admin.site.register(Territorio)
