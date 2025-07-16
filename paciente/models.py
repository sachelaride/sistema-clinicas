import uuid
from django.db import models
from django.utils import timezone

class Sexo(models.TextChoices):
    MASCULINO = 'M', 'Masculino'
    FEMININO = 'F', 'Feminino'
    OUTRO = 'O', 'Outro'

class Paciente(models.Model):
    paciente_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=100, db_index=True)
    sobrenome = models.CharField(max_length=100, db_index=True)
    cpf = models.CharField(max_length=14, unique=True, null=True, blank=True)
    data_nascimento = models.DateField(null=True, blank=True)
    sexo = models.CharField(max_length=1, choices=Sexo.choices, null=True, blank=True)
    endereco = models.TextField(null=True, blank=True)
    telefone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True, db_index=True)
    perfil_epidemiologico = models.JSONField(null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    clinicas = models.ManyToManyField('clinica.Clinica', related_name='pacientes', blank=True)

    def nome_completo(self):
        return f"{self.nome} {self.sobrenome}".strip()

    def idade(self):
        if self.data_nascimento:
            hoje = timezone.now().date()
            return hoje.year - self.data_nascimento.year - (
                (hoje.month, hoje.day) < (self.data_nascimento.month, self.data_nascimento.day)
            )
        return None

    def __str__(self):
        return self.nome_completo()

class ResponsavelLegal(models.Model):
    responsavel_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='responsaveis')
    nome = models.CharField(max_length=150)
    cpf = models.CharField(max_length=14, null=True, blank=True)
    rg = models.CharField(max_length=20, null=True, blank=True)
    telefone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    grau_parentesco = models.CharField(max_length=50, null=True, blank=True)
    endereco = models.TextField(null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

class TipoDocumento(models.Model):
    tipo_id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=50, unique=True)
    descricao = models.TextField(null=True, blank=True)
    obrigatorio = models.BooleanField(default=False)

    def __str__(self):
        return self.nome

class DocumentoPaciente(models.Model):
    documento_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='documentos')
    tipo_documento = models.ForeignKey(TipoDocumento, on_delete=models.SET_NULL, null=True, blank=True)
    dados_ocr = models.TextField(null=True, blank=True)
    caminho_arquivo = models.FileField(upload_to='documentos_pacientes/')
    enviado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Documento de {self.paciente.nome_completo()} - {self.tipo_documento.nome}"

class ConsentimentoPaciente(models.Model):
    consentimento_id = models.AutoField(primary_key=True)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='consentimentos')
    tipo_consentimento = models.CharField(max_length=50)
    data_consentimento = models.DateTimeField(auto_now_add=True)
    ativo = models.BooleanField(default=True)
    detalhes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Consentimento de {self.paciente.nome_completo()} para {self.tipo_consentimento}"