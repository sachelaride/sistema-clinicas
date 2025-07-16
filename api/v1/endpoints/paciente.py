"""
Endpoints da API para o módulo de pacientes
"""
from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File, Path
from sqlalchemy.orm import Session

from database.session import get_db
from schemas.paciente import (
    Paciente, PacienteCreate, PacienteUpdate, PacienteCompleto,
    PacienteFiltro, PacienteResumo, EstatisticasPacientes,
    ResponsavelLegal, ResponsavelLegalCreate,
    TipoDocumento, TipoDocumentoCreate,
    DocumentoPaciente, DocumentoPacienteCreate,
    ConsentimentoPaciente, ConsentimentoPacienteCreate
)
from schemas.usuario import Usuario
from services.paciente_service import paciente_service
from crud.paciente import (
    crud_paciente, crud_responsavel_legal, crud_tipo_documento,
    crud_documento_paciente, crud_consentimento_paciente
)
from api.dependencies import (
    get_current_user, can_create_paciente, can_read_paciente,
    can_update_paciente, can_delete_paciente
)


router = APIRouter(prefix="/pacientes", tags=["Pacientes"])


@router.get("/", response_model=List[PacienteResumo])
async def listar_pacientes(
    skip: int = Query(0, ge=0, description="Número de registros para pular"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros"),
    nome: Optional[str] = Query(None, description="Filtrar por nome"),
    email: Optional[str] = Query(None, description="Filtrar por email"),
    telefone: Optional[str] = Query(None, description="Filtrar por telefone"),
    sexo: Optional[str] = Query(None, regex="^[MFO]$", description="Filtrar por sexo"),
    current_user: Usuario = Depends(can_read_paciente()),
    db: Session = Depends(get_db)
):
    """
    Listar pacientes com filtros opcionais
    
    Permite buscar pacientes por:
    - Nome (busca parcial)
    - Email (busca parcial)  
    - Telefone (busca parcial)
    - Sexo (M/F/O)
    """
    filtros = PacienteFiltro(
        nome=nome,
        email=email,
        telefone=telefone,
        sexo=sexo
    )
    
    pacientes = paciente_service.buscar_pacientes(db, filtros, skip, limit)
    
    # Converter para resumo
    return [
        PacienteResumo(
            paciente_id=p.paciente_id,
            nome_completo=p.nome_completo,
            data_nascimento=p.data_nascimento,
            telefone=p.telefone,
            email=p.email,
            idade=p.idade
        )
        for p in pacientes
    ]


@router.get("/{paciente_id}", response_model=PacienteCompleto)
async def obter_paciente(
    paciente_id: UUID,
    current_user: Usuario = Depends(can_read_paciente()),
    db: Session = Depends(get_db)
):
    """
    Obter detalhes completos de um paciente
    
    Inclui:
    - Dados pessoais
    - Responsáveis legais
    - Documentos
    - Consentimentos
    """
    paciente = crud_paciente.get(db, paciente_id)
    if not paciente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Paciente não encontrado"
        )
    
    return paciente


@router.post("/", response_model=Paciente, status_code=status.HTTP_201_CREATED)
async def criar_paciente(
    paciente_data: PacienteCreate,
    current_user: Usuario = Depends(can_create_paciente()),
    db: Session = Depends(get_db)
):
    """
    Criar novo paciente
    
    Cria automaticamente um consentimento LGPD básico
    """
    try:
        return paciente_service.criar_paciente(db, paciente_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/{paciente_id}", response_model=Paciente)
async def atualizar_paciente(
    paciente_id: UUID,
    paciente_data: PacienteUpdate,
    current_user: Usuario = Depends(can_update_paciente()),
    db: Session = Depends(get_db)
):
    """
    Atualizar dados de um paciente
    """
    try:
        paciente = paciente_service.atualizar_paciente(db, paciente_id, paciente_data)
        if not paciente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Paciente não encontrado"
            )
        return paciente
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{paciente_id}")
async def excluir_paciente(
    paciente_id: UUID,
    current_user: Usuario = Depends(can_delete_paciente()),
    db: Session = Depends(get_db)
):
    """
    Excluir um paciente
    
    **Atenção**: Esta ação remove permanentemente todos os dados
    relacionados ao paciente (responsáveis, documentos, consentimentos)
    """
    paciente = crud_paciente.delete(db, paciente_id)
    if not paciente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Paciente não encontrado"
        )
    
    return {"message": "Paciente excluído com sucesso"}


# Endpoints para responsáveis legais
@router.get("/{paciente_id}/responsaveis", response_model=List[ResponsavelLegal])
async def listar_responsaveis(
    paciente_id: UUID,
    current_user: Usuario = Depends(can_read_paciente()),
    db: Session = Depends(get_db)
):
    """Listar responsáveis legais de um paciente"""
    # Verificar se paciente existe
    paciente = crud_paciente.get(db, paciente_id)
    if not paciente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Paciente não encontrado"
        )
    
    return crud_responsavel_legal.get_by_paciente(db, paciente_id)


@router.post("/{paciente_id}/responsaveis", response_model=ResponsavelLegal, status_code=status.HTTP_201_CREATED)
async def adicionar_responsavel(
    paciente_id: UUID,
    responsavel_data: ResponsavelLegalCreate,
    current_user: Usuario = Depends(can_update_paciente()),
    db: Session = Depends(get_db)
):
    """Adicionar responsável legal ao paciente"""
    # Garantir que o paciente_id do path seja usado
    responsavel_data.paciente_id = paciente_id
    
    try:
        return paciente_service.adicionar_responsavel(db, responsavel_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/responsaveis/{responsavel_id}")
async def remover_responsavel(
    responsavel_id: UUID,
    current_user: Usuario = Depends(can_update_paciente()),
    db: Session = Depends(get_db)
):
    """Remover responsável legal"""
    responsavel = crud_responsavel_legal.delete(db, responsavel_id)
    if not responsavel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Responsável não encontrado"
        )
    
    return {"message": "Responsável removido com sucesso"}


# Endpoints para documentos
@router.get("/{paciente_id}/documentos", response_model=List[DocumentoPaciente])
async def listar_documentos(
    paciente_id: UUID,
    current_user: Usuario = Depends(can_read_paciente()),
    db: Session = Depends(get_db)
):
    """Listar documentos de um paciente"""
    # Verificar se paciente existe
    paciente = crud_paciente.get(db, paciente_id)
    if not paciente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Paciente não encontrado"
        )
    
    return crud_documento_paciente.get_by_paciente(db, paciente_id)


@router.post("/{paciente_id}/documentos/upload")
async def upload_documento(
    paciente_id: UUID,
    arquivo: UploadFile = File(...),
    tipo_id: Optional[int] = Query(None, description="ID do tipo de documento"),
    current_user: Usuario = Depends(can_update_paciente()),
    db: Session = Depends(get_db)
):
    """
    Upload de documento do paciente
    
    Suporta extração automática de dados via OCR (simulado)
    """
    try:
        resultado = paciente_service.upload_documento(db, paciente_id, tipo_id, arquivo)
        return {
            "message": "Documento enviado com sucesso",
            **resultado
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/documentos/{documento_id}")
async def remover_documento(
    documento_id: UUID,
    current_user: Usuario = Depends(can_update_paciente()),
    db: Session = Depends(get_db)
):
    """Remover documento do paciente"""
    documento = crud_documento_paciente.delete(db, documento_id)
    if not documento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Documento não encontrado"
        )
    
    return {"message": "Documento removido com sucesso"}


# Endpoints para consentimentos
@router.get("/{paciente_id}/consentimentos", response_model=List[ConsentimentoPaciente])
async def listar_consentimentos(
    paciente_id: UUID,
    apenas_ativos: bool = Query(True, description="Listar apenas consentimentos ativos"),
    current_user: Usuario = Depends(can_read_paciente()),
    db: Session = Depends(get_db)
):
    """Listar consentimentos de um paciente"""
    # Verificar se paciente existe
    paciente = crud_paciente.get(db, paciente_id)
    if not paciente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Paciente não encontrado"
        )
    
    if apenas_ativos:
        return crud_consentimento_paciente.get_ativos_by_paciente(db, paciente_id)
    else:
        return crud_consentimento_paciente.get_by_paciente(db, paciente_id)


@router.post("/{paciente_id}/consentimentos", response_model=ConsentimentoPaciente, status_code=status.HTTP_201_CREATED)
async def registrar_consentimento(
    paciente_id: UUID,
    consentimento_data: ConsentimentoPacienteCreate,
    current_user: Usuario = Depends(can_update_paciente()),
    db: Session = Depends(get_db)
):
    """Registrar novo consentimento LGPD"""
    # Garantir que o paciente_id do path seja usado
    consentimento_data.paciente_id = paciente_id
    
    try:
        return paciente_service.registrar_consentimento(db, consentimento_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.patch("/consentimentos/{consentimento_id}/revogar")
async def revogar_consentimento(
    consentimento_id: int,
    current_user: Usuario = Depends(can_update_paciente()),
    db: Session = Depends(get_db)
):
    """Revogar consentimento LGPD"""
    consentimento = crud_consentimento_paciente.revogar_consentimento(db, consentimento_id)
    if not consentimento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Consentimento não encontrado"
        )
    
    return {"message": "Consentimento revogado com sucesso"}


# Endpoints para tipos de documentos
@router.get("/tipos-documentos", response_model=List[TipoDocumento])
async def listar_tipos_documentos(
    current_user: Usuario = Depends(can_read_paciente()),
    db: Session = Depends(get_db)
):
    """Listar tipos de documentos disponíveis"""
    return crud_tipo_documento.get_multi(db)


@router.post("/tipos-documentos", response_model=TipoDocumento, status_code=status.HTTP_201_CREATED)
async def criar_tipo_documento(
    tipo_data: TipoDocumentoCreate,
    current_user: Usuario = Depends(can_update_paciente()),
    db: Session = Depends(get_db)
):
    """Criar novo tipo de documento"""
    # Verificar se nome já existe
    existing = crud_tipo_documento.get_by_nome(db, tipo_data.nome)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tipo de documento já existe"
        )
    
    return crud_tipo_documento.create(db, tipo_data)


# Endpoints para relatórios e estatísticas
@router.get("/aniversariantes/{mes}", response_model=List[PacienteResumo])
async def aniversariantes_mes(
    mes: int = Path(..., ge=1, le=12, description="Mês (1-12)"),
    current_user: Usuario = Depends(can_read_paciente()),
    db: Session = Depends(get_db)
):
    """Listar aniversariantes do mês"""
    pacientes = paciente_service.get_aniversariantes_mes(db, mes)
    
    return [
        PacienteResumo(
            paciente_id=p.paciente_id,
            nome_completo=p.nome_completo,
            data_nascimento=p.data_nascimento,
            telefone=p.telefone,
            email=p.email,
            idade=p.idade
        )
        for p in pacientes
    ]


@router.get("/faixa-etaria/{idade_min}/{idade_max}", response_model=List[PacienteResumo])
async def pacientes_faixa_etaria(
    idade_min: int = Path(..., ge=0, description="Idade mínima"),
    idade_max: int = Path(..., ge=0, le=120, description="Idade máxima"),
    current_user: Usuario = Depends(can_read_paciente()),
    db: Session = Depends(get_db)
):
    """Listar pacientes por faixa etária"""
    if idade_min > idade_max:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Idade mínima deve ser menor que idade máxima"
        )
    
    pacientes = paciente_service.get_pacientes_por_idade(db, idade_min, idade_max)
    
    return [
        PacienteResumo(
            paciente_id=p.paciente_id,
            nome_completo=p.nome_completo,
            data_nascimento=p.data_nascimento,
            telefone=p.telefone,
            email=p.email,
            idade=p.idade
        )
        for p in pacientes
    ]


@router.get("/estatisticas", response_model=EstatisticasPacientes)
async def estatisticas_pacientes(
    current_user: Usuario = Depends(can_read_paciente()),
    db: Session = Depends(get_db)
):
    """Obter estatísticas gerais dos pacientes"""
    return paciente_service.get_estatisticas(db)


@router.get("/{paciente_id}/documentos/validacao")
async def validar_documentos_obrigatorios(
    paciente_id: UUID,
    current_user: Usuario = Depends(can_read_paciente()),
    db: Session = Depends(get_db)
):
    """Validar se paciente possui todos os documentos obrigatórios"""
    # Verificar se paciente existe
    paciente = crud_paciente.get(db, paciente_id)
    if not paciente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Paciente não encontrado"
        )
    
    return paciente_service.validar_documentos_obrigatorios(db, paciente_id)


@router.patch("/{paciente_id}/perfil-epidemiologico")
async def atualizar_perfil_epidemiologico(
    paciente_id: UUID,
    dados: dict,
    current_user: Usuario = Depends(can_update_paciente()),
    db: Session = Depends(get_db)
):
    """Atualizar perfil epidemiológico do paciente"""
    paciente = paciente_service.atualizar_perfil_epidemiologico(db, paciente_id, dados)
    if not paciente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Paciente não encontrado"
        )
    
    return {"message": "Perfil epidemiológico atualizado com sucesso"}

