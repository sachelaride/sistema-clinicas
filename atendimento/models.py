from django.db import models
from django.conf import settings
import uuid

class Atendimento(models.Model):
    atendimento_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    paciente = models.ForeignKey('paciente.Paciente', on_delete=models.CASCADE, related_name='atendimentos')
    agendamento = models.OneToOneField('agendamento.Agendamento', on_delete=models.SET_NULL, null=True, blank=True, related_name='atendimento')
    clinica = models.ForeignKey('clinica.Clinica', on_delete=models.CASCADE, related_name='atendimentos')
    atendente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='atendimentos_realizados')
    anotacoes = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=50, default='iniciado', choices=[
        ('iniciado', 'Iniciado'),
        ('em_progresso', 'Em Progresso'),
        ('concluido', 'Concluído'),
        ('cancelado', 'Cancelado'),
    ])
    entrada = models.DateTimeField(blank=True, null=True)
    saida = models.DateTimeField(blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Atendimento"
        verbose_name_plural = "Atendimentos"

    def __str__(self):
        return f"Atendimento de {self.paciente.nome_completo} em {self.clinica.nome}"