"""
Operações CRUD para o módulo de Agendamento.
"""
from sqlalchemy.orm import Session
from models import agendamento as models
from schemas import agendamento as schemas
from typing import List, Optional
from uuid import UUID
from datetime import datetime

# CRUD para Sala
def get_sala(db: Session, sala_id: int) -> Optional[models.Sala]:
    return db.query(models.Sala).filter(models.Sala.id == sala_id).first()

def get_salas_by_clinica(db: Session, clinica_id: int) -> List[models.Sala]:
    return db.query(models.Sala).filter(models.Sala.clinica_id == clinica_id).all()

def create_sala(db: Session, sala: schemas.SalaCreate) -> models.Sala:
    db_sala = models.Sala(**sala.dict())
    db.add(db_sala)
    db.commit()
    db.refresh(db_sala)
    return db_sala

# CRUD para Servico
def get_servico(db: Session, servico_id: int) -> Optional[models.Servico]:
    return db.query(models.Servico).filter(models.Servico.id == servico_id).first()

def get_servicos_by_clinica(db: Session, clinica_id: int) -> List[models.Servico]:
    return db.query(models.Servico).filter(models.Servico.clinica_id == clinica_id).all()

def create_servico(db: Session, servico: schemas.ServicoCreate) -> models.Servico:
    db_servico = models.Servico(**servico.dict())
    db.add(db_servico)
    db.commit()
    db.refresh(db_servico)
    return db_servico

# CRUD para HorarioDisponibilidade
def get_horarios_by_usuario(db: Session, usuario_id: UUID) -> List[models.HorarioDisponibilidade]:
    return db.query(models.HorarioDisponibilidade).filter(models.HorarioDisponibilidade.usuario_id == usuario_id).all()

def create_horario(db: Session, horario: schemas.HorarioDisponibilidadeCreate) -> models.HorarioDisponibilidade:
    db_horario = models.HorarioDisponibilidade(**horario.dict())
    db.add(db_horario)
    db.commit()
    db.refresh(db_horario)
    return db_horario

# CRUD para Agendamento
def get_agendamento(db: Session, agendamento_id: UUID) -> Optional[models.Agendamento]:
    return db.query(models.Agendamento).filter(models.Agendamento.id == agendamento_id).first()

def get_agendamentos_by_periodo(
    db: Session, clinica_id: int, start: datetime, end: datetime
) -> List[models.Agendamento]:
    return (
        db.query(models.Agendamento)
        .filter(
            models.Agendamento.clinica_id == clinica_id,
            models.Agendamento.data_hora_inicio < end,
            models.Agendamento.data_hora_fim > start,
        )
        .all()
    )

def create_agendamento(db: Session, agendamento: schemas.AgendamentoCreate, criado_por_id: UUID, clinica_id: int) -> models.Agendamento:
    db_agendamento = models.Agendamento(
        **agendamento.dict(),
        criado_por_id=criado_por_id,
        clinica_id=clinica_id
    )
    db.add(db_agendamento)
    db.commit()
    db.refresh(db_agendamento)
    return db_agendamento

def update_agendamento(db: Session, db_agendamento: models.Agendamento, agendamento_in: schemas.AgendamentoUpdate) -> models.Agendamento:
    update_data = agendamento_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_agendamento, field, value)
    db.commit()
    db.refresh(db_agendamento)
    return db_agendamento
