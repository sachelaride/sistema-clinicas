from django import forms
from .models import Prontuario, AnexoProntuario, VersaoProntuario

class ProntuarioForm(forms.ModelForm):
    class Meta:
        model = Prontuario
        fields = '__all__'
        widgets = {
            'prontuario_id': forms.TextInput(attrs={'readonly': 'readonly', 'class': 'form-input'}),
            'paciente': forms.Select(attrs={'class': 'form-select'}),
            'agendamento': forms.Select(attrs={'class': 'form-select'}),
            'clinica': forms.Select(attrs={'class': 'form-select'}),
            'aluno': forms.Select(attrs={'class': 'form-select'}),
            'coordenador': forms.Select(attrs={'class': 'form-select'}),
            'anotacoes': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 8}),
        }

class AnexoProntuarioForm(forms.ModelForm):
    class Meta:
        model = AnexoProntuario
        fields = '__all__'
        widgets = {
            'anexo_id': forms.TextInput(attrs={'readonly': 'readonly', 'class': 'form-input'}),
            'prontuario': forms.Select(attrs={'class': 'form-select'}),
            'tipo_anexo': forms.TextInput(attrs={'class': 'form-input'}),
            'caminho_arquivo': forms.FileInput(attrs={'class': 'form-input-file'}),
            'metadados': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 4}),
        }

class VersaoProntuarioForm(forms.ModelForm):
    class Meta:
        model = VersaoProntuario
        fields = '__all__'
        widgets = {
            'versao_id': forms.TextInput(attrs={'readonly': 'readonly', 'class': 'form-input'}),
            'prontuario': forms.Select(attrs={'class': 'form-select'}),
            'aluno': forms.Select(attrs={'class': 'form-select'}),
            'coordenador': forms.Select(attrs={'class': 'form-select'}),
            'anotacoes': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 8}),
        }