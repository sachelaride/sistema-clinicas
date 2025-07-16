"""
Operações CRUD (Create, Read, Update, Delete) para o modelo Clinica.
"""
from sqlalchemy.orm import Session
from models.clinica import Clinica
from schemas.clinica import ClinicaCreate, ClinicaUpdate
from typing import List, Optional

def get_clinica(db: Session, clinica_id: int) -> Optional[Clinica]:
    """
    Busca uma clínica pelo seu ID.
    """
    return db.query(Clinica).filter(Clinica.id == clinica_id).first()

def get_clinica_by_nome(db: Session, nome: str) -> Optional[Clinica]:
    """
    Busca uma clínica pelo seu nome.
    """
    return db.query(Clinica).filter(Clinica.nome == nome).first()

def get_clinicas(db: Session, skip: int = 0, limit: int = 100) -> List[Clinica]:
    """
    Lista todas as clínicas com paginação.
    """
    return db.query(Clinica).offset(skip).limit(limit).all()

def create_clinica(db: Session, clinica: ClinicaCreate) -> Clinica:
    """
    Cria uma nova clínica no banco de dados.
    """
    db_clinica = Clinica(
        nome=clinica.nome,
        descricao=clinica.descricao,
        ativo=clinica.ativo
    )
    db.add(db_clinica)
    db.commit()
    db.refresh(db_clinica)
    return db_clinica

def update_clinica(db: Session, db_clinica: Clinica, clinica_in: ClinicaUpdate) -> Clinica:
    """
    Atualiza os dados de uma clínica existente.
    """
    update_data = clinica_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_clinica, field, value)
    
    db.add(db_clinica)
    db.commit()
    db.refresh(db_clinica)
    return db_clinica

def delete_clinica(db: Session, clinica_id: int) -> Optional[Clinica]:
    """
    Deleta uma clínica do banco de dados.
    """
    db_clinica = db.query(Clinica).filter(Clinica.id == clinica_id).first()
    if db_clinica:
        db.delete(db_clinica)
        db.commit()
    return db_clinica
