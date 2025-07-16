"""
Operações CRUD para o módulo de Auditoria Centralizada.
"""
from sqlalchemy.orm import Session
from models.auditoria import LogAuditoriaGeral
from schemas.auditoria import LogAuditoriaGeralCreate
from typing import List, Optional
from uuid import UUID

def create_log_auditoria(db: Session, log_data: LogAuditoriaGeralCreate) -> LogAuditoriaGeral:
    db_log = LogAuditoriaGeral(**log_data.dict())
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

def get_logs_auditoria(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    usuario_id: Optional[UUID] = None,
    clinica_id: Optional[int] = None,
    acao: Optional[str] = None,
    nome_tabela: Optional[str] = None
) -> List[LogAuditoriaGeral]:
    query = db.query(LogAuditoriaGeral)
    if usuario_id:
        query = query.filter(LogAuditoriaGeral.usuario_id == usuario_id)
    if clinica_id:
        query = query.filter(LogAuditoriaGeral.clinica_id == clinica_id)
    if acao:
        query = query.filter(LogAuditoriaGeral.acao.ilike(f"%{acao}%"))
    if nome_tabela:
        query = query.filter(LogAuditoriaGeral.nome_tabela.ilike(f"%{nome_tabela}%"))
    return query.offset(skip).limit(limit).all()
