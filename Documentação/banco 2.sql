-- [12] Estoque Aprimorado

-- Tabela de Fornecedores
CREATE TABLE
  fornecedores (
    fornecedor_id SERIAL PRIMARY KEY,
    nome VARCHAR(255) UNIQUE NOT NULL,
    cnpj VARCHAR(18) UNIQUE,
    contato_nome VARCHAR(100),
    contato_email VARCHAR(100),
    contato_telefone VARCHAR(20),
    endereco TEXT,
    criado_em TIMESTAMPTZ DEFAULT now (),
    atualizado_em TIMESTAMPTZ DEFAULT now ()
  );

-- Tabela de Localizações de Estoque (para modularidade por clínica/setor)
CREATE TABLE
  localizacoes_estoque (
    localizacao_id SERIAL PRIMARY KEY,
    nome VARCHAR(100) UNIQUE NOT NULL,
    descricao TEXT,
    clinica_id INTEGER REFERENCES clinicas (clinica_id) ON DELETE CASCADE, -- Opcional: vincular a uma clínica específica
    criado_em TIMESTAMPTZ DEFAULT now (),
    atualizado_em TIMESTAMPTZ DEFAULT now ()
  );

-- Modificação da Tabela de Produtos
-- Adição de campos para controle de unidades e códigos
ALTER TABLE
  produtos
ADD
  COLUMN codigo_barras VARCHAR(50) UNIQUE,
ADD
  COLUMN preco_custo NUMERIC(10, 2),
ADD
  COLUMN preco_venda NUMERIC(10, 2),
ADD
  COLUMN unidade_compra VARCHAR(20),
ADD
  COLUMN fator_conversao NUMERIC(10, 4) DEFAULT 1.0; -- Ex: 1 caixa = 10 unidades

-- Tabela de Lotes de Produtos (para rastreamento de validade e origem)
CREATE TABLE
  lotes_produtos (
    lote_id UUID PRIMARY KEY DEFAULT uuid_generate_v4 (),
    produto_id INTEGER REFERENCES produtos (produto_id) ON DELETE CASCADE,
    numero_lote VARCHAR(100) NOT NULL,
    data_fabricacao DATE,
    data_validade DATE,
    quantidade_inicial NUMERIC(10, 2) NOT NULL,
    quantidade_atual NUMERIC(10, 2) NOT NULL,
    fornecedor_id INTEGER REFERENCES fornecedores (fornecedor_id),
    localizacao_id INTEGER REFERENCES localizacoes_estoque (localizacao_id),
    criado_em TIMESTAMPTZ DEFAULT now (),
    atualizado_em TIMESTAMPTZ DEFAULT now (),
    UNIQUE (produto_id, numero_lote) -- Garante que um lote é único para um produto
  );

-- Tabela de Pedidos de Compra
CREATE TYPE status_pedido_enum AS ENUM (
  'pendente',
  'aprovado',
  'recebido_parcial',
  'recebido_total',
  'cancelado'
);

CREATE TABLE
  pedidos_compra (
    pedido_id UUID PRIMARY KEY DEFAULT uuid_generate_v4 (),
    fornecedor_id INTEGER REFERENCES fornecedores (fornecedor_id) ON DELETE CASCADE,
    data_pedido TIMESTAMPTZ DEFAULT now (),
    data_entrega_prevista DATE,
    status status_pedido_enum DEFAULT 'pendente',
    total_valor NUMERIC(10, 2),
    observacoes TEXT,
    criado_por UUID REFERENCES usuarios (usuario_id),
    criado_em TIMESTAMPTZ DEFAULT now (),
    atualizado_em TIMESTAMPTZ DEFAULT now ()
  );

-- Tabela de Itens do Pedido de Compra
CREATE TABLE
  itens_pedido_compra (
    item_pedido_id SERIAL PRIMARY KEY,
    pedido_id UUID REFERENCES pedidos_compra (pedido_id) ON DELETE CASCADE,
    produto_id INTEGER REFERENCES produtos (produto_id) ON DELETE CASCADE,
    quantidade_pedida NUMERIC(10, 2) NOT NULL,
    quantidade_recebida NUMERIC(10, 2) DEFAULT 0,
    preco_unitario NUMERIC(10, 2) NOT NULL,
    criado_em TIMESTAMPTZ DEFAULT now ()
  );

-- Tabela de Ajustes de Estoque (para inventário, perdas, etc.)
CREATE TYPE tipo_ajuste_enum AS ENUM (
  'entrada_inventario',
  'saida_inventario',
  'perda',
  'quebra',
  'devolucao_fornecedor',
  'outros_entrada',
  'outros_saida'
);

CREATE TABLE
  ajustes_estoque (
    ajuste_id UUID PRIMARY KEY DEFAULT uuid_generate_v4 (),
    produto_id INTEGER REFERENCES produtos (produto_id) ON DELETE CASCADE,
    lote_id UUID REFERENCES lotes_produtos (lote_id) ON DELETE CASCADE,
    localizacao_id INTEGER REFERENCES localizacoes_estoque (localizacao_id) ON DELETE CASCADE,
    quantidade NUMERIC(10, 2) NOT NULL,
    tipo_ajuste tipo_ajuste_enum NOT NULL,
    motivo TEXT,
    ajustado_por UUID REFERENCES usuarios (usuario_id),
    ajustado_em TIMESTAMPTZ DEFAULT now ()
  );

-- Modificação da Tabela de Movimentos de Estoque
-- Adição de lote_id e localizacao_id para rastreabilidade granular
ALTER TABLE
  movimentos_estoque
ADD
  COLUMN lote_id UUID REFERENCES lotes_produtos (lote_id) ON DELETE CASCADE,
ADD
  COLUMN localizacao_id INTEGER REFERENCES localizacoes_estoque (localizacao_id) ON DELETE CASCADE;

-- Adição de índices para otimização de consultas
CREATE INDEX idx_lotes_produtos_produto_id ON lotes_produtos (produto_id);
CREATE INDEX idx_lotes_produtos_data_validade ON lotes_produtos (data_validade);
CREATE INDEX idx_movimentos_estoque_lote_id ON movimentos_estoque (lote_id);
CREATE INDEX idx_movimentos_estoque_localizacao_id ON movimentos_estoque (localizacao_id);
CREATE INDEX idx_pedidos_compra_fornecedor_id ON pedidos_compra (fornecedor_id);
CREATE INDEX idx_ajustes_estoque_produto_id ON ajustes_estoque (produto_id);
CREATE INDEX idx_ajustes_estoque_lote_id ON ajustes_estoque (lote_id);
CREATE INDEX idx_ajustes_estoque_localizacao_id ON ajustes_estoque (localizacao_id);
