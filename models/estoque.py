"""
Modelos SQLAlchemy para o módulo de estoque
"""
from sqlalchemy import Column, Integer, String, Text, Numeric, Date, DateTime, Boolean, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum

from database.base import Base


class StatusPedidoEnum(enum.Enum):
    """Enum para status de pedidos de compra"""
    PENDENTE = "pendente"
    APROVADO = "aprovado"
    RECEBIDO_PARCIAL = "recebido_parcial"
    RECEBIDO_TOTAL = "recebido_total"
    CANCELADO = "cancelado"


class TipoAjusteEnum(enum.Enum):
    """Enum para tipos de ajuste de estoque"""
    ENTRADA_INVENTARIO = "entrada_inventario"
    SAIDA_INVENTARIO = "saida_inventario"
    PERDA = "perda"
    QUEBRA = "quebra"
    DEVOLUCAO_FORNECEDOR = "devolucao_fornecedor"
    OUTROS_ENTRADA = "outros_entrada"
    OUTROS_SAIDA = "outros_saida"


class Fornecedor(Base):
    """Modelo para fornecedores"""
    __tablename__ = "fornecedores"
    
    fornecedor_id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), unique=True, nullable=False, index=True)
    cnpj = Column(String(18), unique=True, nullable=True)
    contato_nome = Column(String(100), nullable=True)
    contato_email = Column(String(100), nullable=True)
    contato_telefone = Column(String(20), nullable=True)
    endereco = Column(Text, nullable=True)
    criado_em = Column(DateTime(timezone=True), server_default=func.now())
    atualizado_em = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relacionamentos
    lotes = relationship("LoteProduto", back_populates="fornecedor")
    pedidos_compra = relationship("PedidoCompra", back_populates="fornecedor")


class LocalizacaoEstoque(Base):
    """Modelo para localizações de estoque"""
    __tablename__ = "localizacoes_estoque"
    
    localizacao_id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), unique=True, nullable=False, index=True)
    descricao = Column(Text, nullable=True)
    clinica_id = Column(Integer, nullable=True)  # FK para clinicas (não implementada aqui)
    criado_em = Column(DateTime(timezone=True), server_default=func.now())
    atualizado_em = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relacionamentos
    lotes = relationship("LoteProduto", back_populates="localizacao")
    movimentos = relationship("MovimentoEstoque", back_populates="localizacao")
    ajustes = relationship("AjusteEstoque", back_populates="localizacao")


class Produto(Base):
    """Modelo para produtos"""
    __tablename__ = "produtos"
    
    produto_id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False, index=True)
    descricao = Column(Text, nullable=True)
    unidade = Column(String(20), nullable=True)
    nivel_minimo_estoque = Column(Numeric(10, 2), default=0)
    codigo_barras = Column(String(50), unique=True, nullable=True)
    preco_custo = Column(Numeric(10, 2), nullable=True)
    preco_venda = Column(Numeric(10, 2), nullable=True)
    unidade_compra = Column(String(20), nullable=True)
    fator_conversao = Column(Numeric(10, 4), default=1.0)
    
    # Relacionamentos
    lotes = relationship("LoteProduto", back_populates="produto")
    movimentos = relationship("MovimentoEstoque", back_populates="produto")
    itens_pedido = relationship("ItemPedidoCompra", back_populates="produto")
    ajustes = relationship("AjusteEstoque", back_populates="produto")


class LoteProduto(Base):
    """Modelo para lotes de produtos"""
    __tablename__ = "lotes_produtos"
    
    lote_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    produto_id = Column(Integer, ForeignKey("produtos.produto_id"), nullable=False)
    numero_lote = Column(String(100), nullable=False)
    data_fabricacao = Column(Date, nullable=True)
    data_validade = Column(Date, nullable=True)
    quantidade_inicial = Column(Numeric(10, 2), nullable=False)
    quantidade_atual = Column(Numeric(10, 2), nullable=False)
    fornecedor_id = Column(Integer, ForeignKey("fornecedores.fornecedor_id"), nullable=True)
    localizacao_id = Column(Integer, ForeignKey("localizacoes_estoque.localizacao_id"), nullable=True)
    criado_em = Column(DateTime(timezone=True), server_default=func.now())
    atualizado_em = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relacionamentos
    produto = relationship("Produto", back_populates="lotes")
    fornecedor = relationship("Fornecedor", back_populates="lotes")
    localizacao = relationship("LocalizacaoEstoque", back_populates="lotes")
    movimentos = relationship("MovimentoEstoque", back_populates="lote")
    ajustes = relationship("AjusteEstoque", back_populates="lote")


class PedidoCompra(Base):
    """Modelo para pedidos de compra"""
    __tablename__ = "pedidos_compra"
    
    pedido_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    fornecedor_id = Column(Integer, ForeignKey("fornecedores.fornecedor_id"), nullable=False)
    data_pedido = Column(DateTime(timezone=True), server_default=func.now())
    data_entrega_prevista = Column(Date, nullable=True)
    status = Column(Enum(StatusPedidoEnum), default=StatusPedidoEnum.PENDENTE)
    total_valor = Column(Numeric(10, 2), nullable=True)
    observacoes = Column(Text, nullable=True)
    criado_por = Column(UUID(as_uuid=True), nullable=True)  # FK para usuarios (não implementada aqui)
    criado_em = Column(DateTime(timezone=True), server_default=func.now())
    atualizado_em = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relacionamentos
    fornecedor = relationship("Fornecedor", back_populates="pedidos_compra")
    itens = relationship("ItemPedidoCompra", back_populates="pedido")


class ItemPedidoCompra(Base):
    """Modelo para itens de pedidos de compra"""
    __tablename__ = "itens_pedido_compra"
    
    item_pedido_id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(UUID(as_uuid=True), ForeignKey("pedidos_compra.pedido_id"), nullable=False)
    produto_id = Column(Integer, ForeignKey("produtos.produto_id"), nullable=False)
    quantidade_pedida = Column(Numeric(10, 2), nullable=False)
    quantidade_recebida = Column(Numeric(10, 2), default=0)
    preco_unitario = Column(Numeric(10, 2), nullable=False)
    criado_em = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relacionamentos
    pedido = relationship("PedidoCompra", back_populates="itens")
    produto = relationship("Produto", back_populates="itens_pedido")


class MovimentoEstoque(Base):
    """Modelo para movimentos de estoque"""
    __tablename__ = "movimentos_estoque"
    
    movimento_id = Column(Integer, primary_key=True, index=True)
    produto_id = Column(Integer, ForeignKey("produtos.produto_id"), nullable=False)
    quantidade = Column(Numeric(10, 2), nullable=False)
    tipo_movimento = Column(String(10), nullable=False)  # 'entrada' ou 'saida'
    referencia = Column(String(100), nullable=True)
    movimentado_em = Column(DateTime(timezone=True), server_default=func.now())
    movimentado_por = Column(UUID(as_uuid=True), nullable=True)  # FK para usuarios
    lote_id = Column(UUID(as_uuid=True), ForeignKey("lotes_produtos.lote_id"), nullable=True)
    localizacao_id = Column(Integer, ForeignKey("localizacoes_estoque.localizacao_id"), nullable=True)
    
    # Relacionamentos
    produto = relationship("Produto", back_populates="movimentos")
    lote = relationship("LoteProduto", back_populates="movimentos")
    localizacao = relationship("LocalizacaoEstoque", back_populates="movimentos")


class AjusteEstoque(Base):
    """Modelo para ajustes de estoque"""
    __tablename__ = "ajustes_estoque"
    
    ajuste_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    produto_id = Column(Integer, ForeignKey("produtos.produto_id"), nullable=False)
    lote_id = Column(UUID(as_uuid=True), ForeignKey("lotes_produtos.lote_id"), nullable=False)
    localizacao_id = Column(Integer, ForeignKey("localizacoes_estoque.localizacao_id"), nullable=False)
    quantidade = Column(Numeric(10, 2), nullable=False)
    tipo_ajuste = Column(Enum(TipoAjusteEnum), nullable=False)
    motivo = Column(Text, nullable=True)
    ajustado_por = Column(UUID(as_uuid=True), nullable=True)  # FK para usuarios
    ajustado_em = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relacionamentos
    produto = relationship("Produto", back_populates="ajustes")
    lote = relationship("LoteProduto", back_populates="ajustes")
    localizacao = relationship("LocalizacaoEstoque", back_populates="ajustes")

