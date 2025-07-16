from django.contrib import admin
from .models import Atendimento

@admin.register(Atendimento)
class AtendimentoAdmin(admin.ModelAdmin):
    list_display = ('paciente', 'agendamento', 'clinica', 'atendente', 'status', 'entrada', 'saida')
    search_fields = ('paciente__nome', 'clinica__nome', 'atendente__username')
    list_filter = ('status', 'clinica', 'atendente')
    raw_id_fields = ('paciente', 'agendamento', 'clinica', 'atendente')