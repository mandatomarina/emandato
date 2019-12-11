from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field
from import_export import resources
from cidadaos.admin import M2MField, M2MCreateWithForeignKey, ForeignCreateWidget
from .models import Emenda, Orgao, Fase, Territorio
from cidadaos.models import Tema, Entidade, Cidadao
# Register your models here.

class EmendaResource(resources.ModelResource):
    territorio = M2MField(attribute="territorio",column_name='territorio',widget=M2MCreateWithForeignKey(Territorio,',', 'nome', create=True))
    tema = Field(attribute="tema",column_name='tema',widget=ForeignCreateWidget(Tema, 'nome'))
    fase = Field(attribute="fase",column_name='fase',widget=ForeignCreateWidget(Fase, 'nome'))
    entidade = Field(attribute="entidade",column_name='entidade',widget=ForeignCreateWidget(Entidade, 'nome'))
    responsavel = Field(attribute="responsavel",column_name='responsavel',widget=ForeignCreateWidget(Cidadao, 'nome'))
    tecnico = Field(attribute="tecnico",column_name='tecnico',widget=ForeignCreateWidget(Cidadao, 'nome'))
    orgao = Field(attribute='orgao', column_name='orgao', widget=ForeignCreateWidget(Orgao, 'nome'))

    

    class Meta:
        model = Emenda
        import_id_fields = ('projeto',)
        #fields = ('projeto', 'territorio')
        #export_order = ('nome', 'sobrenome', 'email', 'telefone', 'endereco', 'cidade', 'estado', 'sexo', 'raca', 'cargo', 'entidade', 'tema', 'engajamento', 'aniversario')#, 'engajamento')

class EmendaAdmin(ImportExportModelAdmin):

    def territorios(self, obj):
        return ",".join([p.nome for p in obj.territorio.all()])

    resource_class = EmendaResource
    list_display = ('projeto', 'territorios',)

admin.site.register(Emenda, EmendaAdmin)
admin.site.register(Orgao)
admin.site.register(Fase)
admin.site.register(Territorio)
