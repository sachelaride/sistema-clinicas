"""
Schemas Pydantic para o módulo de Agendamento.
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, time
from uuid import UUID
from models.agendamento import StatusAgendamento, DiaSemana

# Schemas para Sala
class SalaBase(BaseModel):
    nome: str
    tipo: Optional[str] = None
    ativa: bool = True

class SalaCreate(SalaBase):
    clinica_id: int

class SalaUpdate(BaseModel):
    nome: Optional[str] = None
    tipo: Optional[str] = None
    ativa: Optional[bool] = None

class Sala(SalaBase):
    id: int
    clinica_id: int

    class Config:
        orm_mode = True

# Schemas para Servico
class ServicoBase(BaseModel):
    nome: str
    duracao_media_minutos: int
    descricao: Optional[str] = None
    ativo: bool = True

class ServicoCreate(ServicoBase):
    clinica_id: int

class ServicoUpdate(BaseModel):
    nome: Optional[str] = None
    duracao_media_minutos: Optional[int] = None
    descricao: Optional[str] = None
    ativo: Optional[bool] = None

class Servico(ServicoBase):
    id: int
    clinica_id: int

    class Config:
        orm_mode = True

# Schemas para HorarioDisponibilidade
class HorarioDisponibilidadeBase(BaseModel):
    dia_semana: DiaSemana
    hora_inicio: time
    hora_fim: time

class HorarioDisponibilidadeCreate(HorarioDisponibilidadeBase):
    usuario_id: UUID

class HorarioDisponibilidade(HorarioDisponibilidadeBase):
    id: int
    usuario_id: UUID

    class Config:
        orm_mode = True

# Schemas para Agendamento
class AgendamentoBase(BaseModel):
    paciente_id: UUID
    profissional_id: UUID
    sala_id: int
    servico_id: int
    data_hora_inicio: datetime
    data_hora_fim: datetime
    observacoes: Optional[str] = None

class AgendamentoCreate(AgendamentoBase):
    pass

class AgendamentoUpdate(BaseModel):
    paciente_id: Optional[UUID] = None
    profissional_id: Optional[UUID] = None
    sala_id: Optional[int] = None
    servico_id: Optional[int] = None
    data_hora_inicio: Optional[datetime] = None
    data_hora_fim: Optional[datetime] = None
    status: Optional[StatusAgendamento] = None
    observacoes: Optional[str] = None

class Agendamento(AgendamentoBase):
    id: UUID
    clinica_id: int
    status: StatusAgendamento
    criado_em: datetime
    atualizado_em: Optional[datetime] = None
    criado_por_id: Optional[UUID] = None

    class Config:
        orm_mode = True
