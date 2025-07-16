"""
Endpoints da API para o módulo de Agendamento.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from datetime import datetime

from database.session import get_db
from models.usuario import Usuario
from schemas import agendamento as schemas
from crud import agendamento as crud
from api.dependencies import get_current_user # Assumindo que você tem essa dependência

router = APIRouter(prefix="/agendamento", tags=["Agendamento"])

# Endpoints para Salas
@router.post("/salas", response_model=schemas.Sala)
def create_sala(sala: schemas.SalaCreate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    # Apenas usuários da mesma clínica podem criar salas
    if sala.clinica_id != current_user.clinica_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado a criar sala para outra clínica")
    return crud.create_sala(db=db, sala=sala)

@router.get("/salas/clinica/{clinica_id}", response_model=List[schemas.Sala])
def get_salas(clinica_id: int, db: Session = Depends(get_db)):
    return crud.get_salas_by_clinica(db=db, clinica_id=clinica_id)

# Endpoints para Serviços
@router.post("/servicos", response_model=schemas.Servico)
def create_servico(servico: schemas.ServicoCreate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    if servico.clinica_id != current_user.clinica_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado a criar serviço para outra clínica")
    return crud.create_servico(db=db, servico=servico)

@router.get("/servicos/clinica/{clinica_id}", response_model=List[schemas.Servico])
def get_servicos(clinica_id: int, db: Session = Depends(get_db)):
    return crud.get_servicos_by_clinica(db=db, clinica_id=clinica_id)

# Endpoints para Horarios de Disponibilidade
@router.post("/disponibilidade", response_model=schemas.HorarioDisponibilidade)
def create_horario_disponibilidade(horario: schemas.HorarioDisponibilidadeCreate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    if horario.usuario_id != current_user.usuario_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado a criar horário para outro usuário")
    return crud.create_horario(db=db, horario=horario)

@router.get("/disponibilidade/{usuario_id}", response_model=List[schemas.HorarioDisponibilidade])
def get_horarios_disponibilidade(usuario_id: UUID, db: Session = Depends(get_db)):
    return crud.get_horarios_by_usuario(db=db, usuario_id=usuario_id)

# Endpoints para Agendamentos
@router.post("/", response_model=schemas.Agendamento)
def create_agendamento(agendamento: schemas.AgendamentoCreate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    # O agendamento é criado na clínica do atendente logado
    return crud.create_agendamento(db=db, agendamento=agendamento, criado_por_id=current_user.usuario_id, clinica_id=current_user.clinica_id)

@router.get("/calendario", response_model=List[schemas.Agendamento])
def get_calendario(start: datetime, end: datetime, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    return crud.get_agendamentos_by_periodo(db=db, clinica_id=current_user.clinica_id, start=start, end=end)

@router.put("/{agendamento_id}", response_model=schemas.Agendamento)
def update_agendamento(agendamento_id: UUID, agendamento_in: schemas.AgendamentoUpdate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    db_agendamento = crud.get_agendamento(db, agendamento_id)
    if not db_agendamento or db_agendamento.clinica_id != current_user.clinica_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agendamento não encontrado")
    return crud.update_agendamento(db=db, db_agendamento=db_agendamento, agendamento_in=agendamento_in)
