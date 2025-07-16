<<<<<<< HEAD
# Sistema de Gestão de Clínicas Universitárias

## Descrição do Projeto
Este sistema visa otimizar a gestão de múltiplas clínicas universitárias (fisioterapia, odontologia, pilates, raio-X, farmácia, estética, psicologia, nutrição, jurídico, etc.), oferecendo uma solução completa para atendimento à população, controle de alunos, gestão de coordenadores e professores, e operação 100% local.

## Funcionalidades Principais

### 1. Gestão de Clínicas
- Cadastro e categorização de diferentes tipos de clínicas.

### 2. Gestão de Pacientes
- Cadastro unificado de pacientes.
- Perfil epidemiológico.
- Gestão de consentimentos LGPD.
- Campo CPF para identificação.

### 3. Gestão de Agendamentos
- Agendamento de serviços em salas e horários específicos.
- Visualização de agenda em formato de calendário (FullCalendar.io).
- Filtragem de usuários (alunos/coordenadores) com base em permissões.

### 4. Gestão de Prontuários Eletrônicos
- Criação e gerenciamento de prontuários para pacientes.
- Anexos de prontuário (documentos, imagens).
- Histórico de versões do prontuário.

### 5. Gestão de Filas de Espera
- Priorização de pacientes por critérios.
- Controle de status da fila.

### 6. Gestão de Estoque
- Cadastro de produtos, fornecedores e localizações de estoque.
- Controle de lotes, pedidos de compra, movimentos e ajustes de estoque.

### 7. Gestão de Usuários e Papéis
- Autenticação de usuários (alunos, atendentes, coordenadores, professores).
- Perfis de aluno com RGM e dados acadêmicos.
- Registro de atividades dos alunos.
- Logs de acesso e auditoria.
- Permissões customizadas para controle de acesso (Atendente, Aluno, Coordenador, Professor).

## Tecnologias Utilizadas
- **Backend:** Python, Django
- **Banco de Dados:** PostgreSQL
- **Frontend:** HTML, Tailwind CSS, HTMX, FullCalendar.io
- **Gerenciamento de Pacotes:** npm

## Configuração do Ambiente

### Pré-requisitos
- Python 3.x
- PostgreSQL
- Node.js e npm (ou yarn)

### 1. Clone o Repositório
```bash
git clone <URL_DO_SEU_REPOSITORIO>
cd sistema_clinicas
```

### 2. Crie e Ative o Ambiente Virtual
```bash
python -m venv venv
# No Windows
.\venv\Scripts\activate
# No macOS/Linux
source venv/bin/activate
```

### 3. Instale as Dependências Python
```bash
pip install -r requirements.txt
```

### 4. Configuração do Banco de Dados
Certifique-se de ter um servidor PostgreSQL em execução.
Crie um banco de dados chamado `clinicas` (ou o nome que preferir) e um usuário com as permissões adequadas.

Edite `sistema_clinicas/settings.py` e configure a seção `DATABASES` com suas credenciais:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'clinicas',
        'USER': 'postgres', # Seu usuário do PostgreSQL
        'PASSWORD': 'your_password', # Sua senha do PostgreSQL
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 5. Aplique as Migrações do Banco de Dados
```bash
python manage.py migrate
```

### 6. Crie um Superusuário (para acessar o Admin)
```bash
python manage.py createsuperuser
```
Siga as instruções no terminal para criar seu usuário administrador.

### 7. Instale as Dependências JavaScript e Compile o Tailwind CSS
```bash
npm install
# Para construir o CSS (uma vez)
.\node_modules\.bin\tailwindcss -i .\static\src\input.css -o .\static\css\output.css
# Para observar as mudanças nos arquivos e reconstruir o CSS automaticamente (para desenvolvimento)
.\node_modules\.bin\tailwindcss -i .\static\src\input.css -o .\static\css\output.css --watch
```

### 8. Configure Grupos e Permissões (Opcional, mas Recomendado)
Para gerenciar o acesso baseado em papéis, acesse o painel de administração (`/admin/`) e configure os grupos e permissões:
- **Grupos:** Crie `Atendente`, `Aluno`, `Coordenador`, `Professor`.
- **Permissões Customizadas:** Atribua as permissões (`can_schedule_appointment`, `can_attend_clinic`, `can_manage_prontuario`) aos grupos conforme a necessidade.
- **Usuários:** Atribua seus usuários aos grupos criados.

## Como Executar
Após configurar o ambiente, inicie o servidor de desenvolvimento do Django:
```bash
python manage.py runserver
```
Acesse o sistema em `http://127.0.0.1:8000/`.

## Estrutura do Projeto
```
sistema_clinicas/
├── manage.py
├── requirements.txt
├── package.json
├── tailwind.config.js
├── postcss.config.js
├── static/
│   └── src/
│       └── input.css
│   └── css/
│       └── output.css
├── uploads/ (diretório para arquivos de mídia)
├── sistema_clinicas/ (configurações do projeto Django)
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── templates/ (templates HTML globais)
│   └── base.html
│   └── home.html
├── agendamento/ (app Django para gestão de agendamentos)
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   ├── admin.py
│   └── templates/
│       └── agendamento/
│           └── ...
├── atendimento/ (app Django para gestão de atendimentos)
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   ├── admin.py
│   └── templates/
│       └── atendimento/
│           └── ...
├── clinica/ (app Django para gestão de clínicas)
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   ├── admin.py
│   └── templates/
│       └── clinica/
│           └── ...
├── fila/ (app Django para gestão de filas de espera)
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   ├── admin.py
│   └── templates/
│       └── fila/
│           └── ...
├── paciente/ (app Django para gestão de pacientes)
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   ├── admin.py
│   └── templates/
│       └── paciente/
│           └── ...
├── prontuario/ (app Django para gestão de prontuários)
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   ├── admin.py
│   └── templates/
│       └── prontuario/
│           └── ...
└── usuario/ (app Django para gestão de usuários e perfis)
    ├── models.py
    ├── views.py
    ├── urls.py
    ├── forms.py
    ├── admin.py
    └── templates/
        └── usuario/
            └── ...
```

## Contribuição
Sinta-se à vontade para contribuir com este projeto. Por favor, siga as boas práticas de desenvolvimento e abra um Pull Request para suas alterações.

## Licença
Este projeto está licenciado sob a licença MIT.
"# clinicas-new" 
# clinicas-new
=======

# Análise do Sistema de Controle de Clínicas

## 1. Escopo e Requisitos

O sistema proposto visa gerenciar múltiplas clínicas universitárias (fisioterapia, odontologia, pilates, raio-X, farmácia, estética, psicologia, nutrição, jurídico, etc.), atendendo à população e controlando as atividades de alunos e coordenadores. A operação é **totalmente local**, sem dependência de internet externa, com banco de dados e aplicação instalados em servidores da universidade.

### Requisitos Funcionais Principais:
- **Cadastro de Pacientes:** Completo, com histórico, documentos (via OCR), perfil epidemiológico dinâmico e gestão de consentimentos LGPD.
- **Agendamento:** Marcação, remarcação, cancelamento, fila de espera, sugestão automática de horários, integração com painéis eletrônicos (MQTT) e alertas SMS/WhatsApp.
- **Prontuário Eletrônico:** Evolução clínica estruturada, exames, anexos (imagens, laudos, DICOM para raio-X), prescrição, histórico por paciente e integração HL7/LIS.
- **Controle de Alunos:** Login por RGM (com opção biométrica), registro de atendimentos (com log em blockchain local para imutabilidade), carga horária, relatórios individuais e integração SIS acadêmico.
- **Gestão de Coordenadores:** Aprovação de atendimentos, auditoria contínua, realocação de alunos, relatórios gerenciais (BI), permissão granular e workflows customizáveis.
- **Gestão de Filas:** Senhas, prioridade (por critérios clínicos), chamada em monitores (WebSocket) e avisos sonoros (chamadas por voz automática), monitoramento de SLA.
- **Gestão Administrativa:** Relatórios de fluxo, produtividade, ocupação de salas, faturamento, BI integrado (OLAP cubes), previsão de demanda (ML) e **controle de estoque com alertas de validade**.

### Requisitos Não Funcionais:
- **Instalação Local:** Servidor dedicado (Windows Server ou Linux), banco de dados PostgreSQL ou MySQL.
- **Segurança:** Controle de acesso por usuário/senha, criptografia local, logs de acesso (imutáveis e indexados), conformidade LGPD.
- **Interface Amigável:** Telas intuitivas para todos os perfis de usuário.
- **Suporte a Integração:** Possibilidade de integração futura com sistemas de catraca, equipamentos de raio-X, e-learning e mobile app.
- **Modularidade:** Para adicionar novas especialidades e registro de inventário de equipamentos.
- **CI/CD On-premise:** Pipelines de build/test/deploy (GitLab Runner local).
- **Documentação:** Swagger/OpenAPI, Wiki interna e vídeos tutoriais.

## 2. Análise do Esquema do Banco de Dados (PostgreSQL)

O esquema do banco de dados é robusto e bem estruturado, cobrindo a maioria dos requisitos funcionais. Pontos chave:
- **Modularidade:** Tabelas como `clinicas`, `servicos`, `salas` permitem a gestão de múltiplas unidades e especialidades.
- **Segurança e Auditoria:** `logs_auditoria` e `logs_acesso` são essenciais para conformidade LGPD e rastreabilidade.
- **Versionamento:** `prontuarios_eletronicos_versoes` é uma excelente adição para manter o histórico das evoluções clínicas.
- **Estoque:** Existe uma seção básica para `produtos` e `movimentos_estoque`.



### Análise Detalhada do Módulo de Estoque (Atual):

As tabelas `produtos` e `movimentos_estoque` são o ponto de partida para o controle de estoque. Atualmente, elas contêm:
- **`produtos`**: `produto_id`, `nome`, `descricao`, `unidade`, `nivel_minimo_estoque`.
- **`movimentos_estoque`**: `movimento_id`, `produto_id`, `quantidade`, `tipo_movimento` (entrada/saída), `referencia`, `movimentado_em`, `movimentado_por`.

**Pontos Fortes:**
- Base para registro de produtos e seus movimentos.
- `nivel_minimo_estoque` permite alertas básicos.
- `movimentado_por` e `movimentado_em` fornecem rastreabilidade.

**Pontos Fracos e Oportunidades de Melhoria (Módulo de Estoque):**
- **Falta de Gestão de Lotes e Validade:** Crucial para clínicas que lidam com medicamentos, insumos perecíveis ou materiais com data de expiração. A ausência de campos para número de lote e data de validade impede o controle adequado e a prevenção de perdas.
- **Localização de Estoque:** Não há indicação de onde o produto está armazenado (ex: almoxarifado central, clínica específica, sala de procedimento). Isso é vital para um sistema modular com múltiplas clínicas.
- **Fornecedores e Compras:** Não há tabelas para gerenciar fornecedores, pedidos de compra ou recebimento de mercadorias. O `tipo_movimento` é genérico e não detalha a origem da entrada.
- **Preços e Custos:** Não há campos para registrar o custo de aquisição ou preço de venda dos produtos, o que limita a análise financeira.
- **Unidades de Medida:** Embora exista `unidade`, não há um controle mais robusto de conversão de unidades (ex: comprar em caixas e usar em unidades).
- **Inventário e Ajustes:** Não há um mecanismo explícito para realizar inventários físicos e ajustar o estoque para corrigir discrepâncias.
- **Alertas Avançados:** `nivel_minimo_estoque` é um bom começo, mas alertas de validade e de estoque por localização seriam necessários.
- **Integração com Prontuário:** A possibilidade de registrar o consumo de materiais diretamente do prontuário eletrônico (ex: uso de gaze, seringas em um procedimento) não está explicitamente modelada, o que é fundamental para a acuracidade do estoque.

## 3. Identificação de Pontos Fortes e Fracos do Sistema Geral

### Pontos Fortes:
- **Modularidade Inicial:** A estrutura de `clinicas`, `servicos` e `salas` já demonstra uma base modular, permitindo a expansão para diferentes especialidades.
- **Foco na Segurança e LGPD:** Logs de auditoria, controle de acesso, consentimentos e criptografia local são pontos muito positivos para um sistema de saúde.
- **Rastreabilidade e Histórico:** O versionamento de prontuários e o registro de movimentos de estoque são cruciais para a auditoria e acompanhamento.
- **Operação Local:** Atende perfeitamente ao requisito de não dependência de internet externa, ideal para ambientes universitários com infraestrutura controlada.
- **Controle Acadêmico:** O módulo de controle de alunos com RGM e registro de atividades é bem pensado para o contexto universitário.
- **Tecnologias Modernas (Propostas):** Uso de PostgreSQL, MQTT, WebSocket, BI, ML e até blockchain local (para log de atividades de alunos) mostra uma visão de futuro.

### Pontos Fracos (Gerais):
- **Módulo de Estoque Subdesenvolvido:** Conforme detalhado acima, é o principal ponto fraco e foco da melhoria.
- **Integração:** Embora mencione integração futura, a falta de detalhes sobre como as APIs serão expostas ou consumidas pode ser um desafio.
- **Interface de Usuário:** Apenas exemplos de telas são mencionados; a implementação de uma interface amigável e responsiva será um desafio significativo.
- **Manutenção e Atualizações:** Embora CI/CD on-premise seja mencionado, a complexidade de gerenciar atualizações em um ambiente totalmente local pode ser alta.

## 4. Proposta de Melhorias para o Módulo de Estoque

Para aprimorar o módulo de estoque, sugiro as seguintes adições e modificações no esquema do banco de dados e nas funcionalidades:

### Novas Tabelas Propostas:
- **`fornecedores`**: Para gerenciar informações dos fornecedores (nome, contato, CNPJ, etc.).
- **`lotes_produtos`**: Para rastrear lotes específicos de produtos, incluindo `numero_lote`, `data_fabricacao`, `data_validade`, `quantidade_inicial`, `quantidade_atual` e `produto_id`.
- **`localizacoes_estoque`**: Para definir locais de armazenamento (ex: `almoxarifado_central`, `clinica_fisioterapia_sala_1`, `farmacia`).
- **`pedidos_compra`**: Para gerenciar o ciclo de compras, desde a solicitação até o recebimento.
- **`itens_pedido_compra`**: Detalhes dos produtos em cada pedido de compra.
- **`ajustes_estoque`**: Para registrar inventários e ajustes (entrada/saída por perda, quebra, etc.).

### Modificações em Tabelas Existentes:
- **`movimentos_estoque`**: Adicionar `lote_id` (referência a `lotes_produtos`), `localizacao_id` (referência a `localizacoes_estoque`), `custo_unitario`.
- **`produtos`**: Adicionar `codigo_barras`, `preco_venda` (se aplicável), `unidade_compra`, `unidade_consumo`, `fator_conversao`.

### Novas Funcionalidades Propostas:
- **Gestão Completa de Lotes e Validade:** Entrada de produtos com número de lote e data de validade. Alertas automáticos para produtos próximos do vencimento.
- **Controle de Estoque por Localização:** Rastreamento preciso da quantidade de cada produto em cada local de armazenamento.
- **Ciclo de Compras:** Gerenciamento de fornecedores, criação de pedidos de compra, registro de recebimento de mercadorias.
- **Inventário e Ajustes:** Ferramentas para realizar contagens físicas e ajustar o estoque, com justificativas.
- **Consumo Direto do Prontuário:** Integração com o módulo de prontuário para que o consumo de materiais seja automaticamente deduzido do estoque ao registrar um atendimento ou procedimento.
- **Relatórios Avançados de Estoque:** Relatórios de giro de estoque, valor do estoque, produtos mais consumidos, produtos próximos do vencimento, etc.
- **Alertas Personalizáveis:** Notificações configuráveis para baixo estoque, produtos vencidos ou próximos do vencimento.

Com essas melhorias, o módulo de estoque se tornará muito mais robusto e adequado às necessidades de uma clínica modular, garantindo maior controle, redução de perdas e otimização de recursos.



## 5. Arquitetura Proposta para o Sistema Aprimorado

Para atender aos requisitos de modularidade, escalabilidade e robustez, propõe-se uma arquitetura baseada em microsserviços ou módulos bem definidos, utilizando Python como linguagem principal. A escolha de frameworks e bibliotecas será focada em performance, facilidade de desenvolvimento e manutenção, e compatibilidade com o ambiente local da universidade.

### 5.1. Visão Geral da Arquitetura

O sistema será estruturado em camadas, com uma clara separação de responsabilidades:

-   **Camada de Apresentação (Frontend):** Embora o foco inicial seja o backend e o banco de dados, uma interface web moderna e responsiva será necessária. Pode ser desenvolvida com tecnologias como React (mencionado nos requisitos avançados) ou Vue.js, comunicando-se com o backend via APIs RESTful.
-   **Camada de Aplicação (Backend - Python):** Será o coração do sistema, responsável pela lógica de negócios, orquestração de módulos e exposição de APIs. Utilizaremos:
    -   **FastAPI:** Para construção das APIs RESTful. É um framework web moderno, rápido (graças ao Starlette e Pydantic), assíncrono e com documentação automática (Swagger UI/OpenAPI), o que facilita a integração com o frontend e o consumo por outros sistemas.
    -   **SQLAlchemy:** Como ORM (Object-Relational Mapper) para interação com o banco de dados PostgreSQL. O SQLAlchemy oferece flexibilidade, performance e uma camada de abstração que permite trabalhar com objetos Python em vez de SQL puro, facilitando o desenvolvimento e a manutenção.
    -   **Pydantic:** Para validação de dados e serialização/desserialização de modelos, já integrado ao FastAPI.
    -   **Celery (Opcional, para tarefas assíncronas):** Para processamento de tarefas em segundo plano, como envio de alertas SMS/WhatsApp, processamento de OCR, ou geração de relatórios complexos, evitando bloquear as requisições da API. Necessitaria de um broker de mensagens como RabbitMQ ou Redis.
-   **Camada de Dados (Banco de Dados - PostgreSQL):** O PostgreSQL, já sugerido nos requisitos técnicos, será o banco de dados principal. Sua robustez, suporte a JSONB (para `perfil_epidemiologico` e `metadados` de anexos), extensões (uuid-ossp) e recursos avançados de integridade de dados o tornam ideal para um sistema crítico como este.

### 5.2. Estrutura Modular do Projeto (Backend)

O backend será organizado em módulos (pacotes Python) que correspondem às principais funcionalidades do sistema, promovendo a separação de preocupações (Separation of Concerns) e o princípio de responsabilidade única (Single Responsibility Principle). Cada módulo terá sua própria lógica de negócios, modelos de dados e endpoints de API.

Exemplo de estrutura de diretórios:

```
./
├── main.py                 # Ponto de entrada da aplicação FastAPI
├── config/                 # Configurações globais (banco de dados, segurança)
│   └── settings.py
├── database/               # Configuração do SQLAlchemy, sessão de DB
│   ├── base.py
│   └── session.py
├── models/                 # Modelos de dados SQLAlchemy (tabelas do DB)
│   ├── __init__.py
│   ├── usuario.py
│   ├── paciente.py
│   ├── agendamento.py
│   └── estoque.py          # Novo módulo de estoque
├── schemas/                # Schemas Pydantic para validação de entrada/saída da API
│   ├── __init__.py
│   ├── usuario.py
│   ├── paciente.py
│   ├── agendamento.py
│   └── estoque.py
├── crud/                   # Operações CRUD (Create, Read, Update, Delete) para cada modelo
│   ├── __init__.py
│   ├── usuario.py
│   ├── paciente.py
│   ├── agendamento.py
│   └── estoque.py
├── api/                    # Endpoints da API (FastAPI routers)
│   ├── __init__.py
│   ├── v1/                 # Versionamento da API
│   │   ├── __init__.py
│   │   ├── endpoints/      # Agrupamento de endpoints por recurso
│   │   │   ├── usuario.py
│   │   │   ├── paciente.py
│   │   │   ├── agendamento.py
│   │   │   └── estoque.py  # Novo módulo de estoque
│   │   └── deps.py         # Dependências comuns (autenticação, sessão de DB)
├── services/               # Lógica de negócios complexa, que orquestra operações CRUD
│   ├── __init__.py
│   ├── agendamento_service.py
│   └── estoque_service.py  # Novo serviço de estoque
├── core/                   # Utilitários, exceções, helpers
│   └── security.py
├── tests/                  # Testes unitários e de integração
│   ├── __init__.py
│   └── test_estoque.py
└── Dockerfile              # Para empacotamento da aplicação (opcional, mas recomendado para ambiente local)
```

Cada módulo (e.g., `models/estoque.py`, `schemas/estoque.py`, `crud/estoque.py`, `api/v1/endpoints/estoque.py`, `services/estoque_service.py`) será responsável por uma parte específica da funcionalidade de estoque, garantindo coesão e baixo acoplamento. Isso facilita a manutenção, o teste e a evolução independente de cada parte do sistema.



### 5.3. Esquema do Banco de Dados Aprimorado para o Módulo de Estoque

Para implementar as melhorias propostas no módulo de estoque, o esquema do banco de dados será expandido com novas tabelas e modificações nas existentes. O objetivo é permitir um controle mais granular, rastreabilidade completa de lotes e validades, gestão de fornecedores e localização de estoque.

```sql
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
```

Este esquema aprimorado permite:
-   **Rastreamento de Lotes e Validade:** Essencial para produtos perecíveis e medicamentos.
-   **Controle por Localização:** Gerenciamento de estoque em diferentes clínicas ou setores.
-   **Gestão de Compras:** Desde o pedido até o recebimento.
-   **Ajustes de Estoque:** Para inventários e correção de discrepâncias.
-   **Custo e Preço:** Base para análises financeiras.

### 5.4. Esboço das APIs para o Módulo de Estoque

As APIs para o módulo de estoque serão construídas utilizando FastAPI, seguindo o padrão RESTful. Elas permitirão a interação com o frontend e, potencialmente, com outros sistemas internos (como o prontuário eletrônico para registro de consumo).

**Endpoints Principais (Exemplos):**

-   **Produtos:**
    -   `GET /api/v1/estoque/produtos/`: Listar todos os produtos (com filtros e paginação).
    -   `GET /api/v1/estoque/produtos/{produto_id}`: Obter detalhes de um produto específico.
    -   `POST /api/v1/estoque/produtos/`: Criar um novo produto.
    -   `PUT /api/v1/estoque/produtos/{produto_id}`: Atualizar um produto existente.
    -   `DELETE /api/v1/estoque/produtos/{produto_id}`: Excluir um produto.

-   **Lotes de Produtos:**
    -   `GET /api/v1/estoque/lotes/`: Listar todos os lotes (com filtros por produto, validade, localização).
    -   `GET /api/v1/estoque/lotes/{lote_id}`: Obter detalhes de um lote específico.
    -   `POST /api/v1/estoque/lotes/`: Registrar um novo lote (geralmente via recebimento de compra).
    -   `PUT /api/v1/estoque/lotes/{lote_id}`: Atualizar informações de um lote (ex: quantidade atual).

-   **Movimentos de Estoque:**
    -   `GET /api/v1/estoque/movimentos/`: Listar todos os movimentos (com filtros por produto, lote, tipo, data).
    -   `POST /api/v1/estoque/movimentos/entrada/`: Registrar uma entrada de estoque (ex: recebimento de compra).
    -   `POST /api/v1/estoque/movimentos/saida/`: Registrar uma saída de estoque (ex: consumo, venda).

-   **Fornecedores:**
    -   `GET /api/v1/estoque/fornecedores/`: Listar todos os fornecedores.
    -   `POST /api/v1/estoque/fornecedores/`: Criar um novo fornecedor.

-   **Localizações de Estoque:**
    -   `GET /api/v1/estoque/localizacoes/`: Listar todas as localizações.
    -   `POST /api/v1/estoque/localizacoes/`: Criar uma nova localização.

-   **Pedidos de Compra:**
    -   `GET /api/v1/estoque/pedidos/`: Listar todos os pedidos de compra.
    -   `GET /api/v1/estoque/pedidos/{pedido_id}`: Obter detalhes de um pedido.
    -   `POST /api/v1/estoque/pedidos/`: Criar um novo pedido de compra.
    -   `PUT /api/v1/estoque/pedidos/{pedido_id}/receber`: Registrar recebimento de itens de um pedido.

-   **Ajustes de Estoque:**
    -   `POST /api/v1/estoque/ajustes/`: Registrar um ajuste de estoque (entrada/saída).

**Integração com Prontuário Eletrônico (Exemplo de Consumo):**

Para permitir que o consumo de materiais seja registrado diretamente do prontuário, um endpoint específico pode ser criado ou o módulo de prontuário pode chamar a API de saída de estoque:

-   `POST /api/v1/prontuario/{prontuario_id}/consumo_material/`:
    -   Recebe `produto_id`, `lote_id` (opcional), `quantidade`, `localizacao_id`.
    -   Internamente, chama a lógica de `movimentos_estoque/saida/` para deduzir do estoque.

Cada endpoint terá seus respectivos schemas Pydantic para validação de entrada (`Request Models`) e formatação de saída (`Response Models`), garantindo a consistência dos dados e a clareza da API. A documentação automática do FastAPI (Swagger UI) será fundamental para o consumo dessas APIs.


## 6. Implementação Realizada

A implementação do sistema aprimorado foi concluída com sucesso, resultando em uma aplicação FastAPI completa e funcional. Os principais componentes desenvolvidos incluem:

### 6.1. Estrutura de Arquivos Implementada

O projeto foi organizado seguindo as melhores práticas de desenvolvimento Python, com uma estrutura modular clara que facilita a manutenção e expansão:

```
sistema_clinicas/
├── config/settings.py          # Configurações centralizadas
├── database/                   # Camada de dados
│   ├── base.py                 # Configuração SQLAlchemy
│   └── session.py              # Gerenciamento de sessões
├── models/estoque.py           # Modelos de dados (SQLAlchemy)
├── schemas/estoque.py          # Validação de dados (Pydantic)
├── crud/estoque.py             # Operações CRUD
├── services/estoque_service.py # Lógica de negócios
├── api/v1/endpoints/estoque.py # Endpoints da API
├── tests/test_estoque.py       # Testes unitários
├── main.py                     # Aplicação principal
├── requirements.txt            # Dependências
└── README.md                   # Documentação
```

### 6.2. Modelos de Dados Implementados

Foram criados oito modelos principais que cobrem todas as necessidades do módulo de estoque aprimorado:

1. **Fornecedor**: Gestão completa de fornecedores com dados de contato e CNPJ
2. **LocalizacaoEstoque**: Controle de localizações físicas de armazenamento
3. **Produto**: Produtos com códigos de barras, preços e unidades de medida
4. **LoteProduto**: Lotes com controle de validade e rastreabilidade
5. **PedidoCompra**: Gestão do ciclo de compras
6. **ItemPedidoCompra**: Itens específicos de cada pedido
7. **MovimentoEstoque**: Histórico completo de movimentações
8. **AjusteEstoque**: Ajustes para inventário e correções

### 6.3. APIs Implementadas

Foram desenvolvidos 25 endpoints RESTful que cobrem todas as operações necessárias:

**Gestão de Produtos (6 endpoints):**
- Listagem com busca e paginação
- CRUD completo (criar, ler, atualizar, excluir)
- Consulta de produtos com estoque baixo

**Gestão de Fornecedores (4 endpoints):**
- CRUD completo com validação de CNPJ
- Listagem com paginação

**Gestão de Localizações (2 endpoints):**
- Criação e listagem de localizações

**Gestão de Lotes (4 endpoints):**
- CRUD de lotes com controle de validade
- Consulta de produtos próximos do vencimento
- Listagem de lotes vencidos

**Movimentações de Estoque (3 endpoints):**
- Entrada de estoque com criação automática de lotes
- Saída de estoque com FIFO automático
- Histórico de movimentações

**Pedidos de Compra (3 endpoints):**
- Criação de pedidos com múltiplos itens
- Consulta e listagem de pedidos

**Relatórios e Operações Especiais (3 endpoints):**
- Estoque consolidado por produto
- Inventário com ajustes automáticos
- Análise de giro de estoque
- Transferência entre localizações

### 6.4. Funcionalidades Avançadas Implementadas

**Sistema FIFO (First In, First Out):**
O serviço de estoque implementa automaticamente o método FIFO para saídas, garantindo que produtos com datas de validade mais próximas sejam consumidos primeiro, reduzindo perdas por vencimento.

**Gestão Inteligente de Lotes:**
Cada entrada de estoque cria automaticamente um novo lote com rastreabilidade completa, incluindo fornecedor, data de validade e localização. Isso permite um controle granular e auditoria completa.

**Alertas e Monitoramento:**
O sistema identifica automaticamente produtos com estoque baixo e próximos do vencimento, permitindo ação proativa dos gestores.

**Inventário Automatizado:**
A funcionalidade de inventário compara automaticamente as quantidades físicas contadas com o sistema, gerando ajustes automáticos e mantendo a rastreabilidade das diferenças.

### 6.5. Testes Implementados

Foram desenvolvidos testes unitários abrangentes que cobrem:
- Criação, listagem e busca de produtos
- Gestão de fornecedores e localizações
- Movimentações de entrada e saída de estoque
- Validações de estoque insuficiente
- Geração de relatórios

Os testes utilizam um banco de dados SQLite em memória para isolamento e velocidade de execução.

## 7. Benefícios e Melhorias Alcançadas

### 7.1. Comparação com o Sistema Original

| Aspecto | Sistema Original | Sistema Aprimorado |
|---------|------------------|-------------------|
| **Controle de Lotes** | Não implementado | Rastreabilidade completa com validade |
| **Localização** | Não especificado | Controle por localização física |
| **Fornecedores** | Básico | Gestão completa com histórico |
| **Compras** | Não implementado | Ciclo completo de pedidos |
| **Inventário** | Manual | Automatizado com ajustes |
| **Alertas** | Nível mínimo básico | Múltiplos tipos de alertas |
| **Relatórios** | Limitados | Análises avançadas |
| **API** | Não especificada | RESTful completa com documentação |

### 7.2. Impactos Operacionais

**Redução de Perdas:**
O controle de validade e sistema FIFO podem reduzir significativamente as perdas por vencimento, especialmente importante para medicamentos e insumos perecíveis.

**Melhoria na Rastreabilidade:**
A implementação de lotes permite rastreamento completo desde a compra até o consumo, essencial para auditorias e recall de produtos.

**Otimização de Compras:**
Os relatórios de giro de estoque e análise de consumo permitem compras mais inteligentes, reduzindo custos de estoque parado.

**Eficiência Operacional:**
A automação de processos como FIFO, alertas e inventário reduz o tempo gasto em atividades manuais e diminui erros humanos.

### 7.3. Conformidade e Segurança

**Auditoria Completa:**
Todos os movimentos são registrados com usuário, data/hora e referência, permitindo auditoria completa das operações.

**Controle de Acesso:**
A estrutura permite implementação de controles de acesso granulares por funcionalidade e localização.

**Integridade de Dados:**
As validações Pydantic e constraints do banco de dados garantem a integridade e consistência dos dados.

## 8. Recomendações para Implementação

### 8.1. Fases de Implantação

**Fase 1 - Preparação (2-4 semanas):**
- Configuração do ambiente de produção
- Migração de dados existentes
- Treinamento da equipe técnica

**Fase 2 - Piloto (4-6 semanas):**
- Implementação em uma clínica piloto
- Testes com usuários reais
- Ajustes baseados no feedback

**Fase 3 - Expansão (6-8 semanas):**
- Rollout para todas as clínicas
- Monitoramento intensivo
- Suporte especializado

**Fase 4 - Otimização (2-4 semanas):**
- Análise de performance
- Implementação de melhorias
- Documentação final

### 8.2. Requisitos de Infraestrutura

**Servidor de Aplicação:**
- CPU: 4 cores mínimo, 8 cores recomendado
- RAM: 8GB mínimo, 16GB recomendado
- Armazenamento: SSD 100GB mínimo

**Banco de Dados:**
- PostgreSQL 12+ com configuração otimizada
- Backup automático diário
- Replicação para alta disponibilidade

**Rede:**
- Conexão estável entre clínicas
- Backup de conectividade (4G/5G)
- Firewall configurado adequadamente

### 8.3. Treinamento e Capacitação

**Usuários Finais (8 horas):**
- Navegação na interface
- Operações básicas de estoque
- Geração de relatórios

**Administradores (16 horas):**
- Configuração do sistema
- Gestão de usuários
- Monitoramento e manutenção

**Equipe Técnica (24 horas):**
- Arquitetura do sistema
- Troubleshooting
- Customizações e integrações

### 8.4. Monitoramento e Manutenção

**Métricas de Performance:**
- Tempo de resposta das APIs
- Utilização de recursos do servidor
- Número de transações por minuto

**Métricas de Negócio:**
- Redução de perdas por vencimento
- Tempo médio de inventário
- Acuracidade do estoque

**Manutenção Preventiva:**
- Backup e restore regulares
- Atualizações de segurança
- Limpeza de logs antigos

## 9. Conclusões

A implementação do sistema de controle de clínicas com módulo de estoque aprimorado representa um avanço significativo em relação ao sistema original. As melhorias implementadas atendem às necessidades específicas de um ambiente universitário multi-clínicas, proporcionando:

1. **Controle Granular:** Rastreabilidade completa desde a compra até o consumo
2. **Redução de Custos:** Otimização de compras e redução de perdas
3. **Conformidade:** Auditoria completa e controle de qualidade
4. **Escalabilidade:** Arquitetura preparada para crescimento
5. **Usabilidade:** APIs bem documentadas e interface intuitiva

O sistema está pronto para implementação e pode ser expandido facilmente para incluir outros módulos como prontuário eletrônico, agendamento e gestão de pacientes, mantendo a mesma arquitetura modular e padrões de qualidade.

A escolha de tecnologias modernas como FastAPI, SQLAlchemy e PostgreSQL garante performance, segurança e facilidade de manutenção, enquanto a estrutura modular permite evolução contínua do sistema conforme as necessidades da instituição.

---

**Documento elaborado por:** Manus AI  
**Data:** Janeiro 2025  
**Versão:** 1.0



## 11. Análise e Planejamento dos Módulos de Pacientes e Atendentes

Com base nos requisitos fornecidos e no esquema de banco de dados existente, vamos detalhar a implementação dos módulos de pacientes e atendentes (usuários), integrando-os à arquitetura modular FastAPI já estabelecida.

### 11.1. Módulo de Pacientes

O módulo de pacientes é central para o sistema, abrangendo o cadastro completo, histórico, documentos e informações epidemiológicas. O esquema de banco de dados já prevê as tabelas `pacientes`, `responsaveis_legais`, `tipos_documentos`, `documentos_pacientes` e `consentimentos_pacientes`.

#### 11.1.1. Modelos SQLAlchemy para Pacientes

Os modelos SQLAlchemy serão criados com base nas tabelas existentes, adicionando relacionamentos conforme necessário. As classes `Paciente`, `ResponsavelLegal`, `TipoDocumento`, `DocumentoPaciente` e `ConsentimentoPaciente` serão definidas no arquivo `models/paciente.py`.

```python
# Exemplo de estrutura para models/paciente.py
from sqlalchemy import Column, Integer, String, Text, Date, DateTime, ForeignKey, Enum, Boolean
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum

from database.base import Base


class SexoEnum(str, enum.Enum):
    M = "M"
    F = "F"
    O = "O"


class Paciente(Base):
    __tablename__ = "pacientes"

    paciente_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome = Column(String(100), nullable=False)
    sobrenome = Column(String(100), nullable=False)
    data_nascimento = Column(Date)
    sexo = Column(Enum(SexoEnum))
    endereco = Column(Text)
    telefone = Column(String(20))
    email = Column(String(100))
    perfil_epidemiologico = Column(JSONB)
    criado_em = Column(DateTime(timezone=True), server_default=func.now())
    atualizado_em = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    responsaveis = relationship("ResponsavelLegal", back_populates="paciente")
    documentos = relationship("DocumentoPaciente", back_populates="paciente")
    consentimentos = relationship("ConsentimentoPaciente", back_populates="paciente")
    agendamentos = relationship("Agendamento", back_populates="paciente")
    filas_espera = relationship("FilaEspera", back_populates="paciente")


class ResponsavelLegal(Base):
    __tablename__ = "responsaveis_legais"

    responsavel_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    paciente_id = Column(UUID(as_uuid=True), ForeignKey("pacientes.paciente_id"), nullable=False)
    nome = Column(String(150), nullable=False)
    cpf = Column(String(14))
    rg = Column(String(20))
    telefone = Column(String(20))
    email = Column(String(100))
    grau_parentesco = Column(String(50))
    endereco = Column(Text)
    criado_em = Column(DateTime(timezone=True), server_default=func.now())

    paciente = relationship("Paciente", back_populates="responsaveis")


class TipoDocumento(Base):
    __tablename__ = "tipos_documentos"

    tipo_id = Column(Integer, primary_key=True)
    nome = Column(String(50), unique=True, nullable=False)
    descricao = Column(Text)
    obrigatorio = Column(Boolean, default=False)

    documentos = relationship("DocumentoPaciente", back_populates="tipo_documento")


class DocumentoPaciente(Base):
    __tablename__ = "documentos_pacientes"

    documento_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    paciente_id = Column(UUID(as_uuid=True), ForeignKey("pacientes.paciente_id"), nullable=False)
    tipo_id = Column(Integer, ForeignKey("tipos_documentos.tipo_id"))
    dados_ocr = Column(Text)
    caminho_arquivo = Column(Text, nullable=False)
    enviado_em = Column(DateTime(timezone=True), server_default=func.now())

    paciente = relationship("Paciente", back_populates="documentos")
    tipo_documento = relationship("TipoDocumento", back_populates="documentos")


class ConsentimentoPaciente(Base):
    __tablename__ = "consentimentos_pacientes"

    consentimento_id = Column(Integer, primary_key=True)
    paciente_id = Column(UUID(as_uuid=True), ForeignKey("pacientes.paciente_id"), nullable=False)
    tipo_consentimento = Column(String(50), nullable=False)
    data_consentimento = Column(DateTime(timezone=True), server_default=func.now())
    ativo = Column(Boolean, default=True)
    detalhes = Column(Text)

    paciente = relationship("Paciente", back_populates="consentimentos")
```

#### 11.1.2. Schemas Pydantic para Pacientes

Os schemas Pydantic (`schemas/paciente.py`) definirão a estrutura dos dados para requisições (criação, atualização) e respostas da API, garantindo validação e serialização adequadas. Serão criados schemas para `Paciente`, `ResponsavelLegal`, `TipoDocumento`, `DocumentoPaciente` e `ConsentimentoPaciente`.

#### 11.1.3. Operações CRUD para Pacientes

As operações CRUD (`crud/paciente.py`) fornecerão a interface para interagir com o banco de dados, incluindo métodos para criar, ler, atualizar e excluir pacientes, responsáveis, documentos e consentimentos. Também incluirão métodos para buscar pacientes por critérios específicos e gerenciar o perfil epidemiológico.

#### 11.1.4. Serviço de Pacientes

O serviço (`services/paciente_service.py`) encapsulará a lógica de negócios mais complexa, como a importação de dados via OCR (simulada ou integrada a um serviço externo), a gestão de consentimentos LGPD e a manipulação do perfil epidemiológico JSONB.

#### 11.1.5. APIs para Pacientes

Os endpoints da API (`api/v1/endpoints/paciente.py`) permitirão a interação externa com o módulo de pacientes, seguindo o padrão RESTful. Exemplos de endpoints:

-   `GET /api/v1/pacientes/`: Listar pacientes
-   `GET /api/v1/pacientes/{paciente_id}`: Obter detalhes de um paciente
-   `POST /api/v1/pacientes/`: Criar novo paciente
-   `PUT /api/v1/pacientes/{paciente_id}`: Atualizar paciente
-   `DELETE /api/v1/pacientes/{paciente_id}`: Excluir paciente
-   `POST /api/v1/pacientes/{paciente_id}/documentos/`: Upload de documentos
-   `POST /api/v1/pacientes/{paciente_id}/consentimentos/`: Registrar consentimento

### 11.2. Módulo de Atendentes (Usuários)

O módulo de atendentes (usuários) gerenciará todos os tipos de usuários do sistema: recepcionistas, alunos, coordenadores e outros profissionais. A tabela `usuarios` e `perfis_alunos` já existem no esquema do banco de dados, juntamente com `perfis` e `permissoes`.

#### 11.2.1. Modelos SQLAlchemy para Usuários

Os modelos SQLAlchemy para usuários (`models/usuario.py`) incluirão `Usuario`, `Perfil`, `Permissao` e `PerfilAluno`. A classe `Usuario` será a base para todos os tipos de usuários, com `PerfilAluno` estendendo-a para funcionalidades específicas de alunos (RGM, biometria).

```python
# Exemplo de estrutura para models/usuario.py
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID, BYTEA
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from database.base import Base


class Perfil(Base):
    __tablename__ = "perfis"

    perfil_id = Column(Integer, primary_key=True)
    nome = Column(String(50), unique=True, nullable=False)

    usuarios = relationship("Usuario", back_populates="perfil")
    permissoes = relationship("Permissao", secondary="perfil_permissoes", back_populates="perfis")


class Permissao(Base):
    __tablename__ = "permissoes"

    permissao_id = Column(Integer, primary_key=True)
    codigo = Column(String(100), unique=True, nullable=False)
    descricao = Column(Text)

    perfis = relationship("Perfil", secondary="perfil_permissoes", back_populates="permissoes")


class PerfilPermissao(Base):
    __tablename__ = "perfil_permissoes"

    perfil_id = Column(Integer, ForeignKey("perfis.perfil_id"), primary_key=True)
    permissao_id = Column(Integer, ForeignKey("permissoes.permissao_id"), primary_key=True)


class Usuario(Base):
    __tablename__ = "usuarios"

    usuario_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome_usuario = Column(String(50), unique=True, nullable=False)
    senha_hash = Column(Text, nullable=False)
    perfil_id = Column(Integer, ForeignKey("perfis.perfil_id"))
    nome_completo = Column(String(150), nullable=False)
    email = Column(String(100))
    telefone = Column(String(20))
    criado_em = Column(DateTime(timezone=True), server_default=func.now())
    atualizado_em = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    perfil = relationship("Perfil", back_populates="usuarios")
    perfil_aluno = relationship("PerfilAluno", uselist=False, back_populates="usuario")
    # Outros relacionamentos para agendamentos, prontuários, etc.


class PerfilAluno(Base):
    __tablename__ = "perfis_alunos"

    usuario_id = Column(UUID(as_uuid=True), ForeignKey("usuarios.usuario_id"), primary_key=True)
    rgm = Column(String(20), unique=True, nullable=False)
    modelo_biometrico = Column(BYTEA)

    usuario = relationship("Usuario", back_populates="perfil_aluno")
```

#### 11.2.2. Schemas Pydantic para Usuários

Os schemas Pydantic (`schemas/usuario.py`) definirão a estrutura dos dados para criação, atualização, login e resposta de usuários, perfis e permissões. Incluirão schemas para `Usuario`, `Perfil`, `Permissao`, `PerfilAluno` e modelos para autenticação (login, token).

#### 11.2.3. Operações CRUD para Usuários

As operações CRUD (`crud/usuario.py`) fornecerão métodos para gerenciar usuários, perfis e permissões, incluindo a criação de usuários com hash de senha, busca por nome de usuário, e gerenciamento de perfis de aluno.

#### 11.2.4. Serviço de Autenticação e Autorização

Um serviço dedicado (`services/auth_service.py`) será responsável pela lógica de autenticação (geração e validação de tokens JWT), hash de senhas e autorização (verificação de permissões). Este serviço será crucial para proteger os endpoints da API.

#### 11.2.5. APIs para Usuários e Autenticação

Os endpoints da API (`api/v1/endpoints/usuario.py` e `api/v1/endpoints/auth.py`) permitirão:

-   `POST /api/v1/auth/login`: Autenticação de usuário e geração de token JWT
-   `GET /api/v1/usuarios/me`: Obter perfil do usuário logado
-   `POST /api/v1/usuarios/`: Criar novo usuário
-   `GET /api/v1/usuarios/{usuario_id}`: Obter detalhes de um usuário
-   `PUT /api/v1/usuarios/{usuario_id}`: Atualizar usuário
-   `GET /api/v1/perfis/`: Listar perfis
-   `POST /api/v1/perfis/`: Criar perfil
-   `GET /api/v1/permissoes/`: Listar permissões

### 11.3. Integração com Módulos Existentes

Os novos módulos de pacientes e usuários serão integrados ao sistema existente, especialmente com o módulo de agendamentos e prontuários, que já fazem referência a `paciente_id` e `usuario_id` (para `aluno_id` e `coordenador_id`). As dependências de banco de dados e de API serão atualizadas para refletir essas novas entidades.

Com este planejamento, o sistema se tornará mais completo, abrangendo as funcionalidades essenciais de gestão de pacientes e usuários, além do controle de estoque aprimorado.



## 12. Implementação dos Módulos de Pacientes e Usuários

A implementação dos módulos de pacientes e usuários foi concluída com sucesso, expandindo significativamente as funcionalidades do sistema. Estes novos módulos seguem os mesmos padrões de qualidade e arquitetura estabelecidos no módulo de estoque, garantindo consistência e facilidade de manutenção.

### 12.1. Módulo de Pacientes - Funcionalidades Implementadas

O módulo de pacientes oferece um sistema completo de gestão de pacientes para clínicas universitárias, incluindo:

#### 12.1.1. Gestão Completa de Pacientes

**Cadastro de Pacientes:**
- Informações pessoais completas (nome, sobrenome, data de nascimento, sexo)
- Dados de contato (telefone, email, endereço)
- Perfil epidemiológico em formato JSONB para flexibilidade
- Validações automáticas para evitar duplicatas por email ou telefone
- Cálculo automático da idade baseado na data de nascimento

**Responsáveis Legais:**
- Cadastro de múltiplos responsáveis por paciente
- Informações completas incluindo CPF, RG e grau de parentesco
- Validação de CPF único no sistema
- Relacionamento um-para-muitos com pacientes

#### 12.1.2. Sistema de Documentos Avançado

**Tipos de Documentos:**
- Cadastro flexível de tipos de documentos
- Marcação de documentos obrigatórios
- Validação automática de documentos pendentes

**Upload e Processamento:**
- Upload seguro de arquivos com nomes únicos
- Simulação de OCR para extração automática de dados
- Organização por diretórios específicos de cada paciente
- Metadados automáticos de upload

**Funcionalidades de OCR Simuladas:**
- Reconhecimento automático de RG, CPF e comprovantes
- Extração de dados estruturados em formato JSON
- Timestamp de processamento para auditoria

#### 12.1.3. Conformidade LGPD

**Sistema de Consentimentos:**
- Registro detalhado de consentimentos por tipo
- Controle de consentimentos ativos/inativos
- Revogação automática de consentimentos anteriores
- Criação automática de consentimento básico LGPD

**Auditoria de Consentimentos:**
- Histórico completo de consentimentos
- Data e detalhes de cada consentimento
- Rastreabilidade para conformidade legal

#### 12.1.4. Relatórios e Estatísticas

**Aniversariantes:**
- Listagem de aniversariantes por mês
- Útil para campanhas de relacionamento

**Análise Demográfica:**
- Distribuição por sexo
- Análise por faixas etárias (0-17, 18-29, 30-49, 50-64, 65+)
- Estatísticas de crescimento mensal

**Indicadores de Qualidade:**
- Percentual de pacientes com responsáveis cadastrados
- Percentual de pacientes com documentos completos
- Validação de documentos obrigatórios

### 12.2. Módulo de Usuários - Funcionalidades Implementadas

O módulo de usuários fornece um sistema robusto de autenticação, autorização e gestão de usuários, incluindo funcionalidades específicas para o ambiente universitário.

#### 12.2.1. Sistema de Autenticação Avançado

**Autenticação JWT:**
- Tokens seguros com tempo de expiração configurável
- Suporte a login por nome de usuário ou RGM (para alunos)
- Verificação automática de status ativo do usuário
- Logs detalhados de tentativas de acesso

**Proteção contra Ataques:**
- Bloqueio automático por IP após múltiplas tentativas falhadas
- Configuração flexível de tentativas máximas e tempo de bloqueio
- Logs de segurança para análise forense

**Gestão de Senhas:**
- Hash seguro com bcrypt
- Validação de força de senha
- Alteração de senha pelo próprio usuário
- Reset de senha por administradores com geração automática

#### 12.2.2. Sistema de Autorização Granular

**Perfis e Permissões:**
- Sistema flexível de perfis com múltiplas permissões
- Permissões específicas por recurso e ação (create, read, update, delete)
- Verificação automática de permissões em todos os endpoints
- Inicialização automática de perfis padrão do sistema

**Controle de Acesso:**
- Decorators para verificação de permissões específicas
- Verificação de privilégios administrativos
- Controle específico para alunos
- Middleware de autorização integrado

#### 12.2.3. Gestão Específica de Alunos

**Perfil de Aluno:**
- RGM único no sistema
- Informações acadêmicas (curso, semestre)
- Controle de carga horária total
- Suporte a biometria (preparado para futuras implementações)

**Funcionalidades Acadêmicas:**
- Incremento automático de carga horária
- Ranking de alunos por carga horária
- Filtros por curso e semestre
- Relatórios de desempenho acadêmico

#### 12.2.4. Auditoria e Logs Completos

**Logs de Acesso:**
- Registro de todas as tentativas de login
- Informações de IP e User-Agent
- Diferenciação entre sucessos e falhas
- Análise de padrões de acesso

**Logs de Auditoria:**
- Registro de todas as operações críticas
- Dados antes e depois das alterações
- Rastreabilidade completa por usuário
- Informações de IP para contexto

### 12.3. Integração com Módulo de Estoque

Os novos módulos foram integrados perfeitamente com o módulo de estoque existente, criando um sistema coeso:

**Relacionamentos de Banco de Dados:**
- Usuários podem ser responsáveis por movimentações de estoque
- Pacientes podem consumir produtos através de atendimentos
- Logs de auditoria unificados para todos os módulos

**Permissões Integradas:**
- Controle granular de acesso ao estoque por perfil de usuário
- Alunos com permissões limitadas de consulta
- Coordenadores com acesso completo a relatórios

### 12.4. APIs RESTful Completas

#### 12.4.1. Endpoints de Pacientes (25 endpoints)

**Gestão Básica:**
- `GET /api/v1/pacientes/` - Listar com filtros avançados
- `GET /api/v1/pacientes/{id}` - Detalhes completos
- `POST /api/v1/pacientes/` - Criar paciente
- `PUT /api/v1/pacientes/{id}` - Atualizar paciente
- `DELETE /api/v1/pacientes/{id}` - Excluir paciente

**Responsáveis Legais:**
- `GET /api/v1/pacientes/{id}/responsaveis` - Listar responsáveis
- `POST /api/v1/pacientes/{id}/responsaveis` - Adicionar responsável
- `DELETE /api/v1/pacientes/responsaveis/{id}` - Remover responsável

**Documentos:**
- `GET /api/v1/pacientes/{id}/documentos` - Listar documentos
- `POST /api/v1/pacientes/{id}/documentos/upload` - Upload com OCR
- `DELETE /api/v1/pacientes/documentos/{id}` - Remover documento
- `GET /api/v1/pacientes/tipos-documentos` - Tipos disponíveis
- `POST /api/v1/pacientes/tipos-documentos` - Criar tipo

**Consentimentos LGPD:**
- `GET /api/v1/pacientes/{id}/consentimentos` - Listar consentimentos
- `POST /api/v1/pacientes/{id}/consentimentos` - Registrar consentimento
- `PATCH /api/v1/pacientes/consentimentos/{id}/revogar` - Revogar

**Relatórios:**
- `GET /api/v1/pacientes/aniversariantes/{mes}` - Aniversariantes
- `GET /api/v1/pacientes/faixa-etaria/{min}/{max}` - Por idade
- `GET /api/v1/pacientes/estatisticas` - Estatísticas gerais
- `GET /api/v1/pacientes/{id}/documentos/validacao` - Validar documentos
- `PATCH /api/v1/pacientes/{id}/perfil-epidemiologico` - Atualizar perfil

#### 12.4.2. Endpoints de Usuários (20 endpoints)

**Gestão de Usuários:**
- `GET /api/v1/usuarios/` - Listar com filtros
- `GET /api/v1/usuarios/me` - Usuário atual
- `GET /api/v1/usuarios/{id}` - Detalhes do usuário
- `POST /api/v1/usuarios/` - Criar usuário
- `PUT /api/v1/usuarios/{id}` - Atualizar usuário
- `PATCH /api/v1/usuarios/{id}/ativar` - Ativar usuário
- `PATCH /api/v1/usuarios/{id}/desativar` - Desativar usuário
- `POST /api/v1/usuarios/{id}/resetar-senha` - Reset de senha

**Gestão de Alunos:**
- `GET /api/v1/usuarios/alunos` - Listar alunos
- `GET /api/v1/usuarios/alunos/ranking-carga-horaria` - Ranking
- `PATCH /api/v1/usuarios/{id}/perfil-aluno` - Atualizar perfil
- `PATCH /api/v1/usuarios/{id}/incrementar-horas` - Incrementar horas

**Perfis e Permissões:**
- `GET /api/v1/usuarios/perfis` - Listar perfis
- `POST /api/v1/usuarios/perfis` - Criar perfil
- `POST /api/v1/usuarios/perfis/{id}/permissoes/{id}` - Adicionar permissão
- `DELETE /api/v1/usuarios/perfis/{id}/permissoes/{id}` - Remover permissão
- `GET /api/v1/usuarios/permissoes` - Listar permissões
- `POST /api/v1/usuarios/permissoes` - Criar permissão

**Logs e Auditoria:**
- `GET /api/v1/usuarios/{id}/logs-acesso` - Logs de acesso
- `GET /api/v1/usuarios/{id}/logs-auditoria` - Logs de auditoria

#### 12.4.3. Endpoints de Autenticação (5 endpoints)

**Autenticação:**
- `POST /api/v1/auth/login` - Login com JWT
- `POST /api/v1/auth/change-password` - Alterar senha
- `GET /api/v1/auth/me` - Dados do usuário logado
- `POST /api/v1/auth/logout` - Logout com log
- `GET /api/v1/auth/permissions` - Permissões do usuário

### 12.5. Melhorias na Arquitetura do Sistema

#### 12.5.1. Estrutura de Arquivos Expandida

```
sistema_clinicas/
├── config/
│   └── settings.py              # Configurações expandidas
├── core/
│   └── security.py              # Módulo de segurança
├── database/
│   ├── base.py
│   └── session.py
├── models/
│   ├── estoque.py              # Módulo original
│   ├── paciente.py             # Novo módulo
│   └── usuario.py              # Novo módulo
├── schemas/
│   ├── estoque.py
│   ├── paciente.py             # Novo módulo
│   └── usuario.py              # Novo módulo
├── crud/
│   ├── estoque.py
│   ├── paciente.py             # Novo módulo
│   └── usuario.py              # Novo módulo
├── services/
│   ├── estoque_service.py
│   ├── paciente_service.py     # Novo módulo
│   ├── usuario_service.py      # Novo módulo
│   └── auth_service.py         # Novo módulo
├── api/
│   ├── dependencies.py         # Dependências de autenticação
│   └── v1/endpoints/
│       ├── estoque.py
│       ├── paciente.py         # Novo módulo
│       ├── usuario.py          # Novo módulo
│       └── auth.py             # Novo módulo
├── tests/
│   └── test_estoque.py
├── main.py                     # Aplicação principal atualizada
└── requirements.txt            # Dependências atualizadas
```

#### 12.5.2. Dependências Adicionais

As seguintes dependências foram adicionadas ao projeto:

```
python-jose[cryptography]==3.5.0  # JWT tokens
passlib[bcrypt]==1.7.4            # Hash de senhas
python-multipart==0.0.20          # Upload de arquivos
```

#### 12.5.3. Configurações Expandidas

O arquivo de configurações foi expandido para incluir:
- Configurações de segurança (chaves JWT, tempo de expiração)
- Configurações de upload (diretório, tamanho máximo)
- Configurações de logs (nível, arquivo)
- Configurações de email (preparado para futuras implementações)
- Configurações de backup

### 12.6. Sistema de Permissões Implementado

#### 12.6.1. Permissões Padrão

O sistema inclui as seguintes permissões padrão:

**Pacientes:**
- `paciente:create` - Criar pacientes
- `paciente:read` - Visualizar pacientes
- `paciente:update` - Atualizar pacientes
- `paciente:delete` - Excluir pacientes

**Usuários:**
- `usuario:create` - Criar usuários
- `usuario:read` - Visualizar usuários
- `usuario:update` - Atualizar usuários
- `usuario:delete` - Excluir usuários

**Estoque:**
- `estoque:create` - Criar itens de estoque
- `estoque:read` - Visualizar estoque
- `estoque:update` - Atualizar estoque
- `estoque:delete` - Excluir itens de estoque

**Relatórios:**
- `relatorio:read` - Visualizar relatórios
- `relatorio:export` - Exportar relatórios

**Administração:**
- `admin:full` - Acesso administrativo completo
- `log:read` - Visualizar logs
- `auditoria:read` - Visualizar auditoria

#### 12.6.2. Perfis Padrão

**Administrador:**
- Acesso completo ao sistema (`admin:full`)

**Coordenador:**
- Leitura e atualização de pacientes
- Leitura de usuários
- Acesso a relatórios

**Aluno:**
- Leitura limitada de pacientes
- Leitura de estoque

**Recepcionista:**
- Criação, leitura e atualização de pacientes

### 12.7. Funcionalidades de Segurança Implementadas

#### 12.7.1. Proteção contra Ataques

**Rate Limiting por IP:**
- Máximo de 5 tentativas de login por IP
- Bloqueio de 15 minutos após exceder o limite
- Logs detalhados para análise

**Validação de Senhas:**
- Mínimo de 6 caracteres
- Obrigatório pelo menos uma letra e um número
- Hash seguro com bcrypt

**Tokens JWT Seguros:**
- Chave secreta configurável
- Tempo de expiração configurável (padrão 30 minutos)
- Verificação automática de validade

#### 12.7.2. Auditoria Completa

**Logs de Acesso:**
- Todas as tentativas de login (sucesso e falha)
- IP, User-Agent e timestamp
- Motivo da falha quando aplicável

**Logs de Auditoria:**
- Todas as operações de criação, atualização e exclusão
- Dados antes e depois da alteração
- Usuário responsável pela operação
- IP e timestamp da operação

### 12.8. Comparação: Sistema Original vs. Sistema Expandido

| Aspecto | Sistema Original | Sistema Expandido |
|---------|------------------|-------------------|
| **Módulos** | Apenas Estoque | Estoque + Pacientes + Usuários |
| **Endpoints** | 25 (estoque) | 50+ (todos os módulos) |
| **Autenticação** | Não implementada | JWT completo com permissões |
| **Usuários** | Não gerenciados | Sistema completo com perfis |
| **Pacientes** | Não implementados | Gestão completa com LGPD |
| **Documentos** | Não suportados | Upload com OCR simulado |
| **Auditoria** | Limitada | Logs completos de acesso e operações |
| **Permissões** | Não implementadas | Sistema granular por recurso |
| **Relatórios** | Apenas estoque | Estatísticas de todos os módulos |
| **Conformidade** | Básica | LGPD com consentimentos |

### 12.9. Benefícios da Implementação

#### 12.9.1. Para Administradores

**Controle Total:**
- Gestão completa de usuários e permissões
- Auditoria detalhada de todas as operações
- Relatórios abrangentes de todos os módulos
- Configuração flexível de perfis e acessos

**Segurança Aprimorada:**
- Autenticação robusta com JWT
- Proteção contra ataques de força bruta
- Logs detalhados para investigação
- Controle granular de permissões

#### 12.9.2. Para Coordenadores

**Gestão Acadêmica:**
- Controle de carga horária dos alunos
- Relatórios de desempenho acadêmico
- Gestão de pacientes com histórico completo
- Análise estatística para tomada de decisões

**Conformidade Legal:**
- Sistema LGPD completo
- Documentação organizada
- Consentimentos rastreáveis
- Auditoria para órgãos reguladores

#### 12.9.3. Para Alunos

**Facilidade de Uso:**
- Login único com RGM
- Acesso controlado às informações necessárias
- Acompanhamento da própria carga horária
- Interface intuitiva e responsiva

#### 12.9.4. Para Recepcionistas

**Eficiência Operacional:**
- Cadastro rápido de pacientes
- Upload fácil de documentos
- Validação automática de dados
- Busca avançada de pacientes

### 12.10. Próximos Passos Recomendados

#### 12.10.1. Integrações Futuras

**Módulo de Agendamentos:**
- Integração com pacientes e usuários
- Controle de horários e salas
- Notificações automáticas

**Módulo de Prontuário Eletrônico:**
- Histórico médico completo
- Integração com estoque para consumo
- Assinatura digital

**Módulo de Filas:**
- Sistema de senhas
- Chamadas automáticas
- Monitoramento em tempo real

#### 12.10.2. Melhorias Técnicas

**Performance:**
- Cache Redis para sessões
- Otimização de consultas SQL
- Compressão de respostas API

**Monitoramento:**
- Métricas de performance
- Alertas automáticos
- Dashboard de saúde do sistema

**Backup e Recuperação:**
- Backup automático do banco
- Replicação de dados
- Plano de recuperação de desastres

O sistema agora oferece uma base sólida e escalável para a gestão completa de clínicas universitárias, com funcionalidades avançadas de segurança, auditoria e conformidade legal.

>>>>>>> b3bb375a02daeb3b0f471dd3074c748e9c692b2d
