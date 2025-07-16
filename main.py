"""
Aplicação principal do Sistema de Clínicas
"""
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time

from config.settings import settings
from database.base import Base, engine
from database.session import get_db
from api.v1.endpoints import estoque, paciente, usuario, auth, clinica, agendamento, prontuario, fila, auditoria
from models.clinica import Clinica # Import model to ensure table creation
from models.agendamento import Agendamento, Sala, Servico, HorarioDisponibilidade # Import models
from models.prontuario import Prontuario, Evolucao, AnexoProntuario # Import models
from models.fila import GuicheAtendimento, FilaEspera # Import models
from models.auditoria import LogAuditoriaGeral # Import models

# Criar tabelas no banco de dados
# Base.metadata.create_all(bind=engine) # Removido: O Alembic agora gerencia as migrações do banco de dados

# Criar aplicação FastAPI
app = FastAPI(
    title="Sistema de Controle de Clínicas",
    description="""
    Sistema modular para gestão de clínicas universitárias com:
    
    - **Módulo de Auditoria Centralizada**: Logs detalhados de todas as operações críticas.
    - **Módulo de Gestão de Filas**: Gerenciamento de filas de espera e chamadas.
    - **Módulo de Prontuário Eletrônico**: Gestão de prontuários, evoluções e anexos.
    - **Módulo de Agendamento**: Gestão de agendamentos, salas, serviços e horários
    - **Módulo de Clínicas**: Gerenciamento de múltiplas unidades de atendimento
    - **Módulo de Pacientes**: Cadastro completo, responsáveis, documentos e consentimentos LGPD
    - **Módulo de Usuários**: Gestão de usuários, alunos, perfis e permissões por clínica
    - **Módulo de Estoque**: Controle avançado com lotes, fornecedores e relatórios
    - **Autenticação**: Sistema JWT com controle granular de permissões
    
    Desenvolvido com FastAPI, SQLAlchemy e PostgreSQL.
    """,
    version="2.0.0",
    contact={
        "name": "Equipe de Desenvolvimento",
        "email": "dev@clinicas.edu.br",
    },
    license_info={
        "name": "Uso Acadêmico",
    },
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especificar domínios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware para timing das requisições
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    request.state.start_time = start_time
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    
    return response

# Incluir routers da API
app.include_router(auth.router, prefix="/api/v1")
app.include_router(auditoria.router, prefix="/api/v1")
app.include_router(fila.router, prefix="/api/v1")
app.include_router(prontuario.router, prefix="/api/v1")
app.include_router(agendamento.router, prefix="/api/v1")
app.include_router(clinica.router, prefix="/api/v1")
app.include_router(paciente.router, prefix="/api/v1")
app.include_router(usuario.router, prefix="/api/v1")
app.include_router(estoque.router, prefix="/api/v1")

# Endpoint raiz
@app.get("/")
async def root():
    """
    Endpoint raiz com informações do sistema
    """
    return {
        "message": "Sistema de Controle de Clínicas",
        "version": "2.0.0",
        "status": "online",
        "modules": [
            "auditoria",
            "fila",
            "prontuario",
            "agendamento",
            "clinicas",
            "pacientes",
            "usuarios", 
            "estoque",
            "autenticacao"
        ],
        "docs": "/docs",
        "redoc": "/redoc"
    }

# Endpoint de saúde
@app.get("/health")
async def health_check():
    """
    Verificação de saúde do sistema
    """
    try:
        # Testar conexão com banco de dados
        db = next(get_db())
        db.execute("SELECT 1")
        db_status = "healthy"
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"
    
    return {
        "status": "healthy" if db_status == "healthy" else "unhealthy",
        "database": db_status,
        "timestamp": time.time()
    }

# Handler para erros não tratados
@app.exception_handler(500)
async def internal_server_error_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Erro interno do servidor",
            "message": "Entre em contato com o suporte técnico"
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
