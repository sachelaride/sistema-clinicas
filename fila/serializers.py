
from rest_framework import serializers
from fila.models import PrioridadeFila, FilaEspera

class PrioridadeFilaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrioridadeFila
        fields = '__all__'

class FilaEsperaSerializer(serializers.ModelSerializer):
    class Meta:
        model = FilaEspera
        fields = '__all__'
