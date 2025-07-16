--
-- PostgreSQL database cluster dump
--

-- Started on 2025-07-14 15:49:10

SET default_transaction_read_only = off;

SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;

--
-- Roles
--

CREATE ROLE postgres;
ALTER ROLE postgres WITH SUPERUSER INHERIT CREATEROLE CREATEDB LOGIN REPLICATION BYPASSRLS;

--
-- User Configurations
--








--
-- Databases
--

--
-- Database "template1" dump
--

\connect template1

--
-- PostgreSQL database dump
--

-- Dumped from database version 17.5
-- Dumped by pg_dump version 17.5

-- Started on 2025-07-14 15:49:10

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

-- Completed on 2025-07-14 15:49:10

--
-- PostgreSQL database dump complete
--

--
-- Database "clinicas" dump
--

--
-- PostgreSQL database dump
--

-- Dumped from database version 17.5
-- Dumped by pg_dump version 17.5

-- Started on 2025-07-14 15:49:11

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 5298 (class 1262 OID 16386)
-- Name: clinicas; Type: DATABASE; Schema: -; Owner: postgres
--

CREATE DATABASE clinicas WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'br';


ALTER DATABASE clinicas OWNER TO postgres;

\connect clinicas

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 2 (class 3079 OID 16857)
-- Name: uuid-ossp; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS "uuid-ossp" WITH SCHEMA public;


--
-- TOC entry 5299 (class 0 OID 0)
-- Dependencies: 2
-- Name: EXTENSION "uuid-ossp"; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION "uuid-ossp" IS 'generate universally unique identifiers (UUIDs)';


--
-- TOC entry 914 (class 1247 OID 16888)
-- Name: prioridade_fila_enum; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.prioridade_fila_enum AS ENUM (
    'baixa',
    'media',
    'alta',
    'urgente'
);


ALTER TYPE public.prioridade_fila_enum OWNER TO postgres;

--
-- TOC entry 908 (class 1247 OID 16869)
-- Name: sexo_enum; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.sexo_enum AS ENUM (
    'M',
    'F',
    'O'
);


ALTER TYPE public.sexo_enum OWNER TO postgres;

--
-- TOC entry 911 (class 1247 OID 16876)
-- Name: status_agendamento_enum; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.status_agendamento_enum AS ENUM (
    'agendado',
    'registrado',
    'concluido',
    'cancelado',
    'faltou'
);


ALTER TYPE public.status_agendamento_enum OWNER TO postgres;

--
-- TOC entry 1007 (class 1247 OID 17386)
-- Name: status_pedido_enum; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.status_pedido_enum AS ENUM (
    'pendente',
    'aprovado',
    'recebido_parcial',
    'recebido_total',
    'cancelado'
);


ALTER TYPE public.status_pedido_enum OWNER TO postgres;

--
-- TOC entry 1022 (class 1247 OID 17502)
-- Name: statuspedidoenum; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.statuspedidoenum AS ENUM (
    'PENDENTE',
    'APROVADO',
    'RECEBIDO_PARCIAL',
    'RECEBIDO_TOTAL',
    'CANCELADO'
);


ALTER TYPE public.statuspedidoenum OWNER TO postgres;

--
-- TOC entry 1016 (class 1247 OID 17439)
-- Name: tipo_ajuste_enum; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.tipo_ajuste_enum AS ENUM (
    'entrada_inventario',
    'saida_inventario',
    'perda',
    'quebra',
    'devolucao_fornecedor',
    'outros_entrada',
    'outros_saida'
);


ALTER TYPE public.tipo_ajuste_enum OWNER TO postgres;

--
-- TOC entry 1025 (class 1247 OID 17514)
-- Name: tipoajusteenum; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.tipoajusteenum AS ENUM (
    'ENTRADA_INVENTARIO',
    'SAIDA_INVENTARIO',
    'PERDA',
    'QUEBRA',
    'DEVOLUCAO_FORNECEDOR',
    'OUTROS_ENTRADA',
    'OUTROS_SAIDA'
);


ALTER TYPE public.tipoajusteenum OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 242 (class 1259 OID 17098)
-- Name: agendamentos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.agendamentos (
    agendamento_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    clinica_id integer,
    paciente_id uuid,
    horario_id integer,
    aluno_id uuid,
    coordenador_id uuid,
    status_id integer,
    criado_em timestamp with time zone DEFAULT now(),
    atualizado_em timestamp with time zone DEFAULT now()
);


ALTER TABLE public.agendamentos OWNER TO postgres;

--
-- TOC entry 269 (class 1259 OID 17453)
-- Name: ajustes_estoque; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.ajustes_estoque (
    ajuste_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    produto_id integer,
    lote_id uuid,
    localizacao_id integer,
    quantidade numeric(10,2) NOT NULL,
    tipo_ajuste public.tipo_ajuste_enum NOT NULL,
    motivo text,
    ajustado_por uuid,
    ajustado_em timestamp with time zone DEFAULT now()
);


ALTER TABLE public.ajustes_estoque OWNER TO postgres;

--
-- TOC entry 245 (class 1259 OID 17182)
-- Name: anexos_prontuario; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.anexos_prontuario (
    anexo_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    prontuario_id uuid,
    tipo_anexo character varying(50),
    caminho_arquivo text,
    metadados jsonb,
    enviado_em timestamp with time zone DEFAULT now()
);


ALTER TABLE public.anexos_prontuario OWNER TO postgres;

--
-- TOC entry 226 (class 1259 OID 16964)
-- Name: clinicas; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.clinicas (
    clinica_id integer NOT NULL,
    nome character varying(100) NOT NULL,
    descricao text
);


ALTER TABLE public.clinicas OWNER TO postgres;

--
-- TOC entry 225 (class 1259 OID 16963)
-- Name: clinicas_clinica_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.clinicas_clinica_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.clinicas_clinica_id_seq OWNER TO postgres;

--
-- TOC entry 5300 (class 0 OID 0)
-- Dependencies: 225
-- Name: clinicas_clinica_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.clinicas_clinica_id_seq OWNED BY public.clinicas.clinica_id;


--
-- TOC entry 260 (class 1259 OID 17310)
-- Name: configuracoes_sistema; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.configuracoes_sistema (
    chave character varying(100) NOT NULL,
    valor text NOT NULL,
    atualizado_em timestamp with time zone DEFAULT now()
);


ALTER TABLE public.configuracoes_sistema OWNER TO postgres;

--
-- TOC entry 237 (class 1259 OID 17057)
-- Name: consentimentos_pacientes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.consentimentos_pacientes (
    consentimento_id integer NOT NULL,
    paciente_id uuid NOT NULL,
    tipo_consentimento character varying(50) NOT NULL,
    data_consentimento timestamp with time zone DEFAULT now(),
    ativo boolean DEFAULT true,
    detalhes text
);


ALTER TABLE public.consentimentos_pacientes OWNER TO postgres;

--
-- TOC entry 236 (class 1259 OID 17056)
-- Name: consentimentos_pacientes_consentimento_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.consentimentos_pacientes_consentimento_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.consentimentos_pacientes_consentimento_id_seq OWNER TO postgres;

--
-- TOC entry 5301 (class 0 OID 0)
-- Dependencies: 236
-- Name: consentimentos_pacientes_consentimento_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.consentimentos_pacientes_consentimento_id_seq OWNED BY public.consentimentos_pacientes.consentimento_id;


--
-- TOC entry 235 (class 1259 OID 17037)
-- Name: documentos_pacientes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.documentos_pacientes (
    documento_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    paciente_id uuid NOT NULL,
    tipo_id integer,
    dados_ocr text,
    caminho_arquivo text NOT NULL,
    enviado_em timestamp with time zone DEFAULT now()
);


ALTER TABLE public.documentos_pacientes OWNER TO postgres;

--
-- TOC entry 249 (class 1259 OID 17216)
-- Name: fila_espera; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.fila_espera (
    fila_id integer NOT NULL,
    clinica_id integer,
    paciente_id uuid,
    numero_fila integer NOT NULL,
    prioridade public.prioridade_fila_enum DEFAULT 'media'::public.prioridade_fila_enum,
    status character varying(20) DEFAULT 'aguardando'::character varying,
    criado_em timestamp with time zone DEFAULT now(),
    chamado_em timestamp with time zone,
    concluido_em timestamp with time zone
);


ALTER TABLE public.fila_espera OWNER TO postgres;

--
-- TOC entry 248 (class 1259 OID 17215)
-- Name: fila_espera_fila_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.fila_espera_fila_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.fila_espera_fila_id_seq OWNER TO postgres;

--
-- TOC entry 5302 (class 0 OID 0)
-- Dependencies: 248
-- Name: fila_espera_fila_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.fila_espera_fila_id_seq OWNED BY public.fila_espera.fila_id;


--
-- TOC entry 262 (class 1259 OID 17325)
-- Name: fornecedores; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.fornecedores (
    fornecedor_id integer NOT NULL,
    nome character varying(255) NOT NULL,
    cnpj character varying(18),
    contato_nome character varying(100),
    contato_email character varying(100),
    contato_telefone character varying(20),
    endereco text,
    criado_em timestamp with time zone DEFAULT now(),
    atualizado_em timestamp with time zone DEFAULT now()
);


ALTER TABLE public.fornecedores OWNER TO postgres;

--
-- TOC entry 261 (class 1259 OID 17324)
-- Name: fornecedores_fornecedor_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.fornecedores_fornecedor_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.fornecedores_fornecedor_id_seq OWNER TO postgres;

--
-- TOC entry 5303 (class 0 OID 0)
-- Dependencies: 261
-- Name: fornecedores_fornecedor_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.fornecedores_fornecedor_id_seq OWNED BY public.fornecedores.fornecedor_id;


--
-- TOC entry 239 (class 1259 OID 17073)
-- Name: horarios; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.horarios (
    horario_id integer NOT NULL,
    servico_id integer,
    sala_id integer,
    inicio timestamp with time zone NOT NULL,
    fim timestamp with time zone NOT NULL
);


ALTER TABLE public.horarios OWNER TO postgres;

--
-- TOC entry 238 (class 1259 OID 17072)
-- Name: horarios_horario_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.horarios_horario_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.horarios_horario_id_seq OWNER TO postgres;

--
-- TOC entry 5304 (class 0 OID 0)
-- Dependencies: 238
-- Name: horarios_horario_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.horarios_horario_id_seq OWNED BY public.horarios.horario_id;


--
-- TOC entry 268 (class 1259 OID 17420)
-- Name: itens_pedido_compra; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.itens_pedido_compra (
    item_pedido_id integer NOT NULL,
    pedido_id uuid,
    produto_id integer,
    quantidade_pedida numeric(10,2) NOT NULL,
    quantidade_recebida numeric(10,2) DEFAULT 0,
    preco_unitario numeric(10,2) NOT NULL,
    criado_em timestamp with time zone DEFAULT now()
);


ALTER TABLE public.itens_pedido_compra OWNER TO postgres;

--
-- TOC entry 267 (class 1259 OID 17419)
-- Name: itens_pedido_compra_item_pedido_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.itens_pedido_compra_item_pedido_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.itens_pedido_compra_item_pedido_id_seq OWNER TO postgres;

--
-- TOC entry 5305 (class 0 OID 0)
-- Dependencies: 267
-- Name: itens_pedido_compra_item_pedido_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.itens_pedido_compra_item_pedido_id_seq OWNED BY public.itens_pedido_compra.item_pedido_id;


--
-- TOC entry 264 (class 1259 OID 17340)
-- Name: localizacoes_estoque; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.localizacoes_estoque (
    localizacao_id integer NOT NULL,
    nome character varying(100) NOT NULL,
    descricao text,
    clinica_id integer,
    criado_em timestamp with time zone DEFAULT now(),
    atualizado_em timestamp with time zone DEFAULT now()
);


ALTER TABLE public.localizacoes_estoque OWNER TO postgres;

--
-- TOC entry 263 (class 1259 OID 17339)
-- Name: localizacoes_estoque_localizacao_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.localizacoes_estoque_localizacao_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.localizacoes_estoque_localizacao_id_seq OWNER TO postgres;

--
-- TOC entry 5306 (class 0 OID 0)
-- Dependencies: 263
-- Name: localizacoes_estoque_localizacao_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.localizacoes_estoque_localizacao_id_seq OWNED BY public.localizacoes_estoque.localizacao_id;


--
-- TOC entry 253 (class 1259 OID 17251)
-- Name: logs_acesso; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.logs_acesso (
    log_id integer NOT NULL,
    usuario_id uuid,
    endereco_ip inet,
    agente_usuario text,
    horario_login timestamp with time zone DEFAULT now(),
    sucesso boolean
);


ALTER TABLE public.logs_acesso OWNER TO postgres;

--
-- TOC entry 252 (class 1259 OID 17250)
-- Name: logs_acesso_log_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.logs_acesso_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.logs_acesso_log_id_seq OWNER TO postgres;

--
-- TOC entry 5307 (class 0 OID 0)
-- Dependencies: 252
-- Name: logs_acesso_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.logs_acesso_log_id_seq OWNED BY public.logs_acesso.log_id;


--
-- TOC entry 251 (class 1259 OID 17236)
-- Name: logs_auditoria; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.logs_auditoria (
    auditoria_id integer NOT NULL,
    usuario_id uuid,
    acao character varying(50),
    nome_tabela character varying(100),
    id_registro text,
    horario_acao timestamp with time zone DEFAULT now(),
    dados_antigos jsonb,
    dados_novos jsonb
);


ALTER TABLE public.logs_auditoria OWNER TO postgres;

--
-- TOC entry 250 (class 1259 OID 17235)
-- Name: logs_auditoria_auditoria_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.logs_auditoria_auditoria_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.logs_auditoria_auditoria_id_seq OWNER TO postgres;

--
-- TOC entry 5308 (class 0 OID 0)
-- Dependencies: 250
-- Name: logs_auditoria_auditoria_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.logs_auditoria_auditoria_id_seq OWNED BY public.logs_auditoria.auditoria_id;


--
-- TOC entry 265 (class 1259 OID 17360)
-- Name: lotes_produtos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.lotes_produtos (
    lote_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    produto_id integer,
    numero_lote character varying(100) NOT NULL,
    data_fabricacao date,
    data_validade date,
    quantidade_inicial numeric(10,2) NOT NULL,
    quantidade_atual numeric(10,2) NOT NULL,
    fornecedor_id integer,
    localizacao_id integer,
    criado_em timestamp with time zone DEFAULT now(),
    atualizado_em timestamp with time zone DEFAULT now()
);


ALTER TABLE public.lotes_produtos OWNER TO postgres;

--
-- TOC entry 259 (class 1259 OID 17291)
-- Name: movimentos_estoque; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.movimentos_estoque (
    movimento_id integer NOT NULL,
    produto_id integer,
    quantidade numeric NOT NULL,
    tipo_movimento character varying(10),
    referencia character varying(100),
    movimentado_em timestamp with time zone DEFAULT now(),
    movimentado_por uuid,
    lote_id uuid,
    localizacao_id integer
);


ALTER TABLE public.movimentos_estoque OWNER TO postgres;

--
-- TOC entry 258 (class 1259 OID 17290)
-- Name: movimentos_estoque_movimento_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.movimentos_estoque_movimento_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.movimentos_estoque_movimento_id_seq OWNER TO postgres;

--
-- TOC entry 5309 (class 0 OID 0)
-- Dependencies: 258
-- Name: movimentos_estoque_movimento_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.movimentos_estoque_movimento_id_seq OWNED BY public.movimentos_estoque.movimento_id;


--
-- TOC entry 255 (class 1259 OID 17266)
-- Name: notificacoes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.notificacoes (
    notificacao_id integer NOT NULL,
    agendamento_id uuid,
    canal character varying(20),
    dados jsonb,
    enviado_em timestamp with time zone,
    status character varying(20) DEFAULT 'pendente'::character varying
);


ALTER TABLE public.notificacoes OWNER TO postgres;

--
-- TOC entry 254 (class 1259 OID 17265)
-- Name: notificacoes_notificacao_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.notificacoes_notificacao_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.notificacoes_notificacao_id_seq OWNER TO postgres;

--
-- TOC entry 5310 (class 0 OID 0)
-- Dependencies: 254
-- Name: notificacoes_notificacao_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.notificacoes_notificacao_id_seq OWNED BY public.notificacoes.notificacao_id;


--
-- TOC entry 231 (class 1259 OID 17001)
-- Name: pacientes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.pacientes (
    paciente_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    nome character varying(100) NOT NULL,
    sobrenome character varying(100) NOT NULL,
    data_nascimento date,
    sexo public.sexo_enum,
    endereco text,
    telefone character varying(20),
    email character varying(100),
    perfil_epidemiologico jsonb,
    criado_em timestamp with time zone DEFAULT now(),
    atualizado_em timestamp with time zone DEFAULT now()
);


ALTER TABLE public.pacientes OWNER TO postgres;

--
-- TOC entry 266 (class 1259 OID 17397)
-- Name: pedidos_compra; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.pedidos_compra (
    pedido_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    fornecedor_id integer,
    data_pedido timestamp with time zone DEFAULT now(),
    data_entrega_prevista date,
    status public.status_pedido_enum DEFAULT 'pendente'::public.status_pedido_enum,
    total_valor numeric(10,2),
    observacoes text,
    criado_por uuid,
    criado_em timestamp with time zone DEFAULT now(),
    atualizado_em timestamp with time zone DEFAULT now()
);


ALTER TABLE public.pedidos_compra OWNER TO postgres;

--
-- TOC entry 222 (class 1259 OID 16917)
-- Name: perfil_permissoes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.perfil_permissoes (
    perfil_id integer NOT NULL,
    permissao_id integer NOT NULL
);


ALTER TABLE public.perfil_permissoes OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 16898)
-- Name: perfis; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.perfis (
    perfil_id integer NOT NULL,
    nome character varying(50) NOT NULL
);


ALTER TABLE public.perfis OWNER TO postgres;

--
-- TOC entry 224 (class 1259 OID 16949)
-- Name: perfis_alunos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.perfis_alunos (
    usuario_id uuid NOT NULL,
    rgm character varying(20) NOT NULL,
    modelo_biometrico bytea
);


ALTER TABLE public.perfis_alunos OWNER TO postgres;

--
-- TOC entry 218 (class 1259 OID 16897)
-- Name: perfis_perfil_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.perfis_perfil_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.perfis_perfil_id_seq OWNER TO postgres;

--
-- TOC entry 5311 (class 0 OID 0)
-- Dependencies: 218
-- Name: perfis_perfil_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.perfis_perfil_id_seq OWNED BY public.perfis.perfil_id;


--
-- TOC entry 221 (class 1259 OID 16907)
-- Name: permissoes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.permissoes (
    permissao_id integer NOT NULL,
    codigo character varying(100) NOT NULL,
    descricao text
);


ALTER TABLE public.permissoes OWNER TO postgres;

--
-- TOC entry 220 (class 1259 OID 16906)
-- Name: permissoes_permissao_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.permissoes_permissao_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.permissoes_permissao_id_seq OWNER TO postgres;

--
-- TOC entry 5312 (class 0 OID 0)
-- Dependencies: 220
-- Name: permissoes_permissao_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.permissoes_permissao_id_seq OWNED BY public.permissoes.permissao_id;


--
-- TOC entry 257 (class 1259 OID 17281)
-- Name: produtos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.produtos (
    produto_id integer NOT NULL,
    nome character varying(100),
    descricao text,
    unidade character varying(20),
    nivel_minimo_estoque numeric DEFAULT 0,
    codigo_barras character varying(50),
    preco_custo numeric(10,2),
    preco_venda numeric(10,2),
    unidade_compra character varying(20),
    fator_conversao numeric(10,4) DEFAULT 1.0
);


ALTER TABLE public.produtos OWNER TO postgres;

--
-- TOC entry 256 (class 1259 OID 17280)
-- Name: produtos_produto_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.produtos_produto_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.produtos_produto_id_seq OWNER TO postgres;

--
-- TOC entry 5313 (class 0 OID 0)
-- Dependencies: 256
-- Name: produtos_produto_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.produtos_produto_id_seq OWNED BY public.produtos.produto_id;


--
-- TOC entry 243 (class 1259 OID 17138)
-- Name: prontuarios_eletronicos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.prontuarios_eletronicos (
    prontuario_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    agendamento_id uuid,
    clinica_id integer,
    aluno_id uuid,
    coordenador_id uuid,
    anotacoes text,
    criado_em timestamp with time zone DEFAULT now(),
    atualizado_em timestamp with time zone DEFAULT now()
);


ALTER TABLE public.prontuarios_eletronicos OWNER TO postgres;

--
-- TOC entry 244 (class 1259 OID 17168)
-- Name: prontuarios_eletronicos_versoes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.prontuarios_eletronicos_versoes (
    versao_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    prontuario_id uuid,
    aluno_id uuid,
    coordenador_id uuid,
    anotacoes text,
    criado_em timestamp with time zone DEFAULT now()
);


ALTER TABLE public.prontuarios_eletronicos_versoes OWNER TO postgres;

--
-- TOC entry 247 (class 1259 OID 17197)
-- Name: registros_presenca; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.registros_presenca (
    registro_id integer NOT NULL,
    aluno_id uuid,
    agendamento_id uuid,
    entrada timestamp with time zone DEFAULT now(),
    saida timestamp with time zone,
    horas_registradas numeric(5,2) GENERATED ALWAYS AS ((EXTRACT(epoch FROM (saida - entrada)) / (3600)::numeric)) STORED
);


ALTER TABLE public.registros_presenca OWNER TO postgres;

--
-- TOC entry 246 (class 1259 OID 17196)
-- Name: registros_presenca_registro_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.registros_presenca_registro_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.registros_presenca_registro_id_seq OWNER TO postgres;

--
-- TOC entry 5314 (class 0 OID 0)
-- Dependencies: 246
-- Name: registros_presenca_registro_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.registros_presenca_registro_id_seq OWNED BY public.registros_presenca.registro_id;


--
-- TOC entry 232 (class 1259 OID 17011)
-- Name: responsaveis_legais; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.responsaveis_legais (
    responsavel_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    paciente_id uuid,
    nome character varying(150) NOT NULL,
    cpf character varying(14),
    rg character varying(20),
    telefone character varying(20),
    email character varying(100),
    grau_parentesco character varying(50),
    endereco text,
    criado_em timestamp with time zone DEFAULT now()
);


ALTER TABLE public.responsaveis_legais OWNER TO postgres;

--
-- TOC entry 230 (class 1259 OID 16989)
-- Name: salas; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.salas (
    sala_id integer NOT NULL,
    clinica_id integer,
    nome character varying(50),
    capacidade integer DEFAULT 1
);


ALTER TABLE public.salas OWNER TO postgres;

--
-- TOC entry 229 (class 1259 OID 16988)
-- Name: salas_sala_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.salas_sala_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.salas_sala_id_seq OWNER TO postgres;

--
-- TOC entry 5315 (class 0 OID 0)
-- Dependencies: 229
-- Name: salas_sala_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.salas_sala_id_seq OWNED BY public.salas.sala_id;


--
-- TOC entry 228 (class 1259 OID 16975)
-- Name: servicos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.servicos (
    servico_id integer NOT NULL,
    clinica_id integer,
    nome character varying(100) NOT NULL,
    descricao text
);


ALTER TABLE public.servicos OWNER TO postgres;

--
-- TOC entry 227 (class 1259 OID 16974)
-- Name: servicos_servico_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.servicos_servico_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.servicos_servico_id_seq OWNER TO postgres;

--
-- TOC entry 5316 (class 0 OID 0)
-- Dependencies: 227
-- Name: servicos_servico_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.servicos_servico_id_seq OWNED BY public.servicos.servico_id;


--
-- TOC entry 241 (class 1259 OID 17090)
-- Name: status_agendamento; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.status_agendamento (
    status_id integer NOT NULL,
    nome public.status_agendamento_enum NOT NULL
);


ALTER TABLE public.status_agendamento OWNER TO postgres;

--
-- TOC entry 240 (class 1259 OID 17089)
-- Name: status_agendamento_status_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.status_agendamento_status_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.status_agendamento_status_id_seq OWNER TO postgres;

--
-- TOC entry 5317 (class 0 OID 0)
-- Dependencies: 240
-- Name: status_agendamento_status_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.status_agendamento_status_id_seq OWNED BY public.status_agendamento.status_id;


--
-- TOC entry 234 (class 1259 OID 17026)
-- Name: tipos_documentos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tipos_documentos (
    tipo_id integer NOT NULL,
    nome character varying(50) NOT NULL,
    descricao text,
    obrigatorio boolean DEFAULT false
);


ALTER TABLE public.tipos_documentos OWNER TO postgres;

--
-- TOC entry 233 (class 1259 OID 17025)
-- Name: tipos_documentos_tipo_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tipos_documentos_tipo_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tipos_documentos_tipo_id_seq OWNER TO postgres;

--
-- TOC entry 5318 (class 0 OID 0)
-- Dependencies: 233
-- Name: tipos_documentos_tipo_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tipos_documentos_tipo_id_seq OWNED BY public.tipos_documentos.tipo_id;


--
-- TOC entry 223 (class 1259 OID 16932)
-- Name: usuarios; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.usuarios (
    usuario_id uuid DEFAULT public.uuid_generate_v4() NOT NULL,
    nome_usuario character varying(50) NOT NULL,
    senha_hash text NOT NULL,
    perfil_id integer,
    nome_completo character varying(150) NOT NULL,
    email character varying(100),
    telefone character varying(20),
    criado_em timestamp with time zone DEFAULT now(),
    atualizado_em timestamp with time zone DEFAULT now()
);


ALTER TABLE public.usuarios OWNER TO postgres;

--
-- TOC entry 4878 (class 2604 OID 16967)
-- Name: clinicas clinica_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clinicas ALTER COLUMN clinica_id SET DEFAULT nextval('public.clinicas_clinica_id_seq'::regclass);


--
-- TOC entry 4891 (class 2604 OID 17060)
-- Name: consentimentos_pacientes consentimento_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.consentimentos_pacientes ALTER COLUMN consentimento_id SET DEFAULT nextval('public.consentimentos_pacientes_consentimento_id_seq'::regclass);


--
-- TOC entry 4909 (class 2604 OID 17219)
-- Name: fila_espera fila_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fila_espera ALTER COLUMN fila_id SET DEFAULT nextval('public.fila_espera_fila_id_seq'::regclass);


--
-- TOC entry 4925 (class 2604 OID 17328)
-- Name: fornecedores fornecedor_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fornecedores ALTER COLUMN fornecedor_id SET DEFAULT nextval('public.fornecedores_fornecedor_id_seq'::regclass);


--
-- TOC entry 4894 (class 2604 OID 17076)
-- Name: horarios horario_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.horarios ALTER COLUMN horario_id SET DEFAULT nextval('public.horarios_horario_id_seq'::regclass);


--
-- TOC entry 4939 (class 2604 OID 17423)
-- Name: itens_pedido_compra item_pedido_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.itens_pedido_compra ALTER COLUMN item_pedido_id SET DEFAULT nextval('public.itens_pedido_compra_item_pedido_id_seq'::regclass);


--
-- TOC entry 4928 (class 2604 OID 17343)
-- Name: localizacoes_estoque localizacao_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.localizacoes_estoque ALTER COLUMN localizacao_id SET DEFAULT nextval('public.localizacoes_estoque_localizacao_id_seq'::regclass);


--
-- TOC entry 4915 (class 2604 OID 17254)
-- Name: logs_acesso log_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.logs_acesso ALTER COLUMN log_id SET DEFAULT nextval('public.logs_acesso_log_id_seq'::regclass);


--
-- TOC entry 4913 (class 2604 OID 17239)
-- Name: logs_auditoria auditoria_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.logs_auditoria ALTER COLUMN auditoria_id SET DEFAULT nextval('public.logs_auditoria_auditoria_id_seq'::regclass);


--
-- TOC entry 4922 (class 2604 OID 17294)
-- Name: movimentos_estoque movimento_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.movimentos_estoque ALTER COLUMN movimento_id SET DEFAULT nextval('public.movimentos_estoque_movimento_id_seq'::regclass);


--
-- TOC entry 4917 (class 2604 OID 17269)
-- Name: notificacoes notificacao_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.notificacoes ALTER COLUMN notificacao_id SET DEFAULT nextval('public.notificacoes_notificacao_id_seq'::regclass);


--
-- TOC entry 4873 (class 2604 OID 16901)
-- Name: perfis perfil_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.perfis ALTER COLUMN perfil_id SET DEFAULT nextval('public.perfis_perfil_id_seq'::regclass);


--
-- TOC entry 4874 (class 2604 OID 16910)
-- Name: permissoes permissao_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.permissoes ALTER COLUMN permissao_id SET DEFAULT nextval('public.permissoes_permissao_id_seq'::regclass);


--
-- TOC entry 4919 (class 2604 OID 17284)
-- Name: produtos produto_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.produtos ALTER COLUMN produto_id SET DEFAULT nextval('public.produtos_produto_id_seq'::regclass);


--
-- TOC entry 4906 (class 2604 OID 17200)
-- Name: registros_presenca registro_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.registros_presenca ALTER COLUMN registro_id SET DEFAULT nextval('public.registros_presenca_registro_id_seq'::regclass);


--
-- TOC entry 4880 (class 2604 OID 16992)
-- Name: salas sala_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.salas ALTER COLUMN sala_id SET DEFAULT nextval('public.salas_sala_id_seq'::regclass);


--
-- TOC entry 4879 (class 2604 OID 16978)
-- Name: servicos servico_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.servicos ALTER COLUMN servico_id SET DEFAULT nextval('public.servicos_servico_id_seq'::regclass);


--
-- TOC entry 4895 (class 2604 OID 17093)
-- Name: status_agendamento status_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.status_agendamento ALTER COLUMN status_id SET DEFAULT nextval('public.status_agendamento_status_id_seq'::regclass);


--
-- TOC entry 4887 (class 2604 OID 17029)
-- Name: tipos_documentos tipo_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tipos_documentos ALTER COLUMN tipo_id SET DEFAULT nextval('public.tipos_documentos_tipo_id_seq'::regclass);


--
-- TOC entry 5265 (class 0 OID 17098)
-- Dependencies: 242
-- Data for Name: agendamentos; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.agendamentos (agendamento_id, clinica_id, paciente_id, horario_id, aluno_id, coordenador_id, status_id, criado_em, atualizado_em) FROM stdin;
\.


--
-- TOC entry 5292 (class 0 OID 17453)
-- Dependencies: 269
-- Data for Name: ajustes_estoque; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ajustes_estoque (ajuste_id, produto_id, lote_id, localizacao_id, quantidade, tipo_ajuste, motivo, ajustado_por, ajustado_em) FROM stdin;
\.


--
-- TOC entry 5268 (class 0 OID 17182)
-- Dependencies: 245
-- Data for Name: anexos_prontuario; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.anexos_prontuario (anexo_id, prontuario_id, tipo_anexo, caminho_arquivo, metadados, enviado_em) FROM stdin;
\.


--
-- TOC entry 5249 (class 0 OID 16964)
-- Dependencies: 226
-- Data for Name: clinicas; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.clinicas (clinica_id, nome, descricao) FROM stdin;
\.


--
-- TOC entry 5283 (class 0 OID 17310)
-- Dependencies: 260
-- Data for Name: configuracoes_sistema; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.configuracoes_sistema (chave, valor, atualizado_em) FROM stdin;
\.


--
-- TOC entry 5260 (class 0 OID 17057)
-- Dependencies: 237
-- Data for Name: consentimentos_pacientes; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.consentimentos_pacientes (consentimento_id, paciente_id, tipo_consentimento, data_consentimento, ativo, detalhes) FROM stdin;
\.


--
-- TOC entry 5258 (class 0 OID 17037)
-- Dependencies: 235
-- Data for Name: documentos_pacientes; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.documentos_pacientes (documento_id, paciente_id, tipo_id, dados_ocr, caminho_arquivo, enviado_em) FROM stdin;
\.


--
-- TOC entry 5272 (class 0 OID 17216)
-- Dependencies: 249
-- Data for Name: fila_espera; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.fila_espera (fila_id, clinica_id, paciente_id, numero_fila, prioridade, status, criado_em, chamado_em, concluido_em) FROM stdin;
\.


--
-- TOC entry 5285 (class 0 OID 17325)
-- Dependencies: 262
-- Data for Name: fornecedores; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.fornecedores (fornecedor_id, nome, cnpj, contato_nome, contato_email, contato_telefone, endereco, criado_em, atualizado_em) FROM stdin;
\.


--
-- TOC entry 5262 (class 0 OID 17073)
-- Dependencies: 239
-- Data for Name: horarios; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.horarios (horario_id, servico_id, sala_id, inicio, fim) FROM stdin;
\.


--
-- TOC entry 5291 (class 0 OID 17420)
-- Dependencies: 268
-- Data for Name: itens_pedido_compra; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.itens_pedido_compra (item_pedido_id, pedido_id, produto_id, quantidade_pedida, quantidade_recebida, preco_unitario, criado_em) FROM stdin;
\.


--
-- TOC entry 5287 (class 0 OID 17340)
-- Dependencies: 264
-- Data for Name: localizacoes_estoque; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.localizacoes_estoque (localizacao_id, nome, descricao, clinica_id, criado_em, atualizado_em) FROM stdin;
\.


--
-- TOC entry 5276 (class 0 OID 17251)
-- Dependencies: 253
-- Data for Name: logs_acesso; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.logs_acesso (log_id, usuario_id, endereco_ip, agente_usuario, horario_login, sucesso) FROM stdin;
\.


--
-- TOC entry 5274 (class 0 OID 17236)
-- Dependencies: 251
-- Data for Name: logs_auditoria; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.logs_auditoria (auditoria_id, usuario_id, acao, nome_tabela, id_registro, horario_acao, dados_antigos, dados_novos) FROM stdin;
\.


--
-- TOC entry 5288 (class 0 OID 17360)
-- Dependencies: 265
-- Data for Name: lotes_produtos; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.lotes_produtos (lote_id, produto_id, numero_lote, data_fabricacao, data_validade, quantidade_inicial, quantidade_atual, fornecedor_id, localizacao_id, criado_em, atualizado_em) FROM stdin;
\.


--
-- TOC entry 5282 (class 0 OID 17291)
-- Dependencies: 259
-- Data for Name: movimentos_estoque; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.movimentos_estoque (movimento_id, produto_id, quantidade, tipo_movimento, referencia, movimentado_em, movimentado_por, lote_id, localizacao_id) FROM stdin;
\.


--
-- TOC entry 5278 (class 0 OID 17266)
-- Dependencies: 255
-- Data for Name: notificacoes; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.notificacoes (notificacao_id, agendamento_id, canal, dados, enviado_em, status) FROM stdin;
\.


--
-- TOC entry 5254 (class 0 OID 17001)
-- Dependencies: 231
-- Data for Name: pacientes; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.pacientes (paciente_id, nome, sobrenome, data_nascimento, sexo, endereco, telefone, email, perfil_epidemiologico, criado_em, atualizado_em) FROM stdin;
\.


--
-- TOC entry 5289 (class 0 OID 17397)
-- Dependencies: 266
-- Data for Name: pedidos_compra; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.pedidos_compra (pedido_id, fornecedor_id, data_pedido, data_entrega_prevista, status, total_valor, observacoes, criado_por, criado_em, atualizado_em) FROM stdin;
\.


--
-- TOC entry 5245 (class 0 OID 16917)
-- Dependencies: 222
-- Data for Name: perfil_permissoes; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.perfil_permissoes (perfil_id, permissao_id) FROM stdin;
\.


--
-- TOC entry 5242 (class 0 OID 16898)
-- Dependencies: 219
-- Data for Name: perfis; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.perfis (perfil_id, nome) FROM stdin;
\.


--
-- TOC entry 5247 (class 0 OID 16949)
-- Dependencies: 224
-- Data for Name: perfis_alunos; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.perfis_alunos (usuario_id, rgm, modelo_biometrico) FROM stdin;
\.


--
-- TOC entry 5244 (class 0 OID 16907)
-- Dependencies: 221
-- Data for Name: permissoes; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.permissoes (permissao_id, codigo, descricao) FROM stdin;
\.


--
-- TOC entry 5280 (class 0 OID 17281)
-- Dependencies: 257
-- Data for Name: produtos; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.produtos (produto_id, nome, descricao, unidade, nivel_minimo_estoque, codigo_barras, preco_custo, preco_venda, unidade_compra, fator_conversao) FROM stdin;
\.


--
-- TOC entry 5266 (class 0 OID 17138)
-- Dependencies: 243
-- Data for Name: prontuarios_eletronicos; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.prontuarios_eletronicos (prontuario_id, agendamento_id, clinica_id, aluno_id, coordenador_id, anotacoes, criado_em, atualizado_em) FROM stdin;
\.


--
-- TOC entry 5267 (class 0 OID 17168)
-- Dependencies: 244
-- Data for Name: prontuarios_eletronicos_versoes; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.prontuarios_eletronicos_versoes (versao_id, prontuario_id, aluno_id, coordenador_id, anotacoes, criado_em) FROM stdin;
\.


--
-- TOC entry 5270 (class 0 OID 17197)
-- Dependencies: 247
-- Data for Name: registros_presenca; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.registros_presenca (registro_id, aluno_id, agendamento_id, entrada, saida) FROM stdin;
\.


--
-- TOC entry 5255 (class 0 OID 17011)
-- Dependencies: 232
-- Data for Name: responsaveis_legais; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.responsaveis_legais (responsavel_id, paciente_id, nome, cpf, rg, telefone, email, grau_parentesco, endereco, criado_em) FROM stdin;
\.


--
-- TOC entry 5253 (class 0 OID 16989)
-- Dependencies: 230
-- Data for Name: salas; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.salas (sala_id, clinica_id, nome, capacidade) FROM stdin;
\.


--
-- TOC entry 5251 (class 0 OID 16975)
-- Dependencies: 228
-- Data for Name: servicos; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.servicos (servico_id, clinica_id, nome, descricao) FROM stdin;
\.


--
-- TOC entry 5264 (class 0 OID 17090)
-- Dependencies: 241
-- Data for Name: status_agendamento; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.status_agendamento (status_id, nome) FROM stdin;
1	agendado
2	registrado
3	concluido
4	cancelado
5	faltou
\.


--
-- TOC entry 5257 (class 0 OID 17026)
-- Dependencies: 234
-- Data for Name: tipos_documentos; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tipos_documentos (tipo_id, nome, descricao, obrigatorio) FROM stdin;
\.


--
-- TOC entry 5246 (class 0 OID 16932)
-- Dependencies: 223
-- Data for Name: usuarios; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.usuarios (usuario_id, nome_usuario, senha_hash, perfil_id, nome_completo, email, telefone, criado_em, atualizado_em) FROM stdin;
\.


--
-- TOC entry 5319 (class 0 OID 0)
-- Dependencies: 225
-- Name: clinicas_clinica_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.clinicas_clinica_id_seq', 1, false);


--
-- TOC entry 5320 (class 0 OID 0)
-- Dependencies: 236
-- Name: consentimentos_pacientes_consentimento_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.consentimentos_pacientes_consentimento_id_seq', 1, false);


--
-- TOC entry 5321 (class 0 OID 0)
-- Dependencies: 248
-- Name: fila_espera_fila_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.fila_espera_fila_id_seq', 1, false);


--
-- TOC entry 5322 (class 0 OID 0)
-- Dependencies: 261
-- Name: fornecedores_fornecedor_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.fornecedores_fornecedor_id_seq', 1, false);


--
-- TOC entry 5323 (class 0 OID 0)
-- Dependencies: 238
-- Name: horarios_horario_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.horarios_horario_id_seq', 1, false);


--
-- TOC entry 5324 (class 0 OID 0)
-- Dependencies: 267
-- Name: itens_pedido_compra_item_pedido_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.itens_pedido_compra_item_pedido_id_seq', 1, false);


--
-- TOC entry 5325 (class 0 OID 0)
-- Dependencies: 263
-- Name: localizacoes_estoque_localizacao_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.localizacoes_estoque_localizacao_id_seq', 1, false);


--
-- TOC entry 5326 (class 0 OID 0)
-- Dependencies: 252
-- Name: logs_acesso_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.logs_acesso_log_id_seq', 1, false);


--
-- TOC entry 5327 (class 0 OID 0)
-- Dependencies: 250
-- Name: logs_auditoria_auditoria_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.logs_auditoria_auditoria_id_seq', 1, false);


--
-- TOC entry 5328 (class 0 OID 0)
-- Dependencies: 258
-- Name: movimentos_estoque_movimento_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.movimentos_estoque_movimento_id_seq', 1, false);


--
-- TOC entry 5329 (class 0 OID 0)
-- Dependencies: 254
-- Name: notificacoes_notificacao_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.notificacoes_notificacao_id_seq', 1, false);


--
-- TOC entry 5330 (class 0 OID 0)
-- Dependencies: 218
-- Name: perfis_perfil_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.perfis_perfil_id_seq', 1, false);


--
-- TOC entry 5331 (class 0 OID 0)
-- Dependencies: 220
-- Name: permissoes_permissao_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.permissoes_permissao_id_seq', 1, false);


--
-- TOC entry 5332 (class 0 OID 0)
-- Dependencies: 256
-- Name: produtos_produto_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.produtos_produto_id_seq', 1, false);


--
-- TOC entry 5333 (class 0 OID 0)
-- Dependencies: 246
-- Name: registros_presenca_registro_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.registros_presenca_registro_id_seq', 1, false);


--
-- TOC entry 5334 (class 0 OID 0)
-- Dependencies: 229
-- Name: salas_sala_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.salas_sala_id_seq', 1, false);


--
-- TOC entry 5335 (class 0 OID 0)
-- Dependencies: 227
-- Name: servicos_servico_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.servicos_servico_id_seq', 1, false);


--
-- TOC entry 5336 (class 0 OID 0)
-- Dependencies: 240
-- Name: status_agendamento_status_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.status_agendamento_status_id_seq', 5, true);


--
-- TOC entry 5337 (class 0 OID 0)
-- Dependencies: 233
-- Name: tipos_documentos_tipo_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tipos_documentos_tipo_id_seq', 1, false);


--
-- TOC entry 4989 (class 2606 OID 17107)
-- Name: agendamentos agendamentos_paciente_id_horario_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.agendamentos
    ADD CONSTRAINT agendamentos_paciente_id_horario_id_key UNIQUE (paciente_id, horario_id);


--
-- TOC entry 4991 (class 2606 OID 17105)
-- Name: agendamentos agendamentos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.agendamentos
    ADD CONSTRAINT agendamentos_pkey PRIMARY KEY (agendamento_id);


--
-- TOC entry 5045 (class 2606 OID 17461)
-- Name: ajustes_estoque ajustes_estoque_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ajustes_estoque
    ADD CONSTRAINT ajustes_estoque_pkey PRIMARY KEY (ajuste_id);


--
-- TOC entry 4999 (class 2606 OID 17190)
-- Name: anexos_prontuario anexos_prontuario_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.anexos_prontuario
    ADD CONSTRAINT anexos_prontuario_pkey PRIMARY KEY (anexo_id);


--
-- TOC entry 4963 (class 2606 OID 16973)
-- Name: clinicas clinicas_nome_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clinicas
    ADD CONSTRAINT clinicas_nome_key UNIQUE (nome);


--
-- TOC entry 4965 (class 2606 OID 16971)
-- Name: clinicas clinicas_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clinicas
    ADD CONSTRAINT clinicas_pkey PRIMARY KEY (clinica_id);


--
-- TOC entry 5022 (class 2606 OID 17317)
-- Name: configuracoes_sistema configuracoes_sistema_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.configuracoes_sistema
    ADD CONSTRAINT configuracoes_sistema_pkey PRIMARY KEY (chave);


--
-- TOC entry 4981 (class 2606 OID 17066)
-- Name: consentimentos_pacientes consentimentos_pacientes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.consentimentos_pacientes
    ADD CONSTRAINT consentimentos_pacientes_pkey PRIMARY KEY (consentimento_id);


--
-- TOC entry 4979 (class 2606 OID 17045)
-- Name: documentos_pacientes documentos_pacientes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.documentos_pacientes
    ADD CONSTRAINT documentos_pacientes_pkey PRIMARY KEY (documento_id);


--
-- TOC entry 5004 (class 2606 OID 17224)
-- Name: fila_espera fila_espera_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fila_espera
    ADD CONSTRAINT fila_espera_pkey PRIMARY KEY (fila_id);


--
-- TOC entry 5024 (class 2606 OID 17338)
-- Name: fornecedores fornecedores_cnpj_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fornecedores
    ADD CONSTRAINT fornecedores_cnpj_key UNIQUE (cnpj);


--
-- TOC entry 5026 (class 2606 OID 17336)
-- Name: fornecedores fornecedores_nome_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fornecedores
    ADD CONSTRAINT fornecedores_nome_key UNIQUE (nome);


--
-- TOC entry 5028 (class 2606 OID 17334)
-- Name: fornecedores fornecedores_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fornecedores
    ADD CONSTRAINT fornecedores_pkey PRIMARY KEY (fornecedor_id);


--
-- TOC entry 4983 (class 2606 OID 17078)
-- Name: horarios horarios_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.horarios
    ADD CONSTRAINT horarios_pkey PRIMARY KEY (horario_id);


--
-- TOC entry 5043 (class 2606 OID 17427)
-- Name: itens_pedido_compra itens_pedido_compra_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.itens_pedido_compra
    ADD CONSTRAINT itens_pedido_compra_pkey PRIMARY KEY (item_pedido_id);


--
-- TOC entry 5030 (class 2606 OID 17351)
-- Name: localizacoes_estoque localizacoes_estoque_nome_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.localizacoes_estoque
    ADD CONSTRAINT localizacoes_estoque_nome_key UNIQUE (nome);


--
-- TOC entry 5032 (class 2606 OID 17349)
-- Name: localizacoes_estoque localizacoes_estoque_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.localizacoes_estoque
    ADD CONSTRAINT localizacoes_estoque_pkey PRIMARY KEY (localizacao_id);


--
-- TOC entry 5010 (class 2606 OID 17259)
-- Name: logs_acesso logs_acesso_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.logs_acesso
    ADD CONSTRAINT logs_acesso_pkey PRIMARY KEY (log_id);


--
-- TOC entry 5007 (class 2606 OID 17244)
-- Name: logs_auditoria logs_auditoria_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.logs_auditoria
    ADD CONSTRAINT logs_auditoria_pkey PRIMARY KEY (auditoria_id);


--
-- TOC entry 5036 (class 2606 OID 17367)
-- Name: lotes_produtos lotes_produtos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.lotes_produtos
    ADD CONSTRAINT lotes_produtos_pkey PRIMARY KEY (lote_id);


--
-- TOC entry 5038 (class 2606 OID 17369)
-- Name: lotes_produtos lotes_produtos_produto_id_numero_lote_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.lotes_produtos
    ADD CONSTRAINT lotes_produtos_produto_id_numero_lote_key UNIQUE (produto_id, numero_lote);


--
-- TOC entry 5020 (class 2606 OID 17299)
-- Name: movimentos_estoque movimentos_estoque_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.movimentos_estoque
    ADD CONSTRAINT movimentos_estoque_pkey PRIMARY KEY (movimento_id);


--
-- TOC entry 5012 (class 2606 OID 17274)
-- Name: notificacoes notificacoes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.notificacoes
    ADD CONSTRAINT notificacoes_pkey PRIMARY KEY (notificacao_id);


--
-- TOC entry 4971 (class 2606 OID 17010)
-- Name: pacientes pacientes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pacientes
    ADD CONSTRAINT pacientes_pkey PRIMARY KEY (paciente_id);


--
-- TOC entry 5041 (class 2606 OID 17408)
-- Name: pedidos_compra pedidos_compra_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pedidos_compra
    ADD CONSTRAINT pedidos_compra_pkey PRIMARY KEY (pedido_id);


--
-- TOC entry 4953 (class 2606 OID 16921)
-- Name: perfil_permissoes perfil_permissoes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.perfil_permissoes
    ADD CONSTRAINT perfil_permissoes_pkey PRIMARY KEY (perfil_id, permissao_id);


--
-- TOC entry 4959 (class 2606 OID 16955)
-- Name: perfis_alunos perfis_alunos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.perfis_alunos
    ADD CONSTRAINT perfis_alunos_pkey PRIMARY KEY (usuario_id);


--
-- TOC entry 4961 (class 2606 OID 16957)
-- Name: perfis_alunos perfis_alunos_rgm_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.perfis_alunos
    ADD CONSTRAINT perfis_alunos_rgm_key UNIQUE (rgm);


--
-- TOC entry 4945 (class 2606 OID 16905)
-- Name: perfis perfis_nome_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.perfis
    ADD CONSTRAINT perfis_nome_key UNIQUE (nome);


--
-- TOC entry 4947 (class 2606 OID 16903)
-- Name: perfis perfis_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.perfis
    ADD CONSTRAINT perfis_pkey PRIMARY KEY (perfil_id);


--
-- TOC entry 4949 (class 2606 OID 16916)
-- Name: permissoes permissoes_codigo_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.permissoes
    ADD CONSTRAINT permissoes_codigo_key UNIQUE (codigo);


--
-- TOC entry 4951 (class 2606 OID 16914)
-- Name: permissoes permissoes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.permissoes
    ADD CONSTRAINT permissoes_pkey PRIMARY KEY (permissao_id);


--
-- TOC entry 5014 (class 2606 OID 17359)
-- Name: produtos produtos_codigo_barras_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.produtos
    ADD CONSTRAINT produtos_codigo_barras_key UNIQUE (codigo_barras);


--
-- TOC entry 5016 (class 2606 OID 17289)
-- Name: produtos produtos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.produtos
    ADD CONSTRAINT produtos_pkey PRIMARY KEY (produto_id);


--
-- TOC entry 4995 (class 2606 OID 17147)
-- Name: prontuarios_eletronicos prontuarios_eletronicos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.prontuarios_eletronicos
    ADD CONSTRAINT prontuarios_eletronicos_pkey PRIMARY KEY (prontuario_id);


--
-- TOC entry 4997 (class 2606 OID 17176)
-- Name: prontuarios_eletronicos_versoes prontuarios_eletronicos_versoes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.prontuarios_eletronicos_versoes
    ADD CONSTRAINT prontuarios_eletronicos_versoes_pkey PRIMARY KEY (versao_id);


--
-- TOC entry 5002 (class 2606 OID 17204)
-- Name: registros_presenca registros_presenca_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.registros_presenca
    ADD CONSTRAINT registros_presenca_pkey PRIMARY KEY (registro_id);


--
-- TOC entry 4973 (class 2606 OID 17019)
-- Name: responsaveis_legais responsaveis_legais_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.responsaveis_legais
    ADD CONSTRAINT responsaveis_legais_pkey PRIMARY KEY (responsavel_id);


--
-- TOC entry 4969 (class 2606 OID 16995)
-- Name: salas salas_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.salas
    ADD CONSTRAINT salas_pkey PRIMARY KEY (sala_id);


--
-- TOC entry 4967 (class 2606 OID 16982)
-- Name: servicos servicos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.servicos
    ADD CONSTRAINT servicos_pkey PRIMARY KEY (servico_id);


--
-- TOC entry 4985 (class 2606 OID 17097)
-- Name: status_agendamento status_agendamento_nome_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.status_agendamento
    ADD CONSTRAINT status_agendamento_nome_key UNIQUE (nome);


--
-- TOC entry 4987 (class 2606 OID 17095)
-- Name: status_agendamento status_agendamento_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.status_agendamento
    ADD CONSTRAINT status_agendamento_pkey PRIMARY KEY (status_id);


--
-- TOC entry 4975 (class 2606 OID 17036)
-- Name: tipos_documentos tipos_documentos_nome_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tipos_documentos
    ADD CONSTRAINT tipos_documentos_nome_key UNIQUE (nome);


--
-- TOC entry 4977 (class 2606 OID 17034)
-- Name: tipos_documentos tipos_documentos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tipos_documentos
    ADD CONSTRAINT tipos_documentos_pkey PRIMARY KEY (tipo_id);


--
-- TOC entry 4955 (class 2606 OID 16943)
-- Name: usuarios usuarios_nome_usuario_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_nome_usuario_key UNIQUE (nome_usuario);


--
-- TOC entry 4957 (class 2606 OID 16941)
-- Name: usuarios usuarios_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_pkey PRIMARY KEY (usuario_id);


--
-- TOC entry 4992 (class 1259 OID 17319)
-- Name: idx_agendamentos_aluno; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_agendamentos_aluno ON public.agendamentos USING btree (aluno_id);


--
-- TOC entry 4993 (class 1259 OID 17318)
-- Name: idx_agendamentos_paciente; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_agendamentos_paciente ON public.agendamentos USING btree (paciente_id);


--
-- TOC entry 5046 (class 1259 OID 17499)
-- Name: idx_ajustes_estoque_localizacao_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_ajustes_estoque_localizacao_id ON public.ajustes_estoque USING btree (localizacao_id);


--
-- TOC entry 5047 (class 1259 OID 17498)
-- Name: idx_ajustes_estoque_lote_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_ajustes_estoque_lote_id ON public.ajustes_estoque USING btree (lote_id);


--
-- TOC entry 5048 (class 1259 OID 17497)
-- Name: idx_ajustes_estoque_produto_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_ajustes_estoque_produto_id ON public.ajustes_estoque USING btree (produto_id);


--
-- TOC entry 5005 (class 1259 OID 17321)
-- Name: idx_fila_espera_status; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_fila_espera_status ON public.fila_espera USING btree (status);


--
-- TOC entry 5008 (class 1259 OID 17322)
-- Name: idx_logs_acesso_horario; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_logs_acesso_horario ON public.logs_acesso USING btree (horario_login);


--
-- TOC entry 5033 (class 1259 OID 17493)
-- Name: idx_lotes_produtos_data_validade; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_lotes_produtos_data_validade ON public.lotes_produtos USING btree (data_validade);


--
-- TOC entry 5034 (class 1259 OID 17492)
-- Name: idx_lotes_produtos_produto_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_lotes_produtos_produto_id ON public.lotes_produtos USING btree (produto_id);


--
-- TOC entry 5017 (class 1259 OID 17495)
-- Name: idx_movimentos_estoque_localizacao_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_movimentos_estoque_localizacao_id ON public.movimentos_estoque USING btree (localizacao_id);


--
-- TOC entry 5018 (class 1259 OID 17494)
-- Name: idx_movimentos_estoque_lote_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_movimentos_estoque_lote_id ON public.movimentos_estoque USING btree (lote_id);


--
-- TOC entry 5039 (class 1259 OID 17496)
-- Name: idx_pedidos_compra_fornecedor_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_pedidos_compra_fornecedor_id ON public.pedidos_compra USING btree (fornecedor_id);


--
-- TOC entry 5000 (class 1259 OID 17320)
-- Name: idx_registros_presenca_aluno; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_registros_presenca_aluno ON public.registros_presenca USING btree (aluno_id);


--
-- TOC entry 5061 (class 2606 OID 17123)
-- Name: agendamentos agendamentos_aluno_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.agendamentos
    ADD CONSTRAINT agendamentos_aluno_id_fkey FOREIGN KEY (aluno_id) REFERENCES public.usuarios(usuario_id);


--
-- TOC entry 5062 (class 2606 OID 17108)
-- Name: agendamentos agendamentos_clinica_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.agendamentos
    ADD CONSTRAINT agendamentos_clinica_id_fkey FOREIGN KEY (clinica_id) REFERENCES public.clinicas(clinica_id);


--
-- TOC entry 5063 (class 2606 OID 17128)
-- Name: agendamentos agendamentos_coordenador_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.agendamentos
    ADD CONSTRAINT agendamentos_coordenador_id_fkey FOREIGN KEY (coordenador_id) REFERENCES public.usuarios(usuario_id);


--
-- TOC entry 5064 (class 2606 OID 17118)
-- Name: agendamentos agendamentos_horario_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.agendamentos
    ADD CONSTRAINT agendamentos_horario_id_fkey FOREIGN KEY (horario_id) REFERENCES public.horarios(horario_id);


--
-- TOC entry 5065 (class 2606 OID 17113)
-- Name: agendamentos agendamentos_paciente_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.agendamentos
    ADD CONSTRAINT agendamentos_paciente_id_fkey FOREIGN KEY (paciente_id) REFERENCES public.pacientes(paciente_id);


--
-- TOC entry 5066 (class 2606 OID 17133)
-- Name: agendamentos agendamentos_status_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.agendamentos
    ADD CONSTRAINT agendamentos_status_id_fkey FOREIGN KEY (status_id) REFERENCES public.status_agendamento(status_id);


--
-- TOC entry 5092 (class 2606 OID 17477)
-- Name: ajustes_estoque ajustes_estoque_ajustado_por_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ajustes_estoque
    ADD CONSTRAINT ajustes_estoque_ajustado_por_fkey FOREIGN KEY (ajustado_por) REFERENCES public.usuarios(usuario_id);


--
-- TOC entry 5093 (class 2606 OID 17472)
-- Name: ajustes_estoque ajustes_estoque_localizacao_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ajustes_estoque
    ADD CONSTRAINT ajustes_estoque_localizacao_id_fkey FOREIGN KEY (localizacao_id) REFERENCES public.localizacoes_estoque(localizacao_id) ON DELETE CASCADE;


--
-- TOC entry 5094 (class 2606 OID 17467)
-- Name: ajustes_estoque ajustes_estoque_lote_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ajustes_estoque
    ADD CONSTRAINT ajustes_estoque_lote_id_fkey FOREIGN KEY (lote_id) REFERENCES public.lotes_produtos(lote_id) ON DELETE CASCADE;


--
-- TOC entry 5095 (class 2606 OID 17462)
-- Name: ajustes_estoque ajustes_estoque_produto_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ajustes_estoque
    ADD CONSTRAINT ajustes_estoque_produto_id_fkey FOREIGN KEY (produto_id) REFERENCES public.produtos(produto_id) ON DELETE CASCADE;


--
-- TOC entry 5072 (class 2606 OID 17191)
-- Name: anexos_prontuario anexos_prontuario_prontuario_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.anexos_prontuario
    ADD CONSTRAINT anexos_prontuario_prontuario_id_fkey FOREIGN KEY (prontuario_id) REFERENCES public.prontuarios_eletronicos(prontuario_id) ON DELETE CASCADE;


--
-- TOC entry 5058 (class 2606 OID 17067)
-- Name: consentimentos_pacientes consentimentos_pacientes_paciente_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.consentimentos_pacientes
    ADD CONSTRAINT consentimentos_pacientes_paciente_id_fkey FOREIGN KEY (paciente_id) REFERENCES public.pacientes(paciente_id) ON DELETE CASCADE;


--
-- TOC entry 5056 (class 2606 OID 17046)
-- Name: documentos_pacientes documentos_pacientes_paciente_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.documentos_pacientes
    ADD CONSTRAINT documentos_pacientes_paciente_id_fkey FOREIGN KEY (paciente_id) REFERENCES public.pacientes(paciente_id) ON DELETE CASCADE;


--
-- TOC entry 5057 (class 2606 OID 17051)
-- Name: documentos_pacientes documentos_pacientes_tipo_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.documentos_pacientes
    ADD CONSTRAINT documentos_pacientes_tipo_id_fkey FOREIGN KEY (tipo_id) REFERENCES public.tipos_documentos(tipo_id);


--
-- TOC entry 5075 (class 2606 OID 17225)
-- Name: fila_espera fila_espera_clinica_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fila_espera
    ADD CONSTRAINT fila_espera_clinica_id_fkey FOREIGN KEY (clinica_id) REFERENCES public.clinicas(clinica_id);


--
-- TOC entry 5076 (class 2606 OID 17230)
-- Name: fila_espera fila_espera_paciente_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fila_espera
    ADD CONSTRAINT fila_espera_paciente_id_fkey FOREIGN KEY (paciente_id) REFERENCES public.pacientes(paciente_id);


--
-- TOC entry 5059 (class 2606 OID 17084)
-- Name: horarios horarios_sala_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.horarios
    ADD CONSTRAINT horarios_sala_id_fkey FOREIGN KEY (sala_id) REFERENCES public.salas(sala_id);


--
-- TOC entry 5060 (class 2606 OID 17079)
-- Name: horarios horarios_servico_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.horarios
    ADD CONSTRAINT horarios_servico_id_fkey FOREIGN KEY (servico_id) REFERENCES public.servicos(servico_id);


--
-- TOC entry 5090 (class 2606 OID 17428)
-- Name: itens_pedido_compra itens_pedido_compra_pedido_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.itens_pedido_compra
    ADD CONSTRAINT itens_pedido_compra_pedido_id_fkey FOREIGN KEY (pedido_id) REFERENCES public.pedidos_compra(pedido_id) ON DELETE CASCADE;


--
-- TOC entry 5091 (class 2606 OID 17433)
-- Name: itens_pedido_compra itens_pedido_compra_produto_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.itens_pedido_compra
    ADD CONSTRAINT itens_pedido_compra_produto_id_fkey FOREIGN KEY (produto_id) REFERENCES public.produtos(produto_id) ON DELETE CASCADE;


--
-- TOC entry 5084 (class 2606 OID 17352)
-- Name: localizacoes_estoque localizacoes_estoque_clinica_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.localizacoes_estoque
    ADD CONSTRAINT localizacoes_estoque_clinica_id_fkey FOREIGN KEY (clinica_id) REFERENCES public.clinicas(clinica_id) ON DELETE CASCADE;


--
-- TOC entry 5078 (class 2606 OID 17260)
-- Name: logs_acesso logs_acesso_usuario_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.logs_acesso
    ADD CONSTRAINT logs_acesso_usuario_id_fkey FOREIGN KEY (usuario_id) REFERENCES public.usuarios(usuario_id);


--
-- TOC entry 5077 (class 2606 OID 17245)
-- Name: logs_auditoria logs_auditoria_usuario_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.logs_auditoria
    ADD CONSTRAINT logs_auditoria_usuario_id_fkey FOREIGN KEY (usuario_id) REFERENCES public.usuarios(usuario_id);


--
-- TOC entry 5085 (class 2606 OID 17375)
-- Name: lotes_produtos lotes_produtos_fornecedor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.lotes_produtos
    ADD CONSTRAINT lotes_produtos_fornecedor_id_fkey FOREIGN KEY (fornecedor_id) REFERENCES public.fornecedores(fornecedor_id);


--
-- TOC entry 5086 (class 2606 OID 17380)
-- Name: lotes_produtos lotes_produtos_localizacao_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.lotes_produtos
    ADD CONSTRAINT lotes_produtos_localizacao_id_fkey FOREIGN KEY (localizacao_id) REFERENCES public.localizacoes_estoque(localizacao_id);


--
-- TOC entry 5087 (class 2606 OID 17370)
-- Name: lotes_produtos lotes_produtos_produto_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.lotes_produtos
    ADD CONSTRAINT lotes_produtos_produto_id_fkey FOREIGN KEY (produto_id) REFERENCES public.produtos(produto_id) ON DELETE CASCADE;


--
-- TOC entry 5080 (class 2606 OID 17487)
-- Name: movimentos_estoque movimentos_estoque_localizacao_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.movimentos_estoque
    ADD CONSTRAINT movimentos_estoque_localizacao_id_fkey FOREIGN KEY (localizacao_id) REFERENCES public.localizacoes_estoque(localizacao_id) ON DELETE CASCADE;


--
-- TOC entry 5081 (class 2606 OID 17482)
-- Name: movimentos_estoque movimentos_estoque_lote_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.movimentos_estoque
    ADD CONSTRAINT movimentos_estoque_lote_id_fkey FOREIGN KEY (lote_id) REFERENCES public.lotes_produtos(lote_id) ON DELETE CASCADE;


--
-- TOC entry 5082 (class 2606 OID 17305)
-- Name: movimentos_estoque movimentos_estoque_movimentado_por_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.movimentos_estoque
    ADD CONSTRAINT movimentos_estoque_movimentado_por_fkey FOREIGN KEY (movimentado_por) REFERENCES public.usuarios(usuario_id);


--
-- TOC entry 5083 (class 2606 OID 17300)
-- Name: movimentos_estoque movimentos_estoque_produto_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.movimentos_estoque
    ADD CONSTRAINT movimentos_estoque_produto_id_fkey FOREIGN KEY (produto_id) REFERENCES public.produtos(produto_id);


--
-- TOC entry 5079 (class 2606 OID 17275)
-- Name: notificacoes notificacoes_agendamento_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.notificacoes
    ADD CONSTRAINT notificacoes_agendamento_id_fkey FOREIGN KEY (agendamento_id) REFERENCES public.agendamentos(agendamento_id);


--
-- TOC entry 5088 (class 2606 OID 17414)
-- Name: pedidos_compra pedidos_compra_criado_por_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pedidos_compra
    ADD CONSTRAINT pedidos_compra_criado_por_fkey FOREIGN KEY (criado_por) REFERENCES public.usuarios(usuario_id);


--
-- TOC entry 5089 (class 2606 OID 17409)
-- Name: pedidos_compra pedidos_compra_fornecedor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pedidos_compra
    ADD CONSTRAINT pedidos_compra_fornecedor_id_fkey FOREIGN KEY (fornecedor_id) REFERENCES public.fornecedores(fornecedor_id) ON DELETE CASCADE;


--
-- TOC entry 5049 (class 2606 OID 16922)
-- Name: perfil_permissoes perfil_permissoes_perfil_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.perfil_permissoes
    ADD CONSTRAINT perfil_permissoes_perfil_id_fkey FOREIGN KEY (perfil_id) REFERENCES public.perfis(perfil_id) ON DELETE CASCADE;


--
-- TOC entry 5050 (class 2606 OID 16927)
-- Name: perfil_permissoes perfil_permissoes_permissao_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.perfil_permissoes
    ADD CONSTRAINT perfil_permissoes_permissao_id_fkey FOREIGN KEY (permissao_id) REFERENCES public.permissoes(permissao_id) ON DELETE CASCADE;


--
-- TOC entry 5052 (class 2606 OID 16958)
-- Name: perfis_alunos perfis_alunos_usuario_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.perfis_alunos
    ADD CONSTRAINT perfis_alunos_usuario_id_fkey FOREIGN KEY (usuario_id) REFERENCES public.usuarios(usuario_id) ON DELETE CASCADE;


--
-- TOC entry 5067 (class 2606 OID 17148)
-- Name: prontuarios_eletronicos prontuarios_eletronicos_agendamento_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.prontuarios_eletronicos
    ADD CONSTRAINT prontuarios_eletronicos_agendamento_id_fkey FOREIGN KEY (agendamento_id) REFERENCES public.agendamentos(agendamento_id) ON DELETE CASCADE;


--
-- TOC entry 5068 (class 2606 OID 17158)
-- Name: prontuarios_eletronicos prontuarios_eletronicos_aluno_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.prontuarios_eletronicos
    ADD CONSTRAINT prontuarios_eletronicos_aluno_id_fkey FOREIGN KEY (aluno_id) REFERENCES public.usuarios(usuario_id);


--
-- TOC entry 5069 (class 2606 OID 17153)
-- Name: prontuarios_eletronicos prontuarios_eletronicos_clinica_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.prontuarios_eletronicos
    ADD CONSTRAINT prontuarios_eletronicos_clinica_id_fkey FOREIGN KEY (clinica_id) REFERENCES public.clinicas(clinica_id);


--
-- TOC entry 5070 (class 2606 OID 17163)
-- Name: prontuarios_eletronicos prontuarios_eletronicos_coordenador_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.prontuarios_eletronicos
    ADD CONSTRAINT prontuarios_eletronicos_coordenador_id_fkey FOREIGN KEY (coordenador_id) REFERENCES public.usuarios(usuario_id);


--
-- TOC entry 5071 (class 2606 OID 17177)
-- Name: prontuarios_eletronicos_versoes prontuarios_eletronicos_versoes_prontuario_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.prontuarios_eletronicos_versoes
    ADD CONSTRAINT prontuarios_eletronicos_versoes_prontuario_id_fkey FOREIGN KEY (prontuario_id) REFERENCES public.prontuarios_eletronicos(prontuario_id) ON DELETE CASCADE;


--
-- TOC entry 5073 (class 2606 OID 17210)
-- Name: registros_presenca registros_presenca_agendamento_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.registros_presenca
    ADD CONSTRAINT registros_presenca_agendamento_id_fkey FOREIGN KEY (agendamento_id) REFERENCES public.agendamentos(agendamento_id);


--
-- TOC entry 5074 (class 2606 OID 17205)
-- Name: registros_presenca registros_presenca_aluno_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.registros_presenca
    ADD CONSTRAINT registros_presenca_aluno_id_fkey FOREIGN KEY (aluno_id) REFERENCES public.usuarios(usuario_id);


--
-- TOC entry 5055 (class 2606 OID 17020)
-- Name: responsaveis_legais responsaveis_legais_paciente_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.responsaveis_legais
    ADD CONSTRAINT responsaveis_legais_paciente_id_fkey FOREIGN KEY (paciente_id) REFERENCES public.pacientes(paciente_id) ON DELETE CASCADE;


--
-- TOC entry 5054 (class 2606 OID 16996)
-- Name: salas salas_clinica_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.salas
    ADD CONSTRAINT salas_clinica_id_fkey FOREIGN KEY (clinica_id) REFERENCES public.clinicas(clinica_id);


--
-- TOC entry 5053 (class 2606 OID 16983)
-- Name: servicos servicos_clinica_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.servicos
    ADD CONSTRAINT servicos_clinica_id_fkey FOREIGN KEY (clinica_id) REFERENCES public.clinicas(clinica_id) ON DELETE CASCADE;


--
-- TOC entry 5051 (class 2606 OID 16944)
-- Name: usuarios usuarios_perfil_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_perfil_id_fkey FOREIGN KEY (perfil_id) REFERENCES public.perfis(perfil_id);


-- Completed on 2025-07-14 15:49:11

--
-- PostgreSQL database dump complete
--

-- Completed on 2025-07-14 15:49:11

--
-- PostgreSQL database cluster dump complete
--

