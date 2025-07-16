"""
Dependências da API para autenticação e autorização
"""
from typing import Optional
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from uuid import UUID

from database.session import get_db
from core.security import verify_token, AuthenticationError, AuthorizationError
from crud.usuario import crud_usuario
from schemas.usuario import Usuario
from services.auth_service import authorization_service


# Configuração do esquema de segurança
security = HTTPBearer(auto_error=False)


async def get_current_user(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: Session = Depends(get_db)
) -> Usuario:
    """Obter usuário atual autenticado"""
    if not credentials:
        raise AuthenticationError("Token de acesso necessário")
    
    # Verificar token
    payload = verify_token(credentials.credentials)
    if not payload:
        raise AuthenticationError("Token inválido ou expirado")
    
    # Extrair dados do token
    usuario_id_str = payload.get("sub")
    if not usuario_id_str:
        raise AuthenticationError("Token inválido")
    
    try:
        usuario_id = UUID(usuario_id_str)
    except ValueError:
        raise AuthenticationError("ID de usuário inválido no token")
    
    # Buscar usuário no banco
    usuario = crud_usuario.get(db, usuario_id)
    if not usuario:
        raise AuthenticationError("Usuário não encontrado")
    
    # Verificar se usuário está ativo
    if not usuario.ativo:
        raise AuthenticationError("Conta desativada")
    
    return usuario


async def get_current_active_user(
    current_user: Usuario = Depends(get_current_user)
) -> Usuario:
    """Obter usuário atual ativo (alias para compatibilidade)"""
    return current_user


def require_permissions(*required_permissions: str):
    """Decorator para exigir permissões específicas"""
    def permission_checker(
        current_user: Usuario = Depends(get_current_user),
        db: Session = Depends(get_db)
    ):
        if not authorization_service.check_permissions(
            db, current_user.usuario_id, list(required_permissions)
        ):
            raise AuthorizationError(
                f"Permissões necessárias: {', '.join(required_permissions)}"
            )
        return current_user
    
    return permission_checker


def require_admin():
    """Exigir privilégios de administrador"""
    def admin_checker(
        current_user: Usuario = Depends(get_current_user),
        db: Session = Depends(get_db)
    ):
        if not authorization_service.is_admin(db, current_user.usuario_id):
            raise AuthorizationError("Privilégios de administrador necessários")
        return current_user
    
    return admin_checker


def require_aluno():
    """Exigir que o usuário seja um aluno"""
    def aluno_checker(
        current_user: Usuario = Depends(get_current_user)
    ):
        if not current_user.is_aluno:
            raise AuthorizationError("Acesso restrito a alunos")
        return current_user
    
    return aluno_checker


class PermissionChecker:
    """Classe para verificação de permissões específicas"""
    
    def __init__(self, permission: str):
        self.permission = permission
    
    def __call__(
        self,
        current_user: Usuario = Depends(get_current_user),
        db: Session = Depends(get_db)
    ):
        if not authorization_service.check_permission(
            db, current_user.usuario_id, self.permission
        ):
            raise AuthorizationError(f"Permissão necessária: {self.permission}")
        return current_user


# Dependências específicas para recursos
def can_create_paciente():
    """Verificar permissão para criar pacientes"""
    from core.security import Permissions
    return PermissionChecker(Permissions.PACIENTE_CREATE)


def can_read_paciente():
    """Verificar permissão para ler pacientes"""
    from core.security import Permissions
    return PermissionChecker(Permissions.PACIENTE_READ)


def can_update_paciente():
    """Verificar permissão para atualizar pacientes"""
    from core.security import Permissions
    return PermissionChecker(Permissions.PACIENTE_UPDATE)


def can_delete_paciente():
    """Verificar permissão para excluir pacientes"""
    from core.security import Permissions
    return PermissionChecker(Permissions.PACIENTE_DELETE)


def can_create_usuario():
    """Verificar permissão para criar usuários"""
    from core.security import Permissions
    return PermissionChecker(Permissions.USUARIO_CREATE)


def can_read_usuario():
    """Verificar permissão para ler usuários"""
    from core.security import Permissions
    return PermissionChecker(Permissions.USUARIO_READ)


def can_update_usuario():
    """Verificar permissão para atualizar usuários"""
    from core.security import Permissions
    return PermissionChecker(Permissions.USUARIO_UPDATE)


def can_delete_usuario():
    """Verificar permissão para excluir usuários"""
    from core.security import Permissions
    return PermissionChecker(Permissions.USUARIO_DELETE)


def can_read_relatorio():
    """Verificar permissão para ler relatórios"""
    from core.security import Permissions
    return PermissionChecker(Permissions.RELATORIO_READ)


def can_export_relatorio():
    """Verificar permissão para exportar relatórios"""
    from core.security import Permissions
    return PermissionChecker(Permissions.RELATORIO_EXPORT)


def can_read_logs():
    """Verificar permissão para ler logs"""
    from core.security import Permissions
    return PermissionChecker(Permissions.LOG_READ)


def can_read_auditoria():
    """Verificar permissão para ler auditoria"""
    from core.security import Permissions
    return PermissionChecker(Permissions.AUDITORIA_READ)


# Dependência para obter informações da requisição
def get_request_info(request: Request) -> dict:
    """Obter informações da requisição para logs"""
    return {
        "ip": request.client.host if request.client else "unknown",
        "user_agent": request.headers.get("User-Agent", ""),
        "method": request.method,
        "url": str(request.url),
        "timestamp": request.state.__dict__.get("start_time")
    }

