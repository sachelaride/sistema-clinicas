from django.contrib import admin
from .models import Prontuario, AnexoProntuario, VersaoProntuario

@admin.register(Prontuario)
class ProntuarioAdmin(admin.ModelAdmin):
    list_display = ('paciente', 'agendamento', 'clinica', 'aluno', 'coordenador', 'criado_em')
    search_fields = ('paciente__nome', 'agendamento__servico__nome', 'aluno__username', 'coordenador__username')
    list_filter = ('clinica', 'aluno', 'coordenador', 'criado_em')
    raw_id_fields = ('paciente', 'agendamento', 'clinica', 'aluno', 'coordenador')

@admin.register(AnexoProntuario)
class AnexoProntuarioAdmin(admin.ModelAdmin):
    list_display = ('prontuario', 'tipo_anexo', 'caminho_arquivo', 'enviado_em')
    search_fields = ('prontuario__paciente__nome', 'tipo_anexo')
    list_filter = ('tipo_anexo', 'enviado_em')

@admin.register(VersaoProntuario)
class VersaoProntuarioAdmin(admin.ModelAdmin):
    list_display = ('prontuario', 'aluno', 'coordenador', 'criado_em')
    search_fields = ('prontuario__paciente__nome', 'aluno__username', 'coordenador__username')
    list_filter = ('criado_em', 'aluno', 'coordenador')