from django import forms
from .models import PrioridadeFila, FilaEspera

class PrioridadeFilaForm(forms.ModelForm):
    class Meta:
        model = PrioridadeFila
        fields = '__all__'
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-input'}),
            'descricao': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 4}),
            'nivel': forms.NumberInput(attrs={'class': 'form-input'}),
        }

class FilaEsperaForm(forms.ModelForm):
    class Meta:
        model = FilaEspera
        fields = '__all__'
        widgets = {
            'fila_id': forms.TextInput(attrs={'readonly': 'readonly', 'class': 'form-input'}),
            'paciente': forms.Select(attrs={'class': 'form-select'}),
            'clinica': forms.Select(attrs={'class': 'form-select'}),
            'numero_fila': forms.NumberInput(attrs={'class': 'form-input'}),
            'prioridade': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'chamado_em': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-input'}),
            'concluido_em': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-input'}),
        }