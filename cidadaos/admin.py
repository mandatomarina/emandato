from django.contrib import admin
from .models import Cidadao, Tema, Engajamento, Partido, Entidade, Demanda
# Register your models here.



class DemandaInline(admin.StackedInline):
    model = Demanda
    extra = 1

class CidadaoAdmin(admin.ModelAdmin):
    def lista_tema(self, obj):
        return ",".join([p.nome for p in obj.tema.all()])

    def lista_entidade(self, obj):
        return ",".join([p.nome for p in obj.entidade.all()])

    list_display = ('nome', 'lista_entidade', 'lista_tema', 'email', 'telefone', 'cidade', 'estado')
    filter_horizontal = ('entidade', 'tema')
    inlines = [
        DemandaInline,
    ]

admin.site.register(Cidadao, CidadaoAdmin)
admin.site.register(Demanda)
admin.site.register(Tema)
admin.site.register(Engajamento)
admin.site.register(Partido)
admin.site.register(Entidade)
