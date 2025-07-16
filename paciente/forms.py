
from django import forms
from .models import Paciente, ResponsavelLegal, TipoDocumento, DocumentoPaciente, ConsentimentoPaciente

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = [
            'nome', 'sobrenome', 'cpf', 'data_nascimento', 'sexo', 
            'endereco', 'telefone', 'email', 'perfil_epidemiologico', 'clinicas'
        ]
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-input'}),
            'sobrenome': forms.TextInput(attrs={'class': 'form-input'}),
            'cpf': forms.TextInput(attrs={'class': 'form-input'}),
            'data_nascimento': forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
            'sexo': forms.Select(attrs={'class': 'form-select'}),
            'endereco': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 4}),
            'telefone': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'perfil_epidemiologico': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 8}),
            'clinicas': forms.SelectMultiple(attrs={'class': 'form-multiselect h-32'}),
        }

class ResponsavelLegalForm(forms.ModelForm):
    class Meta:
        model = ResponsavelLegal
        fields = [
            'paciente', 'nome', 'cpf', 'rg', 'telefone', 
            'email', 'grau_parentesco', 'endereco'
        ]
        widgets = {
            'paciente': forms.Select(attrs={'class': 'form-select'}),
            'nome': forms.TextInput(attrs={'class': 'form-input'}),
            'cpf': forms.TextInput(attrs={'class': 'form-input'}),
            'rg': forms.TextInput(attrs={'class': 'form-input'}),
            'telefone': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'grau_parentesco': forms.TextInput(attrs={'class': 'form-input'}),
            'endereco': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 4}),
        }

class TipoDocumentoForm(forms.ModelForm):
    class Meta:
        model = TipoDocumento
        fields = [
            'nome', 'descricao', 'obrigatorio'
        ]
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-input'}),
            'descricao': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 4}),
            'obrigatorio': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }

class DocumentoPacienteForm(forms.ModelForm):
    class Meta:
        model = DocumentoPaciente
        fields = [
            'paciente', 'tipo_documento', 'dados_ocr', 'caminho_arquivo'
        ]
        widgets = {
            'paciente': forms.Select(attrs={'class': 'form-select'}),
            'tipo_documento': forms.Select(attrs={'class': 'form-select'}),
            'dados_ocr': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 4}),
            'caminho_arquivo': forms.FileInput(attrs={'class': 'form-input-file'}),
        }

class ConsentimentoPacienteForm(forms.ModelForm):
    class Meta:
        model = ConsentimentoPaciente
        fields = [
            'paciente', 'tipo_consentimento', 'ativo', 'detalhes'
        ]
        widgets = {
            'paciente': forms.Select(attrs={'class': 'form-select'}),
            'tipo_consentimento': forms.TextInput(attrs={'class': 'form-input'}),
            'ativo': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'detalhes': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 4}),
        }
