"""
Serviço de autenticação e autorização
"""
from typing import Optional, Dict, Any
from datetime import datetime
from uuid import UUID
from sqlalchemy.orm import Session
from fastapi import Request

from core.security import (
    verify_password, get_password_hash, create_token_response,
    AuthenticationError, AccountLockedError
)
from crud.usuario import crud_usuario, crud_log_acesso, crud_log_auditoria
from schemas.usuario import LoginRequest, LoginResponse, Usuario


class AuthService:
    """Serviço de autenticação"""
    
    def __init__(self):
        self.max_login_attempts = 5
        self.lockout_duration_minutes = 15
    
    def authenticate_user(self, db: Session, login_data: LoginRequest, request: Request) -> Optional[Usuario]:
        """Autenticar usuário"""
        # Verificar tentativas de login por IP
        client_ip = self._get_client_ip(request)
        failed_attempts = crud_log_acesso.get_tentativas_falha(
            db, client_ip, self.lockout_duration_minutes
        )
        
        if failed_attempts >= self.max_login_attempts:
            self._log_access_attempt(db, None, client_ip, request, False, "IP bloqueado")
            raise AccountLockedError("Muitas tentativas de login. Tente novamente mais tarde.")
        
        # Buscar usuário por nome de usuário ou RGM
        usuario = crud_usuario.get_by_nome_usuario(db, login_data.nome_usuario)
        if not usuario:
            # Tentar buscar por RGM se for aluno
            usuario = crud_usuario.get_by_rgm(db, login_data.nome_usuario)
        
        # Verificar credenciais
        if not usuario or not verify_password(login_data.senha, usuario.senha_hash):
            self._log_access_attempt(db, None, client_ip, request, False, "Credenciais inválidas")
            raise AuthenticationError("Nome de usuário ou senha incorretos")
        
        # Verificar se usuário está ativo
        if not usuario.ativo:
            self._log_access_attempt(db, usuario.usuario_id, client_ip, request, False, "Usuário inativo")
            raise AuthenticationError("Conta desativada")
        
        # Login bem-sucedido
        self._log_access_attempt(db, usuario.usuario_id, client_ip, request, True)
        return usuario
    
    def login(self, db: Session, login_data: LoginRequest, request: Request) -> LoginResponse:
        """Realizar login e retornar token"""
        usuario = self.authenticate_user(db, login_data, request)
        
        # Criar token
        token_data = create_token_response(
            usuario_id=str(usuario.usuario_id),
            nome_usuario=usuario.nome_usuario,
            perfil_id=usuario.perfil_id
        )
        
        # Registrar auditoria
        crud_log_auditoria.create(
            db=db,
            usuario_id=usuario.usuario_id,
            acao="LOGIN",
            endereco_ip=self._get_client_ip(request)
        )
        
        return LoginResponse(
            **token_data,
            usuario=usuario
        )
    
    def change_password(self, db: Session, usuario_id: UUID, senha_atual: str, 
                       nova_senha: str, request: Request) -> bool:
        """Alterar senha do usuário"""
        usuario = crud_usuario.get(db, usuario_id)
        if not usuario:
            return False
        
        # Verificar senha atual
        if not verify_password(senha_atual, usuario.senha_hash):
            raise AuthenticationError("Senha atual incorreta")
        
        # Atualizar senha
        crud_usuario.update_senha(db, usuario_id, nova_senha)
        
        # Registrar auditoria
        crud_log_auditoria.create(
            db=db,
            usuario_id=usuario_id,
            acao="CHANGE_PASSWORD",
            endereco_ip=self._get_client_ip(request)
        )
        
        return True
    
    def reset_password(self, db: Session, usuario_id: UUID, nova_senha: str, 
                      admin_id: UUID, request: Request) -> bool:
        """Resetar senha do usuário (admin)"""
        usuario = crud_usuario.get(db, usuario_id)
        if not usuario:
            return False
        
        # Atualizar senha
        crud_usuario.update_senha(db, usuario_id, nova_senha)
        
        # Registrar auditoria
        crud_log_auditoria.create(
            db=db,
            usuario_id=admin_id,
            acao="RESET_PASSWORD",
            nome_tabela="usuarios",
            id_registro=str(usuario_id),
            endereco_ip=self._get_client_ip(request)
        )
        
        return True
    
    def _get_client_ip(self, request: Request) -> str:
        """Obter IP do cliente"""
        # Verificar headers de proxy
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        
        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip
        
        return request.client.host if request.client else "unknown"
    
    def _log_access_attempt(self, db: Session, usuario_id: Optional[UUID], 
                           endereco_ip: str, request: Request, sucesso: bool, 
                           motivo_falha: Optional[str] = None):
        """Registrar tentativa de acesso"""
        user_agent = request.headers.get("User-Agent", "")
        
        crud_log_acesso.create(
            db=db,
            usuario_id=usuario_id,
            endereco_ip=endereco_ip,
            agente_usuario=user_agent,
            sucesso=sucesso,
            motivo_falha=motivo_falha
        )


class AuthorizationService:
    """Serviço de autorização"""
    
    def check_permission(self, db: Session, usuario_id: UUID, permissao: str) -> bool:
        """Verificar se usuário tem permissão específica"""
        return crud_usuario.has_permissao(db, usuario_id, permissao)
    
    def check_permissions(self, db: Session, usuario_id: UUID, permissoes: list) -> bool:
        """Verificar se usuário tem todas as permissões necessárias"""
        user_permissions = crud_usuario.get_permissoes_usuario(db, usuario_id)
        return all(perm in user_permissions for perm in permissoes)
    
    def get_user_permissions(self, db: Session, usuario_id: UUID) -> list:
        """Obter todas as permissões do usuário"""
        return crud_usuario.get_permissoes_usuario(db, usuario_id)
    
    def is_admin(self, db: Session, usuario_id: UUID) -> bool:
        """Verificar se usuário é administrador"""
        from core.security import Permissions
        return self.check_permission(db, usuario_id, Permissions.ADMIN_FULL)
    
    def can_access_resource(self, db: Session, usuario_id: UUID, 
                           resource_type: str, action: str) -> bool:
        """Verificar se usuário pode acessar recurso específico"""
        permission_code = f"{resource_type}:{action}"
        return self.check_permission(db, usuario_id, permission_code)


# Instâncias dos serviços
auth_service = AuthService()
authorization_service = AuthorizationService()

