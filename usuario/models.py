from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.conf import settings
import uuid

class Usuario(AbstractUser):
    usuario_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome_completo = models.CharField(max_length=150)
    telefone = models.CharField(max_length=20, null=True, blank=True)
    clinicas = models.ManyToManyField('clinica.Clinica', related_name='usuarios', blank=True)

    groups = models.ManyToManyField(
        Group,
        verbose_name='grupos',
        blank=True,
        help_text=
            'Os grupos aos quais este usuário pertence. Um usuário receberá todas as permissões concedidas a cada um de seus grupos.',
        related_name="usuario_set",
        related_query_name="usuario",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='permissões do usuário',
        blank=True,
        help_text='Permissões específicas para este usuário.',
        related_name="usuario_set",
        related_query_name="usuario",
    )

    class Meta:
        permissions = [
            ("can_schedule_appointment", "Pode agendar consultas"),
            ("can_attend_clinic", "Pode atender em clínicas"),
            ("can_manage_prontuario", "Pode gerenciar prontuários"),
        ]

    def __str__(self):
        return self.username

class PerfilAluno(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, primary_key=True, related_name='perfil_aluno')
    rgm = models.CharField(max_length=20, unique=True, db_index=True)
    modelo_biometrico = models.BinaryField(null=True, blank=True)
    curso = models.CharField(max_length=100, null=True, blank=True)
    semestre = models.IntegerField(null=True, blank=True)
    carga_horaria_total = models.IntegerField(default=0)

    def __str__(self):
        return f"Perfil de Aluno de {self.usuario.nome_completo}"

class AtividadeAluno(models.Model):
    aluno = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='atividades')
    tipo_atividade = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    data_atividade = models.DateTimeField(auto_now_add=True)
    horas_dedicadas = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    clinica = models.ForeignKey('clinica.Clinica', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = "Atividade do Aluno"
        verbose_name_plural = "Atividades dos Alunos"
        ordering = ['-data_atividade']

    def __str__(self):
        return f"{self.tipo_atividade} por {self.aluno.username} em {self.data_atividade.strftime('%Y-%m-%d')}"

class LogAcesso(models.Model):
    log_id = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    endereco_ip = models.GenericIPAddressField(null=True, blank=True)
    agente_usuario = models.TextField(null=True, blank=True)
    horario_login = models.DateTimeField(auto_now_add=True)
    sucesso = models.BooleanField()
    motivo_falha = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"Log de acesso de {self.usuario} em {self.horario_login}"

class LogAuditoria(models.Model):
    auditoria_id = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    acao = models.CharField(max_length=50)
    nome_tabela = models.CharField(max_length=100, null=True, blank=True)
    id_registro = models.TextField(null=True, blank=True)
    horario_acao = models.DateTimeField(auto_now_add=True)
    dados_antigos = models.JSONField(null=True, blank=True)
    dados_novos = models.JSONField(null=True, blank=True)
    endereco_ip = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        return f"Auditoria de {self.usuario} em {self.horario_acao}"