"""
Schemas Pydantic para o módulo de pacientes
"""
from typing import Optional, List, Dict, Any
from datetime import date, datetime
from uuid import UUID
from pydantic import BaseModel, Field, EmailStr, validator


# Schemas para Paciente
class PacienteBase(BaseModel):
    """Schema base para paciente"""
    nome: str = Field(..., min_length=1, max_length=100, description="Nome do paciente")
    sobrenome: str = Field(..., min_length=1, max_length=100, description="Sobrenome do paciente")
    data_nascimento: Optional[date] = Field(None, description="Data de nascimento")
    sexo: Optional[str] = Field(None, pattern="^[MFO]$", description="Sexo (M/F/O)")
    endereco: Optional[str] = Field(None, description="Endereço completo")
    telefone: Optional[str] = Field(None, max_length=20, description="Telefone de contato")
    email: Optional[EmailStr] = Field(None, description="Email do paciente")
    perfil_epidemiologico: Optional[Dict[str, Any]] = Field(None, description="Dados epidemiológicos")
    
    @validator('data_nascimento')
    def validar_data_nascimento(cls, v):
        if v and v > date.today():
            raise ValueError('Data de nascimento não pode ser futura')
        return v


class PacienteCreate(PacienteBase):
    """Schema para criação de paciente"""
    pass


class PacienteUpdate(BaseModel):
    """Schema para atualização de paciente"""
    nome: Optional[str] = Field(None, min_length=1, max_length=100)
    sobrenome: Optional[str] = Field(None, min_length=1, max_length=100)
    data_nascimento: Optional[date] = None
    sexo: Optional[str] = Field(None, pattern="^[MFO]$")
    endereco: Optional[str] = None
    telefone: Optional[str] = Field(None, max_length=20)
    email: Optional[EmailStr] = None
    perfil_epidemiologico: Optional[Dict[str, Any]] = None


class Paciente(PacienteBase):
    """Schema de resposta para paciente"""
    paciente_id: UUID
    criado_em: datetime
    atualizado_em: datetime
    nome_completo: Optional[str] = None
    idade: Optional[int] = None
    
    class Config:
        from_attributes = True


# Schemas para ResponsavelLegal
class ResponsavelLegalBase(BaseModel):
    """Schema base para responsável legal"""
    nome: str = Field(..., min_length=1, max_length=150, description="Nome do responsável")
    cpf: Optional[str] = Field(None, max_length=14, description="CPF do responsável")
    rg: Optional[str] = Field(None, max_length=20, description="RG do responsável")
    telefone: Optional[str] = Field(None, max_length=20, description="Telefone do responsável")
    email: Optional[EmailStr] = Field(None, description="Email do responsável")
    grau_parentesco: Optional[str] = Field(None, max_length=50, description="Grau de parentesco")
    endereco: Optional[str] = Field(None, description="Endereço do responsável")


class ResponsavelLegalCreate(ResponsavelLegalBase):
    """Schema para criação de responsável legal"""
    paciente_id: UUID = Field(..., description="ID do paciente")


class ResponsavelLegal(ResponsavelLegalBase):
    """Schema de resposta para responsável legal"""
    responsavel_id: UUID
    paciente_id: UUID
    criado_em: datetime
    
    class Config:
        from_attributes = True


# Schemas para TipoDocumento
class TipoDocumentoBase(BaseModel):
    """Schema base para tipo de documento"""
    nome: str = Field(..., min_length=1, max_length=50, description="Nome do tipo de documento")
    descricao: Optional[str] = Field(None, description="Descrição do tipo de documento")
    obrigatorio: bool = Field(False, description="Se o documento é obrigatório")


class TipoDocumentoCreate(TipoDocumentoBase):
    """Schema para criação de tipo de documento"""
    pass


class TipoDocumento(TipoDocumentoBase):
    """Schema de resposta para tipo de documento"""
    tipo_id: int
    
    class Config:
        from_attributes = True


# Schemas para DocumentoPaciente
class DocumentoPacienteBase(BaseModel):
    """Schema base para documento do paciente"""
    dados_ocr: Optional[str] = Field(None, description="Dados extraídos por OCR")
    caminho_arquivo: str = Field(..., description="Caminho do arquivo")


class DocumentoPacienteCreate(DocumentoPacienteBase):
    """Schema para criação de documento do paciente"""
    paciente_id: UUID = Field(..., description="ID do paciente")
    tipo_id: Optional[int] = Field(None, description="ID do tipo de documento")


class DocumentoPaciente(DocumentoPacienteBase):
    """Schema de resposta para documento do paciente"""
    documento_id: UUID
    paciente_id: UUID
    tipo_id: Optional[int]
    enviado_em: datetime
    
    # Relacionamentos
    tipo_documento: Optional[TipoDocumento] = None
    
    class Config:
        from_attributes = True


# Schemas para ConsentimentoPaciente
class ConsentimentoPacienteBase(BaseModel):
    """Schema base para consentimento do paciente"""
    tipo_consentimento: str = Field(..., max_length=50, description="Tipo de consentimento")
    ativo: bool = Field(True, description="Se o consentimento está ativo")
    detalhes: Optional[str] = Field(None, description="Detalhes do consentimento")


class ConsentimentoPacienteCreate(ConsentimentoPacienteBase):
    """Schema para criação de consentimento do paciente"""
    paciente_id: UUID = Field(..., description="ID do paciente")


class ConsentimentoPaciente(ConsentimentoPacienteBase):
    """Schema de resposta para consentimento do paciente"""
    consentimento_id: int
    paciente_id: UUID
    data_consentimento: datetime
    
    class Config:
        from_attributes = True


# Schemas para respostas completas
class PacienteCompleto(Paciente):
    """Schema completo do paciente com relacionamentos"""
    responsaveis: List[ResponsavelLegal] = []
    documentos: List[DocumentoPaciente] = []
    consentimentos: List[ConsentimentoPaciente] = []
    
    class Config:
        from_attributes = True


# Schemas para busca e filtros
class PacienteFiltro(BaseModel):
    """Schema para filtros de busca de pacientes"""
    nome: Optional[str] = Field(None, description="Buscar por nome")
    email: Optional[str] = Field(None, description="Buscar por email")
    telefone: Optional[str] = Field(None, description="Buscar por telefone")
    data_nascimento_inicio: Optional[date] = Field(None, description="Data de nascimento inicial")
    data_nascimento_fim: Optional[date] = Field(None, description="Data de nascimento final")
    sexo: Optional[str] = Field(None, pattern="^[MFO]$", description="Filtrar por sexo")


class PacienteResumo(BaseModel):
    """Schema resumido do paciente para listagens"""
    paciente_id: UUID
    nome_completo: str
    data_nascimento: Optional[date]
    telefone: Optional[str]
    email: Optional[str]
    idade: Optional[int]
    
    class Config:
        from_attributes = True


# Schemas para estatísticas
class EstatisticasPacientes(BaseModel):
    """Schema para estatísticas de pacientes"""
    total_pacientes: int
    pacientes_por_sexo: Dict[str, int]
    pacientes_por_faixa_etaria: Dict[str, int]
    novos_pacientes_mes: int
    pacientes_com_responsavel: int
    pacientes_com_documentos: int

