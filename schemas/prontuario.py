"""
Schemas Pydantic para o módulo de Prontuário Eletrônico.
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Any
from datetime import datetime
from uuid import UUID
from models.prontuario import TipoAnexo

# Schemas para AnexoProntuario
class AnexoProntuarioBase(BaseModel):
    tipo_anexo: TipoAnexo
    descricao: Optional[str] = None

class AnexoProntuarioCreate(AnexoProntuarioBase):
    caminho_arquivo: str

class AnexoProntuario(AnexoProntuarioBase):
    id: UUID
    evolucao_id: UUID
    caminho_arquivo: str
    data_upload: datetime

    class Config:
        orm_mode = True

# Schemas para Evolucao
class EvolucaoBase(BaseModel):
    descricao_clinica: str
    dados_estruturados: Optional[dict] = None

class EvolucaoCreate(EvolucaoBase):
    prontuario_id: UUID
    profissional_id: UUID
    agendamento_id: Optional[UUID] = None

class Evolucao(EvolucaoBase):
    id: UUID
    prontuario_id: UUID
    profissional_id: UUID
    agendamento_id: Optional[UUID] = None
    data_evolucao: datetime
    anexos: List[AnexoProntuario] = []

    class Config:
        orm_mode = True

# Schemas para Prontuario
class ProntuarioBase(BaseModel):
    paciente_id: UUID

class Prontuario(ProntuarioBase):
    id: UUID
    data_abertura: datetime
    ultima_atualizacao: Optional[datetime] = None
    evolucoes: List[Evolucao] = []

    class Config:
        orm_mode = True
