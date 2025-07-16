"""
Schemas Pydantic para o módulo de usuários
"""
from typing import Optional, List
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field, EmailStr, validator


from schemas.clinica import Clinica


# Schemas para Perfil
class PerfilBase(BaseModel):
    """Schema base para perfil"""
    nome: str = Field(..., min_length=1, max_length=50, description="Nome do perfil")


class PerfilCreate(PerfilBase):
    """Schema para criação de perfil"""
    pass


class Perfil(PerfilBase):
    """Schema de resposta para perfil"""
    perfil_id: int
    
    class Config:
        from_attributes = True


# Schemas para Permissao
class PermissaoBase(BaseModel):
    """Schema base para permissão"""
    codigo: str = Field(..., min_length=1, max_length=100, description="Código da permissão")
    descricao: Optional[str] = Field(None, description="Descrição da permissão")


class PermissaoCreate(PermissaoBase):
    """Schema para criação de permissão"""
    pass


class Permissao(PermissaoBase):
    """Schema de resposta para permissão"""
    permissao_id: int
    
    class Config:
        from_attributes = True


# Schemas para PerfilAluno
class PerfilAlunoBase(BaseModel):
    """Schema base para perfil de aluno"""
    rgm: str = Field(..., min_length=1, max_length=20, description="RGM do aluno")
    curso: Optional[str] = Field(None, max_length=100, description="Curso do aluno")
    semestre: Optional[int] = Field(None, ge=1, le=20, description="Semestre atual")
    carga_horaria_total: Optional[int] = Field(0, ge=0, description="Carga horária total")


class PerfilAlunoCreate(PerfilAlunoBase):
    """Schema para criação de perfil de aluno"""
    pass


class PerfilAlunoUpdate(BaseModel):
    """Schema para atualização de perfil de aluno"""
    curso: Optional[str] = Field(None, max_length=100)
    semestre: Optional[int] = Field(None, ge=1, le=20)
    carga_horaria_total: Optional[int] = Field(None, ge=0)


class PerfilAluno(PerfilAlunoBase):
    """Schema de resposta para perfil de aluno"""
    usuario_id: UUID
    
    class Config:
        from_attributes = True


# Schema de resumo da Clínica para ser embutido no usuário
class ClinicaResumo(BaseModel):
    id: int
    nome: str

    class Config:
        from_attributes = True


# Schemas para Usuario
class UsuarioBase(BaseModel):
    """Schema base para usuário"""
    nome_usuario: str = Field(..., min_length=3, max_length=50, description="Nome de usuário")
    nome_completo: str = Field(..., min_length=1, max_length=150, description="Nome completo")
    email: Optional[EmailStr] = Field(None, description="Email do usuário")
    telefone: Optional[str] = Field(None, max_length=20, description="Telefone do usuário")
    perfil_id: Optional[int] = Field(None, description="ID do perfil")
    clinica_id: Optional[int] = Field(None, description="ID da clínica à qual o usuário pertence")
    ativo: bool = Field(True, description="Se o usuário está ativo")


class UsuarioCreate(UsuarioBase):
    """Schema para criação de usuário"""
    senha: str = Field(..., min_length=6, description="Senha do usuário")
    perfil_aluno: Optional[PerfilAlunoCreate] = Field(None, description="Dados do perfil de aluno")
    
    @validator('nome_usuario')
    def validar_nome_usuario(cls, v):
        if not v.replace('_', '').replace('.', '').isalnum():
            raise ValueError('Nome de usuário deve conter apenas letras, números, _ e .')
        return v.lower()


class UsuarioUpdate(BaseModel):
    """Schema para atualização de usuário"""
    nome_completo: Optional[str] = Field(None, min_length=1, max_length=150)
    email: Optional[EmailStr] = None
    telefone: Optional[str] = Field(None, max_length=20)
    perfil_id: Optional[int] = None
    clinica_id: Optional[int] = None
    ativo: Optional[bool] = None


class UsuarioUpdateSenha(BaseModel):
    """Schema para atualização de senha"""
    senha_atual: str = Field(..., description="Senha atual")
    nova_senha: str = Field(..., min_length=6, description="Nova senha")
    confirmar_senha: str = Field(..., description="Confirmação da nova senha")
    
    @validator('confirmar_senha')
    def senhas_devem_coincidir(cls, v, values):
        if 'nova_senha' in values and v != values['nova_senha']:
            raise ValueError('Senhas não coincidem')
        return v


class Usuario(UsuarioBase):
    """Schema de resposta para usuário"""
    usuario_id: UUID
    criado_em: datetime
    atualizado_em: datetime
    
    # Relacionamentos
    perfil: Optional[Perfil] = None
    perfil_aluno: Optional[PerfilAluno] = None
    clinica: Optional[ClinicaResumo] = None
    
    class Config:
        from_attributes = True


# Schemas para autenticação
class LoginRequest(BaseModel):
    """Schema para requisição de login"""
    nome_usuario: str = Field(..., description="Nome de usuário ou RGM")
    senha: str = Field(..., description="Senha do usuário")


class LoginResponse(BaseModel):
    """Schema para resposta de login"""
    access_token: str = Field(..., description="Token de acesso JWT")
    token_type: str = Field("bearer", description="Tipo do token")
    expires_in: int = Field(..., description="Tempo de expiração em segundos")
    usuario: Usuario = Field(..., description="Dados do usuário logado")


class TokenData(BaseModel):
    """Schema para dados do token"""
    usuario_id: Optional[UUID] = None
    nome_usuario: Optional[str] = None
    perfil_id: Optional[int] = None


# Schemas para logs
class LogAcessoBase(BaseModel):
    """Schema base para log de acesso"""
    endereco_ip: Optional[str] = Field(None, description="Endereço IP")
    agente_usuario: Optional[str] = Field(None, description="User Agent")
    sucesso: bool = Field(..., description="Se o login foi bem-sucedido")
    motivo_falha: Optional[str] = Field(None, description="Motivo da falha")


class LogAcesso(LogAcessoBase):
    """Schema de resposta para log de acesso"""
    log_id: int
    usuario_id: Optional[UUID]
    horario_login: datetime
    
    class Config:
        from_attributes = True


class LogAuditoriaBase(BaseModel):
    """Schema base para log de auditoria"""
    acao: str = Field(..., max_length=50, description="Ação realizada")
    nome_tabela: Optional[str] = Field(None, max_length=100, description="Tabela afetada")
    id_registro: Optional[str] = Field(None, description="ID do registro afetado")
    dados_antigos: Optional[str] = Field(None, description="Dados antes da alteração")
    dados_novos: Optional[str] = Field(None, description="Dados após a alteração")
    endereco_ip: Optional[str] = Field(None, description="Endereço IP")


class LogAuditoria(LogAuditoriaBase):
    """Schema de resposta para log de auditoria"""
    auditoria_id: int
    usuario_id: Optional[UUID]
    horario_acao: datetime
    
    class Config:
        from_attributes = True


# Schemas para respostas completas
class UsuarioCompleto(Usuario):
    """Schema completo do usuário com relacionamentos"""
    permissoes: List[str] = Field([], description="Lista de códigos de permissões")
    
    class Config:
        from_attributes = True


# Schemas para filtros e buscas
class UsuarioFiltro(BaseModel):
    """Schema para filtros de busca de usuários"""
    nome: Optional[str] = Field(None, description="Buscar por nome")
    email: Optional[str] = Field(None, description="Buscar por email")
    perfil_id: Optional[int] = Field(None, description="Filtrar por perfil")
    clinica_id: Optional[int] = Field(None, description="Filtrar por clínica")
    ativo: Optional[bool] = Field(None, description="Filtrar por status ativo")
    is_aluno: Optional[bool] = Field(None, description="Filtrar apenas alunos")


class UsuarioResumo(BaseModel):
    """Schema resumido do usuário para listagens"""
    usuario_id: UUID
    nome_usuario: str
    nome_completo: str
    email: Optional[str]
    perfil_nome: Optional[str]
    clinica_nome: Optional[str] = None
    ativo: bool
    is_aluno: bool
    rgm: Optional[str]
    
    class Config:
        from_attributes = True


# Schemas para estatísticas
class EstatisticasUsuarios(BaseModel):
    """Schema para estatísticas de usuários"""
    total_usuarios: int
    usuarios_ativos: int
    usuarios_por_perfil: dict
    total_alunos: int
    novos_usuarios_mes: int
    ultimo_login_usuarios: dict

