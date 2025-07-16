
from django.db import models

class TipoClinica(models.TextChoices):
    FISIOTERAPIA = 'FISIOTERAPIA', 'Fisioterapia'
    ODONTOLOGIA = 'ODONTOLOGIA', 'Odontologia'
    PILATES = 'PILATES', 'Pilates'
    RAIO_X = 'RAIO_X', 'Raio-X'
    FARMACIA = 'FARMACIA', 'Farmácia'
    ESTETICA = 'ESTETICA', 'Estética'
    PSICOLOGIA = 'PSICOLOGIA', 'Psicologia'
    NUTRICAO = 'NUTRICAO', 'Nutrição'
    JURIDICO = 'JURIDICO', 'Jurídico'
    OUTROS = 'OUTROS', 'Outros'

class Clinica(models.Model):
    nome = models.CharField(max_length=255, unique=True)
    tipo = models.CharField(max_length=50, choices=TipoClinica.choices, default=TipoClinica.OUTROS)
    endereco = models.TextField(blank=True, null=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Clínica"
        verbose_name_plural = "Clínicas"

    def __str__(self):
        return self.nome
