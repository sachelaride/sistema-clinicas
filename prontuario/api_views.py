
from rest_framework import viewsets
from prontuario.models import Prontuario, AnexoProntuario, VersaoProntuario
from prontuario.serializers import ProntuarioSerializer, AnexoProntuarioSerializer, VersaoProntuarioSerializer

class ProntuarioViewSet(viewsets.ModelViewSet):
    queryset = Prontuario.objects.all()
    serializer_class = ProntuarioSerializer

class AnexoProntuarioViewSet(viewsets.ModelViewSet):
    queryset = AnexoProntuario.objects.all()
    serializer_class = AnexoProntuarioSerializer

class VersaoProntuarioViewSet(viewsets.ModelViewSet):
    queryset = VersaoProntuario.objects.all()
    serializer_class = VersaoProntuarioSerializer
