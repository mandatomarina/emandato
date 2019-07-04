from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field
from import_export.widgets import ManyToManyWidget, ForeignKeyWidget
from import_export import resources
from .models import Cidadao, Tema, Engajamento, Partido, Entidade, Demanda, Sexo, Raca, Escolaridade
from participa.models import Participacao
from .utils import update_contacts

# Register your models here.

class DemandaInline(admin.StackedInline):
    model = Demanda
    extra = 1

class DemandaAdmin(admin.ModelAdmin):
    list_display = ('cidadao', 'descritivo', 'data', 'status')
    list_editable = ('status',)

    list_filter = ['status']

    ordering = ('-data',)

class ParticipacaoInline(admin.StackedInline):
    model = Participacao
    extra = 0

class CidadaoResource(resources.ModelResource):
    nentidade = Field(attribute="entidade",column_name='entidade',widget=ManyToManyWidget(Entidade,',', 'nome'))
    nengajamento = Field(attribute="engajamento",column_name='engajamento',widget=ForeignKeyWidget(Engajamento, 'nome'))
    ntema = Field(attribute="tema",column_name='tema',widget=ManyToManyWidget(Tema,',', 'nome'))

    class Meta:
        model = Cidadao
        import_id_fields = ('email')
        skip_unchanged = True
        fields = ('nome', 'email', 'telefone', 'cidade', 'estado', 'sexo', 'raca', 'nentidade', 'ntema', 'nengajamento')
        export_order = ('nome', 'email', 'telefone', 'cidade', 'estado', 'sexo', 'raca', 'nentidade', 'ntema', 'nengajamento')

class CidadaoAdmin(ImportExportModelAdmin):

    def lista_tema(self, obj):
        return ",".join([p.nome for p in obj.tema.all()])

    def lista_entidade(self, obj):
        return ",".join([p.nome for p in obj.entidade.all()])

    resource_class = CidadaoResource
    list_display = ('nome', 'lista_entidade', 'lista_tema', 'email', 'telefone', 'cidade', 'estado')
    search_fields = ('nome', 'email')
    list_filter = ['entidade', 'tema', 'engajamento']
    inlines = [
        DemandaInline,
        ParticipacaoInline,
    ]
    autocomplete_fields = ['referencia']
    update_contacts.short_description = "Atualizar contatos no Google Contacts"

    actions = [update_contacts]

admin.site.register(Cidadao, CidadaoAdmin)
admin.site.register(Demanda, DemandaAdmin)
admin.site.register(Tema)
admin.site.register(Engajamento)
admin.site.register(Raca)
admin.site.register(Sexo)
admin.site.register(Escolaridade)
admin.site.register(Partido)
admin.site.register(Entidade)
