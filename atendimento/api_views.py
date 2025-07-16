
from rest_framework import viewsets
from atendimento.models import Atendimento
from atendimento.serializers import AtendimentoSerializer

class AtendimentoViewSet(viewsets.ModelViewSet):
    queryset = Atendimento.objects.all()
    serializer_class = AtendimentoSerializer
