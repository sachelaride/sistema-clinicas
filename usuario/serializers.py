
from rest_framework import serializers
from django.contrib.auth import get_user_model
from usuario.models import PerfilAluno, LogAcesso, LogAuditoria, AtividadeAluno

User = get_user_model()

class PerfilAlunoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerfilAluno
        fields = '__all__'

class UsuarioSerializer(serializers.ModelSerializer):
    perfil_aluno = PerfilAlunoSerializer(read_only=True)

    class Meta:
        model = User
        fields = (
            'usuario_id', 'username', 'nome_completo', 'email', 'telefone',
            'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions', 'clinicas',
            'perfil_aluno'
        )

class AtividadeAlunoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AtividadeAluno
        fields = '__all__'

class LogAcessoSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogAcesso
        fields = '__all__'

class LogAuditoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogAuditoria
        fields = '__all__'
