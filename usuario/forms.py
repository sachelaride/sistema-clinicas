
from django import forms
from django.contrib.auth import get_user_model
from .models import PerfilAluno, LogAcesso, LogAuditoria, AtividadeAluno

User = get_user_model()

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'username', 'nome_completo', 'email', 'telefone', 'is_active',
            'is_staff', 'is_superuser', 'groups', 'user_permissions', 'clinicas'
        )
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-input'}),
            'nome_completo': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'telefone': forms.TextInput(attrs={'class': 'form-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'is_superuser': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'groups': forms.SelectMultiple(attrs={'class': 'form-multiselect h-32'}),
            'user_permissions': forms.SelectMultiple(attrs={'class': 'form-multiselect h-32'}),
            'clinicas': forms.SelectMultiple(attrs={'class': 'form-multiselect h-32'}),
        }

class PerfilAlunoForm(forms.ModelForm):
    class Meta:
        model = PerfilAluno
        fields = '__all__'
        widgets = {
            'usuario': forms.Select(attrs={'class': 'form-select'}),
            'rgm': forms.TextInput(attrs={'class': 'form-input'}),
            'modelo_biometrico': forms.FileInput(attrs={'class': 'form-input-file'}),
            'curso': forms.TextInput(attrs={'class': 'form-input'}),
            'semestre': forms.NumberInput(attrs={'class': 'form-input'}),
            'carga_horaria_total': forms.NumberInput(attrs={'class': 'form-input'}),
        }

class AtividadeAlunoForm(forms.ModelForm):
    class Meta:
        model = AtividadeAluno
        fields = '__all__'
        widgets = {
            'aluno': forms.Select(attrs={'class': 'form-select'}),
            'tipo_atividade': forms.TextInput(attrs={'class': 'form-input'}),
            'descricao': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 4}),
            'data_atividade': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-input'}),
            'horas_dedicadas': forms.NumberInput(attrs={'class': 'form-input'}),
            'clinica': forms.Select(attrs={'class': 'form-select'}),
        }

class LogAcessoForm(forms.ModelForm):
    class Meta:
        model = LogAcesso
        fields = '__all__'
        widgets = {
            'usuario': forms.Select(attrs={'class': 'form-select'}),
            'endereco_ip': forms.TextInput(attrs={'class': 'form-input'}),
            'agente_usuario': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 4}),
            'horario_login': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-input'}),
            'sucesso': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'motivo_falha': forms.TextInput(attrs={'class': 'form-input'}),
        }

class LogAuditoriaForm(forms.ModelForm):
    class Meta:
        model = LogAuditoria
        fields = '__all__'
        widgets = {
            'usuario': forms.Select(attrs={'class': 'form-select'}),
            'acao': forms.TextInput(attrs={'class': 'form-input'}),
            'nome_tabela': forms.TextInput(attrs={'class': 'form-input'}),
            'id_registro': forms.TextInput(attrs={'class': 'form-input'}),
            'horario_acao': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-input'}),
            'dados_antigos': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 4}),
            'dados_novos': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 4}),
            'endereco_ip': forms.TextInput(attrs={'class': 'form-input'}),
        }
