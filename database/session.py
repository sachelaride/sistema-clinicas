"""
Gerenciamento de sessões do banco de dados
"""
from typing import Generator
from sqlalchemy.orm import Session

from database.base import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """
    Dependency para obter uma sessão do banco de dados.
    Usado como dependência do FastAPI.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

