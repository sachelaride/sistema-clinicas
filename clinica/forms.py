from django import forms
from .models import Clinica

class ClinicaForm(forms.ModelForm):
    class Meta:
        model = Clinica
        fields = '__all__'
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-input'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'endereco': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 4}),
            'telefone': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
        }