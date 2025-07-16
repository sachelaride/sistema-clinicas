
from django import forms
from django.contrib.auth import get_user_model
from .models import Servico, Sala, Horario, StatusAgendamento, Agendamento

User = get_user_model()

class ServicoForm(forms.ModelForm):
    class Meta:
        model = Servico
        fields = '__all__'
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-input'}),
            'descricao': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 4}),
            'clinica': forms.Select(attrs={'class': 'form-select'}),
        }

class SalaForm(forms.ModelForm):
    class Meta:
        model = Sala
        fields = '__all__'
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-input'}),
            'capacidade': forms.NumberInput(attrs={'class': 'form-input'}),
            'clinica': forms.Select(attrs={'class': 'form-select'}),
        }

class HorarioForm(forms.ModelForm):
    class Meta:
        model = Horario
        fields = '__all__'
        widgets = {
            'servico': forms.Select(attrs={'class': 'form-select'}),
            'sala': forms.Select(attrs={'class': 'form-select'}),
            'inicio': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-input'}),
            'fim': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-input'}),
        }

class StatusAgendamentoForm(forms.ModelForm):
    class Meta:
        model = StatusAgendamento
        fields = '__all__'
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-input'}),
            'descricao': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 4}),
        }

class AgendamentoForm(forms.ModelForm):
    class Meta:
        model = Agendamento
        fields = '__all__'
        widgets = {
            'agendamento_id': forms.TextInput(attrs={'readonly': 'readonly', 'class': 'form-input'}),
            'paciente': forms.Select(attrs={'class': 'form-select'}),
            'servico': forms.Select(attrs={'class': 'form-select'}),
            'horario': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'aluno': forms.Select(attrs={'class': 'form-select'}),
            'coordenador': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar alunos que podem atender em clínicas
        self.fields['aluno'].queryset = User.objects.filter(user_permissions__codename='can_attend_clinic').distinct()
        # Filtrar coordenadores/professores que podem agendar
        self.fields['coordenador'].queryset = User.objects.filter(user_permissions__codename='can_schedule_appointment').distinct()
