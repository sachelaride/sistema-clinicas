"""
Schemas Pydantic para o módulo de estoque
"""
from typing import Optional, List
from datetime import date, datetime
from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel, Field

from models.estoque import StatusPedidoEnum, TipoAjusteEnum


# Schemas para Fornecedor
class FornecedorBase(BaseModel):
    """Schema base para fornecedor"""
    nome: str = Field(..., max_length=255, description="Nome do fornecedor")
    cnpj: Optional[str] = Field(None, max_length=18, description="CNPJ do fornecedor")
    contato_nome: Optional[str] = Field(None, max_length=100, description="Nome do contato")
    contato_email: Optional[str] = Field(None, max_length=100, description="Email do contato")
    contato_telefone: Optional[str] = Field(None, max_length=20, description="Telefone do contato")
    endereco: Optional[str] = Field(None, description="Endereço do fornecedor")


class FornecedorCreate(FornecedorBase):
    """Schema para criação de fornecedor"""
    pass


class FornecedorUpdate(BaseModel):
    """Schema para atualização de fornecedor"""
    nome: Optional[str] = Field(None, max_length=255)
    cnpj: Optional[str] = Field(None, max_length=18)
    contato_nome: Optional[str] = Field(None, max_length=100)
    contato_email: Optional[str] = Field(None, max_length=100)
    contato_telefone: Optional[str] = Field(None, max_length=20)
    endereco: Optional[str] = None


class Fornecedor(FornecedorBase):
    """Schema de resposta para fornecedor"""
    fornecedor_id: int
    criado_em: datetime
    atualizado_em: datetime
    
    class Config:
        from_attributes = True


# Schemas para LocalizacaoEstoque
class LocalizacaoEstoqueBase(BaseModel):
    """Schema base para localização de estoque"""
    nome: str = Field(..., max_length=100, description="Nome da localização")
    descricao: Optional[str] = Field(None, description="Descrição da localização")
    clinica_id: Optional[int] = Field(None, description="ID da clínica associada")


class LocalizacaoEstoqueCreate(LocalizacaoEstoqueBase):
    """Schema para criação de localização de estoque"""
    pass


class LocalizacaoEstoque(LocalizacaoEstoqueBase):
    """Schema de resposta para localização de estoque"""
    localizacao_id: int
    criado_em: datetime
    atualizado_em: datetime
    
    class Config:
        from_attributes = True


# Schemas para Produto
class ProdutoBase(BaseModel):
    """Schema base para produto"""
    nome: str = Field(..., max_length=100, description="Nome do produto")
    descricao: Optional[str] = Field(None, description="Descrição do produto")
    unidade: Optional[str] = Field(None, max_length=20, description="Unidade de medida")
    nivel_minimo_estoque: Optional[Decimal] = Field(0, description="Nível mínimo de estoque")
    codigo_barras: Optional[str] = Field(None, max_length=50, description="Código de barras")
    preco_custo: Optional[Decimal] = Field(None, description="Preço de custo")
    preco_venda: Optional[Decimal] = Field(None, description="Preço de venda")
    unidade_compra: Optional[str] = Field(None, max_length=20, description="Unidade de compra")
    fator_conversao: Optional[Decimal] = Field(1.0, description="Fator de conversão")


class ProdutoCreate(ProdutoBase):
    """Schema para criação de produto"""
    pass


class ProdutoUpdate(BaseModel):
    """Schema para atualização de produto"""
    nome: Optional[str] = Field(None, max_length=100)
    descricao: Optional[str] = None
    unidade: Optional[str] = Field(None, max_length=20)
    nivel_minimo_estoque: Optional[Decimal] = None
    codigo_barras: Optional[str] = Field(None, max_length=50)
    preco_custo: Optional[Decimal] = None
    preco_venda: Optional[Decimal] = None
    unidade_compra: Optional[str] = Field(None, max_length=20)
    fator_conversao: Optional[Decimal] = None


class Produto(ProdutoBase):
    """Schema de resposta para produto"""
    produto_id: int
    
    class Config:
        from_attributes = True


# Schemas para LoteProduto
class LoteProdutoBase(BaseModel):
    """Schema base para lote de produto"""
    numero_lote: str = Field(..., max_length=100, description="Número do lote")
    data_fabricacao: Optional[date] = Field(None, description="Data de fabricação")
    data_validade: Optional[date] = Field(None, description="Data de validade")
    quantidade_inicial: Decimal = Field(..., description="Quantidade inicial do lote")
    quantidade_atual: Decimal = Field(..., description="Quantidade atual do lote")


class LoteProdutoCreate(LoteProdutoBase):
    """Schema para criação de lote de produto"""
    produto_id: int = Field(..., description="ID do produto")
    fornecedor_id: Optional[int] = Field(None, description="ID do fornecedor")
    localizacao_id: Optional[int] = Field(None, description="ID da localização")


class LoteProduto(LoteProdutoBase):
    """Schema de resposta para lote de produto"""
    lote_id: UUID
    produto_id: int
    fornecedor_id: Optional[int]
    localizacao_id: Optional[int]
    criado_em: datetime
    atualizado_em: datetime
    
    # Relacionamentos
    produto: Optional[Produto] = None
    fornecedor: Optional[Fornecedor] = None
    localizacao: Optional[LocalizacaoEstoque] = None
    
    class Config:
        from_attributes = True


# Schemas para MovimentoEstoque
class MovimentoEstoqueBase(BaseModel):
    """Schema base para movimento de estoque"""
    quantidade: Decimal = Field(..., description="Quantidade movimentada")
    tipo_movimento: str = Field(..., description="Tipo de movimento (entrada/saida)")
    referencia: Optional[str] = Field(None, max_length=100, description="Referência do movimento")


class MovimentoEstoqueCreate(MovimentoEstoqueBase):
    """Schema para criação de movimento de estoque"""
    produto_id: int = Field(..., description="ID do produto")
    lote_id: Optional[UUID] = Field(None, description="ID do lote")
    localizacao_id: Optional[int] = Field(None, description="ID da localização")
    movimentado_por: Optional[UUID] = Field(None, description="ID do usuário que fez o movimento")


class MovimentoEstoque(MovimentoEstoqueBase):
    """Schema de resposta para movimento de estoque"""
    movimento_id: int
    produto_id: int
    lote_id: Optional[UUID]
    localizacao_id: Optional[int]
    movimentado_por: Optional[UUID]
    movimentado_em: datetime
    
    # Relacionamentos
    produto: Optional[Produto] = None
    lote: Optional[LoteProduto] = None
    localizacao: Optional[LocalizacaoEstoque] = None
    
    class Config:
        from_attributes = True


# Schemas para PedidoCompra
class ItemPedidoCompraBase(BaseModel):
    """Schema base para item de pedido de compra"""
    produto_id: int = Field(..., description="ID do produto")
    quantidade_pedida: Decimal = Field(..., description="Quantidade pedida")
    preco_unitario: Decimal = Field(..., description="Preço unitário")


class ItemPedidoCompraCreate(ItemPedidoCompraBase):
    """Schema para criação de item de pedido de compra"""
    pass


class ItemPedidoCompra(ItemPedidoCompraBase):
    """Schema de resposta para item de pedido de compra"""
    item_pedido_id: int
    pedido_id: UUID
    quantidade_recebida: Decimal
    criado_em: datetime
    
    # Relacionamentos
    produto: Optional[Produto] = None
    
    class Config:
        from_attributes = True


class PedidoCompraBase(BaseModel):
    """Schema base para pedido de compra"""
    data_entrega_prevista: Optional[date] = Field(None, description="Data prevista de entrega")
    observacoes: Optional[str] = Field(None, description="Observações do pedido")


class PedidoCompraCreate(PedidoCompraBase):
    """Schema para criação de pedido de compra"""
    fornecedor_id: int = Field(..., description="ID do fornecedor")
    itens: List[ItemPedidoCompraCreate] = Field(..., description="Itens do pedido")


class PedidoCompra(PedidoCompraBase):
    """Schema de resposta para pedido de compra"""
    pedido_id: UUID
    fornecedor_id: int
    data_pedido: datetime
    status: StatusPedidoEnum
    total_valor: Optional[Decimal]
    criado_por: Optional[UUID]
    criado_em: datetime
    atualizado_em: datetime
    
    # Relacionamentos
    fornecedor: Optional[Fornecedor] = None
    itens: List[ItemPedidoCompra] = []
    
    class Config:
        from_attributes = True


# Schemas para AjusteEstoque
class AjusteEstoqueBase(BaseModel):
    """Schema base para ajuste de estoque"""
    quantidade: Decimal = Field(..., description="Quantidade ajustada")
    tipo_ajuste: TipoAjusteEnum = Field(..., description="Tipo de ajuste")
    motivo: Optional[str] = Field(None, description="Motivo do ajuste")


class AjusteEstoqueCreate(AjusteEstoqueBase):
    """Schema para criação de ajuste de estoque"""
    produto_id: int = Field(..., description="ID do produto")
    lote_id: UUID = Field(..., description="ID do lote")
    localizacao_id: int = Field(..., description="ID da localização")
    ajustado_por: Optional[UUID] = Field(None, description="ID do usuário que fez o ajuste")


class AjusteEstoque(AjusteEstoqueBase):
    """Schema de resposta para ajuste de estoque"""
    ajuste_id: UUID
    produto_id: int
    lote_id: UUID
    localizacao_id: int
    ajustado_por: Optional[UUID]
    ajustado_em: datetime
    
    # Relacionamentos
    produto: Optional[Produto] = None
    lote: Optional[LoteProduto] = None
    localizacao: Optional[LocalizacaoEstoque] = None
    
    class Config:
        from_attributes = True


# Schemas para relatórios e consultas
class EstoquePorProduto(BaseModel):
    """Schema para consulta de estoque por produto"""
    produto_id: int
    nome_produto: str
    quantidade_total: Decimal
    nivel_minimo: Decimal
    status_estoque: str  # "normal", "baixo", "critico"
    
    class Config:
        from_attributes = True


class ProdutoProximoVencimento(BaseModel):
    """Schema para produtos próximos do vencimento"""
    produto_id: int
    nome_produto: str
    lote_id: UUID
    numero_lote: str
    data_validade: date
    quantidade_atual: Decimal
    dias_para_vencimento: int
    
    class Config:
        from_attributes = True

