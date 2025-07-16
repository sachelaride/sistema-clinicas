
from rest_framework import viewsets
from paciente.models import Paciente, ResponsavelLegal, TipoDocumento, DocumentoPaciente, ConsentimentoPaciente
from paciente.serializers import PacienteSerializer, ResponsavelLegalSerializer, TipoDocumentoSerializer, DocumentoPacienteSerializer, ConsentimentoPacienteSerializer

class PacienteViewSet(viewsets.ModelViewSet):
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer

class ResponsavelLegalViewSet(viewsets.ModelViewSet):
    queryset = ResponsavelLegal.objects.all()
    serializer_class = ResponsavelLegalSerializer

class TipoDocumentoViewSet(viewsets.ModelViewSet):
    queryset = TipoDocumento.objects.all()
    serializer_class = TipoDocumentoSerializer

class DocumentoPacienteViewSet(viewsets.ModelViewSet):
    queryset = DocumentoPaciente.objects.all()
    serializer_class = DocumentoPacienteSerializer

class ConsentimentoPacienteViewSet(viewsets.ModelViewSet):
    queryset = ConsentimentoPaciente.objects.all()
    serializer_class = ConsentimentoPacienteSerializer
