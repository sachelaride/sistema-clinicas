"""
Endpoints da API para autenticação
"""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session

from database.session import get_db
from schemas.usuario import LoginRequest, LoginResponse, Usuario, UsuarioUpdateSenha
from services.auth_service import auth_service
from api.dependencies import get_current_user


router = APIRouter(prefix="/auth", tags=["Autenticação"])


@router.post("/login", response_model=LoginResponse)
async def login(
    login_data: LoginRequest,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Realizar login no sistema
    
    - **nome_usuario**: Nome de usuário ou RGM (para alunos)
    - **senha**: Senha do usuário
    """
    try:
        return auth_service.login(db, login_data, request)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )


@router.post("/change-password")
async def change_password(
    password_data: UsuarioUpdateSenha,
    request: Request,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Alterar senha do usuário logado
    
    - **senha_atual**: Senha atual do usuário
    - **nova_senha**: Nova senha (mínimo 6 caracteres)
    - **confirmar_senha**: Confirmação da nova senha
    """
    try:
        success = auth_service.change_password(
            db=db,
            usuario_id=current_user.usuario_id,
            senha_atual=password_data.senha_atual,
            nova_senha=password_data.nova_senha,
            request=request
        )
        
        if success:
            return {"message": "Senha alterada com sucesso"}
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Erro ao alterar senha"
            )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/me", response_model=Usuario)
async def get_current_user_info(
    current_user: Usuario = Depends(get_current_user)
):
    """
    Obter informações do usuário logado
    """
    return current_user


@router.post("/logout")
async def logout(
    request: Request,
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Realizar logout do sistema
    
    Note: Em uma implementação JWT stateless, o logout é principalmente
    do lado do cliente (removendo o token). Este endpoint serve para
    registrar o logout nos logs de auditoria.
    """
    from crud.usuario import crud_log_auditoria
    
    # Registrar logout nos logs
    crud_log_auditoria.create(
        db=db,
        usuario_id=current_user.usuario_id,
        acao="LOGOUT",
        endereco_ip=request.client.host if request.client else "unknown"
    )
    
    return {"message": "Logout realizado com sucesso"}


@router.get("/permissions")
async def get_user_permissions(
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obter permissões do usuário logado
    """
    from services.auth_service import authorization_service
    
    permissions = authorization_service.get_user_permissions(
        db, current_user.usuario_id
    )
    
    return {
        "usuario_id": current_user.usuario_id,
        "nome_usuario": current_user.nome_usuario,
        "perfil": current_user.perfil.nome if current_user.perfil else None,
        "permissoes": permissions,
        "is_admin": authorization_service.is_admin(db, current_user.usuario_id),
        "is_aluno": current_user.is_aluno
    }

