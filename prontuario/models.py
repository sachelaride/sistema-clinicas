from django.db import models
from django.conf import settings
import uuid

class Prontuario(models.Model):
    prontuario_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    paciente = models.ForeignKey('paciente.Paciente', on_delete=models.CASCADE, related_name='prontuarios')
    agendamento = models.OneToOneField('agendamento.Agendamento', on_delete=models.SET_NULL, null=True, blank=True, related_name='prontuario')
    clinica = models.ForeignKey('clinica.Clinica', on_delete=models.CASCADE, related_name='prontuarios', null=True, blank=True)
    aluno = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='prontuarios_aluno')
    coordenador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='prontuarios_coordenador')
    anotacoes = models.TextField(blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Prontuário"
        verbose_name_plural = "Prontuários"

    def __str__(self):
        return f"Prontuário de {self.paciente.nome_completo} ({self.prontuario_id})"

class AnexoProntuario(models.Model):
    anexo_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    prontuario = models.ForeignKey(Prontuario, on_delete=models.CASCADE, related_name='anexos')
    tipo_anexo = models.CharField(max_length=50, blank=True, null=True)
    caminho_arquivo = models.FileField(upload_to='prontuarios/anexos/')
    metadados = models.JSONField(blank=True, null=True)
    enviado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Anexo de Prontuário"
        verbose_name_plural = "Anexos de Prontuários"

    def __str__(self):
        return f"Anexo {self.tipo_anexo} para {self.prontuario.paciente.nome_completo}"

class VersaoProntuario(models.Model):
    versao_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    prontuario = models.ForeignKey(Prontuario, on_delete=models.CASCADE, related_name='versoes')
    aluno = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='versoes_prontuario_aluno')
    coordenador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='versoes_prontuario_coordenador')
    anotacoes = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Versão de Prontuário"
        verbose_name_plural = "Versões de Prontuários"
        ordering = ['criado_em']

    def __str__(self):
        return f"Versão {self.criado_em.strftime('%Y-%m-%d %H:%M')} por {self.aluno.username if self.aluno else 'N/A'}"