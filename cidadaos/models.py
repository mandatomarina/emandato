from django.db import models

class Escolaridade(models.Model):
    nome = models.CharField(max_length=200)

    def __str__(self):
        return self.nome

class Raca(models.Model):
    nome = models.CharField(max_length=200)

    def __str__(self):
        return self.nome

class Sexo(models.Model):
    nome = models.CharField(max_length=200)

    def __str__(self):
        return self.nome

class Tema(models.Model):
    nome = models.CharField(max_length=200)
    prioritario = models.BooleanField()

    def __str__(self):
        return self.nome

class Entidade(models.Model):
    nome = models.CharField(max_length=200)

    def __str__(self):
        return self.nome

class Engajamento(models.Model):
    nome = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    rank = models.IntegerField(default=0)

    def __str__(self):
        return self.nome

class Partido(models.Model):

    nome = models.CharField(max_length=200)
    sigla = models.CharField(max_length=10)
    bancada = models.IntegerField(blank=True, default=0)

    def __str__(self):
        return "{} ({})".format(self.nome, str(self.bancada))

# Create your models here.
class Cidadao(models.Model):
    class Meta():
        verbose_name_plural = "Cidadãos"
    nome = models.CharField(max_length=200)
    sobrenome = models.CharField(max_length=200, blank=True, null=True)
    email = models.CharField(max_length=200, unique=True, blank=True, null=True)
    telefone = models.CharField(max_length=200, blank=True, null=True)
    endereco = models.CharField(max_length=200, blank=True, null=True)
    cidade = models.CharField(max_length=200, blank=True, null=True)
    estado = models.CharField(max_length=2, blank=True, null=True)
    aniversario = models.DateField(blank=True, null=True)
    sexo = models.ForeignKey(Sexo, on_delete=models.SET_NULL, null=True, blank=True)
    raca = models.ForeignKey(Raca, on_delete=models.SET_NULL, null=True, blank=True)
    escolaridade = models.ForeignKey(Escolaridade, on_delete=models.SET_NULL, null=True, blank=True)
    obs = models.TextField(blank=True)
    tema = models.ManyToManyField(Tema, related_name='tema_cidadao', blank=True)
    engajamento = models.ForeignKey(Engajamento, on_delete=models.SET_NULL, null=True, blank=True)
    partido = models.ForeignKey(Partido, on_delete=models.SET_NULL, null=True,blank=True)
    referencia = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    entidade = models.ManyToManyField(Entidade, related_name='entidade_cidadao', blank=True)
    novidades = models.BooleanField(default=True, verbose_name="Quer receber novidades?")

    def __str__(self):
        return self.nome


class Categoria(models.Model):
    nome = models.CharField(max_length=200)

    def __str__(self):
        return self.nome

DEMANDA_CHOICES = (
    ('ABERTA', 'Em Aberto'),
    ('ANDAMENTO', 'Em Andamento'),
    ('FINALIZADA', 'Resolvida')
)

class Demanda(models.Model):
    cidadao = models.ForeignKey(Cidadao, on_delete=models.CASCADE)
    data = models.DateField()
    categoria = models.ManyToManyField(Categoria, related_name='categoria_demanda', blank=True)
    descritivo = models.TextField()
    status = models.CharField(max_length=16, choices=DEMANDA_CHOICES, default='ABERTA')

    def __str__(self):
        return self.descritivo
