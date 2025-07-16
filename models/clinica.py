"""
Modelo de dados para a tabela de Clínicas.
"""
from sqlalchemy import Column, Integer, String, Boolean, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database.base import Base

class Clinica(Base):
    """
    Representa uma clínica no sistema.
    Cada clínica é uma entidade separada com seus próprios usuários,
    pacientes e agendamentos.
    """
    __tablename__ = "clinicas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False, unique=True, index=True)
    descricao = Column(Text)
    ativo = Column(Boolean, default=True)

    # Relacionamentos inversos
    # A lista de usuários associados a esta clínica
    usuarios = relationship("Usuario", back_populates="clinica")
    
    # Adicionar outros relacionamentos conforme necessário
    # por exemplo, salas, serviços, etc.
    # salas = relationship("Sala", back_populates="clinica")
    # servicos = relationship("Servico", back_populates="clinica")

    def __repr__(self):
        return f"<Clinica(id={self.id}, nome='{self.nome}')>"
