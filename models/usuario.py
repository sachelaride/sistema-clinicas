"""
Modelos SQLAlchemy para o módulo de usuários
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, Table
from sqlalchemy.dialects.postgresql import UUID, BYTEA
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from database.base import Base


# Tabela de associação para perfis e permissões
perfil_permissoes = Table(
    'perfil_permissoes',
    Base.metadata,
    Column('perfil_id', Integer, ForeignKey('perfis.perfil_id'), primary_key=True),
    Column('permissao_id', Integer, ForeignKey('permissoes.permissao_id'), primary_key=True)
)


class Perfil(Base):
    """Modelo para perfis de usuários"""
    __tablename__ = "perfis"
    
    perfil_id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(50), unique=True, nullable=False, index=True)
    
    # Relacionamentos
    usuarios = relationship("Usuario", back_populates="perfil")
    permissoes = relationship("Permissao", secondary=perfil_permissoes, back_populates="perfis")


class Permissao(Base):
    """Modelo para permissões do sistema"""
    __tablename__ = "permissoes"
    
    permissao_id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String(100), unique=True, nullable=False, index=True)
    descricao = Column(Text, nullable=True)
    
    # Relacionamentos
    perfis = relationship("Perfil", secondary=perfil_permissoes, back_populates="permissoes")


class Usuario(Base):
    """Modelo para usuários do sistema"""
    __tablename__ = "usuarios"
    
    usuario_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    nome_usuario = Column(String(50), unique=True, nullable=False, index=True)
    senha_hash = Column(Text, nullable=False)
    perfil_id = Column(Integer, ForeignKey("perfis.perfil_id"), nullable=True)
    clinica_id = Column(Integer, ForeignKey("clinicas.id"), nullable=True) # Adicionado
    nome_completo = Column(String(150), nullable=False)
    email = Column(String(100), nullable=True, index=True)
    telefone = Column(String(20), nullable=True)
    ativo = Column(Boolean, default=True)
    criado_em = Column(DateTime(timezone=True), server_default=func.now())
    atualizado_em = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relacionamentos
    perfil = relationship("Perfil", back_populates="usuarios")
    clinica = relationship("Clinica", back_populates="usuarios") # Adicionado
    perfil_aluno = relationship("PerfilAluno", uselist=False, back_populates="usuario")
    
    @property
    def is_aluno(self):
        """Verifica se o usuário é um aluno"""
        return self.perfil_aluno is not None
    
    @property
    def rgm(self):
        """Retorna o RGM se for aluno"""
        return self.perfil_aluno.rgm if self.perfil_aluno else None


class PerfilAluno(Base):
    """Modelo para perfil específico de alunos"""
    __tablename__ = "perfis_alunos"
    
    usuario_id = Column(UUID(as_uuid=True), ForeignKey("usuarios.usuario_id"), primary_key=True)
    rgm = Column(String(20), unique=True, nullable=False, index=True)
    modelo_biometrico = Column(BYTEA, nullable=True)
    curso = Column(String(100), nullable=True)
    semestre = Column(Integer, nullable=True)
    carga_horaria_total = Column(Integer, default=0)
    
    # Relacionamentos
    usuario = relationship("Usuario", back_populates="perfil_aluno")


class LogAcesso(Base):
    """Modelo para logs de acesso"""
    __tablename__ = "logs_acesso"
    
    log_id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(UUID(as_uuid=True), ForeignKey("usuarios.usuario_id"), nullable=True)
    endereco_ip = Column(String(45), nullable=True)  # IPv6 suporte
    agente_usuario = Column(Text, nullable=True)
    horario_login = Column(DateTime(timezone=True), server_default=func.now())
    sucesso = Column(Boolean, nullable=False)
    motivo_falha = Column(String(100), nullable=True)
    
    # Relacionamentos
    usuario = relationship("Usuario")


class LogAuditoria(Base):
    """Modelo para logs de auditoria"""
    __tablename__ = "logs_auditoria"
    
    auditoria_id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(UUID(as_uuid=True), ForeignKey("usuarios.usuario_id"), nullable=True)
    acao = Column(String(50), nullable=False)
    nome_tabela = Column(String(100), nullable=True)
    id_registro = Column(Text, nullable=True)
    horario_acao = Column(DateTime(timezone=True), server_default=func.now())
    dados_antigos = Column(Text, nullable=True)  # JSON como texto para compatibilidade
    dados_novos = Column(Text, nullable=True)   # JSON como texto para compatibilidade
    endereco_ip = Column(String(45), nullable=True)
    
    # Relacionamentos
    usuario = relationship("Usuario")

