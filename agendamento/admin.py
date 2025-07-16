from django.contrib import admin
from .models import Servico, Sala, Horario, StatusAgendamento, Agendamento

@admin.register(Servico)
class ServicoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'clinica')
    search_fields = ('nome', 'clinica__nome')
    list_filter = ('clinica',)

@admin.register(Sala)
class SalaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'capacidade', 'clinica')
    search_fields = ('nome', 'clinica__nome')
    list_filter = ('clinica',)

@admin.register(Horario)
class HorarioAdmin(admin.ModelAdmin):
    list_display = ('servico', 'sala', 'inicio', 'fim')
    search_fields = ('servico__nome', 'sala__nome')
    list_filter = ('servico', 'sala', 'inicio')
    date_hierarchy = 'inicio'

@admin.register(StatusAgendamento)
class StatusAgendamentoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao')
    search_fields = ('nome',)

@admin.register(Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):
    list_display = ('paciente', 'servico', 'horario', 'status', 'aluno', 'coordenador')
    search_fields = ('paciente__nome', 'servico__nome', 'aluno__username', 'coordenador__username')
    list_filter = ('status', 'servico', 'aluno', 'coordenador')
    raw_id_fields = ('paciente', 'servico', 'horario', 'status', 'aluno', 'coordenador')