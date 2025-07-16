"""
API v1 do Sistema de Clínicas
"""
from fastapi import APIRouter

from api.v1.endpoints import estoque

api_router = APIRouter()

# Incluir routers dos endpoints
api_router.include_router(estoque.router, prefix="/estoque", tags=["estoque"])

