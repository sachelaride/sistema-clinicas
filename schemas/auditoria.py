"""
Schemas Pydantic para o módulo de Auditoria Centralizada.
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID

class LogAuditoriaGeralBase(BaseModel):
    usuario_id: Optional[UUID] = None
    clinica_id: Optional[int] = None
    acao: str = Field(..., max_length=100)
    nome_tabela: Optional[str] = Field(None, max_length=100)
    id_registro_afetado: Optional[str] = Field(None, max_length=255)
    dados_antigos: Optional[str] = None # JSON string
    dados_novos: Optional[str] = None # JSON string
    endereco_ip: Optional[str] = Field(None, max_length=45)

class LogAuditoriaGeralCreate(LogAuditoriaGeralBase):
    pass

class LogAuditoriaGeral(LogAuditoriaGeralBase):
    id: UUID
    timestamp: datetime

    class Config:
        orm_mode = True
