from django.db import models
from django.conf import settings
import uuid

class PrioridadeFila(models.Model):
    nome = models.CharField(max_length=50, unique=True)
    descricao = models.TextField(blank=True, null=True)
    nivel = models.IntegerField(unique=True, help_text="Nível de prioridade (menor número = maior prioridade)")

    class Meta:
        verbose_name = "Prioridade de Fila"
        verbose_name_plural = "Prioridades de Fila"
        ordering = ['nivel']

    def __str__(self):
        return self.nome

class FilaEspera(models.Model):
    fila_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    paciente = models.ForeignKey('paciente.Paciente', on_delete=models.CASCADE, related_name='filas_espera')
    clinica = models.ForeignKey('clinica.Clinica', on_delete=models.CASCADE, related_name='filas_espera')
    numero_fila = models.IntegerField(help_text="Número sequencial na fila")
    prioridade = models.ForeignKey(PrioridadeFila, on_delete=models.PROTECT, related_name='filas_espera')
    status = models.CharField(max_length=20, default='aguardando', choices=[
        ('aguardando', 'Aguardando'),
        ('chamado', 'Chamado'),
        ('em_atendimento', 'Em Atendimento'),
        ('concluido', 'Concluído'),
        ('cancelado', 'Cancelado'),
    ])
    criado_em = models.DateTimeField(auto_now_add=True)
    chamado_em = models.DateTimeField(blank=True, null=True)
    concluido_em = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = "Fila de Espera"
        verbose_name_plural = "Filas de Espera"
        ordering = ['criado_em']

    def __str__(self):
        return f"Fila {self.numero_fila} - {self.paciente.nome_completo} ({self.prioridade.nome})"