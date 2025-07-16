"""
Operações CRUD para o módulo de Gestão de Filas.
"""
from sqlalchemy.orm import Session
from models import fila as models
from schemas import fila as schemas
from typing import List, Optional
from uuid import UUID
from datetime import datetime

# CRUD para GuicheAtendimento
def get_guiche(db: Session, guiche_id: int) -> Optional[models.GuicheAtendimento]:
    return db.query(models.GuicheAtendimento).filter(models.GuicheAtendimento.id == guiche_id).first()

def get_guiches_by_clinica(db: Session, clinica_id: int) -> List[models.GuicheAtendimento]:
    return db.query(models.GuicheAtendimento).filter(models.GuicheAtendimento.clinica_id == clinica_id).all()

def create_guiche(db: Session, guiche: schemas.GuicheAtendimentoCreate) -> models.GuicheAtendimento:
    db_guiche = models.GuicheAtendimento(**guiche.dict())
    db.add(db_guiche)
    db.commit()
    db.refresh(db_guiche)
    return db_guiche

# CRUD para FilaEspera
def get_fila_espera(db: Session, fila_id: UUID) -> Optional[models.FilaEspera]:
    return db.query(models.FilaEspera).filter(models.FilaEspera.id == fila_id).first()

def get_fila_espera_by_clinica(
    db: Session, clinica_id: int, status: Optional[models.StatusFila] = None
) -> List[models.FilaEspera]:
    query = db.query(models.FilaEspera).filter(models.FilaEspera.clinica_id == clinica_id)
    if status:
        query = query.filter(models.FilaEspera.status == status)
    return query.order_by(models.FilaEspera.prioridade.desc(), models.FilaEspera.hora_chegada.asc()).all()

def create_fila_espera(db: Session, fila_data: schemas.FilaEsperaCreate) -> models.FilaEspera:
    db_fila = models.FilaEspera(**fila_data.dict())
    db.add(db_fila)
    db.commit()
    db.refresh(db_fila)
    return db_fila

def update_fila_espera(db: Session, db_fila: models.FilaEspera, fila_in: schemas.FilaEsperaUpdate) -> models.FilaEspera:
    update_data = fila_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_fila, field, value)
    db.commit()
    db.refresh(db_fila)
    return db_fila

def chamar_proximo_fila(
    db: Session, clinica_id: int, guiche_id: int, chamado_por_usuario_id: UUID
) -> Optional[models.FilaEspera]:
    # Busca o próximo paciente na fila com base na prioridade e hora de chegada
    proximo_paciente = (
        db.query(models.FilaEspera)
        .filter(
            models.FilaEspera.clinica_id == clinica_id,
            models.FilaEspera.status == models.StatusFila.AGUARDANDO
        )
        .order_by(models.FilaEspera.prioridade.desc(), models.FilaEspera.hora_chegada.asc())
        .first()
    )

    if proximo_paciente:
        proximo_paciente.status = models.StatusFila.EM_ATENDIMENTO
        proximo_paciente.guiche_id = guiche_id
        proximo_paciente.chamado_por_usuario_id = chamado_por_usuario_id
        proximo_paciente.hora_chamada = datetime.now()
        db.commit()
        db.refresh(proximo_paciente)
    return proximo_paciente
