from django.contrib import admin
from .models import (
    Fornecedor, LocalizacaoEstoque, Produto, LoteProduto, PedidoCompra, 
    ItemPedidoCompra, MovimentoEstoque, AjusteEstoque
)

@admin.register(Fornecedor)
class FornecedorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cnpj', 'contato_nome', 'contato_email', 'contato_telefone')
    search_fields = ('nome', 'cnpj', 'contato_nome')

@admin.register(LocalizacaoEstoque)
class LocalizacaoEstoqueAdmin(admin.ModelAdmin):
    list_display = ('nome', 'clinica', 'descricao')
    search_fields = ('nome', 'clinica__nome')
    list_filter = ('clinica',)

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'unidade', 'nivel_minimo_estoque', 'preco_venda')
    search_fields = ('nome', 'codigo_barras')
    list_filter = ('unidade',)

@admin.register(LoteProduto)
class LoteProdutoAdmin(admin.ModelAdmin):
    list_display = ('produto', 'numero_lote', 'quantidade_atual', 'data_validade', 'fornecedor', 'localizacao')
    search_fields = ('produto__nome', 'numero_lote', 'fornecedor__nome')
    list_filter = ('data_validade', 'fornecedor', 'localizacao')

@admin.register(PedidoCompra)
class PedidoCompraAdmin(admin.ModelAdmin):
    list_display = ('pedido_id', 'fornecedor', 'data_pedido', 'status', 'total_valor', 'criado_por')
    search_fields = ('pedido_id', 'fornecedor__nome', 'criado_por__username')
    list_filter = ('status', 'data_pedido')

@admin.register(ItemPedidoCompra)
class ItemPedidoCompraAdmin(admin.ModelAdmin):
    list_display = ('pedido', 'produto', 'quantidade_pedida', 'quantidade_recebida', 'preco_unitario')
    search_fields = ('pedido__pedido_id', 'produto__nome')

@admin.register(MovimentoEstoque)
class MovimentoEstoqueAdmin(admin.ModelAdmin):
    list_display = ('produto', 'quantidade', 'tipo_movimento', 'movimentado_em', 'movimentado_por')
    search_fields = ('produto__nome', 'referencia', 'movimentado_por__username')
    list_filter = ('tipo_movimento', 'movimentado_em')

@admin.register(AjusteEstoque)
class AjusteEstoqueAdmin(admin.ModelAdmin):
    list_display = ('produto', 'lote', 'localizacao', 'quantidade', 'tipo_ajuste', 'ajustado_por')
    search_fields = ('produto__nome', 'lote__numero_lote', 'ajustado_por__username')
    list_filter = ('tipo_ajuste', 'ajustado_em')