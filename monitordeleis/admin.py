from django.contrib import admin
from .models import Autor, Natureza, Projeto, Tema, Comentario
from django.utils.html import format_html


class ComentarioInline(admin.TabularInline):
    model = Projeto.comentarios.through
    extra = 1

class ProjetoAdmin(admin.ModelAdmin):

    def nome(self, obj):
        return "{} {}/{}".format(obj.natureza,obj.numero_legislativo, obj.ano_legislativo)

    def proj_temas(self, obj):
        return "\n".join([p.tema for p in obj.tema.all()])

    def proj_autores(self, obj):
        return "\n".join([p.nome for p in obj.autor.all()])

    def visto_por(self, obj):
        return ",".join([p.username for p in obj.users.all()])

    def proj_url(self,obj):
        return format_html(
            '<a href="https://www.al.sp.gov.br/propositura/?id={0}" target="_blank">link</a>',
            obj.idDocumento
        )

    def ver_projeto(self, request, queryset):
        for projeto in queryset:
            projeto.users.add(request.user.id)

    ver_projeto.short_description = "Projeto visto"

    list_display = ('nome', 'proj_autores','ementa','data', 'tema', 'proj_url', 'importante', 'obs', 'visto_por')
    list_editable = ('tema', 'importante', 'obs')
    ordering = ('-data',)
    search_fields = ('ementa',)
    list_filter = ('tema', 'autor')
    actions = ['ver_projeto']
    inlines = (ComentarioInline, )
    actions_on_top=True
    actions_on_bottom=False



admin.site.register(Autor)
admin.site.register(Natureza)
admin.site.register(Tema)
admin.site.register(Comentario)
admin.site.register(Projeto, ProjetoAdmin)
