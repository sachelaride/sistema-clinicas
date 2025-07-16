
from rest_framework import serializers
from prontuario.models import Prontuario, AnexoProntuario, VersaoProntuario

class ProntuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prontuario
        fields = '__all__'

class AnexoProntuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnexoProntuario
        fields = '__all__'

class VersaoProntuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = VersaoProntuario
        fields = '__all__'
