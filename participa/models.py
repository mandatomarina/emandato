from django.db import models
from cidadaos.models import Cidadao

# Create your models here.

class Eixo(models.Model):
    nome = models.CharField(max_length=200)

    def __str__(self):
        return self.nome

class Evento(models.Model):
    nome = models.CharField(max_length=200, verbose_name="Nome do Evento")
    descricao = models.TextField(blank=True)
    data = models.DateField(blank=True, null=True)
    eixo = models.ManyToManyField(Eixo, related_name='eixo_evento', blank=True)
    obs = models.TextField(blank=True)
    participante = models.ManyToManyField(Cidadao, through='Participacao', blank=True)

    def __str__(self):
        return self.nome

class Participacao(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    cidadao = models.ForeignKey(Cidadao, on_delete=models.CASCADE)
    obs = models.TextField(blank=True, null=True)
    compareceu = models.BooleanField(default=False)

    def __str__(self):
        return self.cidadao.nome
