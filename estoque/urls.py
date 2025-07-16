from django.urls import path
from . import views

urlpatterns = [
    path('produtos/', views.produto_list, name='produto_list'),
    path('produtos/<int:pk>/', views.produto_detail, name='produto_detail'),
    path('produtos/new/', views.produto_create, name='produto_create'),
    path('produtos/<int:pk>/edit/', views.produto_update, name='produto_update'),
    path('produtos/<int:pk>/delete/', views.produto_delete, name='produto_delete'),

    path('fornecedores/', views.fornecedor_list, name='fornecedor_list'),
    path('fornecedores/<int:pk>/', views.fornecedor_detail, name='fornecedor_detail'),
    path('fornecedores/new/', views.fornecedor_create, name='fornecedor_create'),
    path('fornecedores/<int:pk>/edit/', views.fornecedor_update, name='fornecedor_update'),
    path('fornecedores/<int:pk>/delete/', views.fornecedor_delete, name='fornecedor_delete'),

    path('localizacoes/', views.localizacao_list, name='localizacao_list'),
    path('localizacoes/<int:pk>/', views.localizacao_detail, name='localizacao_detail'),
    path('localizacoes/new/', views.localizacao_create, name='localizacao_create'),
    path('localizacoes/<int:pk>/edit/', views.localizacao_update, name='localizacao_update'),
    path('localizacoes/<int:pk>/delete/', views.localizacao_delete, name='localizacao_delete'),

    path('produtos/<int:produto_pk>/lotes/new/', views.lote_produto_create, name='lote_produto_create'),
    path('lotes/<uuid:pk>/edit/', views.lote_produto_update, name='lote_produto_update'),
    path('lotes/<uuid:pk>/delete/', views.lote_produto_delete, name='lote_produto_delete'),

    path('pedidos-compra/', views.pedido_compra_list, name='pedido_compra_list'),
    path('pedidos-compra/<uuid:pk>/', views.pedido_compra_detail, name='pedido_compra_detail'),
    path('pedidos-compra/new/', views.pedido_compra_create, name='pedido_compra_create'),
    path('pedidos-compra/<uuid:pk>/edit/', views.pedido_compra_update, name='pedido_compra_update'),
    path('pedidos-compra/<uuid:pk>/delete/', views.pedido_compra_delete, name='pedido_compra_delete'),

    path('pedidos-compra/<uuid:pedido_pk>/itens/new/', views.item_pedido_compra_create, name='item_pedido_compra_create'),
    path('itens-pedido-compra/<int:pk>/edit/', views.item_pedido_compra_update, name='item_pedido_compra_update'),
    path('itens-pedido-compra/<int:pk>/delete/', views.item_pedido_compra_delete, name='item_pedido_compra_delete'),

    path('movimentos-estoque/', views.movimento_estoque_list, name='movimento_estoque_list'),
    path('movimentos-estoque/<int:pk>/', views.movimento_estoque_detail, name='movimento_estoque_detail'),
    path('movimentos-estoque/new/', views.movimento_estoque_create, name='movimento_estoque_create'),
    path('movimentos-estoque/<int:pk>/edit/', views.movimento_estoque_update, name='movimento_estoque_update'),
    path('movimentos-estoque/<int:pk>/delete/', views.movimento_estoque_delete, name='movimento_estoque_delete'),

    path('ajustes-estoque/', views.ajuste_estoque_list, name='ajuste_estoque_list'),
    path('ajustes-estoque/<uuid:pk>/', views.ajuste_estoque_detail, name='ajuste_estoque_detail'),
    path('ajustes-estoque/new/', views.ajuste_estoque_create, name='ajuste_estoque_create'),
    path('ajustes-estoque/<uuid:pk>/edit/', views.ajuste_estoque_update, name='ajuste_estoque_update'),
    path('ajustes-estoque/<uuid:pk>/delete/', views.ajuste_estoque_delete, name='ajuste_estoque_delete'),
]