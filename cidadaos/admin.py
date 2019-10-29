from django.contrib import admin
from django.apps import apps
from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field
from import_export.widgets import ManyToManyWidget, ForeignKeyWidget
from import_export import resources
from .models import Cidadao, Tema, Engajamento, Partido, Entidade, Demanda, Sexo, Raca, Escolaridade
from participa.models import Participacao
from django.conf import settings
from django.contrib.admin import SimpleListFilter
from .forms import RangeNumericForm
import datetime

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


#Widget para criar automaticamente entidades c ForeignKey
class ForeignCreateWidget(ForeignKeyWidget):
    def clean(self, value, row=None, *args, **kwargs):
        return self.model.objects.get_or_create(nome=value)[0] if value else None


#Filtro por idade
class AgeFilter(SimpleListFilter):
    title = 'age' # or use _('country') for translated title
    template = 'filter_numeric_range.html'
    parameter_name = 'idade_from'    
        
    def __init__(self, field, request, params, model):
        super().__init__(field, request, params, model)
        self.request = request

    def getDate(self, years):
            if years:
                return datetime.datetime.now() - datetime.timedelta(int(years) * 365.25)

    def lookups(self, request, model_admin):
        return ((1337, 1337))

    def queryset(self, request, queryset):
        filters = {}
        values = self.used_parameters.get('idade_from', None)
        value_from = values
        value_to = None

        if values and '-' in values:
            value_from = int(values.split('-')[0])
            value_to = int(values.split('-')[1])

        if value_from is not None and value_from != '':
            filters.update({
               'aniversario__lte': self.getDate(value_from),
            })
        
        if value_to is not None and value_to != '':
            filters.update({
                'aniversario__gte': self.getDate(value_to),
            })

        return queryset.filter(**filters)


    def choices(self, changelist):
        # Grab only the "all" option.
        choice = next(super().choices(changelist))
        choice['query_parts'] = (
            (k, v)
            for k, v in changelist.get_filters_params().items()
            if k not in [self.parameter_name]
        )
        yield choice

    

class CidadaoResource(resources.ModelResource):
    entidade = Field(attribute="entidade",column_name='entidade',widget=ManyToManyWidget(Entidade,',', 'nome'))
    engajamento = Field(attribute="engajamento",column_name='engajamento',widget=ForeignCreateWidget(Engajamento, 'nome'))
    tema = Field(attribute="tema",column_name='tema',widget=ManyToManyWidget(Tema,',', 'nome'))

    class Meta:
        model = Cidadao
        import_id_fields = ('email',)
        skip_unchanged = False
        fields = ('nome', 'email', 'telefone', 'cidade', 'estado', 'sexo', 'raca', 'entidade', 'tema', 'engajamento',)#, 'engajamento')
        export_order = ('nome', 'email', 'telefone', 'cidade', 'estado', 'sexo', 'raca', 'entidade', 'tema')#, 'engajamento')

class CidadaoAdmin(ImportExportModelAdmin):
    def idade(self, obj):
        return int((datetime.date.today()-obj.aniversario).days/365.25)

    def lista_tema(self, obj):
        return ",".join([p.nome for p in obj.tema.all()])

    def lista_entidade(self, obj):
        return ",".join([p.nome for p in obj.entidade.all()])

    resource_class = CidadaoResource
    list_display = ('nome', 'lista_entidade', 'lista_tema', 'email', 'telefone', 'cidade', 'estado', 'idade')
    search_fields = ('nome', 'email')
    list_filter = ('entidade', 'tema', 'engajamento', 'sexo', 'raca', AgeFilter)
    inlines = [
        DemandaInline,
        ParticipacaoInline,
    ]
    autocomplete_fields = ['referencia']

    actions = []
    if apps.is_installed("autoriza"):
        from autoriza.utils import update_contacts
        actions += [update_contacts]

    if settings.MAILCHIMP_API:
        from .plugins.mailchimp import update_mailchimp
        actions += [update_mailchimp]

admin.site.register(Cidadao, CidadaoAdmin)
admin.site.register(Demanda, DemandaAdmin)
admin.site.register(Tema)
admin.site.register(Engajamento)
admin.site.register(Raca)
admin.site.register(Sexo)
admin.site.register(Escolaridade)
admin.site.register(Partido)
admin.site.register(Entidade)
