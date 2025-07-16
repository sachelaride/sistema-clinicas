from django import forms
from .models import (
    Fornecedor, LocalizacaoEstoque, Produto, LoteProduto, PedidoCompra, 
    ItemPedidoCompra, MovimentoEstoque, AjusteEstoque
)

class FornecedorForm(forms.ModelForm):
    class Meta:
        model = Fornecedor
        fields = '__all__'
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-input'}),
            'cnpj': forms.TextInput(attrs={'class': 'form-input'}),
            'contato_nome': forms.TextInput(attrs={'class': 'form-input'}),
            'contato_email': forms.EmailInput(attrs={'class': 'form-input'}),
            'contato_telefone': forms.TextInput(attrs={'class': 'form-input'}),
            'endereco': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 4}),
        }

class LocalizacaoEstoqueForm(forms.ModelForm):
    class Meta:
        model = LocalizacaoEstoque
        fields = '__all__'
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-input'}),
            'descricao': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 4}),
            'clinica': forms.Select(attrs={'class': 'form-select'}),
        }

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = '__all__'
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-input'}),
            'descricao': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 4}),
            'unidade': forms.TextInput(attrs={'class': 'form-input'}),
            'nivel_minimo_estoque': forms.NumberInput(attrs={'class': 'form-input'}),
            'codigo_barras': forms.TextInput(attrs={'class': 'form-input'}),
            'preco_custo': forms.NumberInput(attrs={'class': 'form-input'}),
            'preco_venda': forms.NumberInput(attrs={'class': 'form-input'}),
            'unidade_compra': forms.TextInput(attrs={'class': 'form-input'}),
            'fator_conversao': forms.NumberInput(attrs={'class': 'form-input'}),
        }

class LoteProdutoForm(forms.ModelForm):
    class Meta:
        model = LoteProduto
        fields = '__all__'
        widgets = {
            'produto': forms.Select(attrs={'class': 'form-select'}),
            'numero_lote': forms.TextInput(attrs={'class': 'form-input'}),
            'data_fabricacao': forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
            'data_validade': forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
            'quantidade_inicial': forms.NumberInput(attrs={'class': 'form-input'}),
            'quantidade_atual': forms.NumberInput(attrs={'class': 'form-input'}),
            'fornecedor': forms.Select(attrs={'class': 'form-select'}),
            'localizacao': forms.Select(attrs={'class': 'form-select'}),
        }

class PedidoCompraForm(forms.ModelForm):
    class Meta:
        model = PedidoCompra
        fields = '__all__'
        widgets = {
            'fornecedor': forms.Select(attrs={'class': 'form-select'}),
            'data_pedido': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-input'}),
            'data_entrega_prevista': forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'total_valor': forms.NumberInput(attrs={'class': 'form-input'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 4}),
            'criado_por': forms.Select(attrs={'class': 'form-select'}),
        }

class ItemPedidoCompraForm(forms.ModelForm):
    class Meta:
        model = ItemPedidoCompra
        fields = '__all__'
        widgets = {
            'pedido': forms.Select(attrs={'class': 'form-select'}),
            'produto': forms.Select(attrs={'class': 'form-select'}),
            'quantidade_pedida': forms.NumberInput(attrs={'class': 'form-input'}),
            'quantidade_recebida': forms.NumberInput(attrs={'class': 'form-input'}),
            'preco_unitario': forms.NumberInput(attrs={'class': 'form-input'}),
        }

class MovimentoEstoqueForm(forms.ModelForm):
    class Meta:
        model = MovimentoEstoque
        fields = '__all__'
        widgets = {
            'produto': forms.Select(attrs={'class': 'form-select'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-input'}),
            'tipo_movimento': forms.TextInput(attrs={'class': 'form-input'}),
            'referencia': forms.TextInput(attrs={'class': 'form-input'}),
            'movimentado_em': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-input'}),
            'movimentado_por': forms.Select(attrs={'class': 'form-select'}),
            'lote': forms.Select(attrs={'class': 'form-select'}),
            'localizacao': forms.Select(attrs={'class': 'form-select'}),
        }

class AjusteEstoqueForm(forms.ModelForm):
    class Meta:
        model = AjusteEstoque
        fields = '__all__'
        widgets = {
            'produto': forms.Select(attrs={'class': 'form-select'}),
            'lote': forms.Select(attrs={'class': 'form-select'}),
            'localizacao': forms.Select(attrs={'class': 'form-select'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-input'}),
            'tipo_ajuste': forms.Select(attrs={'class': 'form-select'}),
            'motivo': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 4}),
            'ajustado_por': forms.Select(attrs={'class': 'form-select'}),
        }