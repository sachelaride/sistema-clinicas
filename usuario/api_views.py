
from rest_framework import viewsets
from django.contrib.auth import get_user_model
from usuario.models import PerfilAluno, LogAcesso, LogAuditoria, AtividadeAluno
from usuario.serializers import UsuarioSerializer, PerfilAlunoSerializer, LogAcessoSerializer, LogAuditoriaSerializer, AtividadeAlunoSerializer

User = get_user_model()

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsuarioSerializer

class PerfilAlunoViewSet(viewsets.ModelViewSet):
    queryset = PerfilAluno.objects.all()
    serializer_class = PerfilAlunoSerializer

class AtividadeAlunoViewSet(viewsets.ModelViewSet):
    queryset = AtividadeAluno.objects.all()
    serializer_class = AtividadeAlunoSerializer

class LogAcessoViewSet(viewsets.ModelViewSet):
    queryset = LogAcesso.objects.all()
    serializer_class = LogAcessoSerializer

class LogAuditoriaViewSet(viewsets.ModelViewSet):
    queryset = LogAuditoria.objects.all()
    serializer_class = LogAuditoriaSerializer
