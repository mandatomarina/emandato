from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from .models import Cidadao, Tema, Engajamento, Partido, Entidade, Demanda, Sexo

# Register your models here.

class DemandaInline(admin.StackedInline):
    model = Demanda
    extra = 1

class CidadaoAdmin(ImportExportModelAdmin):
    def lista_tema(self, obj):
        return ",".join([p.nome for p in obj.tema.all()])

    def lista_entidade(self, obj):
        return ",".join([p.nome for p in obj.entidade.all()])

    list_display = ('nome', 'lista_entidade', 'lista_tema', 'email', 'telefone', 'cidade', 'estado')
    filter_horizontal = ('entidade', 'tema')
    search_fields = ('nome', 'email')
    inlines = [
        DemandaInline,
    ]
    autocomplete_fields = ['referencia']

class CidadaoResource(resources.ModelResource):
    class Meta:
        model = Cidadao
        import_id_fields = ('email',)
        skip_unchanged = True

admin.site.register(Cidadao, CidadaoAdmin)
admin.site.register(Demanda)
admin.site.register(Tema)
admin.site.register(Engajamento)
admin.site.register(Sexo)
admin.site.register(Partido)
admin.site.register(Entidade)
