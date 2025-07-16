"""
Modelos de dados para o módulo de Gestão de Filas.
"""
import enum
from sqlalchemy import (
    Column, Integer, String, Text, DateTime, ForeignKey, Enum, Boolean
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from database.base import Base

class StatusFila(str, enum.Enum):
    AGUARDANDO = "aguardando"
    EM_ATENDIMENTO = "em_atendimento"
    ATENDIDO = "atendido"
    CANCELADO = "cancelado"
    NAO_COMPARECEU = "nao_compareceu"

class PrioridadeFila(str, enum.Enum):
    NORMAL = "normal"
    PRIORITARIO = "prioritario"
    EMERGENCIA = "emergencia"

class GuicheAtendimento(Base):
    """
    Representa um guichê ou local de atendimento onde pacientes podem ser chamados.
    """
    __tablename__ = "guiches_atendimento"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    clinica_id = Column(Integer, ForeignKey("clinicas.id"), nullable=False)
    descricao = Column(Text)
    ativo = Column(Boolean, default=True)

    clinica = relationship("Clinica")
    # Relacionamento inverso para fila_espera, se necessário

class FilaEspera(Base):
    """
    Representa um paciente na fila de espera para um serviço específico.
    """
    __tablename__ = "filas_espera"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    paciente_id = Column(UUID(as_uuid=True), ForeignKey("pacientes.paciente_id"), nullable=False)
    clinica_id = Column(Integer, ForeignKey("clinicas.id"), nullable=False)
    servico_id = Column(Integer, ForeignKey("servicos.id"), nullable=True) # Opcional, se a fila for geral
    
    status = Column(Enum(StatusFila), default=StatusFila.AGUARDANDO, nullable=False)
    prioridade = Column(Enum(PrioridadeFila), default=PrioridadeFila.NORMAL, nullable=False)
    
    hora_chegada = Column(DateTime(timezone=True), server_default=func.now())
    hora_chamada = Column(DateTime(timezone=True), nullable=True)
    hora_atendimento_inicio = Column(DateTime(timezone=True), nullable=True)
    hora_atendimento_fim = Column(DateTime(timezone=True), nullable=True)
    
    guiche_id = Column(Integer, ForeignKey("guiches_atendimento.id"), nullable=True)
    chamado_por_usuario_id = Column(UUID(as_uuid=True), ForeignKey("usuarios.usuario_id"), nullable=True)

    paciente = relationship("Paciente")
    clinica = relationship("Clinica")
    servico = relationship("Servico")
    guiche = relationship("GuicheAtendimento")
    chamado_por = relationship("Usuario")
