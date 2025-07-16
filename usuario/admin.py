
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, PerfilAluno, LogAcesso, LogAuditoria, AtividadeAluno

@admin.register(Usuario)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'nome_completo', 'is_staff', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('nome_completo', 'telefone', 'clinicas')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('nome_completo', 'telefone', 'clinicas')}),
    )

@admin.register(PerfilAluno)
class PerfilAlunoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'rgm', 'curso', 'semestre')
    search_fields = ('usuario__username', 'rgm', 'curso')
    list_filter = ('curso', 'semestre')

@admin.register(AtividadeAluno)
class AtividadeAlunoAdmin(admin.ModelAdmin):
    list_display = ('aluno', 'tipo_atividade', 'data_atividade', 'horas_dedicadas', 'clinica')
    search_fields = ('aluno__username', 'tipo_atividade', 'clinica__nome')
    list_filter = ('tipo_atividade', 'clinica', 'data_atividade')
    raw_id_fields = ('aluno', 'clinica')

@admin.register(LogAcesso)
class LogAcessoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'horario_login', 'sucesso', 'endereco_ip')
    search_fields = ('usuario__username', 'endereco_ip', 'motivo_falha')
    list_filter = ('sucesso', 'horario_login')

@admin.register(LogAuditoria)
class LogAuditoriaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'acao', 'horario_acao', 'nome_tabela', 'id_registro')
    search_fields = ('usuario__username', 'acao', 'nome_tabela', 'id_registro')
    list_filter = ('acao', 'horario_acao', 'nome_tabela')
