-- ###########################################################
-- Banco de dados PostgreSQL para sistema local de clínicas universitárias
-- Completo com versionamento, histórico, controle legal e separação por clínica
-- ###########################################################
-- [1] Extensões e ENUMs
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TYPE sexo_enum AS ENUM ('M', 'F', 'O');

CREATE TYPE status_agendamento_enum AS ENUM (
  'agendado',
  'registrado',
  'concluido',
  'cancelado',
  'faltou'
);

CREATE TYPE prioridade_fila_enum AS ENUM ('baixa', 'media', 'alta', 'urgente');

-- [2] Perfis e Permissões
CREATE TABLE
  perfis (
    perfil_id SERIAL PRIMARY KEY,
    nome VARCHAR(50) UNIQUE NOT NULL
  );

CREATE TABLE
  permissoes (
    permissao_id SERIAL PRIMARY KEY,
    codigo VARCHAR(100) UNIQUE NOT NULL,
    descricao TEXT
  );

CREATE TABLE
  perfil_permissoes (
    perfil_id INTEGER REFERENCES perfis (perfil_id) ON DELETE CASCADE,
    permissao_id INTEGER REFERENCES permissoes (permissao_id) ON DELETE CASCADE,
    PRIMARY KEY (perfil_id, permissao_id)
  );

-- [3] Usuários
CREATE TABLE
  usuarios (
    usuario_id UUID PRIMARY KEY DEFAULT uuid_generate_v4 (),
    nome_usuario VARCHAR(50) UNIQUE NOT NULL,
    senha_hash TEXT NOT NULL,
    perfil_id INTEGER REFERENCES perfis (perfil_id),
    nome_completo VARCHAR(150) NOT NULL,
    email VARCHAR(100),
    telefone VARCHAR(20),
    criado_em TIMESTAMPTZ DEFAULT now (),
    atualizado_em TIMESTAMPTZ DEFAULT now ()
  );

CREATE TABLE
  perfis_alunos (
    usuario_id UUID PRIMARY KEY REFERENCES usuarios (usuario_id) ON DELETE CASCADE,
    rgm VARCHAR(20) UNIQUE NOT NULL,
    modelo_biometrico BYTEA
  );

-- [4] Clínicas, Serviços, Salas
CREATE TABLE
  clinicas (
    clinica_id SERIAL PRIMARY KEY,
    nome VARCHAR(100) UNIQUE NOT NULL,
    descricao TEXT
  );

CREATE TABLE
  servicos (
    servico_id SERIAL PRIMARY KEY,
    clinica_id INTEGER REFERENCES clinicas (clinica_id) ON DELETE CASCADE,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT
  );

CREATE TABLE
  salas (
    sala_id SERIAL PRIMARY KEY,
    clinica_id INTEGER REFERENCES clinicas (clinica_id),
    nome VARCHAR(50),
    capacidade INTEGER DEFAULT 1
  );

-- [5] Pacientes e Responsáveis
CREATE TABLE
  pacientes (
    paciente_id UUID PRIMARY KEY DEFAULT uuid_generate_v4 (),
    nome VARCHAR(100) NOT NULL,
    sobrenome VARCHAR(100) NOT NULL,
    data_nascimento DATE,
    sexo sexo_enum,
    endereco TEXT,
    telefone VARCHAR(20),
    email VARCHAR(100),
    perfil_epidemiologico JSONB,
    criado_em TIMESTAMPTZ DEFAULT now (),
    atualizado_em TIMESTAMPTZ DEFAULT now ()
  );

CREATE TABLE
  responsaveis_legais (
    responsavel_id UUID PRIMARY KEY DEFAULT uuid_generate_v4 (),
    paciente_id UUID REFERENCES pacientes (paciente_id) ON DELETE CASCADE,
    nome VARCHAR(150) NOT NULL,
    cpf VARCHAR(14),
    rg VARCHAR(20),
    telefone VARCHAR(20),
    email VARCHAR(100),
    grau_parentesco VARCHAR(50),
    endereco TEXT,
    criado_em TIMESTAMPTZ DEFAULT now ()
  );

-- [6] Documentos e Consentimentos
CREATE TABLE
  tipos_documentos (
    tipo_id SERIAL PRIMARY KEY,
    nome VARCHAR(50) UNIQUE NOT NULL,
    descricao TEXT,
    obrigatorio BOOLEAN DEFAULT FALSE
  );

CREATE TABLE
  documentos_pacientes (
    documento_id UUID PRIMARY KEY DEFAULT uuid_generate_v4 (),
    paciente_id UUID NOT NULL REFERENCES pacientes (paciente_id) ON DELETE CASCADE,
    tipo_id INTEGER REFERENCES tipos_documentos (tipo_id),
    dados_ocr TEXT,
    caminho_arquivo TEXT NOT NULL,
    enviado_em TIMESTAMPTZ DEFAULT now ()
  );

CREATE TABLE
  consentimentos_pacientes (
    consentimento_id SERIAL PRIMARY KEY,
    paciente_id UUID NOT NULL REFERENCES pacientes (paciente_id) ON DELETE CASCADE,
    tipo_consentimento VARCHAR(50) NOT NULL,
    data_consentimento TIMESTAMPTZ DEFAULT now (),
    ativo BOOLEAN DEFAULT TRUE,
    detalhes TEXT
  );

-- [7] Horários e Agendamentos
CREATE TABLE
  horarios (
    horario_id SERIAL PRIMARY KEY,
    servico_id INTEGER REFERENCES servicos (servico_id),
    sala_id INTEGER REFERENCES salas (sala_id),
    inicio TIMESTAMPTZ NOT NULL,
    fim TIMESTAMPTZ NOT NULL
  );

CREATE TABLE
  status_agendamento (
    status_id SERIAL PRIMARY KEY,
    nome status_agendamento_enum UNIQUE NOT NULL
  );

INSERT INTO
  status_agendamento (nome)
VALUES
  ('agendado'),
  ('registrado'),
  ('concluido'),
  ('cancelado'),
  ('faltou');

CREATE TABLE
  agendamentos (
    agendamento_id UUID PRIMARY KEY DEFAULT uuid_generate_v4 (),
    clinica_id INTEGER REFERENCES clinicas (clinica_id),
    paciente_id UUID REFERENCES pacientes (paciente_id),
    horario_id INTEGER REFERENCES horarios (horario_id),
    aluno_id UUID REFERENCES usuarios (usuario_id),
    coordenador_id UUID REFERENCES usuarios (usuario_id),
    status_id INTEGER REFERENCES status_agendamento (status_id),
    criado_em TIMESTAMPTZ DEFAULT now (),
    atualizado_em TIMESTAMPTZ DEFAULT now (),
    UNIQUE (paciente_id, horario_id)
  );

-- [8] Prontuários e Histórico
CREATE TABLE
  prontuarios_eletronicos (
    prontuario_id UUID PRIMARY KEY DEFAULT uuid_generate_v4 (),
    agendamento_id UUID REFERENCES agendamentos (agendamento_id) ON DELETE CASCADE,
    clinica_id INTEGER REFERENCES clinicas (clinica_id),
    aluno_id UUID REFERENCES usuarios (usuario_id),
    coordenador_id UUID REFERENCES usuarios (usuario_id),
    anotacoes TEXT,
    criado_em TIMESTAMPTZ DEFAULT now (),
    atualizado_em TIMESTAMPTZ DEFAULT now ()
  );

CREATE TABLE
  prontuarios_eletronicos_versoes (
    versao_id UUID PRIMARY KEY DEFAULT uuid_generate_v4 (),
    prontuario_id UUID REFERENCES prontuarios_eletronicos (prontuario_id) ON DELETE CASCADE,
    aluno_id UUID,
    coordenador_id UUID,
    anotacoes TEXT,
    criado_em TIMESTAMPTZ DEFAULT now ()
  );

CREATE TABLE
  anexos_prontuario (
    anexo_id UUID PRIMARY KEY DEFAULT uuid_generate_v4 (),
    prontuario_id UUID REFERENCES prontuarios_eletronicos (prontuario_id) ON DELETE CASCADE,
    tipo_anexo VARCHAR(50),
    caminho_arquivo TEXT,
    metadados JSONB,
    enviado_em TIMESTAMPTZ DEFAULT now ()
  );

-- [9] Presenças e Fila
CREATE TABLE
  registros_presenca (
    registro_id SERIAL PRIMARY KEY,
    aluno_id UUID REFERENCES usuarios (usuario_id),
    agendamento_id UUID REFERENCES agendamentos (agendamento_id),
    entrada TIMESTAMPTZ DEFAULT now (),
    saida TIMESTAMPTZ,
    horas_registradas NUMERIC(5, 2) GENERATED ALWAYS AS (
      EXTRACT(
        EPOCH
        FROM
          (saida - entrada)
      ) / 3600
    ) STORED
  );

CREATE TABLE
  fila_espera (
    fila_id SERIAL PRIMARY KEY,
    clinica_id INTEGER REFERENCES clinicas (clinica_id),
    paciente_id UUID REFERENCES pacientes (paciente_id),
    numero_fila INTEGER NOT NULL,
    prioridade prioridade_fila_enum DEFAULT 'media',
    status VARCHAR(20) DEFAULT 'aguardando',
    criado_em TIMESTAMPTZ DEFAULT now (),
    chamado_em TIMESTAMPTZ,
    concluido_em TIMESTAMPTZ
  );

-- [10] Auditoria e Logs
CREATE TABLE
  logs_auditoria (
    auditoria_id SERIAL PRIMARY KEY,
    usuario_id UUID REFERENCES usuarios (usuario_id),
    acao VARCHAR(50),
    nome_tabela VARCHAR(100),
    id_registro TEXT,
    horario_acao TIMESTAMPTZ DEFAULT now (),
    dados_antigos JSONB,
    dados_novos JSONB
  );

CREATE TABLE
  logs_acesso (
    log_id SERIAL PRIMARY KEY,
    usuario_id UUID REFERENCES usuarios (usuario_id),
    endereco_ip INET,
    agente_usuario TEXT,
    horario_login TIMESTAMPTZ DEFAULT now (),
    sucesso BOOLEAN
  );

-- [11] Notificações
CREATE TABLE
  notificacoes (
    notificacao_id SERIAL PRIMARY KEY,
    agendamento_id UUID REFERENCES agendamentos (agendamento_id),
    canal VARCHAR(20),
    dados JSONB,
    enviado_em TIMESTAMPTZ,
    status VARCHAR(20) DEFAULT 'pendente'
  );

-- [12] Estoque
CREATE TABLE
  produtos (
    produto_id SERIAL PRIMARY KEY,
    nome VARCHAR(100),
    descricao TEXT,
    unidade VARCHAR(20),
    nivel_minimo_estoque NUMERIC DEFAULT 0
  );

CREATE TABLE
  movimentos_estoque (
    movimento_id SERIAL PRIMARY KEY,
    produto_id INTEGER REFERENCES produtos (produto_id),
    quantidade NUMERIC NOT NULL,
    tipo_movimento VARCHAR(10),
    referencia VARCHAR(100),
    movimentado_em TIMESTAMPTZ DEFAULT now (),
    movimentado_por UUID REFERENCES usuarios (usuario_id)
  );

-- [13] Configurações do Sistema
CREATE TABLE
  configuracoes_sistema (
    chave VARCHAR(100) PRIMARY KEY,
    valor TEXT NOT NULL,
    atualizado_em TIMESTAMPTZ DEFAULT now ()
  );

-- [14] Índices
CREATE INDEX idx_agendamentos_paciente ON agendamentos (paciente_id);

CREATE INDEX idx_agendamentos_aluno ON agendamentos (aluno_id);

CREATE INDEX idx_registros_presenca_aluno ON registros_presenca (aluno_id);

CREATE INDEX idx_fila_espera_status ON fila_espera (status);

CREATE INDEX idx_logs_acesso_horario ON logs_acesso (horario_login);

-- ###########################################################