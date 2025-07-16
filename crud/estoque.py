"""
Operações CRUD para o módulo de estoque
"""
from typing import List, Optional
from datetime import date, datetime, timedelta
from decimal import Decimal
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func

from models.estoque import (
    Produto, LoteProduto, Fornecedor, LocalizacaoEstoque,
    MovimentoEstoque, PedidoCompra, ItemPedidoCompra, AjusteEstoque,
    StatusPedidoEnum, TipoAjusteEnum
)
from schemas.estoque import (
    ProdutoCreate, ProdutoUpdate,
    LoteProdutoCreate,
    FornecedorCreate, FornecedorUpdate,
    LocalizacaoEstoqueCreate,
    MovimentoEstoqueCreate,
    PedidoCompraCreate,
    AjusteEstoqueCreate
)


# CRUD para Produto
class CRUDProduto:
    """Operações CRUD para produtos"""
    
    def get(self, db: Session, produto_id: int) -> Optional[Produto]:
        """Buscar produto por ID"""
        return db.query(Produto).filter(Produto.produto_id == produto_id).first()
    
    def get_by_codigo_barras(self, db: Session, codigo_barras: str) -> Optional[Produto]:
        """Buscar produto por código de barras"""
        return db.query(Produto).filter(Produto.codigo_barras == codigo_barras).first()
    
    def get_multi(self, db: Session, skip: int = 0, limit: int = 100) -> List[Produto]:
        """Listar produtos com paginação"""
        return db.query(Produto).offset(skip).limit(limit).all()
    
    def search(self, db: Session, termo: str, skip: int = 0, limit: int = 100) -> List[Produto]:
        """Buscar produtos por nome ou descrição"""
        return db.query(Produto).filter(
            or_(
                Produto.nome.ilike(f"%{termo}%"),
                Produto.descricao.ilike(f"%{termo}%")
            )
        ).offset(skip).limit(limit).all()
    
    def create(self, db: Session, obj_in: ProdutoCreate) -> Produto:
        """Criar novo produto"""
        db_obj = Produto(**obj_in.dict())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def update(self, db: Session, db_obj: Produto, obj_in: ProdutoUpdate) -> Produto:
        """Atualizar produto"""
        update_data = obj_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def delete(self, db: Session, produto_id: int) -> Optional[Produto]:
        """Excluir produto"""
        obj = db.query(Produto).filter(Produto.produto_id == produto_id).first()
        if obj:
            db.delete(obj)
            db.commit()
        return obj
    
    def get_estoque_baixo(self, db: Session) -> List[Produto]:
        """Buscar produtos com estoque baixo"""
        # Subquery para calcular estoque atual por produto
        estoque_atual = db.query(
            LoteProduto.produto_id,
            func.sum(LoteProduto.quantidade_atual).label('total_estoque')
        ).group_by(LoteProduto.produto_id).subquery()
        
        return db.query(Produto).join(
            estoque_atual, Produto.produto_id == estoque_atual.c.produto_id
        ).filter(
            estoque_atual.c.total_estoque <= Produto.nivel_minimo_estoque
        ).all()


# CRUD para Fornecedor
class CRUDFornecedor:
    """Operações CRUD para fornecedores"""
    
    def get(self, db: Session, fornecedor_id: int) -> Optional[Fornecedor]:
        """Buscar fornecedor por ID"""
        return db.query(Fornecedor).filter(Fornecedor.fornecedor_id == fornecedor_id).first()
    
    def get_by_cnpj(self, db: Session, cnpj: str) -> Optional[Fornecedor]:
        """Buscar fornecedor por CNPJ"""
        return db.query(Fornecedor).filter(Fornecedor.cnpj == cnpj).first()
    
    def get_multi(self, db: Session, skip: int = 0, limit: int = 100) -> List[Fornecedor]:
        """Listar fornecedores com paginação"""
        return db.query(Fornecedor).offset(skip).limit(limit).all()
    
    def create(self, db: Session, obj_in: FornecedorCreate) -> Fornecedor:
        """Criar novo fornecedor"""
        db_obj = Fornecedor(**obj_in.dict())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def update(self, db: Session, db_obj: Fornecedor, obj_in: FornecedorUpdate) -> Fornecedor:
        """Atualizar fornecedor"""
        update_data = obj_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj


# CRUD para LocalizacaoEstoque
class CRUDLocalizacaoEstoque:
    """Operações CRUD para localizações de estoque"""
    
    def get(self, db: Session, localizacao_id: int) -> Optional[LocalizacaoEstoque]:
        """Buscar localização por ID"""
        return db.query(LocalizacaoEstoque).filter(
            LocalizacaoEstoque.localizacao_id == localizacao_id
        ).first()
    
    def get_multi(self, db: Session, skip: int = 0, limit: int = 100) -> List[LocalizacaoEstoque]:
        """Listar localizações com paginação"""
        return db.query(LocalizacaoEstoque).offset(skip).limit(limit).all()
    
    def create(self, db: Session, obj_in: LocalizacaoEstoqueCreate) -> LocalizacaoEstoque:
        """Criar nova localização"""
        db_obj = LocalizacaoEstoque(**obj_in.dict())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


# CRUD para LoteProduto
class CRUDLoteProduto:
    """Operações CRUD para lotes de produtos"""
    
    def get(self, db: Session, lote_id: UUID) -> Optional[LoteProduto]:
        """Buscar lote por ID"""
        return db.query(LoteProduto).filter(LoteProduto.lote_id == lote_id).first()
    
    def get_by_produto(self, db: Session, produto_id: int) -> List[LoteProduto]:
        """Buscar lotes por produto"""
        return db.query(LoteProduto).filter(LoteProduto.produto_id == produto_id).all()
    
    def get_proximos_vencimento(self, db: Session, dias: int = 30) -> List[LoteProduto]:
        """Buscar lotes próximos do vencimento"""
        data_limite = date.today() + timedelta(days=dias)
        return db.query(LoteProduto).filter(
            and_(
                LoteProduto.data_validade <= data_limite,
                LoteProduto.quantidade_atual > 0
            )
        ).all()
    
    def get_vencidos(self, db: Session) -> List[LoteProduto]:
        """Buscar lotes vencidos"""
        return db.query(LoteProduto).filter(
            and_(
                LoteProduto.data_validade < date.today(),
                LoteProduto.quantidade_atual > 0
            )
        ).all()
    
    def create(self, db: Session, obj_in: LoteProdutoCreate) -> LoteProduto:
        """Criar novo lote"""
        db_obj = LoteProduto(**obj_in.dict())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def atualizar_quantidade(self, db: Session, lote_id: UUID, nova_quantidade: Decimal) -> Optional[LoteProduto]:
        """Atualizar quantidade atual do lote"""
        lote = self.get(db, lote_id)
        if lote:
            lote.quantidade_atual = nova_quantidade
            db.commit()
            db.refresh(lote)
        return lote


# CRUD para MovimentoEstoque
class CRUDMovimentoEstoque:
    """Operações CRUD para movimentos de estoque"""
    
    def get_multi(self, db: Session, skip: int = 0, limit: int = 100) -> List[MovimentoEstoque]:
        """Listar movimentos com paginação"""
        return db.query(MovimentoEstoque).order_by(
            MovimentoEstoque.movimentado_em.desc()
        ).offset(skip).limit(limit).all()
    
    def get_by_produto(self, db: Session, produto_id: int) -> List[MovimentoEstoque]:
        """Buscar movimentos por produto"""
        return db.query(MovimentoEstoque).filter(
            MovimentoEstoque.produto_id == produto_id
        ).order_by(MovimentoEstoque.movimentado_em.desc()).all()
    
    def create(self, db: Session, obj_in: MovimentoEstoqueCreate) -> MovimentoEstoque:
        """Criar novo movimento de estoque"""
        db_obj = MovimentoEstoque(**obj_in.dict())
        db.add(db_obj)
        
        # Se for um movimento com lote, atualizar a quantidade do lote
        if obj_in.lote_id:
            lote = db.query(LoteProduto).filter(LoteProduto.lote_id == obj_in.lote_id).first()
            if lote:
                if obj_in.tipo_movimento == "entrada":
                    lote.quantidade_atual += obj_in.quantidade
                elif obj_in.tipo_movimento == "saida":
                    lote.quantidade_atual -= obj_in.quantidade
        
        db.commit()
        db.refresh(db_obj)
        return db_obj


# CRUD para PedidoCompra
class CRUDPedidoCompra:
    """Operações CRUD para pedidos de compra"""
    
    def get(self, db: Session, pedido_id: UUID) -> Optional[PedidoCompra]:
        """Buscar pedido por ID"""
        return db.query(PedidoCompra).filter(PedidoCompra.pedido_id == pedido_id).first()
    
    def get_multi(self, db: Session, skip: int = 0, limit: int = 100) -> List[PedidoCompra]:
        """Listar pedidos com paginação"""
        return db.query(PedidoCompra).order_by(
            PedidoCompra.data_pedido.desc()
        ).offset(skip).limit(limit).all()
    
    def get_by_status(self, db: Session, status: StatusPedidoEnum) -> List[PedidoCompra]:
        """Buscar pedidos por status"""
        return db.query(PedidoCompra).filter(PedidoCompra.status == status).all()
    
    def create(self, db: Session, obj_in: PedidoCompraCreate) -> PedidoCompra:
        """Criar novo pedido de compra"""
        # Calcular total do pedido
        total_valor = sum(item.quantidade_pedida * item.preco_unitario for item in obj_in.itens)
        
        # Criar pedido
        pedido_data = obj_in.dict(exclude={'itens'})
        pedido_data['total_valor'] = total_valor
        db_pedido = PedidoCompra(**pedido_data)
        db.add(db_pedido)
        db.flush()  # Para obter o ID do pedido
        
        # Criar itens do pedido
        for item_data in obj_in.itens:
            item_dict = item_data.dict()
            item_dict['pedido_id'] = db_pedido.pedido_id
            db_item = ItemPedidoCompra(**item_dict)
            db.add(db_item)
        
        db.commit()
        db.refresh(db_pedido)
        return db_pedido
    
    def atualizar_status(self, db: Session, pedido_id: UUID, novo_status: StatusPedidoEnum) -> Optional[PedidoCompra]:
        """Atualizar status do pedido"""
        pedido = self.get(db, pedido_id)
        if pedido:
            pedido.status = novo_status
            db.commit()
            db.refresh(pedido)
        return pedido


# CRUD para AjusteEstoque
class CRUDAjusteEstoque:
    """Operações CRUD para ajustes de estoque"""
    
    def get_multi(self, db: Session, skip: int = 0, limit: int = 100) -> List[AjusteEstoque]:
        """Listar ajustes com paginação"""
        return db.query(AjusteEstoque).order_by(
            AjusteEstoque.ajustado_em.desc()
        ).offset(skip).limit(limit).all()
    
    def create(self, db: Session, obj_in: AjusteEstoqueCreate) -> AjusteEstoque:
        """Criar novo ajuste de estoque"""
        db_obj = AjusteEstoque(**obj_in.dict())
        db.add(db_obj)
        
        # Atualizar quantidade do lote
        lote = db.query(LoteProduto).filter(LoteProduto.lote_id == obj_in.lote_id).first()
        if lote:
            if obj_in.tipo_ajuste in [TipoAjusteEnum.ENTRADA_INVENTARIO, TipoAjusteEnum.OUTROS_ENTRADA]:
                lote.quantidade_atual += obj_in.quantidade
            else:
                lote.quantidade_atual -= obj_in.quantidade
        
        # Criar movimento de estoque correspondente
        tipo_movimento = "entrada" if obj_in.tipo_ajuste in [
            TipoAjusteEnum.ENTRADA_INVENTARIO, TipoAjusteEnum.OUTROS_ENTRADA
        ] else "saida"
        
        movimento = MovimentoEstoque(
            produto_id=obj_in.produto_id,
            quantidade=obj_in.quantidade,
            tipo_movimento=tipo_movimento,
            referencia=f"Ajuste: {obj_in.tipo_ajuste.value}",
            lote_id=obj_in.lote_id,
            localizacao_id=obj_in.localizacao_id,
            movimentado_por=obj_in.ajustado_por
        )
        db.add(movimento)
        
        db.commit()
        db.refresh(db_obj)
        return db_obj


# Instâncias dos CRUDs
crud_produto = CRUDProduto()
crud_fornecedor = CRUDFornecedor()
crud_localizacao_estoque = CRUDLocalizacaoEstoque()
crud_lote_produto = CRUDLoteProduto()
crud_movimento_estoque = CRUDMovimentoEstoque()
crud_pedido_compra = CRUDPedidoCompra()
crud_ajuste_estoque = CRUDAjusteEstoque()

