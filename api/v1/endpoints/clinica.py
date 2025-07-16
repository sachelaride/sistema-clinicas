"""
Endpoints da API para o gerenciamento de Clínicas.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database.session import get_db
from schemas.clinica import Clinica, ClinicaCreate, ClinicaUpdate
from crud import clinica as crud_clinica
# Supondo que você terá um sistema de dependências para autenticação e autorização
# from api.dependencies import get_current_active_admin_user

router = APIRouter(
    prefix="/clinicas",
    tags=["Clínicas"],
    # dependencies=[Depends(get_current_active_admin_user)] # Proteger todos os endpoints
)

@router.post("/", response_model=Clinica, status_code=status.HTTP_201_CREATED)
def create_clinica(clinica: ClinicaCreate, db: Session = Depends(get_db)):
    """
    Cria uma nova clínica.
    
    - **nome**: Nome único da clínica.
    - **descricao**: Descrição opcional.
    - **ativo**: Define se a clínica está ativa.
    """
    db_clinica = crud_clinica.get_clinica_by_nome(db, nome=clinica.nome)
    if db_clinica:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uma clínica com este nome já existe."
        )
    return crud_clinica.create_clinica(db=db, clinica=clinica)

@router.get("/", response_model=List[Clinica])
def read_clinicas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Lista todas as clínicas cadastradas.
    """
    clinicas = crud_clinica.get_clinicas(db, skip=skip, limit=limit)
    return clinicas

@router.get("/{clinica_id}", response_model=Clinica)
def read_clinica(clinica_id: int, db: Session = Depends(get_db)):
    """
    Obtém os detalhes de uma clínica específica pelo seu ID.
    """
    db_clinica = crud_clinica.get_clinica(db, clinica_id=clinica_id)
    if db_clinica is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Clínica não encontrada")
    return db_clinica

@router.put("/{clinica_id}", response_model=Clinica)
def update_clinica(clinica_id: int, clinica_in: ClinicaUpdate, db: Session = Depends(get_db)):
    """
    Atualiza os dados de uma clínica.
    """
    db_clinica = crud_clinica.get_clinica(db, clinica_id=clinica_id)
    if db_clinica is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Clínica não encontrada")
    
    # Verifica se o novo nome já está em uso por outra clínica
    if clinica_in.nome and clinica_in.nome != db_clinica.nome:
        existing_clinica = crud_clinica.get_clinica_by_nome(db, nome=clinica_in.nome)
        if existing_clinica:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Uma clínica com este nome já existe."
            )

    return crud_clinica.update_clinica(db=db, db_clinica=db_clinica, clinica_in=clinica_in)

@router.delete("/{clinica_id}", response_model=Clinica)
def delete_clinica(clinica_id: int, db: Session = Depends(get_db)):
    """
    Deleta uma clínica.
    
    (Nota: Em um sistema real, talvez seja melhor desativar a clínica em vez de deletar,
    para manter a integridade dos dados históricos.)
    """
    db_clinica = crud_clinica.delete_clinica(db, clinica_id=clinica_id)
    if db_clinica is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Clínica não encontrada")
    return db_clinica
