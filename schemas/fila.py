"""
Schemas Pydantic para o módulo de Gestão de Filas.
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID
from models.fila import StatusFila, PrioridadeFila

# Schemas para GuicheAtendimento
class GuicheAtendimentoBase(BaseModel):
    nome: str
    descricao: Optional[str] = None
    ativo: bool = True

class GuicheAtendimentoCreate(GuicheAtendimentoBase):
    clinica_id: int

class GuicheAtendimentoUpdate(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None
    ativo: Optional[bool] = None

class GuicheAtendimento(GuicheAtendimentoBase):
    id: int
    clinica_id: int

    class Config:
        orm_mode = True

# Schemas para FilaEspera
class FilaEsperaBase(BaseModel):
    paciente_id: UUID
    servico_id: Optional[int] = None
    prioridade: PrioridadeFila = PrioridadeFila.NORMAL

class FilaEsperaCreate(FilaEsperaBase):
    clinica_id: int

class FilaEsperaUpdate(BaseModel):
    status: Optional[StatusFila] = None
    prioridade: Optional[PrioridadeFila] = None
    guiche_id: Optional[int] = None
    chamado_por_usuario_id: Optional[UUID] = None

class FilaEspera(FilaEsperaBase):
    id: UUID
    clinica_id: int
    status: StatusFila
    hora_chegada: datetime
    hora_chamada: Optional[datetime] = None
    hora_atendimento_inicio: Optional[datetime] = None
    hora_atendimento_fim: Optional[datetime] = None
    guiche_id: Optional[int] = None
    chamado_por_usuario_id: Optional[UUID] = None

    class Config:
        orm_mode = True
