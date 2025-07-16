from django import forms
from django.contrib.auth import get_user_model
from .models import Atendimento

User = get_user_model()

class AtendimentoForm(forms.ModelForm):
    class Meta:
        model = Atendimento
        fields = '__all__'
        widgets = {
            'atendimento_id': forms.TextInput(attrs={'readonly': 'readonly'}),
            'entrada': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'saida': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar atendentes que podem atender em clínicas
        self.fields['atendente'].queryset = User.objects.filter(user_permissions__codename='can_attend_clinic').distinct()