"""
Endpoints da API para o módulo de estoque
"""
from typing import List, Optional, Dict, Any
from datetime import date
from decimal import Decimal
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from database.session import get_db
from crud.estoque import (
    crud_produto, crud_fornecedor, crud_localizacao_estoque,
    crud_lote_produto, crud_movimento_estoque, crud_pedido_compra
)
from schemas.estoque import (
    Produto, ProdutoCreate, ProdutoUpdate,
    Fornecedor, FornecedorCreate, FornecedorUpdate,
    LocalizacaoEstoque, LocalizacaoEstoqueCreate,
    LoteProduto, LoteProdutoCreate,
    MovimentoEstoque, MovimentoEstoqueCreate,
    PedidoCompra, PedidoCompraCreate,
    AjusteEstoque, AjusteEstoqueCreate,
    EstoquePorProduto, ProdutoProximoVencimento
)
from services.estoque_service import estoque_service

router = APIRouter()


# Endpoints para Produtos
@router.get("/produtos/", response_model=List[Produto])
def listar_produtos(
    skip: int = 0,
    limit: int = 100,
    termo_busca: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Listar produtos com opção de busca"""
    if termo_busca:
        return crud_produto.search(db, termo_busca, skip=skip, limit=limit)
    return crud_produto.get_multi(db, skip=skip, limit=limit)


@router.get("/produtos/{produto_id}", response_model=Produto)
def obter_produto(produto_id: int, db: Session = Depends(get_db)):
    """Obter produto por ID"""
    produto = crud_produto.get(db, produto_id)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return produto


@router.post("/produtos/", response_model=Produto)
def criar_produto(produto: ProdutoCreate, db: Session = Depends(get_db)):
    """Criar novo produto"""
    # Verificar se código de barras já existe
    if produto.codigo_barras:
        produto_existente = crud_produto.get_by_codigo_barras(db, produto.codigo_barras)
        if produto_existente:
            raise HTTPException(
                status_code=400,
                detail="Produto com este código de barras já existe"
            )
    
    return crud_produto.create(db, produto)


@router.put("/produtos/{produto_id}", response_model=Produto)
def atualizar_produto(
    produto_id: int,
    produto_update: ProdutoUpdate,
    db: Session = Depends(get_db)
):
    """Atualizar produto"""
    produto = crud_produto.get(db, produto_id)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    return crud_produto.update(db, produto, produto_update)


@router.delete("/produtos/{produto_id}")
def excluir_produto(produto_id: int, db: Session = Depends(get_db)):
    """Excluir produto"""
    produto = crud_produto.delete(db, produto_id)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return {"message": "Produto excluído com sucesso"}


@router.get("/produtos/estoque-baixo/", response_model=List[Produto])
def produtos_estoque_baixo(db: Session = Depends(get_db)):
    """Listar produtos com estoque baixo"""
    return crud_produto.get_estoque_baixo(db)


# Endpoints para Fornecedores
@router.get("/fornecedores/", response_model=List[Fornecedor])
def listar_fornecedores(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Listar fornecedores"""
    return crud_fornecedor.get_multi(db, skip=skip, limit=limit)


@router.get("/fornecedores/{fornecedor_id}", response_model=Fornecedor)
def obter_fornecedor(fornecedor_id: int, db: Session = Depends(get_db)):
    """Obter fornecedor por ID"""
    fornecedor = crud_fornecedor.get(db, fornecedor_id)
    if not fornecedor:
        raise HTTPException(status_code=404, detail="Fornecedor não encontrado")
    return fornecedor


@router.post("/fornecedores/", response_model=Fornecedor)
def criar_fornecedor(fornecedor: FornecedorCreate, db: Session = Depends(get_db)):
    """Criar novo fornecedor"""
    # Verificar se CNPJ já existe
    if fornecedor.cnpj:
        fornecedor_existente = crud_fornecedor.get_by_cnpj(db, fornecedor.cnpj)
        if fornecedor_existente:
            raise HTTPException(
                status_code=400,
                detail="Fornecedor com este CNPJ já existe"
            )
    
    return crud_fornecedor.create(db, fornecedor)


@router.put("/fornecedores/{fornecedor_id}", response_model=Fornecedor)
def atualizar_fornecedor(
    fornecedor_id: int,
    fornecedor_update: FornecedorUpdate,
    db: Session = Depends(get_db)
):
    """Atualizar fornecedor"""
    fornecedor = crud_fornecedor.get(db, fornecedor_id)
    if not fornecedor:
        raise HTTPException(status_code=404, detail="Fornecedor não encontrado")
    
    return crud_fornecedor.update(db, fornecedor, fornecedor_update)


# Endpoints para Localizações de Estoque
@router.get("/localizacoes/", response_model=List[LocalizacaoEstoque])
def listar_localizacoes(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Listar localizações de estoque"""
    return crud_localizacao_estoque.get_multi(db, skip=skip, limit=limit)


@router.post("/localizacoes/", response_model=LocalizacaoEstoque)
def criar_localizacao(
    localizacao: LocalizacaoEstoqueCreate,
    db: Session = Depends(get_db)
):
    """Criar nova localização de estoque"""
    return crud_localizacao_estoque.create(db, localizacao)


# Endpoints para Lotes de Produtos
@router.get("/lotes/", response_model=List[LoteProduto])
def listar_lotes(
    produto_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Listar lotes de produtos"""
    if produto_id:
        return crud_lote_produto.get_by_produto(db, produto_id)
    # Implementar listagem geral se necessário
    return []


@router.get("/lotes/{lote_id}", response_model=LoteProduto)
def obter_lote(lote_id: UUID, db: Session = Depends(get_db)):
    """Obter lote por ID"""
    lote = crud_lote_produto.get(db, lote_id)
    if not lote:
        raise HTTPException(status_code=404, detail="Lote não encontrado")
    return lote


@router.post("/lotes/", response_model=LoteProduto)
def criar_lote(lote: LoteProdutoCreate, db: Session = Depends(get_db)):
    """Criar novo lote de produto"""
    # Verificar se produto existe
    produto = crud_produto.get(db, lote.produto_id)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    return crud_lote_produto.create(db, lote)


@router.get("/lotes/proximo-vencimento/", response_model=List[ProdutoProximoVencimento])
def lotes_proximo_vencimento(
    dias: int = Query(30, description="Número de dias para considerar próximo do vencimento"),
    db: Session = Depends(get_db)
):
    """Listar produtos próximos do vencimento"""
    return estoque_service.get_produtos_proximo_vencimento(db, dias)


@router.get("/lotes/vencidos/", response_model=List[LoteProduto])
def lotes_vencidos(db: Session = Depends(get_db)):
    """Listar lotes vencidos"""
    return crud_lote_produto.get_vencidos(db)


# Endpoints para Movimentos de Estoque
@router.get("/movimentos/", response_model=List[MovimentoEstoque])
def listar_movimentos(
    skip: int = 0,
    limit: int = 100,
    produto_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Listar movimentos de estoque"""
    if produto_id:
        return crud_movimento_estoque.get_by_produto(db, produto_id)
    return crud_movimento_estoque.get_multi(db, skip=skip, limit=limit)


@router.post("/movimentos/entrada/", response_model=Dict[str, Any])
def registrar_entrada_estoque(
    produto_id: int,
    quantidade: Decimal,
    numero_lote: str,
    data_validade: Optional[date] = None,
    fornecedor_id: Optional[int] = None,
    localizacao_id: Optional[int] = None,
    preco_custo: Optional[Decimal] = None,
    db: Session = Depends(get_db)
):
    """Registrar entrada de estoque"""
    try:
        lote = estoque_service.registrar_entrada_estoque(
            db=db,
            produto_id=produto_id,
            quantidade=quantidade,
            numero_lote=numero_lote,
            data_validade=data_validade,
            fornecedor_id=fornecedor_id,
            localizacao_id=localizacao_id,
            preco_custo=preco_custo
        )
        return {
            "message": "Entrada registrada com sucesso",
            "lote_id": str(lote.lote_id),
            "quantidade": quantidade
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/movimentos/saida/", response_model=Dict[str, Any])
def registrar_saida_estoque(
    produto_id: int,
    quantidade: Decimal,
    lote_id: Optional[UUID] = None,
    localizacao_id: Optional[int] = None,
    referencia: str = "Consumo",
    db: Session = Depends(get_db)
):
    """Registrar saída de estoque"""
    sucesso = estoque_service.registrar_saida_estoque(
        db=db,
        produto_id=produto_id,
        quantidade=quantidade,
        lote_id=lote_id,
        localizacao_id=localizacao_id,
        referencia=referencia
    )
    
    if not sucesso:
        raise HTTPException(
            status_code=400,
            detail="Estoque insuficiente para realizar a saída"
        )
    
    return {
        "message": "Saída registrada com sucesso",
        "quantidade": quantidade
    }


# Endpoints para Pedidos de Compra
@router.get("/pedidos/", response_model=List[PedidoCompra])
def listar_pedidos(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Listar pedidos de compra"""
    return crud_pedido_compra.get_multi(db, skip=skip, limit=limit)


@router.get("/pedidos/{pedido_id}", response_model=PedidoCompra)
def obter_pedido(pedido_id: UUID, db: Session = Depends(get_db)):
    """Obter pedido de compra por ID"""
    pedido = crud_pedido_compra.get(db, pedido_id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return pedido


@router.post("/pedidos/", response_model=PedidoCompra)
def criar_pedido(pedido: PedidoCompraCreate, db: Session = Depends(get_db)):
    """Criar novo pedido de compra"""
    # Verificar se fornecedor existe
    fornecedor = crud_fornecedor.get(db, pedido.fornecedor_id)
    if not fornecedor:
        raise HTTPException(status_code=404, detail="Fornecedor não encontrado")
    
    return crud_pedido_compra.create(db, pedido)


# Endpoints para Ajustes de Estoque
@router.post("/ajustes/", response_model=AjusteEstoque)
def criar_ajuste(ajuste: AjusteEstoqueCreate, db: Session = Depends(get_db)):
    """Criar ajuste de estoque"""
    return crud_ajuste_estoque.create(db, ajuste)


# Endpoints para Relatórios
@router.get("/relatorios/estoque-consolidado/", response_model=List[EstoquePorProduto])
def relatorio_estoque_consolidado(db: Session = Depends(get_db)):
    """Relatório de estoque consolidado por produto"""
    return estoque_service.get_estoque_consolidado(db)


@router.post("/inventario/", response_model=List[Dict[str, Any]])
def realizar_inventario(
    inventario_data: List[Dict[str, Any]],
    db: Session = Depends(get_db)
):
    """Realizar inventário e ajustar diferenças"""
    return estoque_service.realizar_inventario(db, inventario_data)


@router.get("/relatorios/giro-estoque/", response_model=List[Dict[str, Any]])
def relatorio_giro_estoque(
    data_inicio: date,
    data_fim: date,
    db: Session = Depends(get_db)
):
    """Relatório de giro de estoque"""
    return estoque_service.get_relatorio_giro_estoque(db, data_inicio, data_fim)


@router.post("/transferencia/", response_model=Dict[str, Any])
def transferir_estoque(
    lote_id: UUID,
    localizacao_origem_id: int,
    localizacao_destino_id: int,
    quantidade: Decimal,
    db: Session = Depends(get_db)
):
    """Transferir estoque entre localizações"""
    sucesso = estoque_service.transferir_estoque(
        db=db,
        lote_id=lote_id,
        localizacao_origem_id=localizacao_origem_id,
        localizacao_destino_id=localizacao_destino_id,
        quantidade=quantidade
    )
    
    if not sucesso:
        raise HTTPException(
            status_code=400,
            detail="Não foi possível realizar a transferência"
        )
    
    return {"message": "Transferência realizada com sucesso"}

