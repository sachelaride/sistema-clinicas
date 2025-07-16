"""
Módulo de segurança para autenticação e autorização
"""
from datetime import datetime, timedelta
from typing import Optional, Union
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status

from config.settings import settings


# Configuração do contexto de criptografia
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configurações JWT
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verificar se a senha está correta"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Gerar hash da senha"""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Criar token JWT de acesso"""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> Optional[dict]:
    """Verificar e decodificar token JWT"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


def create_token_response(usuario_id: str, nome_usuario: str, perfil_id: Optional[int] = None) -> dict:
    """Criar resposta de token de autenticação"""
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    token_data = {
        "sub": str(usuario_id),
        "username": nome_usuario,
        "perfil_id": perfil_id
    }
    
    access_token = create_access_token(
        data=token_data,
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }


class SecurityUtils:
    """Utilitários de segurança"""
    
    @staticmethod
    def validate_password_strength(password: str) -> bool:
        """Validar força da senha"""
        if len(password) < 6:
            return False
        
        # Pelo menos uma letra e um número
        has_letter = any(c.isalpha() for c in password)
        has_digit = any(c.isdigit() for c in password)
        
        return has_letter and has_digit
    
    @staticmethod
    def generate_temp_password(length: int = 8) -> str:
        """Gerar senha temporária"""
        import random
        import string
        
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(length))
    
    @staticmethod
    def is_safe_redirect_url(url: str) -> bool:
        """Verificar se URL de redirecionamento é segura"""
        # Implementação básica - pode ser expandida
        if not url:
            return False
        
        # Não permitir URLs externas
        if url.startswith(('http://', 'https://', '//')):
            return False
        
        # Deve começar com /
        return url.startswith('/')


class PermissionChecker:
    """Verificador de permissões"""
    
    def __init__(self, required_permissions: list):
        self.required_permissions = required_permissions
    
    def __call__(self, user_permissions: list) -> bool:
        """Verificar se usuário tem as permissões necessárias"""
        return all(perm in user_permissions for perm in self.required_permissions)


# Constantes de permissões
class Permissions:
    """Constantes de permissões do sistema"""
    
    # Pacientes
    PACIENTE_CREATE = "paciente:create"
    PACIENTE_READ = "paciente:read"
    PACIENTE_UPDATE = "paciente:update"
    PACIENTE_DELETE = "paciente:delete"
    
    # Usuários
    USUARIO_CREATE = "usuario:create"
    USUARIO_READ = "usuario:read"
    USUARIO_UPDATE = "usuario:update"
    USUARIO_DELETE = "usuario:delete"
    
    # Estoque
    ESTOQUE_CREATE = "estoque:create"
    ESTOQUE_READ = "estoque:read"
    ESTOQUE_UPDATE = "estoque:update"
    ESTOQUE_DELETE = "estoque:delete"
    
    # Relatórios
    RELATORIO_READ = "relatorio:read"
    RELATORIO_EXPORT = "relatorio:export"
    
    # Administração
    ADMIN_FULL = "admin:full"
    ADMIN_USERS = "admin:users"
    ADMIN_SYSTEM = "admin:system"
    
    # Logs e auditoria
    LOG_READ = "log:read"
    AUDITORIA_READ = "auditoria:read"


# Exceções customizadas
class AuthenticationError(HTTPException):
    """Erro de autenticação"""
    def __init__(self, detail: str = "Não foi possível validar as credenciais"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )


class AuthorizationError(HTTPException):
    """Erro de autorização"""
    def __init__(self, detail: str = "Permissões insuficientes"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
        )


class AccountLockedError(HTTPException):
    """Erro de conta bloqueada"""
    def __init__(self, detail: str = "Conta temporariamente bloqueada"):
        super().__init__(
            status_code=status.HTTP_423_LOCKED,
            detail=detail,
        )

