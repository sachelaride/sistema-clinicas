"""
Modelo de dados para o módulo de Auditoria Centralizada.
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from database.base import Base

class LogAuditoriaGeral(Base):
    """
    Modelo para logs de auditoria centralizados, registrando ações críticas
    em todo o sistema.
    """
    __tablename__ = "logs_auditoria_geral"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    usuario_id = Column(UUID(as_uuid=True), ForeignKey("usuarios.usuario_id"), nullable=True) # Quem realizou a ação
    clinica_id = Column(Integer, ForeignKey("clinicas.id"), nullable=True) # Em qual clínica a ação ocorreu
    
    acao = Column(String(100), nullable=False) # Ex: "CREATE_PACIENTE", "UPDATE_ESTOQUE"
    nome_tabela = Column(String(100), nullable=True) # Tabela afetada (ex: "pacientes", "produtos")
    id_registro_afetado = Column(String(255), nullable=True) # ID do registro afetado (UUID ou INT)
    
    dados_antigos = Column(Text, nullable=True) # JSON string dos dados antes da alteração
    dados_novos = Column(Text, nullable=True) # JSON string dos dados depois da alteração
    
    endereco_ip = Column(String(45), nullable=True) # IP de onde a ação foi realizada
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    usuario = relationship("Usuario")
    clinica = relationship("Clinica")
