"""
Serviço de estoque com lógica de negócios
"""
from typing import List, Optional, Dict, Any
from datetime import date, datetime, timedelta
from decimal import Decimal
from uuid import UUID
from sqlalchemy.orm import Session

from crud.estoque import (
    crud_produto, crud_fornecedor, crud_localizacao_estoque,
    crud_lote_produto, crud_movimento_estoque, crud_pedido_compra,
    crud_ajuste_estoque
)
from schemas.estoque import (
    ProdutoCreate, ProdutoUpdate, Produto,
    LoteProdutoCreate, LoteProduto,
    MovimentoEstoqueCreate,
    EstoquePorProduto, ProdutoProximoVencimento
)
from models.estoque import StatusPedidoEnum, TipoAjusteEnum


class EstoqueService:
    """Serviço para lógica de negócios do estoque"""
    
    def __init__(self):
        pass
    
    def get_estoque_consolidado(self, db: Session) -> List[EstoquePorProduto]:
        """
        Retorna o estoque consolidado por produto
        """
        produtos = crud_produto.get_multi(db)
        resultado = []
        
        for produto in produtos:
            lotes = crud_lote_produto.get_by_produto(db, produto.produto_id)
            quantidade_total = sum(lote.quantidade_atual for lote in lotes)
            
            # Determinar status do estoque
            if quantidade_total <= 0:
                status = "critico"
            elif quantidade_total <= produto.nivel_minimo_estoque:
                status = "baixo"
            else:
                status = "normal"
            
            estoque_produto = EstoquePorProduto(
                produto_id=produto.produto_id,
                nome_produto=produto.nome,
                quantidade_total=quantidade_total,
                nivel_minimo=produto.nivel_minimo_estoque,
                status_estoque=status
            )
            resultado.append(estoque_produto)
        
        return resultado
    
    def get_produtos_proximo_vencimento(self, db: Session, dias: int = 30) -> List[ProdutoProximoVencimento]:
        """
        Retorna produtos próximos do vencimento
        """
        lotes_proximos = crud_lote_produto.get_proximos_vencimento(db, dias)
        resultado = []
        
        for lote in lotes_proximos:
            produto = crud_produto.get(db, lote.produto_id)
            if produto:
                dias_para_vencimento = (lote.data_validade - date.today()).days
                
                produto_vencimento = ProdutoProximoVencimento(
                    produto_id=produto.produto_id,
                    nome_produto=produto.nome,
                    lote_id=lote.lote_id,
                    numero_lote=lote.numero_lote,
                    data_validade=lote.data_validade,
                    quantidade_atual=lote.quantidade_atual,
                    dias_para_vencimento=dias_para_vencimento
                )
                resultado.append(produto_vencimento)
        
        return resultado
    
    def registrar_entrada_estoque(
        self,
        db: Session,
        produto_id: int,
        quantidade: Decimal,
        numero_lote: str,
        data_validade: Optional[date] = None,
        fornecedor_id: Optional[int] = None,
        localizacao_id: Optional[int] = None,
        preco_custo: Optional[Decimal] = None,
        usuario_id: Optional[UUID] = None
    ) -> LoteProduto:
        """
        Registra entrada de estoque criando um novo lote
        """
        # Criar novo lote
        lote_data = LoteProdutoCreate(
            produto_id=produto_id,
            numero_lote=numero_lote,
            data_validade=data_validade,
            quantidade_inicial=quantidade,
            quantidade_atual=quantidade,
            fornecedor_id=fornecedor_id,
            localizacao_id=localizacao_id
        )
        lote = crud_lote_produto.create(db, lote_data)
        
        # Registrar movimento de estoque
        movimento_data = MovimentoEstoqueCreate(
            produto_id=produto_id,
            quantidade=quantidade,
            tipo_movimento="entrada",
            referencia=f"Entrada - Lote {numero_lote}",
            lote_id=lote.lote_id,
            localizacao_id=localizacao_id,
            movimentado_por=usuario_id
        )
        crud_movimento_estoque.create(db, movimento_data)
        
        # Atualizar preço de custo do produto se fornecido
        if preco_custo:
            produto = crud_produto.get(db, produto_id)
            if produto:
                produto_update = ProdutoUpdate(preco_custo=preco_custo)
                crud_produto.update(db, produto, produto_update)
        
        return lote
    
    def registrar_saida_estoque(
        self,
        db: Session,
        produto_id: int,
        quantidade: Decimal,
        lote_id: Optional[UUID] = None,
        localizacao_id: Optional[int] = None,
        referencia: str = "Consumo",
        usuario_id: Optional[UUID] = None
    ) -> bool:
        """
        Registra saída de estoque usando FIFO (First In, First Out)
        """
        if lote_id:
            # Saída de lote específico
            lote = crud_lote_produto.get(db, lote_id)
            if not lote or lote.quantidade_atual < quantidade:
                return False
            
            # Registrar movimento
            movimento_data = MovimentoEstoqueCreate(
                produto_id=produto_id,
                quantidade=quantidade,
                tipo_movimento="saida",
                referencia=referencia,
                lote_id=lote_id,
                localizacao_id=localizacao_id,
                movimentado_por=usuario_id
            )
            crud_movimento_estoque.create(db, movimento_data)
            return True
        
        else:
            # Saída automática usando FIFO
            lotes = crud_lote_produto.get_by_produto(db, produto_id)
            lotes_disponiveis = [l for l in lotes if l.quantidade_atual > 0]
            lotes_disponiveis.sort(key=lambda x: x.data_validade or date.max)
            
            quantidade_restante = quantidade
            
            for lote in lotes_disponiveis:
                if quantidade_restante <= 0:
                    break
                
                quantidade_usar = min(quantidade_restante, lote.quantidade_atual)
                
                # Registrar movimento
                movimento_data = MovimentoEstoqueCreate(
                    produto_id=produto_id,
                    quantidade=quantidade_usar,
                    tipo_movimento="saida",
                    referencia=referencia,
                    lote_id=lote.lote_id,
                    localizacao_id=localizacao_id,
                    movimentado_por=usuario_id
                )
                crud_movimento_estoque.create(db, movimento_data)
                
                quantidade_restante -= quantidade_usar
            
            return quantidade_restante <= 0
    
    def transferir_estoque(
        self,
        db: Session,
        lote_id: UUID,
        localizacao_origem_id: int,
        localizacao_destino_id: int,
        quantidade: Decimal,
        usuario_id: Optional[UUID] = None
    ) -> bool:
        """
        Transfere estoque entre localizações
        """
        lote = crud_lote_produto.get(db, lote_id)
        if not lote or lote.quantidade_atual < quantidade:
            return False
        
        # Registrar saída da localização origem
        movimento_saida = MovimentoEstoqueCreate(
            produto_id=lote.produto_id,
            quantidade=quantidade,
            tipo_movimento="saida",
            referencia=f"Transferência para localização {localizacao_destino_id}",
            lote_id=lote_id,
            localizacao_id=localizacao_origem_id,
            movimentado_por=usuario_id
        )
        crud_movimento_estoque.create(db, movimento_saida)
        
        # Registrar entrada na localização destino
        movimento_entrada = MovimentoEstoqueCreate(
            produto_id=lote.produto_id,
            quantidade=quantidade,
            tipo_movimento="entrada",
            referencia=f"Transferência da localização {localizacao_origem_id}",
            lote_id=lote_id,
            localizacao_id=localizacao_destino_id,
            movimentado_por=usuario_id
        )
        crud_movimento_estoque.create(db, movimento_entrada)
        
        return True
    
    def realizar_inventario(
        self,
        db: Session,
        inventario_data: List[Dict[str, Any]],
        usuario_id: Optional[UUID] = None
    ) -> List[Dict[str, Any]]:
        """
        Realiza inventário e ajusta diferenças
        inventario_data: [{"lote_id": UUID, "quantidade_contada": Decimal}, ...]
        """
        resultados = []
        
        for item in inventario_data:
            lote_id = item["lote_id"]
            quantidade_contada = item["quantidade_contada"]
            
            lote = crud_lote_produto.get(db, lote_id)
            if not lote:
                continue
            
            diferenca = quantidade_contada - lote.quantidade_atual
            
            if diferenca != 0:
                # Determinar tipo de ajuste
                if diferenca > 0:
                    tipo_ajuste = TipoAjusteEnum.ENTRADA_INVENTARIO
                else:
                    tipo_ajuste = TipoAjusteEnum.SAIDA_INVENTARIO
                    diferenca = abs(diferenca)
                
                # Criar ajuste
                ajuste_data = {
                    "produto_id": lote.produto_id,
                    "lote_id": lote_id,
                    "localizacao_id": lote.localizacao_id,
                    "quantidade": diferenca,
                    "tipo_ajuste": tipo_ajuste,
                    "motivo": "Ajuste por inventário",
                    "ajustado_por": usuario_id
                }
                
                crud_ajuste_estoque.create(db, ajuste_data)
                
                resultados.append({
                    "lote_id": lote_id,
                    "produto_nome": lote.produto.nome if lote.produto else "N/A",
                    "quantidade_sistema": lote.quantidade_atual,
                    "quantidade_contada": quantidade_contada,
                    "diferenca": quantidade_contada - lote.quantidade_atual,
                    "ajustado": True
                })
            else:
                resultados.append({
                    "lote_id": lote_id,
                    "produto_nome": lote.produto.nome if lote.produto else "N/A",
                    "quantidade_sistema": lote.quantidade_atual,
                    "quantidade_contada": quantidade_contada,
                    "diferenca": 0,
                    "ajustado": False
                })
        
        return resultados
    
    def get_relatorio_giro_estoque(
        self,
        db: Session,
        data_inicio: date,
        data_fim: date
    ) -> List[Dict[str, Any]]:
        """
        Gera relatório de giro de estoque por produto
        """
        # Esta é uma implementação simplificada
        # Em um sistema real, seria necessário calcular o giro baseado em vendas/consumo
        produtos = crud_produto.get_multi(db)
        resultado = []
        
        for produto in produtos:
            movimentos = crud_movimento_estoque.get_by_produto(db, produto.produto_id)
            movimentos_periodo = [
                m for m in movimentos
                if data_inicio <= m.movimentado_em.date() <= data_fim
            ]
            
            total_saidas = sum(
                m.quantidade for m in movimentos_periodo
                if m.tipo_movimento == "saida"
            )
            
            lotes = crud_lote_produto.get_by_produto(db, produto.produto_id)
            estoque_medio = sum(l.quantidade_atual for l in lotes) / 2 if lotes else 0
            
            giro = total_saidas / estoque_medio if estoque_medio > 0 else 0
            
            resultado.append({
                "produto_id": produto.produto_id,
                "nome_produto": produto.nome,
                "total_saidas": total_saidas,
                "estoque_medio": estoque_medio,
                "giro_estoque": giro
            })
        
        return resultado


# Instância do serviço
estoque_service = EstoqueService()

