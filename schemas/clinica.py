"""
Schemas Pydantic para o módulo de Clínicas.

Define a estrutura de dados para a criação, atualização e leitura
de informações de clínicas via API.
"""
from pydantic import BaseModel
from typing import Optional

# Schema base com os campos comuns
class ClinicaBase(BaseModel):
    """
    Schema base para uma clínica, com campos compartilhados.
    """
    nome: str
    descricao: Optional[str] = None
    ativo: bool = True

# Schema para a criação de uma nova clínica (entrada da API)
class ClinicaCreate(ClinicaBase):
    """
    Schema usado para criar uma nova clínica. Herda de ClinicaBase.
    """
    pass

# Schema para a atualização de uma clínica (entrada da API)
class ClinicaUpdate(BaseModel):
    """
    Schema usado para atualizar uma clínica existente.
    Todos os campos são opcionais.
    """
    nome: Optional[str] = None
    descricao: Optional[str] = None
    ativo: Optional[bool] = None

# Schema para a leitura de uma clínica (saída da API)
class Clinica(ClinicaBase):
    """
    Schema completo para representar uma clínica na resposta da API.
    Inclui o ID e herda os outros campos de ClinicaBase.
    """
    id: int

    class Config:
        orm_mode = True
