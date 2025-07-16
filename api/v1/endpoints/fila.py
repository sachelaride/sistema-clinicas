"""
Endpoints da API para o módulo de Gestão de Filas.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from database.session import get_db
from models.usuario import Usuario
from schemas import fila as schemas
from crud import fila as crud
from api.dependencies import get_current_user # Assumindo que você tem essa dependência

router = APIRouter(prefix="/fila", tags=["Gestão de Filas"])

# Endpoints para Guiches de Atendimento
@router.post("/guiches", response_model=schemas.GuicheAtendimento)
def create_guiche(guiche: schemas.GuicheAtendimentoCreate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    """Cria um novo guichê de atendimento."""
    # Apenas usuários da mesma clínica podem criar guichês
    if guiche.clinica_id != current_user.clinica_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado a criar guichê para outra clínica")
    return crud.create_guiche(db=db, guiche=guiche)

@router.get("/guiches/clinica/{clinica_id}", response_model=List[schemas.GuicheAtendimento])
def get_guiches(clinica_id: int, db: Session = Depends(get_db)):
    """Lista todos os guichês de atendimento de uma clínica."""
    return crud.get_guiches_by_clinica(db=db, clinica_id=clinica_id)

# Endpoints para Fila de Espera
@router.post("/entrada", response_model=schemas.FilaEspera)
def add_to_fila(
    fila_data: schemas.FilaEsperaBase,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Adiciona um paciente à fila de espera da clínica do usuário logado."""
    # O paciente é adicionado à fila da clínica do atendente logado
    fila_create = schemas.FilaEsperaCreate(
        paciente_id=fila_data.paciente_id,
        servico_id=fila_data.servico_id,
        prioridade=fila_data.prioridade,
        clinica_id=current_user.clinica_id # Associa à clínica do usuário logado
    )
    return crud.create_fila_espera(db=db, fila_data=fila_create)

@router.get("/clinica/{clinica_id}", response_model=List[schemas.FilaEspera])
def get_fila_clinica(
    clinica_id: int,
    db: Session = Depends(get_db),
    status: Optional[schemas.StatusFila] = None
):
    """Lista a fila de espera de uma clínica, opcionalmente filtrando por status."""
    return crud.get_fila_espera_by_clinica(db=db, clinica_id=clinica_id, status=status)

@router.post("/chamar-proximo", response_model=Optional[schemas.FilaEspera])
def chamar_proximo(
    guiche_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Chama o próximo paciente da fila de espera para um guichê específico."""
    # Verifica se o guichê pertence à clínica do usuário logado
    guiche = crud.get_guiche(db, guiche_id)
    if not guiche or guiche.clinica_id != current_user.clinica_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Guichê não encontrado ou não pertence à sua clínica")

    paciente_chamado = crud.chamar_proximo_fila(
        db=db,
        clinica_id=current_user.clinica_id,
        guiche_id=guiche_id,
        chamado_por_usuario_id=current_user.usuario_id
    )
    if not paciente_chamado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nenhum paciente aguardando na fila.")
    return paciente_chamado

@router.patch("/{fila_id}/status", response_model=schemas.FilaEspera)
def update_fila_status(
    fila_id: UUID,
    status_update: schemas.FilaEsperaUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Atualiza o status de um item na fila (ex: atendido, cancelado)."""
    db_fila = crud.get_fila_espera(db, fila_id)
    if not db_fila or db_fila.clinica_id != current_user.clinica_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item da fila não encontrado ou não pertence à sua clínica")
    
    return crud.update_fila_espera(db=db, db_fila=db_fila, fila_in=status_update)
