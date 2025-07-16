
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta

from usuario.models import LogAcesso

class CustomAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        User = get_user_model()
        
        # Obter IP do cliente
        client_ip = self._get_client_ip(request)

        # Verificar tentativas de login por IP
        max_login_attempts = 5  # Definir limite de tentativas
        lockout_duration_minutes = 15 # Definir duração do bloqueio

        failed_attempts_count = LogAcesso.objects.filter(
            endereco_ip=client_ip,
            sucesso=False,
            horario_login__gte=timezone.now() - timedelta(minutes=lockout_duration_minutes)
        ).count()

        if failed_attempts_count >= max_login_attempts:
            self._log_access_attempt(None, client_ip, request, False, "IP bloqueado por muitas tentativas")
            return None # IP bloqueado

        # Tentar buscar usuário por username ou RGM
        try:
            user = User.objects.get(Q(username=username) | Q(perfil_aluno__rgm=username))
        except User.DoesNotExist:
            self._log_access_attempt(None, client_ip, request, False, "Usuário ou RGM não encontrado")
            return None

        # Verificar senha
        if user.check_password(password):
            if not user.is_active:
                self._log_access_attempt(user, client_ip, request, False, "Conta desativada")
                return None # Conta desativada
            
            self._log_access_attempt(user, client_ip, request, True) # Login bem-sucedido
            return user
        else:
            self._log_access_attempt(user, client_ip, request, False, "Senha incorreta")
            return None

    def _get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def _log_access_attempt(self, user, ip_address, request, success, reason=None):
        LogAcesso.objects.create(
            usuario=user,
            endereco_ip=ip_address,
            agente_usuario=request.META.get('HTTP_USER_AGENT', ''),
            sucesso=success,
            motivo_falha=reason
        )
