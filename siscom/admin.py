from django.contrib import admin
from .models import Conteudo, Midia, Formato


# Register your models here.
class ConteudoAdmin(admin.ModelAdmin):

    def lista_formato(self, obj):
        return ",".join([p.nome for p in obj.formato.all()])

    def lista_midia(self, obj):
        return ",".join([p.nome for p in obj.midia.all()])


    list_display = ('data', 'lista_midia', 'tema', 'briefing', 'legenda', 'lista_formato', 'obs')
    list_editable = ('obs',)

    list_filter = ['tema', 'midia', 'formato', 'data']

    ordering = ('-data',)


admin.site.register(Conteudo, ConteudoAdmin)
admin.site.register(Midia)
admin.site.register(Formato)
