from django.shortcuts import render, redirect, get_object_or_404
from .models import Produto, Fornecedor, LocalizacaoEstoque, LoteProduto, PedidoCompra, ItemPedidoCompra, MovimentoEstoque, AjusteEstoque
from .forms import ProdutoForm, FornecedorForm, LocalizacaoEstoqueForm, LoteProdutoForm, PedidoCompraForm, ItemPedidoCompraForm, MovimentoEstoqueForm, AjusteEstoqueForm

def produto_list(request):
    produtos = Produto.objects.all()
    return render(request, 'estoque/produto_list.html', {'produtos': produtos})

def produto_detail(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    return render(request, 'estoque/produto_detail.html', {'produto': produto})

def produto_create(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            produto = form.save()
            return redirect('produto_detail', pk=produto.pk)
    else:
        form = ProdutoForm()
    return render(request, 'estoque/produto_form.html', {'form': form, 'action': 'Criar'})

def produto_update(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    if request.method == 'POST':
        form = ProdutoForm(request.POST, instance=produto)
        if form.is_valid():
            produto = form.save()
            return redirect('produto_detail', pk=produto.pk)
    else:
        form = ProdutoForm(instance=produto)
    return render(request, 'estoque/produto_form.html', {'form': form, 'action': 'Atualizar'})

def produto_delete(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    if request.method == 'POST':
        produto.delete()
        return redirect('produto_list')
    return render(request, 'estoque/produto_confirm_delete.html', {'produto': produto})

def fornecedor_list(request):
    fornecedores = Fornecedor.objects.all()
    return render(request, 'estoque/fornecedor_list.html', {'fornecedores': fornecedores})

def fornecedor_detail(request, pk):
    fornecedor = get_object_or_404(Fornecedor, pk=pk)
    return render(request, 'estoque/fornecedor_detail.html', {'fornecedor': fornecedor})

def fornecedor_create(request):
    if request.method == 'POST':
        form = FornecedorForm(request.POST)
        if form.is_valid():
            fornecedor = form.save()
            return redirect('fornecedor_detail', pk=fornecedor.pk)
    else:
        form = FornecedorForm()
    return render(request, 'estoque/fornecedor_form.html', {'form': form, 'action': 'Criar'})

def fornecedor_update(request, pk):
    fornecedor = get_object_or_404(Fornecedor, pk=pk)
    if request.method == 'POST':
        form = FornecedorForm(request.POST, instance=fornecedor)
        if form.is_valid():
            fornecedor = form.save()
            return redirect('fornecedor_detail', pk=fornecedor.pk)
    else:
        form = FornecedorForm(instance=fornecedor)
    return render(request, 'estoque/fornecedor_form.html', {'form': form, 'action': 'Atualizar'})

def fornecedor_delete(request, pk):
    fornecedor = get_object_or_404(Fornecedor, pk=pk)
    if request.method == 'POST':
        fornecedor.delete()
        return redirect('fornecedor_list')
    return render(request, 'estoque/fornecedor_confirm_delete.html', {'fornecedor': fornecedor})

def localizacao_list(request):
    localizacoes = LocalizacaoEstoque.objects.all()
    return render(request, 'estoque/localizacao_list.html', {'localizacoes': localizacoes})

def localizacao_detail(request, pk):
    localizacao = get_object_or_404(LocalizacaoEstoque, pk=pk)
    return render(request, 'estoque/localizacao_detail.html', {'localizacao': localizacao})

def localizacao_create(request):
    if request.method == 'POST':
        form = LocalizacaoEstoqueForm(request.POST)
        if form.is_valid():
            localizacao = form.save()
            return redirect('localizacao_detail', pk=localizacao.pk)
    else:
        form = LocalizacaoEstoqueForm()
    return render(request, 'estoque/localizacao_form.html', {'form': form, 'action': 'Criar'})

def localizacao_update(request, pk):
    localizacao = get_object_or_404(LocalizacaoEstoque, pk=pk)
    if request.method == 'POST':
        form = LocalizacaoEstoqueForm(request.POST, instance=localizacao)
        if form.is_valid():
            localizacao = form.save()
            return redirect('localizacao_detail', pk=localizacao.pk)
    else:
        form = LocalizacaoEstoqueForm(instance=localizacao)
    return render(request, 'estoque/localizacao_form.html', {'form': form, 'action': 'Atualizar'})

def localizacao_delete(request, pk):
    localizacao = get_object_or_404(LocalizacaoEstoque, pk=pk)
    if request.method == 'POST':
        localizacao.delete()
        return redirect('localizacao_list')
    return render(request, 'estoque/localizacao_confirm_delete.html', {'localizacao': localizacao})

# Views para LoteProduto
def lote_produto_create(request, produto_pk):
    produto = get_object_or_404(Produto, pk=produto_pk)
    if request.method == 'POST':
        form = LoteProdutoForm(request.POST)
        if form.is_valid():
            lote = form.save(commit=False)
            lote.produto = produto
            lote.save()
            return redirect('produto_detail', pk=produto.pk)
    else:
        form = LoteProdutoForm(initial={'produto': produto})
    return render(request, 'estoque/lote_produto_form.html', {'form': form, 'produto': produto, 'action': 'Adicionar'})

def lote_produto_update(request, pk):
    lote = get_object_or_404(LoteProduto, pk=pk)
    if request.method == 'POST':
        form = LoteProdutoForm(request.POST, instance=lote)
        if form.is_valid():
            lote = form.save()
            return redirect('produto_detail', pk=lote.produto.pk)
    else:
        form = LoteProdutoForm(instance=lote)
    return render(request, 'estoque/lote_produto_form.html', {'form': form, 'lote': lote, 'action': 'Atualizar'})

def lote_produto_delete(request, pk):
    lote = get_object_or_404(LoteProduto, pk=pk)
    produto_pk = lote.produto.pk
    if request.method == 'POST':
        lote.delete()
        return redirect('produto_detail', pk=produto_pk)
    return render(request, 'estoque/lote_produto_confirm_delete.html', {'lote': lote})

# Views para PedidoCompra
def pedido_compra_list(request):
    pedidos = PedidoCompra.objects.all()
    return render(request, 'estoque/pedido_compra_list.html', {'pedidos': pedidos})

def pedido_compra_detail(request, pk):
    pedido = get_object_or_404(PedidoCompra, pk=pk)
    return render(request, 'estoque/pedido_compra_detail.html', {'pedido': pedido})

def pedido_compra_create(request):
    if request.method == 'POST':
        form = PedidoCompraForm(request.POST)
        if form.is_valid():
            pedido = form.save()
            return redirect('pedido_compra_detail', pk=pedido.pk)
    else:
        form = PedidoCompraForm()
    return render(request, 'estoque/pedido_compra_form.html', {'form': form, 'action': 'Criar'})

def pedido_compra_update(request, pk):
    pedido = get_object_or_404(PedidoCompra, pk=pk)
    if request.method == 'POST':
        form = PedidoCompraForm(request.POST, instance=pedido)
        if form.is_valid():
            pedido = form.save()
            return redirect('pedido_compra_detail', pk=pedido.pk)
    else:
        form = PedidoCompraForm(instance=pedido)
    return render(request, 'estoque/pedido_compra_form.html', {'form': form, 'action': 'Atualizar'})

def pedido_compra_delete(request, pk):
    pedido = get_object_or_404(PedidoCompra, pk=pk)
    if request.method == 'POST':
        pedido.delete()
        return redirect('pedido_compra_list')
    return render(request, 'estoque/pedido_compra_confirm_delete.html', {'pedido': pedido})

# Views para ItemPedidoCompra
def item_pedido_compra_create(request, pedido_pk):
    pedido = get_object_or_404(PedidoCompra, pk=pedido_pk)
    if request.method == 'POST':
        form = ItemPedidoCompraForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.pedido = pedido
            item.save()
            return redirect('pedido_compra_detail', pk=pedido.pk)
    else:
        form = ItemPedidoCompraForm(initial={'pedido': pedido})
    return render(request, 'estoque/item_pedido_compra_form.html', {'form': form, 'pedido': pedido, 'action': 'Adicionar'})

def item_pedido_compra_update(request, pk):
    item = get_object_or_404(ItemPedidoCompra, pk=pk)
    if request.method == 'POST':
        form = ItemPedidoCompraForm(request.POST, instance=item)
        if form.is_valid():
            item = form.save()
            return redirect('pedido_compra_detail', pk=item.pedido.pk)
    else:
        form = ItemPedidoCompraForm(instance=item)
    return render(request, 'estoque/item_pedido_compra_form.html', {'form': form, 'item': item, 'action': 'Atualizar'})

def item_pedido_compra_delete(request, pk):
    item = get_object_or_404(ItemPedidoCompra, pk=pk)
    pedido_pk = item.pedido.pk
    if request.method == 'POST':
        item.delete()
        return redirect('pedido_compra_detail', pk=pedido_pk)
    return render(request, 'estoque/item_pedido_compra_confirm_delete.html', {'item': item})

# Views para MovimentoEstoque
def movimento_estoque_list(request):
    movimentos = MovimentoEstoque.objects.all()
    return render(request, 'estoque/movimento_estoque_list.html', {'movimentos': movimentos})

def movimento_estoque_detail(request, pk):
    movimento = get_object_or_404(MovimentoEstoque, pk=pk)
    return render(request, 'estoque/movimento_estoque_detail.html', {'movimento': movimento})

def movimento_estoque_create(request):
    if request.method == 'POST':
        form = MovimentoEstoqueForm(request.POST)
        if form.is_valid():
            movimento = form.save()
            return redirect('movimento_estoque_detail', pk=movimento.pk)
    else:
        form = MovimentoEstoqueForm()
    return render(request, 'estoque/movimento_estoque_form.html', {'form': form, 'action': 'Criar'})

def movimento_estoque_update(request, pk):
    movimento = get_object_or_404(MovimentoEstoque, pk=pk)
    if request.method == 'POST':
        form = MovimentoEstoqueForm(request.POST, instance=movimento)
        if form.is_valid():
            movimento = form.save()
            return redirect('movimento_estoque_detail', pk=movimento.pk)
    else:
        form = MovimentoEstoqueForm(instance=movimento)
    return render(request, 'estoque/movimento_estoque_form.html', {'form': form, 'action': 'Atualizar'})

def movimento_estoque_delete(request, pk):
    movimento = get_object_or_404(MovimentoEstoque, pk=pk)
    if request.method == 'POST':
        movimento.delete()
        return redirect('movimento_estoque_list')
    return render(request, 'estoque/movimento_estoque_confirm_delete.html', {'movimento': movimento})

# Views para AjusteEstoque
def ajuste_estoque_list(request):
    ajustes = AjusteEstoque.objects.all()
    return render(request, 'estoque/ajuste_estoque_list.html', {'ajustes': ajustes})

def ajuste_estoque_detail(request, pk):
    ajuste = get_object_or_404(AjusteEstoque, pk=pk)
    return render(request, 'estoque/ajuste_estoque_detail.html', {'ajuste': ajuste})

def ajuste_estoque_create(request):
    if request.method == 'POST':
        form = AjusteEstoqueForm(request.POST)
        if form.is_valid():
            ajuste = form.save()
            return redirect('ajuste_estoque_detail', pk=ajuste.pk)
    else:
        form = AjusteEstoqueForm()
    return render(request, 'estoque/ajuste_estoque_form.html', {'form': form, 'action': 'Criar'})

def ajuste_estoque_update(request, pk):
    ajuste = get_object_or_404(AjusteEstoque, pk=pk)
    if request.method == 'POST':
        form = AjusteEstoqueForm(request.POST, instance=ajuste)
        if form.is_valid():
            ajuste = form.save()
            return redirect('ajuste_estoque_detail', pk=ajuste.pk)
    else:
        form = AjusteEstoqueForm(instance=ajuste)
    return render(request, 'estoque/ajuste_estoque_form.html', {'form': form, 'action': 'Atualizar'})

def ajuste_estoque_delete(request, pk):
    ajuste = get_object_or_404(AjusteEstoque, pk=pk)
    if request.method == 'POST':
        ajuste.delete()
        return redirect('ajuste_estoque_list')
    return render(request, 'estoque/ajuste_estoque_confirm_delete.html', {'ajuste': ajuste})