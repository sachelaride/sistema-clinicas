"""
Endpoints da API para o módulo de usuários
"""
from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from database.session import get_db
from schemas.usuario import (
    Usuario, UsuarioCreate, UsuarioUpdate, UsuarioCompleto,
    UsuarioFiltro, UsuarioResumo, EstatisticasUsuarios,
    Perfil, PerfilCreate,
    Permissao, PermissaoCreate,
    PerfilAluno, PerfilAlunoUpdate,
    LogAcesso, LogAuditoria
)
from services.usuario_service import usuario_service, perfil_service
from crud.usuario import (
    crud_usuario, crud_perfil, crud_permissao,
    crud_perfil_aluno, crud_log_acesso, crud_log_auditoria
)
from api.dependencies import (
    get_current_user, require_admin, require_aluno,
    can_create_usuario, can_read_usuario, can_update_usuario, can_delete_usuario,
    can_read_logs, can_read_auditoria
)


router = APIRouter(prefix="/usuarios", tags=["Usuários"])


@router.get("/", response_model=List[UsuarioResumo])
async def listar_usuarios(
    skip: int = Query(0, ge=0, description="Número de registros para pular"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros"),
    nome: Optional[str] = Query(None, description="Filtrar por nome"),
    email: Optional[str] = Query(None, description="Filtrar por email"),
    perfil_id: Optional[int] = Query(None, description="Filtrar por perfil"),
    clinica_id: Optional[int] = Query(None, description="Filtrar por clínica"),
    ativo: Optional[bool] = Query(None, description="Filtrar por status ativo"),
    is_aluno: Optional[bool] = Query(None, description="Filtrar apenas alunos"),
    current_user: Usuario = Depends(can_read_usuario()),
    db: Session = Depends(get_db)
):
    """
    Listar usuários com filtros opcionais
    
    Permite buscar usuários por:
    - Nome (busca parcial no nome de usuário e nome completo)
    - Email (busca parcial)
    - Perfil
    - Clínica
    - Status ativo/inativo
    - Apenas alunos
    """
    filtros = UsuarioFiltro(
        nome=nome,
        email=email,
        perfil_id=perfil_id,
        clinica_id=clinica_id,
        ativo=ativo,
        is_aluno=is_aluno
    )
    
    usuarios = usuario_service.buscar_usuarios(db, filtros, skip, limit)
    
    # Converter para resumo
    return [
        UsuarioResumo(
            usuario_id=u.usuario_id,
            nome_usuario=u.nome_usuario,
            nome_completo=u.nome_completo,
            email=u.email,
            perfil_nome=u.perfil.nome if u.perfil else None,
            clinica_nome=u.clinica.nome if u.clinica else None, # Adicionado
            ativo=u.ativo,
            is_aluno=u.is_aluno,
            rgm=u.rgm
        )
        for u in usuarios
    ]


@router.get("/me", response_model=UsuarioCompleto)
async def obter_usuario_atual(
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obter informações completas do usuário logado
    """
    from services.auth_service import authorization_service
    
    permissoes = authorization_service.get_user_permissions(db, current_user.usuario_id)
    
    return UsuarioCompleto(
        **current_user.__dict__,
        permissoes=permissoes
    )


@router.get("/{usuario_id}", response_model=UsuarioCompleto)
async def obter_usuario(
    usuario_id: UUID,
    current_user: Usuario = Depends(can_read_usuario()),
    db: Session = Depends(get_db)
):
    """
    Obter detalhes completos de um usuário
    """
    usuario = crud_usuario.get(db, usuario_id)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    
    from services.auth_service import authorization_service
    permissoes = authorization_service.get_user_permissions(db, usuario_id)
    
    return UsuarioCompleto(
        **usuario.__dict__,
        permissoes=permissoes
    )


@router.post("/", response_model=Usuario, status_code=status.HTTP_201_CREATED)
async def criar_usuario(
    usuario_data: UsuarioCreate,
    current_user: Usuario = Depends(can_create_usuario()),
    db: Session = Depends(get_db)
):
    """
    Criar novo usuário
    
    Pode incluir dados de perfil de aluno se fornecidos
    """
    try:
        return usuario_service.criar_usuario(db, usuario_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/{usuario_id}", response_model=Usuario)
async def atualizar_usuario(
    usuario_id: UUID,
    usuario_data: UsuarioUpdate,
    current_user: Usuario = Depends(can_update_usuario()),
    db: Session = Depends(get_db)
):
    """
    Atualizar dados de um usuário
    """
    try:
        usuario = usuario_service.atualizar_usuario(db, usuario_id, usuario_data)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado"
            )
        return usuario
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.patch("/{usuario_id}/ativar")
async def ativar_usuario(
    usuario_id: UUID,
    current_user: Usuario = Depends(require_admin()),
    db: Session = Depends(get_db)
):
    """
    Ativar usuário (apenas administradores)
    """
    usuario = usuario_service.ativar_usuario(db, usuario_id, current_user.usuario_id)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    
    return {"message": "Usuário ativado com sucesso"}


@router.patch("/{usuario_id}/desativar")
async def desativar_usuario(
    usuario_id: UUID,
    current_user: Usuario = Depends(require_admin()),
    db: Session = Depends(get_db)
):
    """
    Desativar usuário (apenas administradores)
    """
    usuario = usuario_service.desativar_usuario(db, usuario_id, current_user.usuario_id)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    
    return {"message": "Usuário desativado com sucesso"}


@router.post("/{usuario_id}/resetar-senha")
async def resetar_senha(
    usuario_id: UUID,
    current_user: Usuario = Depends(require_admin()),
    db: Session = Depends(get_db)
):
    """
    Resetar senha do usuário (apenas administradores)
    
    Retorna uma senha temporária que deve ser alterada no primeiro login
    """
    try:
        nova_senha = usuario_service.resetar_senha(db, usuario_id, current_user.usuario_id)
        return {
            "message": "Senha resetada com sucesso",
            "senha_temporaria": nova_senha,
            "aviso": "O usuário deve alterar esta senha no primeiro login"
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


# Endpoints específicos para alunos
@router.get("/alunos", response_model=List[UsuarioResumo])
async def listar_alunos(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    curso: Optional[str] = Query(None, description="Filtrar por curso"),
    semestre: Optional[int] = Query(None, ge=1, le=20, description="Filtrar por semestre"),
    current_user: Usuario = Depends(can_read_usuario()),
    db: Session = Depends(get_db)
):
    """
    Listar apenas usuários que são alunos
    """
    if curso:
        alunos = usuario_service.get_alunos_por_curso(db, curso)
    elif semestre:
        alunos = usuario_service.get_alunos_por_semestre(db, semestre)
    else:
        alunos = crud_usuario.get_alunos(db, skip, limit)
    
    return [
        UsuarioResumo(
            usuario_id=u.usuario_id,
            nome_usuario=u.nome_usuario,
            nome_completo=u.nome_completo,
            email=u.email,
            perfil_nome=u.perfil.nome if u.perfil else None,
            ativo=u.ativo,
            is_aluno=True,
            rgm=u.rgm
        )
        for u in alunos
    ]


@router.get("/alunos/ranking-carga-horaria")
async def ranking_carga_horaria(
    limit: int = Query(10, ge=1, le=50, description="Número de alunos no ranking"),
    current_user: Usuario = Depends(can_read_usuario()),
    db: Session = Depends(get_db)
):
    """
    Ranking de alunos por carga horária
    """
    return usuario_service.get_ranking_carga_horaria(db, limit)


@router.patch("/{usuario_id}/perfil-aluno", response_model=Usuario)
async def atualizar_perfil_aluno(
    usuario_id: UUID,
    perfil_data: PerfilAlunoUpdate,
    current_user: Usuario = Depends(can_update_usuario()),
    db: Session = Depends(get_db)
):
    """
    Atualizar perfil específico de aluno
    """
    usuario = usuario_service.atualizar_perfil_aluno(db, usuario_id, perfil_data)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado ou não é aluno"
        )
    
    return usuario


@router.patch("/{usuario_id}/incrementar-horas")
async def incrementar_carga_horaria(
    usuario_id: UUID,
    horas: int = Query(..., ge=1, le=24, description="Número de horas a incrementar"),
    current_user: Usuario = Depends(can_update_usuario()),
    db: Session = Depends(get_db)
):
    """
    Incrementar carga horária do aluno
    """
    sucesso = usuario_service.incrementar_carga_horaria(db, usuario_id, horas)
    if not sucesso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado ou não é aluno"
        )
    
    return {"message": f"Carga horária incrementada em {horas} horas"}


# Endpoints para perfis
@router.get("/perfis", response_model=List[Perfil])
async def listar_perfis(
    current_user: Usuario = Depends(can_read_usuario()),
    db: Session = Depends(get_db)
):
    """
    Listar todos os perfis disponíveis
    """
    return crud_perfil.get_multi(db)


@router.post("/perfis", response_model=Perfil, status_code=status.HTTP_201_CREATED)
async def criar_perfil(
    perfil_data: PerfilCreate,
    current_user: Usuario = Depends(require_admin()),
    db: Session = Depends(get_db)
):
    """
    Criar novo perfil (apenas administradores)
    """
    try:
        return perfil_service.criar_perfil(db, perfil_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/perfis/{perfil_id}/permissoes/{permissao_id}")
async def adicionar_permissao_perfil(
    perfil_id: int,
    permissao_id: int,
    current_user: Usuario = Depends(require_admin()),
    db: Session = Depends(get_db)
):
    """
    Adicionar permissão a um perfil (apenas administradores)
    """
    sucesso = perfil_service.adicionar_permissao_perfil(
        db, perfil_id, permissao_id, current_user.usuario_id
    )
    
    if not sucesso:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Erro ao adicionar permissão ao perfil"
        )
    
    return {"message": "Permissão adicionada ao perfil com sucesso"}


@router.delete("/perfis/{perfil_id}/permissoes/{permissao_id}")
async def remover_permissao_perfil(
    perfil_id: int,
    permissao_id: int,
    current_user: Usuario = Depends(require_admin()),
    db: Session = Depends(get_db)
):
    """
    Remover permissão de um perfil (apenas administradores)
    """
    sucesso = perfil_service.remover_permissao_perfil(
        db, perfil_id, permissao_id, current_user.usuario_id
    )
    
    if not sucesso:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Erro ao remover permissão do perfil"
        )
    
    return {"message": "Permissão removida do perfil com sucesso"}


# Endpoints para permissões
@router.get("/permissoes", response_model=List[Permissao])
async def listar_permissoes(
    current_user: Usuario = Depends(require_admin()),
    db: Session = Depends(get_db)
):
    """
    Listar todas as permissões disponíveis (apenas administradores)
    """
    return crud_permissao.get_multi(db)


@router.post("/permissoes", response_model=Permissao, status_code=status.HTTP_201_CREATED)
async def criar_permissao(
    permissao_data: PermissaoCreate,
    current_user: Usuario = Depends(require_admin()),
    db: Session = Depends(get_db)
):
    """
    Criar nova permissão (apenas administradores)
    """
    try:
        return perfil_service.criar_permissao(db, permissao_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


# Endpoints para logs e auditoria
@router.get("/{usuario_id}/logs-acesso", response_model=List[LogAcesso])
async def logs_acesso_usuario(
    usuario_id: UUID,
    limit: int = Query(50, ge=1, le=500, description="Número máximo de logs"),
    current_user: Usuario = Depends(can_read_logs()),
    db: Session = Depends(get_db)
):
    """
    Obter logs de acesso de um usuário
    """
    return crud_log_acesso.get_by_usuario(db, usuario_id, limit)


@router.get("/{usuario_id}/logs-auditoria", response_model=List[LogAuditoria])
async def logs_auditoria_usuario(
    usuario_id: UUID,
    limit: int = Query(100, ge=1, le=500, description="Número máximo de logs"),
    current_user: Usuario = Depends(can_read_auditoria()),
    db: Session = Depends(get_db)
):
    """
    Obter logs de auditoria de um usuário
    """
    return crud_log_auditoria.get_by_usuario(db, usuario_id, limit)


# Endpoints para estatísticas
@router.get("/estatisticas", response_model=EstatisticasUsuarios)
async def estatisticas_usuarios(
    current_user: Usuario = Depends(can_read_usuario()),
    db: Session = Depends(get_db)
):
    """
    Obter estatísticas gerais dos usuários
    """
    return usuario_service.get_estatisticas(db)


# Endpoints para inicialização do sistema
@router.post("/inicializar-sistema")
async def inicializar_sistema(
    db: Session = Depends(get_db)
):
    """
    Inicializar perfis e permissões padrão do sistema (apenas administradores)
    
    Este endpoint deve ser usado apenas uma vez após a instalação inicial
    """
    try:
        # Inicializar permissões
        permissoes_criadas = perfil_service.inicializar_permissoes_padrao(db)
        
        # Inicializar perfis
        perfis_criados = perfil_service.inicializar_perfis_padrao(db)
        
        return {
            "message": "Sistema inicializado com sucesso",
            "perfis_criados": perfis_criados,
            "total_permissoes": len(permissoes_criadas)
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao inicializar sistema: {str(e)}"
        )

