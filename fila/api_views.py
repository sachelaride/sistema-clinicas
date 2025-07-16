
from rest_framework import viewsets
from fila.models import PrioridadeFila, FilaEspera
from fila.serializers import PrioridadeFilaSerializer, FilaEsperaSerializer

class PrioridadeFilaViewSet(viewsets.ModelViewSet):
    queryset = PrioridadeFila.objects.all()
    serializer_class = PrioridadeFilaSerializer

class FilaEsperaViewSet(viewsets.ModelViewSet):
    queryset = FilaEspera.objects.all()
    serializer_class = FilaEsperaSerializer
