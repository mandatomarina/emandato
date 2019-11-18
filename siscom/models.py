from django.db import models
from django.urls import reverse

class Midia(models.Model):
    nome = models.CharField(max_length=200)

    def __str__(self):
        return self.nome

class Formato(models.Model):
    nome = models.CharField(max_length=200)

    def __str__(self):
        return self.nome

PERIODO_CHOICES = (
    ('MANHA', 'Manhã'),
    ('TARDE', 'Tarde'),
    ('NOITE', 'Noite')
)

# Create your models here.
class Conteudo(models.Model):
    tema = models.CharField(max_length=280)
    briefing = models.TextField(blank=True)
    legenda = models.TextField(blank=True)
    midia = models.ManyToManyField(Midia, related_name='midia_conteudo', blank=True)
    formato = models.ManyToManyField(Formato, related_name='formato_conteudo', blank=True)
    obs = models.TextField(blank=True)
    data = models.DateField()
    periodo = models.CharField(max_length=16, choices=PERIODO_CHOICES, default='TARDE')


    def get_admin_url(self):
        return reverse('admin:%s_%s_change' % (self._meta.app_label, self._meta.model_name),
                   args=[self.id])
    def __str__(self):
        return '/'.join(m.nome for m in self.midia.all()) + ': ' + self.tema
