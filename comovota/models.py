from django.db import models
from django.utils import timezone
from monitordeleis.models import Projeto
import datetime

VOTO_CHOICES = (
    ('SIM', 'Sim'),
    ('NAO', 'Não'),
    ('ABSTENCAO', 'Abstenção'),
    ('OBSTRUCAO', 'Obstrução'),
    ('FALTA_JUS', 'Falta justificada'),
    ('FALTA_NJUS', 'Falta não justificada')
)

# Create your models here.
class Orgao(models.Model):
    nome = models.CharField(max_length=64)

    def __str__(self):
        return self.nome

class Voto(models.Model):
    tipo = models.CharField(max_length=10, null=True, blank=True)
    numero = models.CharField(max_length=4, null=True, blank=True)
    ano = models.CharField(max_length=4, null=True, blank=True)
    ementa_cidada = models.TextField(null=True)
    voto = models.CharField(max_length=10, choices=VOTO_CHOICES)
    justificativa = models.TextField(null=True)
    data = models.DateField(blank=True, default=timezone.now)
    orgao = models.ForeignKey(Orgao, on_delete=models.SET_NULL, blank=True, null=True)
    resultado = models.TextField(null=True, blank=True)
    materia = models.ForeignKey(Projeto, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.voto
