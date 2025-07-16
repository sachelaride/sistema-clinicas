
from rest_framework import viewsets
from agendamento.models import Servico, Sala, Horario, StatusAgendamento, Agendamento
from agendamento.serializers import ServicoSerializer, SalaSerializer, HorarioSerializer, StatusAgendamentoSerializer, AgendamentoSerializer

class ServicoViewSet(viewsets.ModelViewSet):
    queryset = Servico.objects.all()
    serializer_class = ServicoSerializer

class SalaViewSet(viewsets.ModelViewSet):
    queryset = Sala.objects.all()
    serializer_class = SalaSerializer

class HorarioViewSet(viewsets.ModelViewSet):
    queryset = Horario.objects.all()
    serializer_class = HorarioSerializer

class StatusAgendamentoViewSet(viewsets.ModelViewSet):
    queryset = StatusAgendamento.objects.all()
    serializer_class = StatusAgendamentoSerializer

class AgendamentoViewSet(viewsets.ModelViewSet):
    queryset = Agendamento.objects.all()
    serializer_class = AgendamentoSerializer
