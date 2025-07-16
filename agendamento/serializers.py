
from rest_framework import serializers
from agendamento.models import Servico, Sala, Horario, StatusAgendamento, Agendamento

class ServicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servico
        fields = '__all__'

class SalaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sala
        fields = '__all__'

class HorarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Horario
        fields = '__all__'

class StatusAgendamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusAgendamento
        fields = '__all__'

class AgendamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agendamento
        fields = '__all__'
