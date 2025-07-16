"""
Endpoints da API para o módulo de Auditoria Centralizada.
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from database.session import get_db
from schemas.auditoria import LogAuditoriaGeral
from crud import auditoria as crud
from models.usuario import Usuario
from api.dependencies import get_current_user # Assumindo que você tem essa dependência

router = APIRouter(prefix="/auditoria", tags=["Auditoria Centralizada"])

@router.get("/logs", response_model=List[LogAuditoriaGeral])
def get_auditoria_logs(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    usuario_id: Optional[UUID] = Query(None),
    clinica_id: Optional[int] = Query(None),
    acao: Optional[str] = Query(None),
    nome_tabela: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user) # Apenas usuários autorizados podem ver logs
):
    """
    Retorna logs de auditoria, com opções de filtro.
    """
    # Em um sistema real, você adicionaria validação de permissão aqui
    # para garantir que apenas administradores ou usuários com permissão específica
    # possam acessar os logs de auditoria.

    # Se o usuário não for admin, ele só pode ver os próprios logs ou logs da sua clínica
    # if not current_user.is_admin:
    #     if usuario_id and usuario_id != current_user.usuario_id:
    #         raise HTTPException(status_code=403, detail="Não autorizado a ver logs de outros usuários")
    #     if clinica_id and clinica_id != current_user.clinica_id:
    #         raise HTTPException(status_code=403, detail="Não autorizado a ver logs de outras clínicas")
    #     if not usuario_id and not clinica_id: # Se não especificou, filtra pelos próprios
    #         usuario_id = current_user.usuario_id
    #         clinica_id = current_user.clinica_id

    logs = crud.get_logs_auditoria(
        db,
        skip=skip,
        limit=limit,
        usuario_id=usuario_id,
        clinica_id=clinica_id,
        acao=acao,
        nome_tabela=nome_tabela
    )
    return logs
