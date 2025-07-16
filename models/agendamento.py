"""
Modelos de dados para o módulo de Agendamento.
"""
import enum
from sqlalchemy import (
    Column, Integer, String, Text, DateTime, ForeignKey, Time, Enum, Boolean
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from database.base import Base

class StatusAgendamento(str, enum.Enum):
    AGENDADO = "agendado"
    CONFIRMADO = "confirmado"
    CANCELADO_PACIENTE = "cancelado_paciente"
    CANCELADO_CLINICA = "cancelado_clinica"
    REALIZADO = "realizado"
    AUSENTE = "ausente"

class DiaSemana(str, enum.Enum):
    SEGUNDA = "segunda"
    TERCA = "terca"
    QUARTA = "quarta"
    QUINTA = "quinta"
    SEXTA = "sexta"
    SABADO = "sabado"
    DOMINGO = "domingo"

class Sala(Base):
    __tablename__ = "salas"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    clinica_id = Column(Integer, ForeignKey("clinicas.id"), nullable=False)
    tipo = Column(String(50)) # Ex: Consultório, Cadeira Odontológica
    ativa = Column(Boolean, default=True)

    clinica = relationship("Clinica")
    agendamentos = relationship("Agendamento", back_populates="sala")

class Servico(Base):
    __tablename__ = "servicos"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    clinica_id = Column(Integer, ForeignKey("clinicas.id"), nullable=False)
    duracao_media_minutos = Column(Integer, nullable=False)
    descricao = Column(Text)
    ativo = Column(Boolean, default=True)

    clinica = relationship("Clinica")
    agendamentos = relationship("Agendamento", back_populates="servico")

class HorarioDisponibilidade(Base):
    __tablename__ = "horarios_disponibilidade"
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(UUID(as_uuid=True), ForeignKey("usuarios.usuario_id"), nullable=False)
    dia_semana = Column(Enum(DiaSemana), nullable=False)
    hora_inicio = Column(Time, nullable=False)
    hora_fim = Column(Time, nullable=False)

    usuario = relationship("Usuario")

class Agendamento(Base):
    __tablename__ = "agendamentos"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    paciente_id = Column(UUID(as_uuid=True), ForeignKey("pacientes.paciente_id"), nullable=False)
    profissional_id = Column(UUID(as_uuid=True), ForeignKey("usuarios.usuario_id"), nullable=False)
    sala_id = Column(Integer, ForeignKey("salas.id"), nullable=False)
    servico_id = Column(Integer, ForeignKey("servicos.id"), nullable=False)
    clinica_id = Column(Integer, ForeignKey("clinicas.id"), nullable=False)
    
    data_hora_inicio = Column(DateTime(timezone=True), nullable=False)
    data_hora_fim = Column(DateTime(timezone=True), nullable=False)
    
    status = Column(Enum(StatusAgendamento), default=StatusAgendamento.AGENDADO, nullable=False)
    observacoes = Column(Text)
    
    criado_por_id = Column(UUID(as_uuid=True), ForeignKey("usuarios.usuario_id"))
    criado_em = Column(DateTime(timezone=True), server_default=func.now())
    atualizado_em = Column(DateTime(timezone=True), onupdate=func.now())

    paciente = relationship("Paciente")
    profissional = relationship("Usuario", foreign_keys=[profissional_id])
    criado_por = relationship("Usuario", foreign_keys=[criado_por_id])
    sala = relationship("Sala", back_populates="agendamentos")
    servico = relationship("Servico", back_populates="agendamentos")
    clinica = relationship("Clinica")
