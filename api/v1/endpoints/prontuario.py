"""
Endpoints da API para o módulo de Prontuário Eletrônico.
"""
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
import shutil

from database.session import get_db
from models.usuario import Usuario
from schemas import prontuario as schemas
from crud import prontuario as crud
from api.dependencies import get_current_user

router = APIRouter(prefix="/prontuarios", tags=["Prontuário Eletrônico"])

@router.get("/paciente/{paciente_id}", response_model=schemas.Prontuario)
def get_prontuario_paciente(paciente_id: UUID, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    """Obtém ou cria o prontuário de um paciente."""
    db_prontuario = crud.get_prontuario_by_paciente(db, paciente_id)
    if not db_prontuario:
        # Aqui você pode querer verificar se o paciente existe antes de criar
        db_prontuario = crud.create_prontuario(db, paciente_id)
    return db_prontuario

@router.post("/evolucoes", response_model=schemas.Evolucao)

def create_evolucao(evolucao: schemas.EvolucaoCreate, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    """Adiciona uma nova evolução a um prontuário."""
    # Validar se o profissional logado é o mesmo da evolução
    if evolucao.profissional_id != current_user.usuario_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado a criar evolução para outro profissional")
    return crud.create_evolucao(db, evolucao)

@router.get("/{prontuario_id}/evolucoes", response_model=List[schemas.Evolucao])
def get_evolucoes(prontuario_id: UUID, db: Session = Depends(get_db), current_user: Usuario = Depends(get_current_user)):
    """Lista todas as evoluções de um prontuário."""
    return crud.get_evolucoes_by_prontuario(db, prontuario_id)

@router.post("/evolucoes/{evolucao_id}/anexos", response_model=schemas.AnexoProntuario)
async def upload_anexo(
    evolucao_id: UUID,
    tipo_anexo: schemas.TipoAnexo,
    file: UploadFile = File(...),
    descricao: str = "",
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Faz upload de um anexo para uma evolução."""
    # Salvar o arquivo em disco (em um ambiente de produção, use um storage de objetos)
    file_path = f"uploads/{evolucao_id}_{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    anexo_data = schemas.AnexoProntuarioCreate(
        tipo_anexo=tipo_anexo,
        descricao=descricao,
        caminho_arquivo=file_path
    )
    return crud.create_anexo(db, anexo_data, evolucao_id)
