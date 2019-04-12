from django.db import models
from datetime import date

PRIORIDADE_CHOICES = (
    ('BAIXA', 'Baixa'),
    ('MEDIA', 'Média'),
    ('ALTA', 'Alta'),
    ('ALTISSIMA', 'Altissima')
)

class Comentario(models.Model):
    texto = models.TextField()

    def __str__(self):
        return self.texto

class Tema(models.Model):
    tema = models.CharField(max_length=200)

    def __str__(self):
        return self.tema

class Autor(models.Model):
    class Meta():
        verbose_name_plural = "Autores"

    idAutor = models.CharField(max_length=200, primary_key=True)
    nome = models.CharField(max_length=200)

    def __str__(self):
        return self.nome

class Natureza(models.Model):
    class Meta():
        verbose_name_plural = "Naturezas"

    idNatureza = models.CharField(max_length=200, primary_key=True)
    nome = models.CharField(max_length=200)
    sigla = models.CharField(max_length=200)
    tipo = models.CharField(max_length=200)

    def __str__(self):
        if self.sigla:
            return self.sigla
        else:
            return self.nome

class Projeto(models.Model):
    class Meta():
        verbose_name_plural = "Projetos"

    ementa = models.CharField(max_length=200)
    idDocumento = models.CharField(max_length=200, primary_key=True)
    numero_legislativo = models.CharField(max_length=200, blank=True)
    ano_legislativo = models.IntegerField(default=0)
    data = models.DateField(blank=True)
    dt_publicacao = models.DateField(blank=True)
    natureza = models.ForeignKey(Natureza, on_delete=models.CASCADE)
    autor = models.ManyToManyField(Autor, related_name='autor_projeto', blank=True)
    tema = models.ForeignKey(Tema, on_delete=models.SET_NULL, blank=True, null=True)
    prioridade = models.CharField(max_length=10, choices=PRIORIDADE_CHOICES, default='BAIXA')
    comentarios = models.ManyToManyField(Comentario, related_name='comentario_projeto', blank=True)
    importante = models.BooleanField(default=False)

    def tempo_emenda(self):
        today = date.today()
        delta = today-self.data
        return str(15-delta.days)+" dias"

    def __str__(self):
        return self.ementa
