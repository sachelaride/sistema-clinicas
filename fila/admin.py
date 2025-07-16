from django.contrib import admin
from .models import PrioridadeFila, FilaEspera

@admin.register(PrioridadeFila)
class PrioridadeFilaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'nivel', 'descricao')
    search_fields = ('nome',)
    list_filter = ('nivel',)

@admin.register(FilaEspera)
class FilaEsperaAdmin(admin.ModelAdmin):
    list_display = ('paciente', 'clinica', 'numero_fila', 'prioridade', 'status', 'criado_em', 'chamado_em', 'concluido_em')
    search_fields = ('paciente__nome', 'clinica__nome')
    list_filter = ('prioridade', 'status', 'clinica', 'criado_em')
    raw_id_fields = ('paciente', 'clinica', 'prioridade')