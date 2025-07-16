
from rest_framework import viewsets
from estoque.models import Fornecedor, LocalizacaoEstoque, Produto, LoteProduto, PedidoCompra, ItemPedidoCompra, MovimentoEstoque, AjusteEstoque
from estoque.serializers import FornecedorSerializer, LocalizacaoEstoqueSerializer, ProdutoSerializer, LoteProdutoSerializer, PedidoCompraSerializer, ItemPedidoCompraSerializer, MovimentoEstoqueSerializer, AjusteEstoqueSerializer

class FornecedorViewSet(viewsets.ModelViewSet):
    queryset = Fornecedor.objects.all()
    serializer_class = FornecedorSerializer

class LocalizacaoEstoqueViewSet(viewsets.ModelViewSet):
    queryset = LocalizacaoEstoque.objects.all()
    serializer_class = LocalizacaoEstoqueSerializer

class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer

class LoteProdutoViewSet(viewsets.ModelViewSet):
    queryset = LoteProduto.objects.all()
    serializer_class = LoteProdutoSerializer

class PedidoCompraViewSet(viewsets.ModelViewSet):
    queryset = PedidoCompra.objects.all()
    serializer_class = PedidoCompraSerializer

class ItemPedidoCompraViewSet(viewsets.ModelViewSet):
    queryset = ItemPedidoCompra.objects.all()
    serializer_class = ItemPedidoCompraSerializer

class MovimentoEstoqueViewSet(viewsets.ModelViewSet):
    queryset = MovimentoEstoque.objects.all()
    serializer_class = MovimentoEstoqueSerializer

class AjusteEstoqueViewSet(viewsets.ModelViewSet):
    queryset = AjusteEstoque.objects.all()
    serializer_class = AjusteEstoqueSerializer
