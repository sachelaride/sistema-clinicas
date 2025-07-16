
from rest_framework import viewsets
from clinica.models import Clinica
from clinica.serializers import ClinicaSerializer

class ClinicaViewSet(viewsets.ModelViewSet):
    queryset = Clinica.objects.all()
    serializer_class = ClinicaSerializer
