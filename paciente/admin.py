from django.contrib import admin
from .models import Paciente, ResponsavelLegal, TipoDocumento, DocumentoPaciente, ConsentimentoPaciente

@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'sobrenome', 'cpf', 'email', 'telefone', 'criado_em')
    search_fields = ('nome', 'sobrenome', 'email', 'telefone')
    list_filter = ('sexo', 'criado_em', 'clinicas')
    date_hierarchy = 'criado_em'
    filter_horizontal = ('clinicas',)

@admin.register(ResponsavelLegal)
class ResponsavelLegalAdmin(admin.ModelAdmin):
    list_display = ('nome', 'paciente', 'grau_parentesco', 'telefone')
    search_fields = ('nome', 'paciente__nome', 'cpf')
    list_filter = ('grau_parentesco',)

@admin.register(TipoDocumento)
class TipoDocumentoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'obrigatorio')
    search_fields = ('nome',)

@admin.register(DocumentoPaciente)
class DocumentoPacienteAdmin(admin.ModelAdmin):
    list_display = ('paciente', 'tipo_documento', 'caminho_arquivo', 'enviado_em')
    search_fields = ('paciente__nome', 'tipo_documento__nome')
    list_filter = ('tipo_documento', 'enviado_em')

@admin.register(ConsentimentoPaciente)
class ConsentimentoPacienteAdmin(admin.ModelAdmin):
    list_display = ('paciente', 'tipo_consentimento', 'ativo', 'data_consentimento')
    search_fields = ('paciente__nome', 'tipo_consentimento')
    list_filter = ('ativo', 'data_consentimento')