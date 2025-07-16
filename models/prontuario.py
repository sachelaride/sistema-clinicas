"""
Modelos de dados para o módulo de Prontuário Eletrônico.
"""
from sqlalchemy import (
    Column, Integer, String, Text, DateTime, ForeignKey, Enum
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum

from database.base import Base

class TipoAnexo(str, enum.Enum):
    EXAME_LABORATORIAL = "exame_laboratorial"
    IMAGEM_RAIOX = "imagem_raiox"
    LAUDO_PDF = "laudo_pdf"
    OUTROS = "outros"

class Prontuario(Base):
    """
    Tabela central que representa o prontuário de um paciente.
    """
    __tablename__ = "prontuarios"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    paciente_id = Column(UUID(as_uuid=True), ForeignKey("pacientes.paciente_id"), nullable=False, unique=True)
    data_abertura = Column(DateTime(timezone=True), server_default=func.now())
    ultima_atualizacao = Column(DateTime(timezone=True), onupdate=func.now())

    paciente = relationship("Paciente", back_populates="prontuario")
    evolucoes = relationship("Evolucao", back_populates="prontuario")

class Evolucao(Base):
    """
    Registra uma evolução ou atendimento no prontuário do paciente.
    """
    __tablename__ = "evolucoes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    prontuario_id = Column(UUID(as_uuid=True), ForeignKey("prontuarios.id"), nullable=False)
    agendamento_id = Column(UUID(as_uuid=True), ForeignKey("agendamentos.id"), nullable=True)
    profissional_id = Column(UUID(as_uuid=True), ForeignKey("usuarios.usuario_id"), nullable=False)
    
    data_evolucao = Column(DateTime(timezone=True), server_default=func.now())
    descricao_clinica = Column(Text, nullable=False)
    dados_estruturados = Column(JSONB) # Para dados específicos de cada área (ex: SOAP)

    prontuario = relationship("Prontuario", back_populates="evolucoes")
    profissional = relationship("Usuario")
    agendamento = relationship("Agendamento")
    anexos = relationship("AnexoProntuario", back_populates="evolucao")

class AnexoProntuario(Base):
    """
    Armazena os anexos de uma evolução do prontuário.
    """
    __tablename__ = "anexos_prontuario"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    evolucao_id = Column(UUID(as_uuid=True), ForeignKey("evolucoes.id"), nullable=False)
    tipo_anexo = Column(Enum(TipoAnexo), nullable=False)
    caminho_arquivo = Column(String(255), nullable=False)
    descricao = Column(Text)
    data_upload = Column(DateTime(timezone=True), server_default=func.now())

    evolucao = relationship("Evolucao", back_populates="anexos")

# Adicionar relacionamento inverso em Paciente
from models.paciente import Paciente
Paciente.prontuario = relationship("Prontuario", uselist=False, back_populates="paciente")
