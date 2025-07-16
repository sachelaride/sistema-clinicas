from django.contrib import admin
from .models import Clinica

@admin.register(Clinica)
class ClinicaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo', 'telefone', 'email', 'criado_em', 'atualizado_em')
    search_fields = ('nome', 'email')
    list_filter = ('tipo', 'criado_em', 'atualizado_em')