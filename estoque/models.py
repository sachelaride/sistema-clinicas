import uuid
from django.db import models
from django.conf import settings

class StatusPedido(models.TextChoices):
    PENDENTE = 'pendente', 'Pendente'
    APROVADO = 'aprovado', 'Aprovado'
    RECEBIDO_PARCIAL = 'recebido_parcial', 'Recebido Parcial'
    RECEBIDO_TOTAL = 'recebido_total', 'Recebido Total'
    CANCELADO = 'cancelado', 'Cancelado'

class TipoAjuste(models.TextChoices):
    ENTRADA_INVENTARIO = 'entrada_inventario', 'Entrada de Inventário'
    SAIDA_INVENTARIO = 'saida_inventario', 'Saída de Inventário'
    PERDA = 'perda', 'Perda'
    QUEBRA = 'quebra', 'Quebra'
    DEVOLUCAO_FORNECEDOR = 'devolucao_fornecedor', 'Devolução ao Fornecedor'
    OUTROS_ENTRADA = 'outros_entrada', 'Outros (Entrada)'
    OUTROS_SAIDA = 'outros_saida', 'Outros (Saída)'

class Fornecedor(models.Model):
    fornecedor_id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255, unique=True, db_index=True)
    cnpj = models.CharField(max_length=18, unique=True, null=True, blank=True)
    contato_nome = models.CharField(max_length=100, null=True, blank=True)
    contato_email = models.EmailField(max_length=100, null=True, blank=True)
    contato_telefone = models.CharField(max_length=20, null=True, blank=True)
    endereco = models.TextField(null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome

class LocalizacaoEstoque(models.Model):
    localizacao_id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100, unique=True, db_index=True)
    descricao = models.TextField(null=True, blank=True)
    clinica = models.ForeignKey('clinica.Clinica', on_delete=models.SET_NULL, null=True, blank=True, related_name='localizacoes_estoque')
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome

class Produto(models.Model):
    produto_id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100, db_index=True)
    descricao = models.TextField(null=True, blank=True)
    unidade = models.CharField(max_length=20, null=True, blank=True)
    nivel_minimo_estoque = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    codigo_barras = models.CharField(max_length=50, unique=True, null=True, blank=True)
    preco_custo = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    preco_venda = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    unidade_compra = models.CharField(max_length=20, null=True, blank=True)
    fator_conversao = models.DecimalField(max_digits=10, decimal_places=4, default=1.0)

    def __str__(self):
        return self.nome

class LoteProduto(models.Model):
    lote_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='lotes')
    numero_lote = models.CharField(max_length=100)
    data_fabricacao = models.DateField(null=True, blank=True)
    data_validade = models.DateField(null=True, blank=True)
    quantidade_inicial = models.DecimalField(max_digits=10, decimal_places=2)
    quantidade_atual = models.DecimalField(max_digits=10, decimal_places=2)
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.SET_NULL, null=True, blank=True, related_name='lotes')
    localizacao = models.ForeignKey(LocalizacaoEstoque, on_delete=models.SET_NULL, null=True, blank=True, related_name='lotes')
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.produto.nome} - Lote {self.numero_lote}"

class PedidoCompra(models.Model):
    pedido_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.PROTECT, related_name='pedidos_compra')
    data_pedido = models.DateTimeField(auto_now_add=True)
    data_entrega_prevista = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=StatusPedido.choices, default=StatusPedido.PENDENTE)
    total_valor = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    observacoes = models.TextField(null=True, blank=True)
    criado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Pedido {self.pedido_id} para {self.fornecedor.nome}"

class ItemPedidoCompra(models.Model):
    item_pedido_id = models.AutoField(primary_key=True)
    pedido = models.ForeignKey(PedidoCompra, on_delete=models.CASCADE, related_name='itens')
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT, related_name='itens_pedido')
    quantidade_pedida = models.DecimalField(max_digits=10, decimal_places=2)
    quantidade_recebida = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantidade_pedida} x {self.produto.nome} no Pedido {self.pedido.pedido_id}"

class MovimentoEstoque(models.Model):
    movimento_id = models.AutoField(primary_key=True)
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT, related_name='movimentos')
    quantidade = models.DecimalField(max_digits=10, decimal_places=2)
    tipo_movimento = models.CharField(max_length=10)  # 'entrada' ou 'saida'
    referencia = models.CharField(max_length=100, null=True, blank=True)
    movimentado_em = models.DateTimeField(auto_now_add=True)
    movimentado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    lote = models.ForeignKey(LoteProduto, on_delete=models.SET_NULL, null=True, blank=True, related_name='movimentos')
    localizacao = models.ForeignKey(LocalizacaoEstoque, on_delete=models.SET_NULL, null=True, blank=True, related_name='movimentos')

    def __str__(self):
        return f"{self.tipo_movimento.capitalize()} de {self.quantidade} {self.produto.nome}"

class AjusteEstoque(models.Model):
    ajuste_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT, related_name='ajustes')
    lote = models.ForeignKey(LoteProduto, on_delete=models.CASCADE, related_name='ajustes')
    localizacao = models.ForeignKey(LocalizacaoEstoque, on_delete=models.CASCADE, related_name='ajustes')
    quantidade = models.DecimalField(max_digits=10, decimal_places=2)
    tipo_ajuste = models.CharField(max_length=30, choices=TipoAjuste.choices)
    motivo = models.TextField(null=True, blank=True)
    ajustado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    ajustado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ajuste de {self.quantidade} em {self.produto.nome} ({self.tipo_ajuste})"