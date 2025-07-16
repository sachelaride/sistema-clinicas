from django.db import models
from django.conf import settings
import uuid

class Servico(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    clinica = models.ForeignKey('clinica.Clinica', on_delete=models.CASCADE, related_name='servicos', null=True, blank=True)

    class Meta:
        verbose_name = "Serviço"
        verbose_name_plural = "Serviços"

    def __str__(self):
        return self.nome

class Sala(models.Model):
    nome = models.CharField(max_length=50)
    capacidade = models.IntegerField(default=1)
    clinica = models.ForeignKey('clinica.Clinica', on_delete=models.CASCADE, related_name='salas', null=True, blank=True)

    class Meta:
        verbose_name = "Sala"
        verbose_name_plural = "Salas"

    def __str__(self):
        return f"{self.nome} ({self.clinica.nome if self.clinica else 'N/A'})"

class Horario(models.Model):
    servico = models.ForeignKey(Servico, on_delete=models.CASCADE, related_name='horarios')
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE, related_name='horarios')
    inicio = models.DateTimeField()
    fim = models.DateTimeField()

    class Meta:
        verbose_name = "Horário"
        verbose_name_plural = "Horários"

    def __str__(self):
        return f"{self.servico.nome} em {self.sala.nome} de {self.inicio.strftime('%H:%M')} a {self.fim.strftime('%H:%M')}"

class StatusAgendamento(models.Model):
    nome = models.CharField(max_length=50, unique=True)
    descricao = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Status de Agendamento"
        verbose_name_plural = "Status de Agendamentos"

    def __str__(self):
        return self.nome

class Agendamento(models.Model):
    agendamento_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    paciente = models.ForeignKey('paciente.Paciente', on_delete=models.CASCADE, related_name='agendamentos')
    servico = models.ForeignKey(Servico, on_delete=models.CASCADE, related_name='agendamentos')
    horario = models.ForeignKey(Horario, on_delete=models.CASCADE, related_name='agendamentos')
    status = models.ForeignKey(StatusAgendamento, on_delete=models.PROTECT, related_name='agendamentos')
    aluno = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='agendamentos_aluno')
    coordenador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='agendamentos_coordenador')
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Agendamento"
        verbose_name_plural = "Agendamentos"

    def __str__(self):
        return f"Agendamento de {self.paciente.nome_completo} para {self.servico.nome}"