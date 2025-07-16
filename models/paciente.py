"""
Modelos SQLAlchemy para o módulo de pacientes
"""
from sqlalchemy import Column, Integer, String, Text, Date, DateTime, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum

from database.base import Base


class SexoEnum(str, enum.Enum):
    """Enum para sexo do paciente"""
    M = "M"
    F = "F"
    O = "O"


class Paciente(Base):
    """Modelo para pacientes"""
    __tablename__ = "pacientes"
    
    paciente_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    nome = Column(String(100), nullable=False, index=True)
    sobrenome = Column(String(100), nullable=False, index=True)
    data_nascimento = Column(Date, nullable=True)
    sexo = Column(String(1), nullable=True)  # Usando String para compatibilidade
    endereco = Column(Text, nullable=True)
    telefone = Column(String(20), nullable=True)
    email = Column(String(100), nullable=True, index=True)
    perfil_epidemiologico = Column(JSONB, nullable=True)
    criado_em = Column(DateTime(timezone=True), server_default=func.now())
    atualizado_em = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relacionamentos
    responsaveis = relationship("ResponsavelLegal", back_populates="paciente", cascade="all, delete-orphan")
    documentos = relationship("DocumentoPaciente", back_populates="paciente", cascade="all, delete-orphan")
    consentimentos = relationship("ConsentimentoPaciente", back_populates="paciente", cascade="all, delete-orphan")
    
    @property
    def nome_completo(self):
        """Propriedade para obter nome completo"""
        return f"{self.nome} {self.sobrenome}".strip()
    
    @property
    def idade(self):
        """Calcula a idade do paciente"""
        if self.data_nascimento:
            from datetime import date
            hoje = date.today()
            return hoje.year - self.data_nascimento.year - (
                (hoje.month, hoje.day) < (self.data_nascimento.month, self.data_nascimento.day)
            )
        return None


class ResponsavelLegal(Base):
    """Modelo para responsáveis legais dos pacientes"""
    __tablename__ = "responsaveis_legais"
    
    responsavel_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    paciente_id = Column(UUID(as_uuid=True), ForeignKey("pacientes.paciente_id"), nullable=False)
    nome = Column(String(150), nullable=False)
    cpf = Column(String(14), nullable=True)
    rg = Column(String(20), nullable=True)
    telefone = Column(String(20), nullable=True)
    email = Column(String(100), nullable=True)
    grau_parentesco = Column(String(50), nullable=True)
    endereco = Column(Text, nullable=True)
    criado_em = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relacionamentos
    paciente = relationship("Paciente", back_populates="responsaveis")


class TipoDocumento(Base):
    """Modelo para tipos de documentos"""
    __tablename__ = "tipos_documentos"
    
    tipo_id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(50), unique=True, nullable=False)
    descricao = Column(Text, nullable=True)
    obrigatorio = Column(Boolean, default=False)
    
    # Relacionamentos
    documentos = relationship("DocumentoPaciente", back_populates="tipo_documento")


class DocumentoPaciente(Base):
    """Modelo para documentos dos pacientes"""
    __tablename__ = "documentos_pacientes"
    
    documento_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    paciente_id = Column(UUID(as_uuid=True), ForeignKey("pacientes.paciente_id"), nullable=False)
    tipo_id = Column(Integer, ForeignKey("tipos_documentos.tipo_id"), nullable=True)
    dados_ocr = Column(Text, nullable=True)
    caminho_arquivo = Column(Text, nullable=False)
    enviado_em = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relacionamentos
    paciente = relationship("Paciente", back_populates="documentos")
    tipo_documento = relationship("TipoDocumento", back_populates="documentos")


class ConsentimentoPaciente(Base):
    """Modelo para consentimentos dos pacientes (LGPD)"""
    __tablename__ = "consentimentos_pacientes"
    
    consentimento_id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(UUID(as_uuid=True), ForeignKey("pacientes.paciente_id"), nullable=False)
    tipo_consentimento = Column(String(50), nullable=False)
    data_consentimento = Column(DateTime(timezone=True), server_default=func.now())
    ativo = Column(Boolean, default=True)
    detalhes = Column(Text, nullable=True)
    
    # Relacionamentos
    paciente = relationship("Paciente", back_populates="consentimentos")

