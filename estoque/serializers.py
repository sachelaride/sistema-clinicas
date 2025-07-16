
from rest_framework import serializers
from estoque.models import Fornecedor, LocalizacaoEstoque, Produto, LoteProduto, PedidoCompra, ItemPedidoCompra, MovimentoEstoque, AjusteEstoque

class FornecedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fornecedor
        fields = '__all__'

class LocalizacaoEstoqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocalizacaoEstoque
        fields = '__all__'

class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = '__all__'

class LoteProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoteProduto
        fields = '__all__'

class ItemPedidoCompraSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemPedidoCompra
        fields = '__all__'

class PedidoCompraSerializer(serializers.ModelSerializer):
    itens = ItemPedidoCompraSerializer(many=True, read_only=True)

    class Meta:
        model = PedidoCompra
        fields = '__all__'

class MovimentoEstoqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovimentoEstoque
        fields = '__all__'

class AjusteEstoqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = AjusteEstoque
        fields = '__all__'
