"""
Operações CRUD para o módulo de Prontuário Eletrônico.
"""
from sqlalchemy.orm import Session, joinedload
from models import prontuario as models
from schemas import prontuario as schemas
from typing import List, Optional
from uuid import UUID

# CRUD para Prontuario
def get_prontuario_by_paciente(db: Session, paciente_id: UUID) -> Optional[models.Prontuario]:
    return db.query(models.Prontuario).filter(models.Prontuario.paciente_id == paciente_id).first()

def create_prontuario(db: Session, paciente_id: UUID) -> models.Prontuario:
    db_prontuario = models.Prontuario(paciente_id=paciente_id)
    db.add(db_prontuario)
    db.commit()
    db.refresh(db_prontuario)
    return db_prontuario

# CRUD para Evolucao
def create_evolucao(db: Session, evolucao: schemas.EvolucaoCreate) -> models.Evolucao:
    db_evolucao = models.Evolucao(**evolucao.dict())
    db.add(db_evolucao)
    db.commit()
    db.refresh(db_evolucao)
    return db_evolucao

def get_evolucoes_by_prontuario(db: Session, prontuario_id: UUID) -> List[models.Evolucao]:
    return (
        db.query(models.Evolucao)
        .filter(models.Evolucao.prontuario_id == prontuario_id)
        .order_by(models.Evolucao.data_evolucao.desc())
        .all()
    )

# CRUD para AnexoProntuario
def create_anexo(db: Session, anexo: schemas.AnexoProntuarioCreate, evolucao_id: UUID) -> models.AnexoProntuario:
    db_anexo = models.AnexoProntuario(**anexo.dict(), evolucao_id=evolucao_id)
    db.add(db_anexo)
    db.commit()
    db.refresh(db_anexo)
    return db_anexo
