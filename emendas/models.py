from django.db import models
from cidadaos.models import Cidadao, Entidade, Tema

# Create your models here.
RECURSO_CHOICES = (
    ('GERAL', 'Geral'),
    ('SAUDE', 'Saúde')
)

class Orgao(models.Model):
    nome = models.CharField(max_length=200, blank=True, null=True)
    
class Fase(models.Model):
    nome = models.CharField(max_length=200, blank=True, null=True)

class Territorio(models.Model):
    nome = models.CharField(max_length=200, blank=True, null=True)

class Emenda(models.Model):
    tema = models.ForeignKey(Tema, on_delete=models.SET_NULL, null=True, blank=True)
    recurso =  models.CharField(max_length=16, choices=RECURSO_CHOICES, default='GERAL')
    fase = models.ForeignKey(Fase, on_delete=models.SET_NULL, null=True, blank=True)
    projeto = models.CharField(max_length=200, blank=True, null=True)
    objeto = models.TextField(blank=True)
    entidade = models.ForeignKey(Entidade, on_delete=models.SET_NULL, null=True, blank=True)
    responsavel = models.ForeignKey(Cidadao, on_delete=models.SET_NULL, null=True, blank=True)
    tecnico = models.ForeignKey(Cidadao, on_delete=models.SET_NULL, null=True, blank=True)
    orgao = models.ForeignKey(Orgao, on_delete=models.SET_NULL, null=True, blank=True)
    territorio = models.ManyToManyField(Territorio, related_name='territorio_emenda', blank=True)