--
-- PostgreSQL database cluster dump
--

-- Started on 2025-07-14 17:33:57

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

-- Started on 2025-07-14 17:33:57

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

-- Completed on 2025-07-14 17:33:58

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

-- Started on 2025-07-14 17:33:58

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
-- TOC entry 5632 (class 1262 OID 16386)
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
-- TOC entry 5633 (class 0 OID 0)
-- Dependencies: 2
-- Name: EXTENSION "uuid-ossp"; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION "uuid-ossp" IS 'generate universally unique identifiers (UUIDs)';


--
-- TOC entry 959 (class 1247 OID 16888)
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
-- TOC entry 953 (class 1247 OID 16869)
-- Name: sexo_enum; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.sexo_enum AS ENUM (
    'M',
    'F',
    'O'
);


ALTER TYPE public.sexo_enum OWNER TO postgres;

--
-- TOC entry 956 (class 1247 OID 16876)
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
-- TOC entry 1052 (class 1247 OID 17386)
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
-- TOC entry 1067 (class 1247 OID 17502)
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
-- TOC entry 1061 (class 1247 OID 17439)
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
-- TOC entry 1070 (class 1247 OID 17514)
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
-- TOC entry 277 (class 1259 OID 17552)
-- Name: auth_group; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(150) NOT NULL
);


ALTER TABLE public.auth_group OWNER TO postgres;

--
-- TOC entry 276 (class 1259 OID 17551)
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.auth_group ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_group_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 279 (class 1259 OID 17560)
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_group_permissions (
    id bigint NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_group_permissions OWNER TO postgres;

--
-- TOC entry 278 (class 1259 OID 17559)
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.auth_group_permissions ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_group_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 275 (class 1259 OID 17546)
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE public.auth_permission OWNER TO postgres;

--
-- TOC entry 274 (class 1259 OID 17545)
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.auth_permission ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_permission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 314 (class 1259 OID 17945)
-- Name: clinica_clinica; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.clinica_clinica (
    id bigint NOT NULL,
    nome character varying(255) NOT NULL,
    endereco text,
    telefone character varying(20),
    email character varying(254),
    criado_em timestamp with time zone NOT NULL,
    atualizado_em timestamp with time zone NOT NULL
);


ALTER TABLE public.clinica_clinica OWNER TO postgres;

--
-- TOC entry 313 (class 1259 OID 17944)
-- Name: clinica_clinica_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.clinica_clinica ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.clinica_clinica_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


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
-- TOC entry 5634 (class 0 OID 0)
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
-- TOC entry 5635 (class 0 OID 0)
-- Dependencies: 236
-- Name: consentimentos_pacientes_consentimento_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.consentimentos_pacientes_consentimento_id_seq OWNED BY public.consentimentos_pacientes.consentimento_id;


--
-- TOC entry 291 (class 1259 OID 17685)
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id uuid NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


ALTER TABLE public.django_admin_log OWNER TO postgres;

--
-- TOC entry 290 (class 1259 OID 17684)
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.django_admin_log ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_admin_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 273 (class 1259 OID 17538)
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE public.django_content_type OWNER TO postgres;

--
-- TOC entry 272 (class 1259 OID 17537)
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.django_content_type ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_content_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 271 (class 1259 OID 17530)
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_migrations (
    id bigint NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE public.django_migrations OWNER TO postgres;

--
-- TOC entry 270 (class 1259 OID 17529)
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.django_migrations ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_migrations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 312 (class 1259 OID 17934)
-- Name: django_session; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE public.django_session OWNER TO postgres;

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
-- TOC entry 292 (class 1259 OID 17705)
-- Name: estoque_ajusteestoque; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.estoque_ajusteestoque (
    ajuste_id uuid NOT NULL,
    quantidade numeric(10,2) NOT NULL,
    tipo_ajuste character varying(30) NOT NULL,
    motivo text,
    ajustado_em timestamp with time zone NOT NULL,
    ajustado_por_id uuid,
    localizacao_id integer NOT NULL,
    lote_id uuid NOT NULL,
    produto_id integer NOT NULL
);


ALTER TABLE public.estoque_ajusteestoque OWNER TO postgres;

--
-- TOC entry 294 (class 1259 OID 17713)
-- Name: estoque_fornecedor; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.estoque_fornecedor (
    fornecedor_id integer NOT NULL,
    nome character varying(255) NOT NULL,
    cnpj character varying(18),
    contato_nome character varying(100),
    contato_email character varying(100),
    contato_telefone character varying(20),
    endereco text,
    criado_em timestamp with time zone NOT NULL,
    atualizado_em timestamp with time zone NOT NULL
);


ALTER TABLE public.estoque_fornecedor OWNER TO postgres;

--
-- TOC entry 293 (class 1259 OID 17712)
-- Name: estoque_fornecedor_fornecedor_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.estoque_fornecedor ALTER COLUMN fornecedor_id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.estoque_fornecedor_fornecedor_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 296 (class 1259 OID 17725)
-- Name: estoque_itempedidocompra; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.estoque_itempedidocompra (
    item_pedido_id integer NOT NULL,
    quantidade_pedida numeric(10,2) NOT NULL,
    quantidade_recebida numeric(10,2) NOT NULL,
    preco_unitario numeric(10,2) NOT NULL,
    criado_em timestamp with time zone NOT NULL,
    pedido_id uuid NOT NULL,
    produto_id integer NOT NULL
);


ALTER TABLE public.estoque_itempedidocompra OWNER TO postgres;

--
-- TOC entry 295 (class 1259 OID 17724)
-- Name: estoque_itempedidocompra_item_pedido_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.estoque_itempedidocompra ALTER COLUMN item_pedido_id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.estoque_itempedidocompra_item_pedido_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 298 (class 1259 OID 17731)
-- Name: estoque_localizacaoestoque; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.estoque_localizacaoestoque (
    localizacao_id integer NOT NULL,
    nome character varying(100) NOT NULL,
    descricao text,
    criado_em timestamp with time zone NOT NULL,
    atualizado_em timestamp with time zone NOT NULL
);


ALTER TABLE public.estoque_localizacaoestoque OWNER TO postgres;

--
-- TOC entry 297 (class 1259 OID 17730)
-- Name: estoque_localizacaoestoque_localizacao_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.estoque_localizacaoestoque ALTER COLUMN localizacao_id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.estoque_localizacaoestoque_localizacao_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 299 (class 1259 OID 17740)
-- Name: estoque_loteproduto; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.estoque_loteproduto (
    lote_id uuid NOT NULL,
    numero_lote character varying(100) NOT NULL,
    data_fabricacao date,
    data_validade date,
    quantidade_inicial numeric(10,2) NOT NULL,
    quantidade_atual numeric(10,2) NOT NULL,
    criado_em timestamp with time zone NOT NULL,
    atualizado_em timestamp with time zone NOT NULL,
    fornecedor_id integer,
    localizacao_id integer,
    produto_id integer NOT NULL
);


ALTER TABLE public.estoque_loteproduto OWNER TO postgres;

--
-- TOC entry 301 (class 1259 OID 17746)
-- Name: estoque_movimentoestoque; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.estoque_movimentoestoque (
    movimento_id integer NOT NULL,
    quantidade numeric(10,2) NOT NULL,
    tipo_movimento character varying(10) NOT NULL,
    referencia character varying(100),
    movimentado_em timestamp with time zone NOT NULL,
    localizacao_id integer,
    lote_id uuid,
    movimentado_por_id uuid,
    produto_id integer NOT NULL
);


ALTER TABLE public.estoque_movimentoestoque OWNER TO postgres;

--
-- TOC entry 300 (class 1259 OID 17745)
-- Name: estoque_movimentoestoque_movimento_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.estoque_movimentoestoque ALTER COLUMN movimento_id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.estoque_movimentoestoque_movimento_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 302 (class 1259 OID 17751)
-- Name: estoque_pedidocompra; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.estoque_pedidocompra (
    pedido_id uuid NOT NULL,
    data_pedido timestamp with time zone NOT NULL,
    data_entrega_prevista date,
    status character varying(20) NOT NULL,
    total_valor numeric(10,2),
    observacoes text,
    criado_em timestamp with time zone NOT NULL,
    atualizado_em timestamp with time zone NOT NULL,
    criado_por_id uuid,
    fornecedor_id integer NOT NULL
);


ALTER TABLE public.estoque_pedidocompra OWNER TO postgres;

--
-- TOC entry 304 (class 1259 OID 17759)
-- Name: estoque_produto; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.estoque_produto (
    produto_id integer NOT NULL,
    nome character varying(100) NOT NULL,
    descricao text,
    unidade character varying(20),
    nivel_minimo_estoque numeric(10,2) NOT NULL,
    codigo_barras character varying(50),
    preco_custo numeric(10,2),
    preco_venda numeric(10,2),
    unidade_compra character varying(20),
    fator_conversao numeric(10,4) NOT NULL
);


ALTER TABLE public.estoque_produto OWNER TO postgres;

--
-- TOC entry 303 (class 1259 OID 17758)
-- Name: estoque_produto_produto_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.estoque_produto ALTER COLUMN produto_id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.estoque_produto_produto_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


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
-- TOC entry 5636 (class 0 OID 0)
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
-- TOC entry 5637 (class 0 OID 0)
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
-- TOC entry 5638 (class 0 OID 0)
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
-- TOC entry 5639 (class 0 OID 0)
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
-- TOC entry 5640 (class 0 OID 0)
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
-- TOC entry 5641 (class 0 OID 0)
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
-- TOC entry 5642 (class 0 OID 0)
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
-- TOC entry 5643 (class 0 OID 0)
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
-- TOC entry 5644 (class 0 OID 0)
-- Dependencies: 254
-- Name: notificacoes_notificacao_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.notificacoes_notificacao_id_seq OWNED BY public.notificacoes.notificacao_id;


--
-- TOC entry 309 (class 1259 OID 17882)
-- Name: paciente_consentimentopaciente; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.paciente_consentimentopaciente (
    consentimento_id integer NOT NULL,
    tipo_consentimento character varying(50) NOT NULL,
    data_consentimento timestamp with time zone NOT NULL,
    ativo boolean NOT NULL,
    detalhes text,
    paciente_id uuid NOT NULL
);


ALTER TABLE public.paciente_consentimentopaciente OWNER TO postgres;

--
-- TOC entry 308 (class 1259 OID 17881)
-- Name: paciente_consentimentopaciente_consentimento_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.paciente_consentimentopaciente ALTER COLUMN consentimento_id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.paciente_consentimentopaciente_consentimento_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 311 (class 1259 OID 17896)
-- Name: paciente_documentopaciente; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.paciente_documentopaciente (
    documento_id uuid NOT NULL,
    dados_ocr text,
    caminho_arquivo character varying(100) NOT NULL,
    enviado_em timestamp with time zone NOT NULL,
    paciente_id uuid NOT NULL,
    tipo_documento_id integer
);


ALTER TABLE public.paciente_documentopaciente OWNER TO postgres;

--
-- TOC entry 305 (class 1259 OID 17864)
-- Name: paciente_paciente; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.paciente_paciente (
    paciente_id uuid NOT NULL,
    nome character varying(100) NOT NULL,
    sobrenome character varying(100) NOT NULL,
    data_nascimento date,
    sexo character varying(1),
    endereco text,
    telefone character varying(20),
    email character varying(100),
    perfil_epidemiologico jsonb,
    criado_em timestamp with time zone NOT NULL,
    atualizado_em timestamp with time zone NOT NULL
);


ALTER TABLE public.paciente_paciente OWNER TO postgres;

--
-- TOC entry 310 (class 1259 OID 17889)
-- Name: paciente_responsavellegal; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.paciente_responsavellegal (
    responsavel_id uuid NOT NULL,
    nome character varying(150) NOT NULL,
    cpf character varying(14),
    rg character varying(20),
    telefone character varying(20),
    email character varying(100),
    grau_parentesco character varying(50),
    endereco text,
    criado_em timestamp with time zone NOT NULL,
    paciente_id uuid NOT NULL
);


ALTER TABLE public.paciente_responsavellegal OWNER TO postgres;

--
-- TOC entry 307 (class 1259 OID 17872)
-- Name: paciente_tipodocumento; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.paciente_tipodocumento (
    tipo_id integer NOT NULL,
    nome character varying(50) NOT NULL,
    descricao text,
    obrigatorio boolean NOT NULL
);


ALTER TABLE public.paciente_tipodocumento OWNER TO postgres;

--
-- TOC entry 306 (class 1259 OID 17871)
-- Name: paciente_tipodocumento_tipo_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.paciente_tipodocumento ALTER COLUMN tipo_id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.paciente_tipodocumento_tipo_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


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
-- TOC entry 5645 (class 0 OID 0)
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
-- TOC entry 5646 (class 0 OID 0)
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
-- TOC entry 5647 (class 0 OID 0)
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
-- TOC entry 5648 (class 0 OID 0)
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
-- TOC entry 5649 (class 0 OID 0)
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
-- TOC entry 5650 (class 0 OID 0)
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
-- TOC entry 5651 (class 0 OID 0)
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
-- TOC entry 5652 (class 0 OID 0)
-- Dependencies: 233
-- Name: tipos_documentos_tipo_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tipos_documentos_tipo_id_seq OWNED BY public.tipos_documentos.tipo_id;


--
-- TOC entry 287 (class 1259 OID 17622)
-- Name: usuario_logacesso; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.usuario_logacesso (
    log_id integer NOT NULL,
    endereco_ip inet,
    agente_usuario text,
    horario_login timestamp with time zone NOT NULL,
    sucesso boolean NOT NULL,
    motivo_falha character varying(100),
    usuario_id uuid
);


ALTER TABLE public.usuario_logacesso OWNER TO postgres;

--
-- TOC entry 286 (class 1259 OID 17621)
-- Name: usuario_logacesso_log_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.usuario_logacesso ALTER COLUMN log_id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.usuario_logacesso_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 289 (class 1259 OID 17630)
-- Name: usuario_logauditoria; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.usuario_logauditoria (
    auditoria_id integer NOT NULL,
    acao character varying(50) NOT NULL,
    nome_tabela character varying(100),
    id_registro text,
    horario_acao timestamp with time zone NOT NULL,
    dados_antigos jsonb,
    dados_novos jsonb,
    endereco_ip inet,
    usuario_id uuid
);


ALTER TABLE public.usuario_logauditoria OWNER TO postgres;

--
-- TOC entry 288 (class 1259 OID 17629)
-- Name: usuario_logauditoria_auditoria_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.usuario_logauditoria ALTER COLUMN auditoria_id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.usuario_logauditoria_auditoria_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 285 (class 1259 OID 17612)
-- Name: usuario_perfilaluno; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.usuario_perfilaluno (
    usuario_id uuid NOT NULL,
    rgm character varying(20) NOT NULL,
    modelo_biometrico bytea,
    curso character varying(100),
    semestre integer,
    carga_horaria_total integer NOT NULL
);


ALTER TABLE public.usuario_perfilaluno OWNER TO postgres;

--
-- TOC entry 280 (class 1259 OID 17591)
-- Name: usuario_usuario; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.usuario_usuario (
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    username character varying(150) NOT NULL,
    first_name character varying(150) NOT NULL,
    last_name character varying(150) NOT NULL,
    email character varying(254) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL,
    usuario_id uuid NOT NULL,
    nome_completo character varying(150) NOT NULL,
    telefone character varying(20)
);


ALTER TABLE public.usuario_usuario OWNER TO postgres;

--
-- TOC entry 282 (class 1259 OID 17601)
-- Name: usuario_usuario_groups; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.usuario_usuario_groups (
    id bigint NOT NULL,
    usuario_id uuid NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public.usuario_usuario_groups OWNER TO postgres;

--
-- TOC entry 281 (class 1259 OID 17600)
-- Name: usuario_usuario_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.usuario_usuario_groups ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.usuario_usuario_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 284 (class 1259 OID 17607)
-- Name: usuario_usuario_user_permissions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.usuario_usuario_user_permissions (
    id bigint NOT NULL,
    usuario_id uuid NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.usuario_usuario_user_permissions OWNER TO postgres;

--
-- TOC entry 283 (class 1259 OID 17606)
-- Name: usuario_usuario_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.usuario_usuario_user_permissions ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.usuario_usuario_user_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


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
-- TOC entry 5004 (class 2604 OID 16967)
-- Name: clinicas clinica_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clinicas ALTER COLUMN clinica_id SET DEFAULT nextval('public.clinicas_clinica_id_seq'::regclass);


--
-- TOC entry 5017 (class 2604 OID 17060)
-- Name: consentimentos_pacientes consentimento_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.consentimentos_pacientes ALTER COLUMN consentimento_id SET DEFAULT nextval('public.consentimentos_pacientes_consentimento_id_seq'::regclass);


--
-- TOC entry 5035 (class 2604 OID 17219)
-- Name: fila_espera fila_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fila_espera ALTER COLUMN fila_id SET DEFAULT nextval('public.fila_espera_fila_id_seq'::regclass);


--
-- TOC entry 5051 (class 2604 OID 17328)
-- Name: fornecedores fornecedor_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fornecedores ALTER COLUMN fornecedor_id SET DEFAULT nextval('public.fornecedores_fornecedor_id_seq'::regclass);


--
-- TOC entry 5020 (class 2604 OID 17076)
-- Name: horarios horario_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.horarios ALTER COLUMN horario_id SET DEFAULT nextval('public.horarios_horario_id_seq'::regclass);


--
-- TOC entry 5065 (class 2604 OID 17423)
-- Name: itens_pedido_compra item_pedido_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.itens_pedido_compra ALTER COLUMN item_pedido_id SET DEFAULT nextval('public.itens_pedido_compra_item_pedido_id_seq'::regclass);


--
-- TOC entry 5054 (class 2604 OID 17343)
-- Name: localizacoes_estoque localizacao_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.localizacoes_estoque ALTER COLUMN localizacao_id SET DEFAULT nextval('public.localizacoes_estoque_localizacao_id_seq'::regclass);


--
-- TOC entry 5041 (class 2604 OID 17254)
-- Name: logs_acesso log_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.logs_acesso ALTER COLUMN log_id SET DEFAULT nextval('public.logs_acesso_log_id_seq'::regclass);


--
-- TOC entry 5039 (class 2604 OID 17239)
-- Name: logs_auditoria auditoria_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.logs_auditoria ALTER COLUMN auditoria_id SET DEFAULT nextval('public.logs_auditoria_auditoria_id_seq'::regclass);


--
-- TOC entry 5048 (class 2604 OID 17294)
-- Name: movimentos_estoque movimento_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.movimentos_estoque ALTER COLUMN movimento_id SET DEFAULT nextval('public.movimentos_estoque_movimento_id_seq'::regclass);


--
-- TOC entry 5043 (class 2604 OID 17269)
-- Name: notificacoes notificacao_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.notificacoes ALTER COLUMN notificacao_id SET DEFAULT nextval('public.notificacoes_notificacao_id_seq'::regclass);


--
-- TOC entry 4999 (class 2604 OID 16901)
-- Name: perfis perfil_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.perfis ALTER COLUMN perfil_id SET DEFAULT nextval('public.perfis_perfil_id_seq'::regclass);


--
-- TOC entry 5000 (class 2604 OID 16910)
-- Name: permissoes permissao_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.permissoes ALTER COLUMN permissao_id SET DEFAULT nextval('public.permissoes_permissao_id_seq'::regclass);


--
-- TOC entry 5045 (class 2604 OID 17284)
-- Name: produtos produto_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.produtos ALTER COLUMN produto_id SET DEFAULT nextval('public.produtos_produto_id_seq'::regclass);


--
-- TOC entry 5032 (class 2604 OID 17200)
-- Name: registros_presenca registro_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.registros_presenca ALTER COLUMN registro_id SET DEFAULT nextval('public.registros_presenca_registro_id_seq'::regclass);


--
-- TOC entry 5006 (class 2604 OID 16992)
-- Name: salas sala_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.salas ALTER COLUMN sala_id SET DEFAULT nextval('public.salas_sala_id_seq'::regclass);


--
-- TOC entry 5005 (class 2604 OID 16978)
-- Name: servicos servico_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.servicos ALTER COLUMN servico_id SET DEFAULT nextval('public.servicos_servico_id_seq'::regclass);


--
-- TOC entry 5021 (class 2604 OID 17093)
-- Name: status_agendamento status_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.status_agendamento ALTER COLUMN status_id SET DEFAULT nextval('public.status_agendamento_status_id_seq'::regclass);


--
-- TOC entry 5013 (class 2604 OID 17029)
-- Name: tipos_documentos tipo_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tipos_documentos ALTER COLUMN tipo_id SET DEFAULT nextval('public.tipos_documentos_tipo_id_seq'::regclass);


--
-- TOC entry 5554 (class 0 OID 17098)
-- Dependencies: 242
-- Data for Name: agendamentos; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.agendamentos (agendamento_id, clinica_id, paciente_id, horario_id, aluno_id, coordenador_id, status_id, criado_em, atualizado_em) FROM stdin;
\.


--
-- TOC entry 5581 (class 0 OID 17453)
-- Dependencies: 269
-- Data for Name: ajustes_estoque; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.ajustes_estoque (ajuste_id, produto_id, lote_id, localizacao_id, quantidade, tipo_ajuste, motivo, ajustado_por, ajustado_em) FROM stdin;
\.


--
-- TOC entry 5557 (class 0 OID 17182)
-- Dependencies: 245
-- Data for Name: anexos_prontuario; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.anexos_prontuario (anexo_id, prontuario_id, tipo_anexo, caminho_arquivo, metadados, enviado_em) FROM stdin;
\.


--
-- TOC entry 5589 (class 0 OID 17552)
-- Dependencies: 277
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_group (id, name) FROM stdin;
1	teste
\.


--
-- TOC entry 5591 (class 0 OID 17560)
-- Dependencies: 279
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_group_permissions (id, group_id, permission_id) FROM stdin;
1	1	1
2	1	2
3	1	3
4	1	4
5	1	5
6	1	6
7	1	7
8	1	8
9	1	9
10	1	10
11	1	11
12	1	12
13	1	13
14	1	14
15	1	15
16	1	16
17	1	17
18	1	18
19	1	19
20	1	20
21	1	21
22	1	22
23	1	23
24	1	24
25	1	25
26	1	26
27	1	27
28	1	28
29	1	29
30	1	30
31	1	31
32	1	32
33	1	33
34	1	34
35	1	35
36	1	36
37	1	37
38	1	38
39	1	39
40	1	40
41	1	41
42	1	42
43	1	43
44	1	44
45	1	45
46	1	46
47	1	47
48	1	48
49	1	49
50	1	50
51	1	51
52	1	52
53	1	53
54	1	54
55	1	55
56	1	56
57	1	57
58	1	58
59	1	59
60	1	60
61	1	61
62	1	62
63	1	63
64	1	64
65	1	65
66	1	66
67	1	67
68	1	68
69	1	69
70	1	70
71	1	71
72	1	72
73	1	73
74	1	74
75	1	75
76	1	76
77	1	77
78	1	78
79	1	79
80	1	80
81	1	81
82	1	82
83	1	83
84	1	84
85	1	85
86	1	86
87	1	87
88	1	88
\.


--
-- TOC entry 5587 (class 0 OID 17546)
-- Dependencies: 275
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add log entry	1	add_logentry
2	Can change log entry	1	change_logentry
3	Can delete log entry	1	delete_logentry
4	Can view log entry	1	view_logentry
5	Can add permission	2	add_permission
6	Can change permission	2	change_permission
7	Can delete permission	2	delete_permission
8	Can view permission	2	view_permission
9	Can add group	3	add_group
10	Can change group	3	change_group
11	Can delete group	3	delete_group
12	Can view group	3	view_group
13	Can add content type	4	add_contenttype
14	Can change content type	4	change_contenttype
15	Can delete content type	4	delete_contenttype
16	Can view content type	4	view_contenttype
17	Can add session	5	add_session
18	Can change session	5	change_session
19	Can delete session	5	delete_session
20	Can view session	5	view_session
21	Can add paciente	6	add_paciente
22	Can change paciente	6	change_paciente
23	Can delete paciente	6	delete_paciente
24	Can view paciente	6	view_paciente
25	Can add tipo documento	7	add_tipodocumento
26	Can change tipo documento	7	change_tipodocumento
27	Can delete tipo documento	7	delete_tipodocumento
28	Can view tipo documento	7	view_tipodocumento
29	Can add consentimento paciente	8	add_consentimentopaciente
30	Can change consentimento paciente	8	change_consentimentopaciente
31	Can delete consentimento paciente	8	delete_consentimentopaciente
32	Can view consentimento paciente	8	view_consentimentopaciente
33	Can add responsavel legal	9	add_responsavellegal
34	Can change responsavel legal	9	change_responsavellegal
35	Can delete responsavel legal	9	delete_responsavellegal
36	Can view responsavel legal	9	view_responsavellegal
37	Can add documento paciente	10	add_documentopaciente
38	Can change documento paciente	10	change_documentopaciente
39	Can delete documento paciente	10	delete_documentopaciente
40	Can view documento paciente	10	view_documentopaciente
41	Can add ajuste estoque	11	add_ajusteestoque
42	Can change ajuste estoque	11	change_ajusteestoque
43	Can delete ajuste estoque	11	delete_ajusteestoque
44	Can view ajuste estoque	11	view_ajusteestoque
45	Can add fornecedor	12	add_fornecedor
46	Can change fornecedor	12	change_fornecedor
47	Can delete fornecedor	12	delete_fornecedor
48	Can view fornecedor	12	view_fornecedor
49	Can add item pedido compra	13	add_itempedidocompra
50	Can change item pedido compra	13	change_itempedidocompra
51	Can delete item pedido compra	13	delete_itempedidocompra
52	Can view item pedido compra	13	view_itempedidocompra
53	Can add localizacao estoque	14	add_localizacaoestoque
54	Can change localizacao estoque	14	change_localizacaoestoque
55	Can delete localizacao estoque	14	delete_localizacaoestoque
56	Can view localizacao estoque	14	view_localizacaoestoque
57	Can add lote produto	15	add_loteproduto
58	Can change lote produto	15	change_loteproduto
59	Can delete lote produto	15	delete_loteproduto
60	Can view lote produto	15	view_loteproduto
61	Can add movimento estoque	16	add_movimentoestoque
62	Can change movimento estoque	16	change_movimentoestoque
63	Can delete movimento estoque	16	delete_movimentoestoque
64	Can view movimento estoque	16	view_movimentoestoque
65	Can add pedido compra	17	add_pedidocompra
66	Can change pedido compra	17	change_pedidocompra
67	Can delete pedido compra	17	delete_pedidocompra
68	Can view pedido compra	17	view_pedidocompra
69	Can add produto	18	add_produto
70	Can change produto	18	change_produto
71	Can delete produto	18	delete_produto
72	Can view produto	18	view_produto
73	Can add user	19	add_usuario
74	Can change user	19	change_usuario
75	Can delete user	19	delete_usuario
76	Can view user	19	view_usuario
77	Can add perfil aluno	20	add_perfilaluno
78	Can change perfil aluno	20	change_perfilaluno
79	Can delete perfil aluno	20	delete_perfilaluno
80	Can view perfil aluno	20	view_perfilaluno
81	Can add log acesso	21	add_logacesso
82	Can change log acesso	21	change_logacesso
83	Can delete log acesso	21	delete_logacesso
84	Can view log acesso	21	view_logacesso
85	Can add log auditoria	22	add_logauditoria
86	Can change log auditoria	22	change_logauditoria
87	Can delete log auditoria	22	delete_logauditoria
88	Can view log auditoria	22	view_logauditoria
89	Can add Clínica	23	add_clinica
90	Can change Clínica	23	change_clinica
91	Can delete Clínica	23	delete_clinica
92	Can view Clínica	23	view_clinica
\.


--
-- TOC entry 5626 (class 0 OID 17945)
-- Dependencies: 314
-- Data for Name: clinica_clinica; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.clinica_clinica (id, nome, endereco, telefone, email, criado_em, atualizado_em) FROM stdin;
\.


--
-- TOC entry 5538 (class 0 OID 16964)
-- Dependencies: 226
-- Data for Name: clinicas; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.clinicas (clinica_id, nome, descricao) FROM stdin;
\.


--
-- TOC entry 5572 (class 0 OID 17310)
-- Dependencies: 260
-- Data for Name: configuracoes_sistema; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.configuracoes_sistema (chave, valor, atualizado_em) FROM stdin;
\.


--
-- TOC entry 5549 (class 0 OID 17057)
-- Dependencies: 237
-- Data for Name: consentimentos_pacientes; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.consentimentos_pacientes (consentimento_id, paciente_id, tipo_consentimento, data_consentimento, ativo, detalhes) FROM stdin;
\.


--
-- TOC entry 5603 (class 0 OID 17685)
-- Dependencies: 291
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
1	2025-07-14 16:43:12.538707-03	1	teste	1	[{"added": {}}]	3	3f4d5a50-2d0d-4167-8d1d-09fc4bacebf4
2	2025-07-14 17:12:43.158319-03	3f4d5a50-2d0d-4167-8d1d-09fc4bacebf4	german	2	[{"changed": {"fields": ["First name", "Last name", "Grupos", "Permiss\\u00f5es do usu\\u00e1rio", "Nome completo", "Telefone"]}}]	19	3f4d5a50-2d0d-4167-8d1d-09fc4bacebf4
\.


--
-- TOC entry 5585 (class 0 OID 17538)
-- Dependencies: 273
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_content_type (id, app_label, model) FROM stdin;
1	admin	logentry
2	auth	permission
3	auth	group
4	contenttypes	contenttype
5	sessions	session
6	paciente	paciente
7	paciente	tipodocumento
8	paciente	consentimentopaciente
9	paciente	responsavellegal
10	paciente	documentopaciente
11	estoque	ajusteestoque
12	estoque	fornecedor
13	estoque	itempedidocompra
14	estoque	localizacaoestoque
15	estoque	loteproduto
16	estoque	movimentoestoque
17	estoque	pedidocompra
18	estoque	produto
19	usuario	usuario
20	usuario	perfilaluno
21	usuario	logacesso
22	usuario	logauditoria
23	clinica	clinica
\.


--
-- TOC entry 5583 (class 0 OID 17530)
-- Dependencies: 271
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_migrations (id, app, name, applied) FROM stdin;
1	contenttypes	0001_initial	2025-07-14 16:37:53.25711-03
2	contenttypes	0002_remove_content_type_name	2025-07-14 16:37:53.277691-03
3	auth	0001_initial	2025-07-14 16:37:53.361033-03
4	auth	0002_alter_permission_name_max_length	2025-07-14 16:37:53.36954-03
5	auth	0003_alter_user_email_max_length	2025-07-14 16:37:53.378922-03
6	auth	0004_alter_user_username_opts	2025-07-14 16:37:53.394907-03
7	auth	0005_alter_user_last_login_null	2025-07-14 16:37:53.404563-03
8	auth	0006_require_contenttypes_0002	2025-07-14 16:37:53.406389-03
9	auth	0007_alter_validators_add_error_messages	2025-07-14 16:37:53.414505-03
10	auth	0008_alter_user_username_max_length	2025-07-14 16:37:53.421495-03
11	auth	0009_alter_user_last_name_max_length	2025-07-14 16:37:53.427228-03
12	auth	0010_alter_group_name_max_length	2025-07-14 16:37:53.436539-03
13	auth	0011_update_proxy_permissions	2025-07-14 16:37:53.444852-03
14	auth	0012_alter_user_first_name_max_length	2025-07-14 16:37:53.451023-03
15	usuario	0001_initial	2025-07-14 16:37:53.575294-03
16	admin	0001_initial	2025-07-14 16:37:53.612677-03
17	admin	0002_logentry_remove_auto_add	2025-07-14 16:37:53.623463-03
18	admin	0003_logentry_add_action_flag_choices	2025-07-14 16:37:53.635557-03
19	estoque	0001_initial	2025-07-14 16:37:53.728208-03
20	estoque	0002_initial	2025-07-14 16:37:54.015881-03
21	paciente	0001_initial	2025-07-14 16:37:54.109529-03
22	sessions	0001_initial	2025-07-14 16:37:54.13-03
23	clinica	0001_initial	2025-07-14 16:48:12.612875-03
\.


--
-- TOC entry 5624 (class 0 OID 17934)
-- Dependencies: 312
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_session (session_key, session_data, expire_date) FROM stdin;
kudrkimhqqmsah4locftfe3szqbhgyn6	.eJxVjDkOwjAQRe_iGltexhslPWeIxh4PYVEiZakQdyeRUkD733v_LTpcl75b5zZ1dxJn4RjIo9fSkiYJJkSZyJDUmSsUrK0wiNNvto3PNuwtPXC4jaqOwzLdi9oVddBZXUdqr8vh_h30OPdbnStrk3y05EJxlhNDsMboGl1MGcDq2EoNwI0Y0RvTnMGUo4YaHBcQny8jIkEL:1ubP4C:l6XOycLVXRKheO--oCax9nTo0PU6yTvEj45Z8guRCzM	2025-07-28 16:42:24.706042-03
zm0z9ljgnerwmejeyvz2heioq1wc0epw	.eJxVjDkOwjAQRe_iGltexhslPWeIxh4PYVEiZakQdyeRUkD733v_LTpcl75b5zZ1dxJn4RjIo9fSkiYJJkSZyJDUmSsUrK0wiNNvto3PNuwtPXC4jaqOwzLdi9oVddBZXUdqr8vh_h30OPdbnStrk3y05EJxlhNDsMboGl1MGcDq2EoNwI0Y0RvTnMGUo4YaHBcQny8jIkEL:1ubPU1:ciuPg5Yd4H0gZ6LRY1XEZ-WG8KjOVJljKKjEI733bDg	2025-07-28 17:09:05.831324-03
\.


--
-- TOC entry 5547 (class 0 OID 17037)
-- Dependencies: 235
-- Data for Name: documentos_pacientes; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.documentos_pacientes (documento_id, paciente_id, tipo_id, dados_ocr, caminho_arquivo, enviado_em) FROM stdin;
\.


--
-- TOC entry 5604 (class 0 OID 17705)
-- Dependencies: 292
-- Data for Name: estoque_ajusteestoque; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.estoque_ajusteestoque (ajuste_id, quantidade, tipo_ajuste, motivo, ajustado_em, ajustado_por_id, localizacao_id, lote_id, produto_id) FROM stdin;
\.


--
-- TOC entry 5606 (class 0 OID 17713)
-- Dependencies: 294
-- Data for Name: estoque_fornecedor; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.estoque_fornecedor (fornecedor_id, nome, cnpj, contato_nome, contato_email, contato_telefone, endereco, criado_em, atualizado_em) FROM stdin;
\.


--
-- TOC entry 5608 (class 0 OID 17725)
-- Dependencies: 296
-- Data for Name: estoque_itempedidocompra; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.estoque_itempedidocompra (item_pedido_id, quantidade_pedida, quantidade_recebida, preco_unitario, criado_em, pedido_id, produto_id) FROM stdin;
\.


--
-- TOC entry 5610 (class 0 OID 17731)
-- Dependencies: 298
-- Data for Name: estoque_localizacaoestoque; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.estoque_localizacaoestoque (localizacao_id, nome, descricao, criado_em, atualizado_em) FROM stdin;
\.


--
-- TOC entry 5611 (class 0 OID 17740)
-- Dependencies: 299
-- Data for Name: estoque_loteproduto; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.estoque_loteproduto (lote_id, numero_lote, data_fabricacao, data_validade, quantidade_inicial, quantidade_atual, criado_em, atualizado_em, fornecedor_id, localizacao_id, produto_id) FROM stdin;
\.


--
-- TOC entry 5613 (class 0 OID 17746)
-- Dependencies: 301
-- Data for Name: estoque_movimentoestoque; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.estoque_movimentoestoque (movimento_id, quantidade, tipo_movimento, referencia, movimentado_em, localizacao_id, lote_id, movimentado_por_id, produto_id) FROM stdin;
\.


--
-- TOC entry 5614 (class 0 OID 17751)
-- Dependencies: 302
-- Data for Name: estoque_pedidocompra; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.estoque_pedidocompra (pedido_id, data_pedido, data_entrega_prevista, status, total_valor, observacoes, criado_em, atualizado_em, criado_por_id, fornecedor_id) FROM stdin;
\.


--
-- TOC entry 5616 (class 0 OID 17759)
-- Dependencies: 304
-- Data for Name: estoque_produto; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.estoque_produto (produto_id, nome, descricao, unidade, nivel_minimo_estoque, codigo_barras, preco_custo, preco_venda, unidade_compra, fator_conversao) FROM stdin;
\.


--
-- TOC entry 5561 (class 0 OID 17216)
-- Dependencies: 249
-- Data for Name: fila_espera; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.fila_espera (fila_id, clinica_id, paciente_id, numero_fila, prioridade, status, criado_em, chamado_em, concluido_em) FROM stdin;
\.


--
-- TOC entry 5574 (class 0 OID 17325)
-- Dependencies: 262
-- Data for Name: fornecedores; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.fornecedores (fornecedor_id, nome, cnpj, contato_nome, contato_email, contato_telefone, endereco, criado_em, atualizado_em) FROM stdin;
\.


--
-- TOC entry 5551 (class 0 OID 17073)
-- Dependencies: 239
-- Data for Name: horarios; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.horarios (horario_id, servico_id, sala_id, inicio, fim) FROM stdin;
\.


--
-- TOC entry 5580 (class 0 OID 17420)
-- Dependencies: 268
-- Data for Name: itens_pedido_compra; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.itens_pedido_compra (item_pedido_id, pedido_id, produto_id, quantidade_pedida, quantidade_recebida, preco_unitario, criado_em) FROM stdin;
\.


--
-- TOC entry 5576 (class 0 OID 17340)
-- Dependencies: 264
-- Data for Name: localizacoes_estoque; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.localizacoes_estoque (localizacao_id, nome, descricao, clinica_id, criado_em, atualizado_em) FROM stdin;
\.


--
-- TOC entry 5565 (class 0 OID 17251)
-- Dependencies: 253
-- Data for Name: logs_acesso; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.logs_acesso (log_id, usuario_id, endereco_ip, agente_usuario, horario_login, sucesso) FROM stdin;
\.


--
-- TOC entry 5563 (class 0 OID 17236)
-- Dependencies: 251
-- Data for Name: logs_auditoria; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.logs_auditoria (auditoria_id, usuario_id, acao, nome_tabela, id_registro, horario_acao, dados_antigos, dados_novos) FROM stdin;
\.


--
-- TOC entry 5577 (class 0 OID 17360)
-- Dependencies: 265
-- Data for Name: lotes_produtos; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.lotes_produtos (lote_id, produto_id, numero_lote, data_fabricacao, data_validade, quantidade_inicial, quantidade_atual, fornecedor_id, localizacao_id, criado_em, atualizado_em) FROM stdin;
\.


--
-- TOC entry 5571 (class 0 OID 17291)
-- Dependencies: 259
-- Data for Name: movimentos_estoque; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.movimentos_estoque (movimento_id, produto_id, quantidade, tipo_movimento, referencia, movimentado_em, movimentado_por, lote_id, localizacao_id) FROM stdin;
\.


--
-- TOC entry 5567 (class 0 OID 17266)
-- Dependencies: 255
-- Data for Name: notificacoes; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.notificacoes (notificacao_id, agendamento_id, canal, dados, enviado_em, status) FROM stdin;
\.


--
-- TOC entry 5621 (class 0 OID 17882)
-- Dependencies: 309
-- Data for Name: paciente_consentimentopaciente; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.paciente_consentimentopaciente (consentimento_id, tipo_consentimento, data_consentimento, ativo, detalhes, paciente_id) FROM stdin;
\.


--
-- TOC entry 5623 (class 0 OID 17896)
-- Dependencies: 311
-- Data for Name: paciente_documentopaciente; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.paciente_documentopaciente (documento_id, dados_ocr, caminho_arquivo, enviado_em, paciente_id, tipo_documento_id) FROM stdin;
\.


--
-- TOC entry 5617 (class 0 OID 17864)
-- Dependencies: 305
-- Data for Name: paciente_paciente; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.paciente_paciente (paciente_id, nome, sobrenome, data_nascimento, sexo, endereco, telefone, email, perfil_epidemiologico, criado_em, atualizado_em) FROM stdin;
\.


--
-- TOC entry 5622 (class 0 OID 17889)
-- Dependencies: 310
-- Data for Name: paciente_responsavellegal; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.paciente_responsavellegal (responsavel_id, nome, cpf, rg, telefone, email, grau_parentesco, endereco, criado_em, paciente_id) FROM stdin;
\.


--
-- TOC entry 5619 (class 0 OID 17872)
-- Dependencies: 307
-- Data for Name: paciente_tipodocumento; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.paciente_tipodocumento (tipo_id, nome, descricao, obrigatorio) FROM stdin;
\.


--
-- TOC entry 5543 (class 0 OID 17001)
-- Dependencies: 231
-- Data for Name: pacientes; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.pacientes (paciente_id, nome, sobrenome, data_nascimento, sexo, endereco, telefone, email, perfil_epidemiologico, criado_em, atualizado_em) FROM stdin;
\.


--
-- TOC entry 5578 (class 0 OID 17397)
-- Dependencies: 266
-- Data for Name: pedidos_compra; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.pedidos_compra (pedido_id, fornecedor_id, data_pedido, data_entrega_prevista, status, total_valor, observacoes, criado_por, criado_em, atualizado_em) FROM stdin;
\.


--
-- TOC entry 5534 (class 0 OID 16917)
-- Dependencies: 222
-- Data for Name: perfil_permissoes; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.perfil_permissoes (perfil_id, permissao_id) FROM stdin;
\.


--
-- TOC entry 5531 (class 0 OID 16898)
-- Dependencies: 219
-- Data for Name: perfis; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.perfis (perfil_id, nome) FROM stdin;
\.


--
-- TOC entry 5536 (class 0 OID 16949)
-- Dependencies: 224
-- Data for Name: perfis_alunos; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.perfis_alunos (usuario_id, rgm, modelo_biometrico) FROM stdin;
\.


--
-- TOC entry 5533 (class 0 OID 16907)
-- Dependencies: 221
-- Data for Name: permissoes; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.permissoes (permissao_id, codigo, descricao) FROM stdin;
\.


--
-- TOC entry 5569 (class 0 OID 17281)
-- Dependencies: 257
-- Data for Name: produtos; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.produtos (produto_id, nome, descricao, unidade, nivel_minimo_estoque, codigo_barras, preco_custo, preco_venda, unidade_compra, fator_conversao) FROM stdin;
\.


--
-- TOC entry 5555 (class 0 OID 17138)
-- Dependencies: 243
-- Data for Name: prontuarios_eletronicos; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.prontuarios_eletronicos (prontuario_id, agendamento_id, clinica_id, aluno_id, coordenador_id, anotacoes, criado_em, atualizado_em) FROM stdin;
\.


--
-- TOC entry 5556 (class 0 OID 17168)
-- Dependencies: 244
-- Data for Name: prontuarios_eletronicos_versoes; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.prontuarios_eletronicos_versoes (versao_id, prontuario_id, aluno_id, coordenador_id, anotacoes, criado_em) FROM stdin;
\.


--
-- TOC entry 5559 (class 0 OID 17197)
-- Dependencies: 247
-- Data for Name: registros_presenca; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.registros_presenca (registro_id, aluno_id, agendamento_id, entrada, saida) FROM stdin;
\.


--
-- TOC entry 5544 (class 0 OID 17011)
-- Dependencies: 232
-- Data for Name: responsaveis_legais; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.responsaveis_legais (responsavel_id, paciente_id, nome, cpf, rg, telefone, email, grau_parentesco, endereco, criado_em) FROM stdin;
\.


--
-- TOC entry 5542 (class 0 OID 16989)
-- Dependencies: 230
-- Data for Name: salas; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.salas (sala_id, clinica_id, nome, capacidade) FROM stdin;
\.


--
-- TOC entry 5540 (class 0 OID 16975)
-- Dependencies: 228
-- Data for Name: servicos; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.servicos (servico_id, clinica_id, nome, descricao) FROM stdin;
\.


--
-- TOC entry 5553 (class 0 OID 17090)
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
-- TOC entry 5546 (class 0 OID 17026)
-- Dependencies: 234
-- Data for Name: tipos_documentos; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tipos_documentos (tipo_id, nome, descricao, obrigatorio) FROM stdin;
\.


--
-- TOC entry 5599 (class 0 OID 17622)
-- Dependencies: 287
-- Data for Name: usuario_logacesso; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.usuario_logacesso (log_id, endereco_ip, agente_usuario, horario_login, sucesso, motivo_falha, usuario_id) FROM stdin;
\.


--
-- TOC entry 5601 (class 0 OID 17630)
-- Dependencies: 289
-- Data for Name: usuario_logauditoria; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.usuario_logauditoria (auditoria_id, acao, nome_tabela, id_registro, horario_acao, dados_antigos, dados_novos, endereco_ip, usuario_id) FROM stdin;
1	LOGIN	\N	\N	2025-07-14 17:09:05.82002-03	\N	\N	127.0.0.1	3f4d5a50-2d0d-4167-8d1d-09fc4bacebf4
\.


--
-- TOC entry 5597 (class 0 OID 17612)
-- Dependencies: 285
-- Data for Name: usuario_perfilaluno; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.usuario_perfilaluno (usuario_id, rgm, modelo_biometrico, curso, semestre, carga_horaria_total) FROM stdin;
\.


--
-- TOC entry 5592 (class 0 OID 17591)
-- Dependencies: 280
-- Data for Name: usuario_usuario; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.usuario_usuario (password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined, usuario_id, nome_completo, telefone) FROM stdin;
pbkdf2_sha256$1000000$LKgsrE2H5us9ZOqvO0eKM3$z1P/215NMwvHodJ4fU3tXkav5r1Fbc4BtL2R0anZrkk=	2025-07-14 17:09:05-03	t	german	German	Sachelaride	sachelaride@gmail.com	t	t	2025-07-14 16:38:46-03	3f4d5a50-2d0d-4167-8d1d-09fc4bacebf4	GERMAN SACHELARIDE	67998599051
\.


--
-- TOC entry 5594 (class 0 OID 17601)
-- Dependencies: 282
-- Data for Name: usuario_usuario_groups; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.usuario_usuario_groups (id, usuario_id, group_id) FROM stdin;
1	3f4d5a50-2d0d-4167-8d1d-09fc4bacebf4	1
\.


--
-- TOC entry 5596 (class 0 OID 17607)
-- Dependencies: 284
-- Data for Name: usuario_usuario_user_permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.usuario_usuario_user_permissions (id, usuario_id, permission_id) FROM stdin;
1	3f4d5a50-2d0d-4167-8d1d-09fc4bacebf4	1
2	3f4d5a50-2d0d-4167-8d1d-09fc4bacebf4	2
3	3f4d5a50-2d0d-4167-8d1d-09fc4bacebf4	3
4	3f4d5a50-2d0d-4167-8d1d-09fc4bacebf4	4
5	3f4d5a50-2d0d-4167-8d1d-09fc4bacebf4	5
6	3f4d5a50-2d0d-4167-8d1d-09fc4bacebf4	6
7	3f4d5a50-2d0d-4167-8d1d-09fc4bacebf4	7
8	3f4d5a50-2d0d-4167-8d1d-09fc4bacebf4	8
9	3f4d5a50-2d0d-4167-8d1d-09fc4bacebf4	9
10	3f4d5a50-2d0d-4167-8d1d-09fc4bacebf4	10
11	3f4d5a50-2d0d-4167-8d1d-09fc4bacebf4	11
12	3f4d5a50-2d0d-4167-8d1d-09fc4bacebf4	12
13	3f4d5a50-2d0d-4167-8d1d-09fc4bacebf4	13
14	3f4d5a50-2d0d-4167-8d1d-09fc4bacebf4	14
15	3f4d5a50-2d0d-4167-8d1d-09fc4bacebf4	15
16	3f4d5a50-2d0d-4167-8d1d-09fc4bacebf4	16
17	3f4d5a50-2d0d-4167-8d1d-09fc4bacebf4	17
18	3f4d5a50-2d0d-4167-8d1d-09fc4bacebf4	18
19	3f4d5a50-2d0d-4167-8d1d-09fc4bacebf4	19
20	3f4d5a50-2d0d-4167-8d1d-09fc4bacebf4	20
21	3f4d5a50-2d0d-4167-8d1d-09fc4bacebf4	21
22	3f4d5a50-2d0d-4167-8d1d-09fc4bacebf4	22
23	3f4d5a50-2d0d-4167-8d1d-09fc4bacebf4	23
24	3f4d5a50-2d0d-4167-8d1d-09fc4bacebf4	24
25	3f4d5a50-2d0d-4167-8d1d-09fc4bacebf4	25
26	3f4d5a50-2d0d-4167-8d1d-09fc4bacebf4	26
27	3f4d5a50-2d0d-4167-8d1d-09fc4bacebf4	27
28	3f4d5a50-2d0d-4167-8d1d-09fc4bacebf4	28
29	3f4d5a50-2d0d-4167-8d1d-09fc4bacebf4	29
30	3f4d5a50-2d0d-4167-8d1d-09fc4bacebf4	30
31	3f4d5a50-2d0d-4167-8d1d-09fc4bacebf4	31
32	3f4d5a50-2d0d-4167-8d1d-09fc4bacebf4	32
33	3f4d5a50-2d0d-4167-8d1d-09fc4bacebf4	33
34	3f4d5a50-2d0d-4167-8d1d-09fc4bacebf4	34
35	3f4d5a50-2d0d-4167-8d1d-09fc4bacebf4	35
36	3f4d5a50-2d0d-4167-8d1d-09fc4bacebf4	36
37	3f4d5a50-2d0d-4167-8d1d-09fc4bacebf4	37
38	3f4d5a50-2d0d-4167-8d1d-09fc4bacebf4	38
39	3f4d5a50-2d0d-4167-8d1d-09fc4bacebf4	39
40	3f4d5a50-2d0d-4167-8d1d-09fc4bacebf4	40
41	3f4d5a50-2d0d-4167-8d1d-09fc4bacebf4	41
42	3f4d5a50-2d0d-4167-8d1d-09fc4bacebf4	42
43	3f4d5a50-2d0d-4167-8d1d-09fc4bacebf4	43
44	3f4d5a50-2d0d-4167-8d1d-09fc4bacebf4	44
45	3f4d5a50-2d0d-4167-8d1d-09fc4bacebf4	45
46	3f4d5a50-2d0d-4167-8d1d-09fc4bacebf4	46
47	3f4d5a50-2d0d-4167-8d1d-09fc4bacebf4	47
48	3f4d5a50-2d0d-4167-8d1d-09fc4bacebf4	48
49	3f4d5a50-2d0d-4167-8d1d-09fc4bacebf4	49
50	3f4d5a50-2d0d-4167-8d1d-09fc4bacebf4	50
51	3f4d5a50-2d0d-4167-8d1d-09fc4bacebf4	51
52	3f4d5a50-2d0d-4167-8d1d-09fc4bacebf4	52
53	3f4d5a50-2d0d-4167-8d1d-09fc4bacebf4	53
54	3f4d5a50-2d0d-4167-8d1d-09fc4bacebf4	54
55	3f4d5a50-2d0d-4167-8d1d-09fc4bacebf4	55
56	3f4d5a50-2d0d-4167-8d1d-09fc4bacebf4	56
57	3f4d5a50-2d0d-4167-8d1d-09fc4bacebf4	57
58	3f4d5a50-2d0d-4167-8d1d-09fc4bacebf4	58
59	3f4d5a50-2d0d-4167-8d1d-09fc4bacebf4	59
60	3f4d5a50-2d0d-4167-8d1d-09fc4bacebf4	60
61	3f4d5a50-2d0d-4167-8d1d-09fc4bacebf4	61
62	3f4d5a50-2d0d-4167-8d1d-09fc4bacebf4	62
63	3f4d5a50-2d0d-4167-8d1d-09fc4bacebf4	63
64	3f4d5a50-2d0d-4167-8d1d-09fc4bacebf4	64
65	3f4d5a50-2d0d-4167-8d1d-09fc4bacebf4	65
66	3f4d5a50-2d0d-4167-8d1d-09fc4bacebf4	66
67	3f4d5a50-2d0d-4167-8d1d-09fc4bacebf4	67
68	3f4d5a50-2d0d-4167-8d1d-09fc4bacebf4	68
69	3f4d5a50-2d0d-4167-8d1d-09fc4bacebf4	69
70	3f4d5a50-2d0d-4167-8d1d-09fc4bacebf4	70
71	3f4d5a50-2d0d-4167-8d1d-09fc4bacebf4	71
72	3f4d5a50-2d0d-4167-8d1d-09fc4bacebf4	72
73	3f4d5a50-2d0d-4167-8d1d-09fc4bacebf4	73
74	3f4d5a50-2d0d-4167-8d1d-09fc4bacebf4	74
75	3f4d5a50-2d0d-4167-8d1d-09fc4bacebf4	75
76	3f4d5a50-2d0d-4167-8d1d-09fc4bacebf4	76
77	3f4d5a50-2d0d-4167-8d1d-09fc4bacebf4	77
78	3f4d5a50-2d0d-4167-8d1d-09fc4bacebf4	78
79	3f4d5a50-2d0d-4167-8d1d-09fc4bacebf4	79
80	3f4d5a50-2d0d-4167-8d1d-09fc4bacebf4	80
81	3f4d5a50-2d0d-4167-8d1d-09fc4bacebf4	81
82	3f4d5a50-2d0d-4167-8d1d-09fc4bacebf4	82
83	3f4d5a50-2d0d-4167-8d1d-09fc4bacebf4	83
84	3f4d5a50-2d0d-4167-8d1d-09fc4bacebf4	84
85	3f4d5a50-2d0d-4167-8d1d-09fc4bacebf4	85
86	3f4d5a50-2d0d-4167-8d1d-09fc4bacebf4	86
87	3f4d5a50-2d0d-4167-8d1d-09fc4bacebf4	87
88	3f4d5a50-2d0d-4167-8d1d-09fc4bacebf4	88
89	3f4d5a50-2d0d-4167-8d1d-09fc4bacebf4	89
90	3f4d5a50-2d0d-4167-8d1d-09fc4bacebf4	90
91	3f4d5a50-2d0d-4167-8d1d-09fc4bacebf4	91
92	3f4d5a50-2d0d-4167-8d1d-09fc4bacebf4	92
\.


--
-- TOC entry 5535 (class 0 OID 16932)
-- Dependencies: 223
-- Data for Name: usuarios; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.usuarios (usuario_id, nome_usuario, senha_hash, perfil_id, nome_completo, email, telefone, criado_em, atualizado_em) FROM stdin;
\.


--
-- TOC entry 5653 (class 0 OID 0)
-- Dependencies: 276
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_group_id_seq', 1, true);


--
-- TOC entry 5654 (class 0 OID 0)
-- Dependencies: 278
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 88, true);


--
-- TOC entry 5655 (class 0 OID 0)
-- Dependencies: 274
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_permission_id_seq', 92, true);


--
-- TOC entry 5656 (class 0 OID 0)
-- Dependencies: 313
-- Name: clinica_clinica_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.clinica_clinica_id_seq', 1, false);


--
-- TOC entry 5657 (class 0 OID 0)
-- Dependencies: 225
-- Name: clinicas_clinica_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.clinicas_clinica_id_seq', 1, false);


--
-- TOC entry 5658 (class 0 OID 0)
-- Dependencies: 236
-- Name: consentimentos_pacientes_consentimento_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.consentimentos_pacientes_consentimento_id_seq', 1, false);


--
-- TOC entry 5659 (class 0 OID 0)
-- Dependencies: 290
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_admin_log_id_seq', 2, true);


--
-- TOC entry 5660 (class 0 OID 0)
-- Dependencies: 272
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_content_type_id_seq', 23, true);


--
-- TOC entry 5661 (class 0 OID 0)
-- Dependencies: 270
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 23, true);


--
-- TOC entry 5662 (class 0 OID 0)
-- Dependencies: 293
-- Name: estoque_fornecedor_fornecedor_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.estoque_fornecedor_fornecedor_id_seq', 1, false);


--
-- TOC entry 5663 (class 0 OID 0)
-- Dependencies: 295
-- Name: estoque_itempedidocompra_item_pedido_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.estoque_itempedidocompra_item_pedido_id_seq', 1, false);


--
-- TOC entry 5664 (class 0 OID 0)
-- Dependencies: 297
-- Name: estoque_localizacaoestoque_localizacao_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.estoque_localizacaoestoque_localizacao_id_seq', 1, false);


--
-- TOC entry 5665 (class 0 OID 0)
-- Dependencies: 300
-- Name: estoque_movimentoestoque_movimento_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.estoque_movimentoestoque_movimento_id_seq', 1, false);


--
-- TOC entry 5666 (class 0 OID 0)
-- Dependencies: 303
-- Name: estoque_produto_produto_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.estoque_produto_produto_id_seq', 1, false);


--
-- TOC entry 5667 (class 0 OID 0)
-- Dependencies: 248
-- Name: fila_espera_fila_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.fila_espera_fila_id_seq', 1, false);


--
-- TOC entry 5668 (class 0 OID 0)
-- Dependencies: 261
-- Name: fornecedores_fornecedor_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.fornecedores_fornecedor_id_seq', 1, false);


--
-- TOC entry 5669 (class 0 OID 0)
-- Dependencies: 238
-- Name: horarios_horario_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.horarios_horario_id_seq', 1, false);


--
-- TOC entry 5670 (class 0 OID 0)
-- Dependencies: 267
-- Name: itens_pedido_compra_item_pedido_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.itens_pedido_compra_item_pedido_id_seq', 1, false);


--
-- TOC entry 5671 (class 0 OID 0)
-- Dependencies: 263
-- Name: localizacoes_estoque_localizacao_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.localizacoes_estoque_localizacao_id_seq', 1, false);


--
-- TOC entry 5672 (class 0 OID 0)
-- Dependencies: 252
-- Name: logs_acesso_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.logs_acesso_log_id_seq', 1, false);


--
-- TOC entry 5673 (class 0 OID 0)
-- Dependencies: 250
-- Name: logs_auditoria_auditoria_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.logs_auditoria_auditoria_id_seq', 1, false);


--
-- TOC entry 5674 (class 0 OID 0)
-- Dependencies: 258
-- Name: movimentos_estoque_movimento_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.movimentos_estoque_movimento_id_seq', 1, false);


--
-- TOC entry 5675 (class 0 OID 0)
-- Dependencies: 254
-- Name: notificacoes_notificacao_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.notificacoes_notificacao_id_seq', 1, false);


--
-- TOC entry 5676 (class 0 OID 0)
-- Dependencies: 308
-- Name: paciente_consentimentopaciente_consentimento_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.paciente_consentimentopaciente_consentimento_id_seq', 1, false);


--
-- TOC entry 5677 (class 0 OID 0)
-- Dependencies: 306
-- Name: paciente_tipodocumento_tipo_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.paciente_tipodocumento_tipo_id_seq', 1, false);


--
-- TOC entry 5678 (class 0 OID 0)
-- Dependencies: 218
-- Name: perfis_perfil_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.perfis_perfil_id_seq', 1, false);


--
-- TOC entry 5679 (class 0 OID 0)
-- Dependencies: 220
-- Name: permissoes_permissao_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.permissoes_permissao_id_seq', 1, false);


--
-- TOC entry 5680 (class 0 OID 0)
-- Dependencies: 256
-- Name: produtos_produto_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.produtos_produto_id_seq', 1, false);


--
-- TOC entry 5681 (class 0 OID 0)
-- Dependencies: 246
-- Name: registros_presenca_registro_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.registros_presenca_registro_id_seq', 1, false);


--
-- TOC entry 5682 (class 0 OID 0)
-- Dependencies: 229
-- Name: salas_sala_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.salas_sala_id_seq', 1, false);


--
-- TOC entry 5683 (class 0 OID 0)
-- Dependencies: 227
-- Name: servicos_servico_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.servicos_servico_id_seq', 1, false);


--
-- TOC entry 5684 (class 0 OID 0)
-- Dependencies: 240
-- Name: status_agendamento_status_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.status_agendamento_status_id_seq', 5, true);


--
-- TOC entry 5685 (class 0 OID 0)
-- Dependencies: 233
-- Name: tipos_documentos_tipo_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tipos_documentos_tipo_id_seq', 1, false);


--
-- TOC entry 5686 (class 0 OID 0)
-- Dependencies: 286
-- Name: usuario_logacesso_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.usuario_logacesso_log_id_seq', 1, false);


--
-- TOC entry 5687 (class 0 OID 0)
-- Dependencies: 288
-- Name: usuario_logauditoria_auditoria_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.usuario_logauditoria_auditoria_id_seq', 1, true);


--
-- TOC entry 5688 (class 0 OID 0)
-- Dependencies: 281
-- Name: usuario_usuario_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.usuario_usuario_groups_id_seq', 1, true);


--
-- TOC entry 5689 (class 0 OID 0)
-- Dependencies: 283
-- Name: usuario_usuario_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.usuario_usuario_user_permissions_id_seq', 92, true);


--
-- TOC entry 5116 (class 2606 OID 17107)
-- Name: agendamentos agendamentos_paciente_id_horario_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.agendamentos
    ADD CONSTRAINT agendamentos_paciente_id_horario_id_key UNIQUE (paciente_id, horario_id);


--
-- TOC entry 5118 (class 2606 OID 17105)
-- Name: agendamentos agendamentos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.agendamentos
    ADD CONSTRAINT agendamentos_pkey PRIMARY KEY (agendamento_id);


--
-- TOC entry 5172 (class 2606 OID 17461)
-- Name: ajustes_estoque ajustes_estoque_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ajustes_estoque
    ADD CONSTRAINT ajustes_estoque_pkey PRIMARY KEY (ajuste_id);


--
-- TOC entry 5126 (class 2606 OID 17190)
-- Name: anexos_prontuario anexos_prontuario_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.anexos_prontuario
    ADD CONSTRAINT anexos_prontuario_pkey PRIMARY KEY (anexo_id);


--
-- TOC entry 5189 (class 2606 OID 17589)
-- Name: auth_group auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- TOC entry 5194 (class 2606 OID 17575)
-- Name: auth_group_permissions auth_group_permissions_group_id_permission_id_0cd325b0_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id);


--
-- TOC entry 5197 (class 2606 OID 17564)
-- Name: auth_group_permissions auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- TOC entry 5191 (class 2606 OID 17556)
-- Name: auth_group auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- TOC entry 5184 (class 2606 OID 17566)
-- Name: auth_permission auth_permission_content_type_id_codename_01ab375a_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename);


--
-- TOC entry 5186 (class 2606 OID 17550)
-- Name: auth_permission auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- TOC entry 5304 (class 2606 OID 17953)
-- Name: clinica_clinica clinica_clinica_nome_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clinica_clinica
    ADD CONSTRAINT clinica_clinica_nome_key UNIQUE (nome);


--
-- TOC entry 5306 (class 2606 OID 17951)
-- Name: clinica_clinica clinica_clinica_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clinica_clinica
    ADD CONSTRAINT clinica_clinica_pkey PRIMARY KEY (id);


--
-- TOC entry 5090 (class 2606 OID 16973)
-- Name: clinicas clinicas_nome_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clinicas
    ADD CONSTRAINT clinicas_nome_key UNIQUE (nome);


--
-- TOC entry 5092 (class 2606 OID 16971)
-- Name: clinicas clinicas_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clinicas
    ADD CONSTRAINT clinicas_pkey PRIMARY KEY (clinica_id);


--
-- TOC entry 5149 (class 2606 OID 17317)
-- Name: configuracoes_sistema configuracoes_sistema_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.configuracoes_sistema
    ADD CONSTRAINT configuracoes_sistema_pkey PRIMARY KEY (chave);


--
-- TOC entry 5108 (class 2606 OID 17066)
-- Name: consentimentos_pacientes consentimentos_pacientes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.consentimentos_pacientes
    ADD CONSTRAINT consentimentos_pacientes_pkey PRIMARY KEY (consentimento_id);


--
-- TOC entry 5228 (class 2606 OID 17692)
-- Name: django_admin_log django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- TOC entry 5179 (class 2606 OID 17544)
-- Name: django_content_type django_content_type_app_label_model_76bd3d3b_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);


--
-- TOC entry 5181 (class 2606 OID 17542)
-- Name: django_content_type django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- TOC entry 5177 (class 2606 OID 17536)
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- TOC entry 5300 (class 2606 OID 17940)
-- Name: django_session django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- TOC entry 5106 (class 2606 OID 17045)
-- Name: documentos_pacientes documentos_pacientes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.documentos_pacientes
    ADD CONSTRAINT documentos_pacientes_pkey PRIMARY KEY (documento_id);


--
-- TOC entry 5234 (class 2606 OID 17711)
-- Name: estoque_ajusteestoque estoque_ajusteestoque_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.estoque_ajusteestoque
    ADD CONSTRAINT estoque_ajusteestoque_pkey PRIMARY KEY (ajuste_id);


--
-- TOC entry 5238 (class 2606 OID 17723)
-- Name: estoque_fornecedor estoque_fornecedor_cnpj_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.estoque_fornecedor
    ADD CONSTRAINT estoque_fornecedor_cnpj_key UNIQUE (cnpj);


--
-- TOC entry 5241 (class 2606 OID 17721)
-- Name: estoque_fornecedor estoque_fornecedor_nome_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.estoque_fornecedor
    ADD CONSTRAINT estoque_fornecedor_nome_key UNIQUE (nome);


--
-- TOC entry 5243 (class 2606 OID 17719)
-- Name: estoque_fornecedor estoque_fornecedor_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.estoque_fornecedor
    ADD CONSTRAINT estoque_fornecedor_pkey PRIMARY KEY (fornecedor_id);


--
-- TOC entry 5246 (class 2606 OID 17729)
-- Name: estoque_itempedidocompra estoque_itempedidocompra_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.estoque_itempedidocompra
    ADD CONSTRAINT estoque_itempedidocompra_pkey PRIMARY KEY (item_pedido_id);


--
-- TOC entry 5250 (class 2606 OID 17739)
-- Name: estoque_localizacaoestoque estoque_localizacaoestoque_nome_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.estoque_localizacaoestoque
    ADD CONSTRAINT estoque_localizacaoestoque_nome_key UNIQUE (nome);


--
-- TOC entry 5252 (class 2606 OID 17737)
-- Name: estoque_localizacaoestoque estoque_localizacaoestoque_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.estoque_localizacaoestoque
    ADD CONSTRAINT estoque_localizacaoestoque_pkey PRIMARY KEY (localizacao_id);


--
-- TOC entry 5256 (class 2606 OID 17744)
-- Name: estoque_loteproduto estoque_loteproduto_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.estoque_loteproduto
    ADD CONSTRAINT estoque_loteproduto_pkey PRIMARY KEY (lote_id);


--
-- TOC entry 5262 (class 2606 OID 17750)
-- Name: estoque_movimentoestoque estoque_movimentoestoque_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.estoque_movimentoestoque
    ADD CONSTRAINT estoque_movimentoestoque_pkey PRIMARY KEY (movimento_id);


--
-- TOC entry 5267 (class 2606 OID 17757)
-- Name: estoque_pedidocompra estoque_pedidocompra_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.estoque_pedidocompra
    ADD CONSTRAINT estoque_pedidocompra_pkey PRIMARY KEY (pedido_id);


--
-- TOC entry 5270 (class 2606 OID 17767)
-- Name: estoque_produto estoque_produto_codigo_barras_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.estoque_produto
    ADD CONSTRAINT estoque_produto_codigo_barras_key UNIQUE (codigo_barras);


--
-- TOC entry 5274 (class 2606 OID 17765)
-- Name: estoque_produto estoque_produto_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.estoque_produto
    ADD CONSTRAINT estoque_produto_pkey PRIMARY KEY (produto_id);


--
-- TOC entry 5131 (class 2606 OID 17224)
-- Name: fila_espera fila_espera_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fila_espera
    ADD CONSTRAINT fila_espera_pkey PRIMARY KEY (fila_id);


--
-- TOC entry 5151 (class 2606 OID 17338)
-- Name: fornecedores fornecedores_cnpj_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fornecedores
    ADD CONSTRAINT fornecedores_cnpj_key UNIQUE (cnpj);


--
-- TOC entry 5153 (class 2606 OID 17336)
-- Name: fornecedores fornecedores_nome_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fornecedores
    ADD CONSTRAINT fornecedores_nome_key UNIQUE (nome);


--
-- TOC entry 5155 (class 2606 OID 17334)
-- Name: fornecedores fornecedores_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fornecedores
    ADD CONSTRAINT fornecedores_pkey PRIMARY KEY (fornecedor_id);


--
-- TOC entry 5110 (class 2606 OID 17078)
-- Name: horarios horarios_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.horarios
    ADD CONSTRAINT horarios_pkey PRIMARY KEY (horario_id);


--
-- TOC entry 5170 (class 2606 OID 17427)
-- Name: itens_pedido_compra itens_pedido_compra_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.itens_pedido_compra
    ADD CONSTRAINT itens_pedido_compra_pkey PRIMARY KEY (item_pedido_id);


--
-- TOC entry 5157 (class 2606 OID 17351)
-- Name: localizacoes_estoque localizacoes_estoque_nome_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.localizacoes_estoque
    ADD CONSTRAINT localizacoes_estoque_nome_key UNIQUE (nome);


--
-- TOC entry 5159 (class 2606 OID 17349)
-- Name: localizacoes_estoque localizacoes_estoque_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.localizacoes_estoque
    ADD CONSTRAINT localizacoes_estoque_pkey PRIMARY KEY (localizacao_id);


--
-- TOC entry 5137 (class 2606 OID 17259)
-- Name: logs_acesso logs_acesso_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.logs_acesso
    ADD CONSTRAINT logs_acesso_pkey PRIMARY KEY (log_id);


--
-- TOC entry 5134 (class 2606 OID 17244)
-- Name: logs_auditoria logs_auditoria_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.logs_auditoria
    ADD CONSTRAINT logs_auditoria_pkey PRIMARY KEY (auditoria_id);


--
-- TOC entry 5163 (class 2606 OID 17367)
-- Name: lotes_produtos lotes_produtos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.lotes_produtos
    ADD CONSTRAINT lotes_produtos_pkey PRIMARY KEY (lote_id);


--
-- TOC entry 5165 (class 2606 OID 17369)
-- Name: lotes_produtos lotes_produtos_produto_id_numero_lote_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.lotes_produtos
    ADD CONSTRAINT lotes_produtos_produto_id_numero_lote_key UNIQUE (produto_id, numero_lote);


--
-- TOC entry 5147 (class 2606 OID 17299)
-- Name: movimentos_estoque movimentos_estoque_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.movimentos_estoque
    ADD CONSTRAINT movimentos_estoque_pkey PRIMARY KEY (movimento_id);


--
-- TOC entry 5139 (class 2606 OID 17274)
-- Name: notificacoes notificacoes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.notificacoes
    ADD CONSTRAINT notificacoes_pkey PRIMARY KEY (notificacao_id);


--
-- TOC entry 5290 (class 2606 OID 17888)
-- Name: paciente_consentimentopaciente paciente_consentimentopaciente_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.paciente_consentimentopaciente
    ADD CONSTRAINT paciente_consentimentopaciente_pkey PRIMARY KEY (consentimento_id);


--
-- TOC entry 5296 (class 2606 OID 17902)
-- Name: paciente_documentopaciente paciente_documentopaciente_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.paciente_documentopaciente
    ADD CONSTRAINT paciente_documentopaciente_pkey PRIMARY KEY (documento_id);


--
-- TOC entry 5280 (class 2606 OID 17870)
-- Name: paciente_paciente paciente_paciente_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.paciente_paciente
    ADD CONSTRAINT paciente_paciente_pkey PRIMARY KEY (paciente_id);


--
-- TOC entry 5293 (class 2606 OID 17895)
-- Name: paciente_responsavellegal paciente_responsavellegal_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.paciente_responsavellegal
    ADD CONSTRAINT paciente_responsavellegal_pkey PRIMARY KEY (responsavel_id);


--
-- TOC entry 5285 (class 2606 OID 17880)
-- Name: paciente_tipodocumento paciente_tipodocumento_nome_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.paciente_tipodocumento
    ADD CONSTRAINT paciente_tipodocumento_nome_key UNIQUE (nome);


--
-- TOC entry 5287 (class 2606 OID 17878)
-- Name: paciente_tipodocumento paciente_tipodocumento_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.paciente_tipodocumento
    ADD CONSTRAINT paciente_tipodocumento_pkey PRIMARY KEY (tipo_id);


--
-- TOC entry 5098 (class 2606 OID 17010)
-- Name: pacientes pacientes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pacientes
    ADD CONSTRAINT pacientes_pkey PRIMARY KEY (paciente_id);


--
-- TOC entry 5168 (class 2606 OID 17408)
-- Name: pedidos_compra pedidos_compra_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pedidos_compra
    ADD CONSTRAINT pedidos_compra_pkey PRIMARY KEY (pedido_id);


--
-- TOC entry 5080 (class 2606 OID 16921)
-- Name: perfil_permissoes perfil_permissoes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.perfil_permissoes
    ADD CONSTRAINT perfil_permissoes_pkey PRIMARY KEY (perfil_id, permissao_id);


--
-- TOC entry 5086 (class 2606 OID 16955)
-- Name: perfis_alunos perfis_alunos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.perfis_alunos
    ADD CONSTRAINT perfis_alunos_pkey PRIMARY KEY (usuario_id);


--
-- TOC entry 5088 (class 2606 OID 16957)
-- Name: perfis_alunos perfis_alunos_rgm_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.perfis_alunos
    ADD CONSTRAINT perfis_alunos_rgm_key UNIQUE (rgm);


--
-- TOC entry 5072 (class 2606 OID 16905)
-- Name: perfis perfis_nome_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.perfis
    ADD CONSTRAINT perfis_nome_key UNIQUE (nome);


--
-- TOC entry 5074 (class 2606 OID 16903)
-- Name: perfis perfis_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.perfis
    ADD CONSTRAINT perfis_pkey PRIMARY KEY (perfil_id);


--
-- TOC entry 5076 (class 2606 OID 16916)
-- Name: permissoes permissoes_codigo_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.permissoes
    ADD CONSTRAINT permissoes_codigo_key UNIQUE (codigo);


--
-- TOC entry 5078 (class 2606 OID 16914)
-- Name: permissoes permissoes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.permissoes
    ADD CONSTRAINT permissoes_pkey PRIMARY KEY (permissao_id);


--
-- TOC entry 5141 (class 2606 OID 17359)
-- Name: produtos produtos_codigo_barras_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.produtos
    ADD CONSTRAINT produtos_codigo_barras_key UNIQUE (codigo_barras);


--
-- TOC entry 5143 (class 2606 OID 17289)
-- Name: produtos produtos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.produtos
    ADD CONSTRAINT produtos_pkey PRIMARY KEY (produto_id);


--
-- TOC entry 5122 (class 2606 OID 17147)
-- Name: prontuarios_eletronicos prontuarios_eletronicos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.prontuarios_eletronicos
    ADD CONSTRAINT prontuarios_eletronicos_pkey PRIMARY KEY (prontuario_id);


--
-- TOC entry 5124 (class 2606 OID 17176)
-- Name: prontuarios_eletronicos_versoes prontuarios_eletronicos_versoes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.prontuarios_eletronicos_versoes
    ADD CONSTRAINT prontuarios_eletronicos_versoes_pkey PRIMARY KEY (versao_id);


--
-- TOC entry 5129 (class 2606 OID 17204)
-- Name: registros_presenca registros_presenca_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.registros_presenca
    ADD CONSTRAINT registros_presenca_pkey PRIMARY KEY (registro_id);


--
-- TOC entry 5100 (class 2606 OID 17019)
-- Name: responsaveis_legais responsaveis_legais_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.responsaveis_legais
    ADD CONSTRAINT responsaveis_legais_pkey PRIMARY KEY (responsavel_id);


--
-- TOC entry 5096 (class 2606 OID 16995)
-- Name: salas salas_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.salas
    ADD CONSTRAINT salas_pkey PRIMARY KEY (sala_id);


--
-- TOC entry 5094 (class 2606 OID 16982)
-- Name: servicos servicos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.servicos
    ADD CONSTRAINT servicos_pkey PRIMARY KEY (servico_id);


--
-- TOC entry 5112 (class 2606 OID 17097)
-- Name: status_agendamento status_agendamento_nome_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.status_agendamento
    ADD CONSTRAINT status_agendamento_nome_key UNIQUE (nome);


--
-- TOC entry 5114 (class 2606 OID 17095)
-- Name: status_agendamento status_agendamento_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.status_agendamento
    ADD CONSTRAINT status_agendamento_pkey PRIMARY KEY (status_id);


--
-- TOC entry 5102 (class 2606 OID 17036)
-- Name: tipos_documentos tipos_documentos_nome_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tipos_documentos
    ADD CONSTRAINT tipos_documentos_nome_key UNIQUE (nome);


--
-- TOC entry 5104 (class 2606 OID 17034)
-- Name: tipos_documentos tipos_documentos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tipos_documentos
    ADD CONSTRAINT tipos_documentos_pkey PRIMARY KEY (tipo_id);


--
-- TOC entry 5221 (class 2606 OID 17628)
-- Name: usuario_logacesso usuario_logacesso_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuario_logacesso
    ADD CONSTRAINT usuario_logacesso_pkey PRIMARY KEY (log_id);


--
-- TOC entry 5224 (class 2606 OID 17636)
-- Name: usuario_logauditoria usuario_logauditoria_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuario_logauditoria
    ADD CONSTRAINT usuario_logauditoria_pkey PRIMARY KEY (auditoria_id);


--
-- TOC entry 5216 (class 2606 OID 17618)
-- Name: usuario_perfilaluno usuario_perfilaluno_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuario_perfilaluno
    ADD CONSTRAINT usuario_perfilaluno_pkey PRIMARY KEY (usuario_id);


--
-- TOC entry 5219 (class 2606 OID 17620)
-- Name: usuario_perfilaluno usuario_perfilaluno_rgm_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuario_perfilaluno
    ADD CONSTRAINT usuario_perfilaluno_rgm_key UNIQUE (rgm);


--
-- TOC entry 5205 (class 2606 OID 17605)
-- Name: usuario_usuario_groups usuario_usuario_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuario_usuario_groups
    ADD CONSTRAINT usuario_usuario_groups_pkey PRIMARY KEY (id);


--
-- TOC entry 5208 (class 2606 OID 17639)
-- Name: usuario_usuario_groups usuario_usuario_groups_usuario_id_group_id_a4cfb0b8_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuario_usuario_groups
    ADD CONSTRAINT usuario_usuario_groups_usuario_id_group_id_a4cfb0b8_uniq UNIQUE (usuario_id, group_id);


--
-- TOC entry 5199 (class 2606 OID 17597)
-- Name: usuario_usuario usuario_usuario_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuario_usuario
    ADD CONSTRAINT usuario_usuario_pkey PRIMARY KEY (usuario_id);


--
-- TOC entry 5210 (class 2606 OID 17653)
-- Name: usuario_usuario_user_permissions usuario_usuario_user_per_usuario_id_permission_id_c0a85055_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuario_usuario_user_permissions
    ADD CONSTRAINT usuario_usuario_user_per_usuario_id_permission_id_c0a85055_uniq UNIQUE (usuario_id, permission_id);


--
-- TOC entry 5213 (class 2606 OID 17611)
-- Name: usuario_usuario_user_permissions usuario_usuario_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuario_usuario_user_permissions
    ADD CONSTRAINT usuario_usuario_user_permissions_pkey PRIMARY KEY (id);


--
-- TOC entry 5202 (class 2606 OID 17599)
-- Name: usuario_usuario usuario_usuario_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuario_usuario
    ADD CONSTRAINT usuario_usuario_username_key UNIQUE (username);


--
-- TOC entry 5082 (class 2606 OID 16943)
-- Name: usuarios usuarios_nome_usuario_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_nome_usuario_key UNIQUE (nome_usuario);


--
-- TOC entry 5084 (class 2606 OID 16941)
-- Name: usuarios usuarios_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_pkey PRIMARY KEY (usuario_id);


--
-- TOC entry 5187 (class 1259 OID 17590)
-- Name: auth_group_name_a6ea08ec_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops);


--
-- TOC entry 5192 (class 1259 OID 17586)
-- Name: auth_group_permissions_group_id_b120cbf9; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON public.auth_group_permissions USING btree (group_id);


--
-- TOC entry 5195 (class 1259 OID 17587)
-- Name: auth_group_permissions_permission_id_84c5c92e; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON public.auth_group_permissions USING btree (permission_id);


--
-- TOC entry 5182 (class 1259 OID 17572)
-- Name: auth_permission_content_type_id_2f476e4b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_permission_content_type_id_2f476e4b ON public.auth_permission USING btree (content_type_id);


--
-- TOC entry 5302 (class 1259 OID 17954)
-- Name: clinica_clinica_nome_70891283_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX clinica_clinica_nome_70891283_like ON public.clinica_clinica USING btree (nome varchar_pattern_ops);


--
-- TOC entry 5226 (class 1259 OID 17703)
-- Name: django_admin_log_content_type_id_c4bce8eb; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON public.django_admin_log USING btree (content_type_id);


--
-- TOC entry 5229 (class 1259 OID 17704)
-- Name: django_admin_log_user_id_c564eba6; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_admin_log_user_id_c564eba6 ON public.django_admin_log USING btree (user_id);


--
-- TOC entry 5298 (class 1259 OID 17942)
-- Name: django_session_expire_date_a5c62663; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_session_expire_date_a5c62663 ON public.django_session USING btree (expire_date);


--
-- TOC entry 5301 (class 1259 OID 17941)
-- Name: django_session_session_key_c0390e0f_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key varchar_pattern_ops);


--
-- TOC entry 5230 (class 1259 OID 17849)
-- Name: estoque_ajusteestoque_ajustado_por_id_58af1482; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX estoque_ajusteestoque_ajustado_por_id_58af1482 ON public.estoque_ajusteestoque USING btree (ajustado_por_id);


--
-- TOC entry 5231 (class 1259 OID 17850)
-- Name: estoque_ajusteestoque_localizacao_id_138969a3; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX estoque_ajusteestoque_localizacao_id_138969a3 ON public.estoque_ajusteestoque USING btree (localizacao_id);


--
-- TOC entry 5232 (class 1259 OID 17853)
-- Name: estoque_ajusteestoque_lote_id_1aba4968; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX estoque_ajusteestoque_lote_id_1aba4968 ON public.estoque_ajusteestoque USING btree (lote_id);


--
-- TOC entry 5235 (class 1259 OID 17863)
-- Name: estoque_ajusteestoque_produto_id_6575b57b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX estoque_ajusteestoque_produto_id_6575b57b ON public.estoque_ajusteestoque USING btree (produto_id);


--
-- TOC entry 5236 (class 1259 OID 17769)
-- Name: estoque_fornecedor_cnpj_7c6dd052_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX estoque_fornecedor_cnpj_7c6dd052_like ON public.estoque_fornecedor USING btree (cnpj varchar_pattern_ops);


--
-- TOC entry 5239 (class 1259 OID 17768)
-- Name: estoque_fornecedor_nome_f562d140_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX estoque_fornecedor_nome_f562d140_like ON public.estoque_fornecedor USING btree (nome varchar_pattern_ops);


--
-- TOC entry 5244 (class 1259 OID 17859)
-- Name: estoque_itempedidocompra_pedido_id_a1a80db1; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX estoque_itempedidocompra_pedido_id_a1a80db1 ON public.estoque_itempedidocompra USING btree (pedido_id);


--
-- TOC entry 5247 (class 1259 OID 17862)
-- Name: estoque_itempedidocompra_produto_id_6d113627; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX estoque_itempedidocompra_produto_id_6d113627 ON public.estoque_itempedidocompra USING btree (produto_id);


--
-- TOC entry 5248 (class 1259 OID 17770)
-- Name: estoque_localizacaoestoque_nome_a550b0d3_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX estoque_localizacaoestoque_nome_a550b0d3_like ON public.estoque_localizacaoestoque USING btree (nome varchar_pattern_ops);


--
-- TOC entry 5253 (class 1259 OID 17851)
-- Name: estoque_loteproduto_fornecedor_id_baadf52b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX estoque_loteproduto_fornecedor_id_baadf52b ON public.estoque_loteproduto USING btree (fornecedor_id);


--
-- TOC entry 5254 (class 1259 OID 17852)
-- Name: estoque_loteproduto_localizacao_id_f1ddb136; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX estoque_loteproduto_localizacao_id_f1ddb136 ON public.estoque_loteproduto USING btree (localizacao_id);


--
-- TOC entry 5257 (class 1259 OID 17861)
-- Name: estoque_loteproduto_produto_id_85d0ece0; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX estoque_loteproduto_produto_id_85d0ece0 ON public.estoque_loteproduto USING btree (produto_id);


--
-- TOC entry 5258 (class 1259 OID 17854)
-- Name: estoque_movimentoestoque_localizacao_id_d42bebfe; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX estoque_movimentoestoque_localizacao_id_d42bebfe ON public.estoque_movimentoestoque USING btree (localizacao_id);


--
-- TOC entry 5259 (class 1259 OID 17855)
-- Name: estoque_movimentoestoque_lote_id_f8a0b051; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX estoque_movimentoestoque_lote_id_f8a0b051 ON public.estoque_movimentoestoque USING btree (lote_id);


--
-- TOC entry 5260 (class 1259 OID 17856)
-- Name: estoque_movimentoestoque_movimentado_por_id_1a9aa827; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX estoque_movimentoestoque_movimentado_por_id_1a9aa827 ON public.estoque_movimentoestoque USING btree (movimentado_por_id);


--
-- TOC entry 5263 (class 1259 OID 17860)
-- Name: estoque_movimentoestoque_produto_id_accf41ff; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX estoque_movimentoestoque_produto_id_accf41ff ON public.estoque_movimentoestoque USING btree (produto_id);


--
-- TOC entry 5264 (class 1259 OID 17857)
-- Name: estoque_pedidocompra_criado_por_id_458886a6; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX estoque_pedidocompra_criado_por_id_458886a6 ON public.estoque_pedidocompra USING btree (criado_por_id);


--
-- TOC entry 5265 (class 1259 OID 17858)
-- Name: estoque_pedidocompra_fornecedor_id_6a13935d; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX estoque_pedidocompra_fornecedor_id_6a13935d ON public.estoque_pedidocompra USING btree (fornecedor_id);


--
-- TOC entry 5268 (class 1259 OID 17773)
-- Name: estoque_produto_codigo_barras_04e5bb66_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX estoque_produto_codigo_barras_04e5bb66_like ON public.estoque_produto USING btree (codigo_barras varchar_pattern_ops);


--
-- TOC entry 5271 (class 1259 OID 17771)
-- Name: estoque_produto_nome_39fca06a; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX estoque_produto_nome_39fca06a ON public.estoque_produto USING btree (nome);


--
-- TOC entry 5272 (class 1259 OID 17772)
-- Name: estoque_produto_nome_39fca06a_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX estoque_produto_nome_39fca06a_like ON public.estoque_produto USING btree (nome varchar_pattern_ops);


--
-- TOC entry 5119 (class 1259 OID 17319)
-- Name: idx_agendamentos_aluno; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_agendamentos_aluno ON public.agendamentos USING btree (aluno_id);


--
-- TOC entry 5120 (class 1259 OID 17318)
-- Name: idx_agendamentos_paciente; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_agendamentos_paciente ON public.agendamentos USING btree (paciente_id);


--
-- TOC entry 5173 (class 1259 OID 17499)
-- Name: idx_ajustes_estoque_localizacao_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_ajustes_estoque_localizacao_id ON public.ajustes_estoque USING btree (localizacao_id);


--
-- TOC entry 5174 (class 1259 OID 17498)
-- Name: idx_ajustes_estoque_lote_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_ajustes_estoque_lote_id ON public.ajustes_estoque USING btree (lote_id);


--
-- TOC entry 5175 (class 1259 OID 17497)
-- Name: idx_ajustes_estoque_produto_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_ajustes_estoque_produto_id ON public.ajustes_estoque USING btree (produto_id);


--
-- TOC entry 5132 (class 1259 OID 17321)
-- Name: idx_fila_espera_status; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_fila_espera_status ON public.fila_espera USING btree (status);


--
-- TOC entry 5135 (class 1259 OID 17322)
-- Name: idx_logs_acesso_horario; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_logs_acesso_horario ON public.logs_acesso USING btree (horario_login);


--
-- TOC entry 5160 (class 1259 OID 17493)
-- Name: idx_lotes_produtos_data_validade; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_lotes_produtos_data_validade ON public.lotes_produtos USING btree (data_validade);


--
-- TOC entry 5161 (class 1259 OID 17492)
-- Name: idx_lotes_produtos_produto_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_lotes_produtos_produto_id ON public.lotes_produtos USING btree (produto_id);


--
-- TOC entry 5144 (class 1259 OID 17495)
-- Name: idx_movimentos_estoque_localizacao_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_movimentos_estoque_localizacao_id ON public.movimentos_estoque USING btree (localizacao_id);


--
-- TOC entry 5145 (class 1259 OID 17494)
-- Name: idx_movimentos_estoque_lote_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_movimentos_estoque_lote_id ON public.movimentos_estoque USING btree (lote_id);


--
-- TOC entry 5166 (class 1259 OID 17496)
-- Name: idx_pedidos_compra_fornecedor_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_pedidos_compra_fornecedor_id ON public.pedidos_compra USING btree (fornecedor_id);


--
-- TOC entry 5127 (class 1259 OID 17320)
-- Name: idx_registros_presenca_aluno; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_registros_presenca_aluno ON public.registros_presenca USING btree (aluno_id);


--
-- TOC entry 5288 (class 1259 OID 17915)
-- Name: paciente_consentimentopaciente_paciente_id_a8a88a87; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX paciente_consentimentopaciente_paciente_id_a8a88a87 ON public.paciente_consentimentopaciente USING btree (paciente_id);


--
-- TOC entry 5294 (class 1259 OID 17932)
-- Name: paciente_documentopaciente_paciente_id_0424bcaa; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX paciente_documentopaciente_paciente_id_0424bcaa ON public.paciente_documentopaciente USING btree (paciente_id);


--
-- TOC entry 5297 (class 1259 OID 17933)
-- Name: paciente_documentopaciente_tipo_documento_id_910bc502; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX paciente_documentopaciente_tipo_documento_id_910bc502 ON public.paciente_documentopaciente USING btree (tipo_documento_id);


--
-- TOC entry 5275 (class 1259 OID 17907)
-- Name: paciente_paciente_email_ae6fbbd6; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX paciente_paciente_email_ae6fbbd6 ON public.paciente_paciente USING btree (email);


--
-- TOC entry 5276 (class 1259 OID 17908)
-- Name: paciente_paciente_email_ae6fbbd6_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX paciente_paciente_email_ae6fbbd6_like ON public.paciente_paciente USING btree (email varchar_pattern_ops);


--
-- TOC entry 5277 (class 1259 OID 17903)
-- Name: paciente_paciente_nome_60e536e7; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX paciente_paciente_nome_60e536e7 ON public.paciente_paciente USING btree (nome);


--
-- TOC entry 5278 (class 1259 OID 17904)
-- Name: paciente_paciente_nome_60e536e7_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX paciente_paciente_nome_60e536e7_like ON public.paciente_paciente USING btree (nome varchar_pattern_ops);


--
-- TOC entry 5281 (class 1259 OID 17905)
-- Name: paciente_paciente_sobrenome_54a51d0b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX paciente_paciente_sobrenome_54a51d0b ON public.paciente_paciente USING btree (sobrenome);


--
-- TOC entry 5282 (class 1259 OID 17906)
-- Name: paciente_paciente_sobrenome_54a51d0b_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX paciente_paciente_sobrenome_54a51d0b_like ON public.paciente_paciente USING btree (sobrenome varchar_pattern_ops);


--
-- TOC entry 5291 (class 1259 OID 17921)
-- Name: paciente_responsavellegal_paciente_id_ea2ec3d0; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX paciente_responsavellegal_paciente_id_ea2ec3d0 ON public.paciente_responsavellegal USING btree (paciente_id);


--
-- TOC entry 5283 (class 1259 OID 17909)
-- Name: paciente_tipodocumento_nome_efaa5e44_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX paciente_tipodocumento_nome_efaa5e44_like ON public.paciente_tipodocumento USING btree (nome varchar_pattern_ops);


--
-- TOC entry 5222 (class 1259 OID 17677)
-- Name: usuario_logacesso_usuario_id_f8ad5375; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX usuario_logacesso_usuario_id_f8ad5375 ON public.usuario_logacesso USING btree (usuario_id);


--
-- TOC entry 5225 (class 1259 OID 17683)
-- Name: usuario_logauditoria_usuario_id_596cd4d4; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX usuario_logauditoria_usuario_id_596cd4d4 ON public.usuario_logauditoria USING btree (usuario_id);


--
-- TOC entry 5217 (class 1259 OID 17671)
-- Name: usuario_perfilaluno_rgm_baddd0ea_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX usuario_perfilaluno_rgm_baddd0ea_like ON public.usuario_perfilaluno USING btree (rgm varchar_pattern_ops);


--
-- TOC entry 5203 (class 1259 OID 17651)
-- Name: usuario_usuario_groups_group_id_b9c090f8; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX usuario_usuario_groups_group_id_b9c090f8 ON public.usuario_usuario_groups USING btree (group_id);


--
-- TOC entry 5206 (class 1259 OID 17650)
-- Name: usuario_usuario_groups_usuario_id_62de76a1; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX usuario_usuario_groups_usuario_id_62de76a1 ON public.usuario_usuario_groups USING btree (usuario_id);


--
-- TOC entry 5211 (class 1259 OID 17665)
-- Name: usuario_usuario_user_permissions_permission_id_5cad0a4b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX usuario_usuario_user_permissions_permission_id_5cad0a4b ON public.usuario_usuario_user_permissions USING btree (permission_id);


--
-- TOC entry 5214 (class 1259 OID 17664)
-- Name: usuario_usuario_user_permissions_usuario_id_5969a193; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX usuario_usuario_user_permissions_usuario_id_5969a193 ON public.usuario_usuario_user_permissions USING btree (usuario_id);


--
-- TOC entry 5200 (class 1259 OID 17637)
-- Name: usuario_usuario_username_9e5f6fb3_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX usuario_usuario_username_9e5f6fb3_like ON public.usuario_usuario USING btree (username varchar_pattern_ops);


--
-- TOC entry 5319 (class 2606 OID 17123)
-- Name: agendamentos agendamentos_aluno_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.agendamentos
    ADD CONSTRAINT agendamentos_aluno_id_fkey FOREIGN KEY (aluno_id) REFERENCES public.usuarios(usuario_id);


--
-- TOC entry 5320 (class 2606 OID 17108)
-- Name: agendamentos agendamentos_clinica_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.agendamentos
    ADD CONSTRAINT agendamentos_clinica_id_fkey FOREIGN KEY (clinica_id) REFERENCES public.clinicas(clinica_id);


--
-- TOC entry 5321 (class 2606 OID 17128)
-- Name: agendamentos agendamentos_coordenador_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.agendamentos
    ADD CONSTRAINT agendamentos_coordenador_id_fkey FOREIGN KEY (coordenador_id) REFERENCES public.usuarios(usuario_id);


--
-- TOC entry 5322 (class 2606 OID 17118)
-- Name: agendamentos agendamentos_horario_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.agendamentos
    ADD CONSTRAINT agendamentos_horario_id_fkey FOREIGN KEY (horario_id) REFERENCES public.horarios(horario_id);


--
-- TOC entry 5323 (class 2606 OID 17113)
-- Name: agendamentos agendamentos_paciente_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.agendamentos
    ADD CONSTRAINT agendamentos_paciente_id_fkey FOREIGN KEY (paciente_id) REFERENCES public.pacientes(paciente_id);


--
-- TOC entry 5324 (class 2606 OID 17133)
-- Name: agendamentos agendamentos_status_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.agendamentos
    ADD CONSTRAINT agendamentos_status_id_fkey FOREIGN KEY (status_id) REFERENCES public.status_agendamento(status_id);


--
-- TOC entry 5350 (class 2606 OID 17477)
-- Name: ajustes_estoque ajustes_estoque_ajustado_por_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ajustes_estoque
    ADD CONSTRAINT ajustes_estoque_ajustado_por_fkey FOREIGN KEY (ajustado_por) REFERENCES public.usuarios(usuario_id);


--
-- TOC entry 5351 (class 2606 OID 17472)
-- Name: ajustes_estoque ajustes_estoque_localizacao_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ajustes_estoque
    ADD CONSTRAINT ajustes_estoque_localizacao_id_fkey FOREIGN KEY (localizacao_id) REFERENCES public.localizacoes_estoque(localizacao_id) ON DELETE CASCADE;


--
-- TOC entry 5352 (class 2606 OID 17467)
-- Name: ajustes_estoque ajustes_estoque_lote_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ajustes_estoque
    ADD CONSTRAINT ajustes_estoque_lote_id_fkey FOREIGN KEY (lote_id) REFERENCES public.lotes_produtos(lote_id) ON DELETE CASCADE;


--
-- TOC entry 5353 (class 2606 OID 17462)
-- Name: ajustes_estoque ajustes_estoque_produto_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.ajustes_estoque
    ADD CONSTRAINT ajustes_estoque_produto_id_fkey FOREIGN KEY (produto_id) REFERENCES public.produtos(produto_id) ON DELETE CASCADE;


--
-- TOC entry 5330 (class 2606 OID 17191)
-- Name: anexos_prontuario anexos_prontuario_prontuario_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.anexos_prontuario
    ADD CONSTRAINT anexos_prontuario_prontuario_id_fkey FOREIGN KEY (prontuario_id) REFERENCES public.prontuarios_eletronicos(prontuario_id) ON DELETE CASCADE;


--
-- TOC entry 5355 (class 2606 OID 17581)
-- Name: auth_group_permissions auth_group_permissio_permission_id_84c5c92e_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5356 (class 2606 OID 17576)
-- Name: auth_group_permissions auth_group_permissions_group_id_b120cbf9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5354 (class 2606 OID 17567)
-- Name: auth_permission auth_permission_content_type_id_2f476e4b_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5316 (class 2606 OID 17067)
-- Name: consentimentos_pacientes consentimentos_pacientes_paciente_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.consentimentos_pacientes
    ADD CONSTRAINT consentimentos_pacientes_paciente_id_fkey FOREIGN KEY (paciente_id) REFERENCES public.pacientes(paciente_id) ON DELETE CASCADE;


--
-- TOC entry 5364 (class 2606 OID 17693)
-- Name: django_admin_log django_admin_log_content_type_id_c4bce8eb_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5365 (class 2606 OID 17698)
-- Name: django_admin_log django_admin_log_user_id_c564eba6_fk_usuario_usuario_usuario_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_usuario_usuario_usuario_id FOREIGN KEY (user_id) REFERENCES public.usuario_usuario(usuario_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5314 (class 2606 OID 17046)
-- Name: documentos_pacientes documentos_pacientes_paciente_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.documentos_pacientes
    ADD CONSTRAINT documentos_pacientes_paciente_id_fkey FOREIGN KEY (paciente_id) REFERENCES public.pacientes(paciente_id) ON DELETE CASCADE;


--
-- TOC entry 5315 (class 2606 OID 17051)
-- Name: documentos_pacientes documentos_pacientes_tipo_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.documentos_pacientes
    ADD CONSTRAINT documentos_pacientes_tipo_id_fkey FOREIGN KEY (tipo_id) REFERENCES public.tipos_documentos(tipo_id);


--
-- TOC entry 5366 (class 2606 OID 17774)
-- Name: estoque_ajusteestoque estoque_ajusteestoqu_ajustado_por_id_58af1482_fk_usuario_u; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.estoque_ajusteestoque
    ADD CONSTRAINT estoque_ajusteestoqu_ajustado_por_id_58af1482_fk_usuario_u FOREIGN KEY (ajustado_por_id) REFERENCES public.usuario_usuario(usuario_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5367 (class 2606 OID 17779)
-- Name: estoque_ajusteestoque estoque_ajusteestoqu_localizacao_id_138969a3_fk_estoque_l; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.estoque_ajusteestoque
    ADD CONSTRAINT estoque_ajusteestoqu_localizacao_id_138969a3_fk_estoque_l FOREIGN KEY (localizacao_id) REFERENCES public.estoque_localizacaoestoque(localizacao_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5368 (class 2606 OID 17794)
-- Name: estoque_ajusteestoque estoque_ajusteestoqu_lote_id_1aba4968_fk_estoque_l; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.estoque_ajusteestoque
    ADD CONSTRAINT estoque_ajusteestoqu_lote_id_1aba4968_fk_estoque_l FOREIGN KEY (lote_id) REFERENCES public.estoque_loteproduto(lote_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5369 (class 2606 OID 17844)
-- Name: estoque_ajusteestoque estoque_ajusteestoqu_produto_id_6575b57b_fk_estoque_p; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.estoque_ajusteestoque
    ADD CONSTRAINT estoque_ajusteestoqu_produto_id_6575b57b_fk_estoque_p FOREIGN KEY (produto_id) REFERENCES public.estoque_produto(produto_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5370 (class 2606 OID 17824)
-- Name: estoque_itempedidocompra estoque_itempedidoco_pedido_id_a1a80db1_fk_estoque_p; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.estoque_itempedidocompra
    ADD CONSTRAINT estoque_itempedidoco_pedido_id_a1a80db1_fk_estoque_p FOREIGN KEY (pedido_id) REFERENCES public.estoque_pedidocompra(pedido_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5371 (class 2606 OID 17839)
-- Name: estoque_itempedidocompra estoque_itempedidoco_produto_id_6d113627_fk_estoque_p; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.estoque_itempedidocompra
    ADD CONSTRAINT estoque_itempedidoco_produto_id_6d113627_fk_estoque_p FOREIGN KEY (produto_id) REFERENCES public.estoque_produto(produto_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5372 (class 2606 OID 17784)
-- Name: estoque_loteproduto estoque_loteproduto_fornecedor_id_baadf52b_fk_estoque_f; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.estoque_loteproduto
    ADD CONSTRAINT estoque_loteproduto_fornecedor_id_baadf52b_fk_estoque_f FOREIGN KEY (fornecedor_id) REFERENCES public.estoque_fornecedor(fornecedor_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5373 (class 2606 OID 17789)
-- Name: estoque_loteproduto estoque_loteproduto_localizacao_id_f1ddb136_fk_estoque_l; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.estoque_loteproduto
    ADD CONSTRAINT estoque_loteproduto_localizacao_id_f1ddb136_fk_estoque_l FOREIGN KEY (localizacao_id) REFERENCES public.estoque_localizacaoestoque(localizacao_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5374 (class 2606 OID 17834)
-- Name: estoque_loteproduto estoque_loteproduto_produto_id_85d0ece0_fk_estoque_p; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.estoque_loteproduto
    ADD CONSTRAINT estoque_loteproduto_produto_id_85d0ece0_fk_estoque_p FOREIGN KEY (produto_id) REFERENCES public.estoque_produto(produto_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5375 (class 2606 OID 17799)
-- Name: estoque_movimentoestoque estoque_movimentoest_localizacao_id_d42bebfe_fk_estoque_l; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.estoque_movimentoestoque
    ADD CONSTRAINT estoque_movimentoest_localizacao_id_d42bebfe_fk_estoque_l FOREIGN KEY (localizacao_id) REFERENCES public.estoque_localizacaoestoque(localizacao_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5376 (class 2606 OID 17804)
-- Name: estoque_movimentoestoque estoque_movimentoest_lote_id_f8a0b051_fk_estoque_l; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.estoque_movimentoestoque
    ADD CONSTRAINT estoque_movimentoest_lote_id_f8a0b051_fk_estoque_l FOREIGN KEY (lote_id) REFERENCES public.estoque_loteproduto(lote_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5377 (class 2606 OID 17809)
-- Name: estoque_movimentoestoque estoque_movimentoest_movimentado_por_id_1a9aa827_fk_usuario_u; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.estoque_movimentoestoque
    ADD CONSTRAINT estoque_movimentoest_movimentado_por_id_1a9aa827_fk_usuario_u FOREIGN KEY (movimentado_por_id) REFERENCES public.usuario_usuario(usuario_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5378 (class 2606 OID 17829)
-- Name: estoque_movimentoestoque estoque_movimentoest_produto_id_accf41ff_fk_estoque_p; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.estoque_movimentoestoque
    ADD CONSTRAINT estoque_movimentoest_produto_id_accf41ff_fk_estoque_p FOREIGN KEY (produto_id) REFERENCES public.estoque_produto(produto_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5379 (class 2606 OID 17814)
-- Name: estoque_pedidocompra estoque_pedidocompra_criado_por_id_458886a6_fk_usuario_u; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.estoque_pedidocompra
    ADD CONSTRAINT estoque_pedidocompra_criado_por_id_458886a6_fk_usuario_u FOREIGN KEY (criado_por_id) REFERENCES public.usuario_usuario(usuario_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5380 (class 2606 OID 17819)
-- Name: estoque_pedidocompra estoque_pedidocompra_fornecedor_id_6a13935d_fk_estoque_f; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.estoque_pedidocompra
    ADD CONSTRAINT estoque_pedidocompra_fornecedor_id_6a13935d_fk_estoque_f FOREIGN KEY (fornecedor_id) REFERENCES public.estoque_fornecedor(fornecedor_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5333 (class 2606 OID 17225)
-- Name: fila_espera fila_espera_clinica_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fila_espera
    ADD CONSTRAINT fila_espera_clinica_id_fkey FOREIGN KEY (clinica_id) REFERENCES public.clinicas(clinica_id);


--
-- TOC entry 5334 (class 2606 OID 17230)
-- Name: fila_espera fila_espera_paciente_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fila_espera
    ADD CONSTRAINT fila_espera_paciente_id_fkey FOREIGN KEY (paciente_id) REFERENCES public.pacientes(paciente_id);


--
-- TOC entry 5317 (class 2606 OID 17084)
-- Name: horarios horarios_sala_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.horarios
    ADD CONSTRAINT horarios_sala_id_fkey FOREIGN KEY (sala_id) REFERENCES public.salas(sala_id);


--
-- TOC entry 5318 (class 2606 OID 17079)
-- Name: horarios horarios_servico_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.horarios
    ADD CONSTRAINT horarios_servico_id_fkey FOREIGN KEY (servico_id) REFERENCES public.servicos(servico_id);


--
-- TOC entry 5348 (class 2606 OID 17428)
-- Name: itens_pedido_compra itens_pedido_compra_pedido_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.itens_pedido_compra
    ADD CONSTRAINT itens_pedido_compra_pedido_id_fkey FOREIGN KEY (pedido_id) REFERENCES public.pedidos_compra(pedido_id) ON DELETE CASCADE;


--
-- TOC entry 5349 (class 2606 OID 17433)
-- Name: itens_pedido_compra itens_pedido_compra_produto_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.itens_pedido_compra
    ADD CONSTRAINT itens_pedido_compra_produto_id_fkey FOREIGN KEY (produto_id) REFERENCES public.produtos(produto_id) ON DELETE CASCADE;


--
-- TOC entry 5342 (class 2606 OID 17352)
-- Name: localizacoes_estoque localizacoes_estoque_clinica_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.localizacoes_estoque
    ADD CONSTRAINT localizacoes_estoque_clinica_id_fkey FOREIGN KEY (clinica_id) REFERENCES public.clinicas(clinica_id) ON DELETE CASCADE;


--
-- TOC entry 5336 (class 2606 OID 17260)
-- Name: logs_acesso logs_acesso_usuario_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.logs_acesso
    ADD CONSTRAINT logs_acesso_usuario_id_fkey FOREIGN KEY (usuario_id) REFERENCES public.usuarios(usuario_id);


--
-- TOC entry 5335 (class 2606 OID 17245)
-- Name: logs_auditoria logs_auditoria_usuario_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.logs_auditoria
    ADD CONSTRAINT logs_auditoria_usuario_id_fkey FOREIGN KEY (usuario_id) REFERENCES public.usuarios(usuario_id);


--
-- TOC entry 5343 (class 2606 OID 17375)
-- Name: lotes_produtos lotes_produtos_fornecedor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.lotes_produtos
    ADD CONSTRAINT lotes_produtos_fornecedor_id_fkey FOREIGN KEY (fornecedor_id) REFERENCES public.fornecedores(fornecedor_id);


--
-- TOC entry 5344 (class 2606 OID 17380)
-- Name: lotes_produtos lotes_produtos_localizacao_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.lotes_produtos
    ADD CONSTRAINT lotes_produtos_localizacao_id_fkey FOREIGN KEY (localizacao_id) REFERENCES public.localizacoes_estoque(localizacao_id);


--
-- TOC entry 5345 (class 2606 OID 17370)
-- Name: lotes_produtos lotes_produtos_produto_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.lotes_produtos
    ADD CONSTRAINT lotes_produtos_produto_id_fkey FOREIGN KEY (produto_id) REFERENCES public.produtos(produto_id) ON DELETE CASCADE;


--
-- TOC entry 5338 (class 2606 OID 17487)
-- Name: movimentos_estoque movimentos_estoque_localizacao_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.movimentos_estoque
    ADD CONSTRAINT movimentos_estoque_localizacao_id_fkey FOREIGN KEY (localizacao_id) REFERENCES public.localizacoes_estoque(localizacao_id) ON DELETE CASCADE;


--
-- TOC entry 5339 (class 2606 OID 17482)
-- Name: movimentos_estoque movimentos_estoque_lote_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.movimentos_estoque
    ADD CONSTRAINT movimentos_estoque_lote_id_fkey FOREIGN KEY (lote_id) REFERENCES public.lotes_produtos(lote_id) ON DELETE CASCADE;


--
-- TOC entry 5340 (class 2606 OID 17305)
-- Name: movimentos_estoque movimentos_estoque_movimentado_por_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.movimentos_estoque
    ADD CONSTRAINT movimentos_estoque_movimentado_por_fkey FOREIGN KEY (movimentado_por) REFERENCES public.usuarios(usuario_id);


--
-- TOC entry 5341 (class 2606 OID 17300)
-- Name: movimentos_estoque movimentos_estoque_produto_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.movimentos_estoque
    ADD CONSTRAINT movimentos_estoque_produto_id_fkey FOREIGN KEY (produto_id) REFERENCES public.produtos(produto_id);


--
-- TOC entry 5337 (class 2606 OID 17275)
-- Name: notificacoes notificacoes_agendamento_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.notificacoes
    ADD CONSTRAINT notificacoes_agendamento_id_fkey FOREIGN KEY (agendamento_id) REFERENCES public.agendamentos(agendamento_id);


--
-- TOC entry 5381 (class 2606 OID 17910)
-- Name: paciente_consentimentopaciente paciente_consentimen_paciente_id_a8a88a87_fk_paciente_; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.paciente_consentimentopaciente
    ADD CONSTRAINT paciente_consentimen_paciente_id_a8a88a87_fk_paciente_ FOREIGN KEY (paciente_id) REFERENCES public.paciente_paciente(paciente_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5383 (class 2606 OID 17922)
-- Name: paciente_documentopaciente paciente_documentopa_paciente_id_0424bcaa_fk_paciente_; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.paciente_documentopaciente
    ADD CONSTRAINT paciente_documentopa_paciente_id_0424bcaa_fk_paciente_ FOREIGN KEY (paciente_id) REFERENCES public.paciente_paciente(paciente_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5384 (class 2606 OID 17927)
-- Name: paciente_documentopaciente paciente_documentopa_tipo_documento_id_910bc502_fk_paciente_; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.paciente_documentopaciente
    ADD CONSTRAINT paciente_documentopa_tipo_documento_id_910bc502_fk_paciente_ FOREIGN KEY (tipo_documento_id) REFERENCES public.paciente_tipodocumento(tipo_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5382 (class 2606 OID 17916)
-- Name: paciente_responsavellegal paciente_responsavel_paciente_id_ea2ec3d0_fk_paciente_; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.paciente_responsavellegal
    ADD CONSTRAINT paciente_responsavel_paciente_id_ea2ec3d0_fk_paciente_ FOREIGN KEY (paciente_id) REFERENCES public.paciente_paciente(paciente_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5346 (class 2606 OID 17414)
-- Name: pedidos_compra pedidos_compra_criado_por_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pedidos_compra
    ADD CONSTRAINT pedidos_compra_criado_por_fkey FOREIGN KEY (criado_por) REFERENCES public.usuarios(usuario_id);


--
-- TOC entry 5347 (class 2606 OID 17409)
-- Name: pedidos_compra pedidos_compra_fornecedor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pedidos_compra
    ADD CONSTRAINT pedidos_compra_fornecedor_id_fkey FOREIGN KEY (fornecedor_id) REFERENCES public.fornecedores(fornecedor_id) ON DELETE CASCADE;


--
-- TOC entry 5307 (class 2606 OID 16922)
-- Name: perfil_permissoes perfil_permissoes_perfil_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.perfil_permissoes
    ADD CONSTRAINT perfil_permissoes_perfil_id_fkey FOREIGN KEY (perfil_id) REFERENCES public.perfis(perfil_id) ON DELETE CASCADE;


--
-- TOC entry 5308 (class 2606 OID 16927)
-- Name: perfil_permissoes perfil_permissoes_permissao_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.perfil_permissoes
    ADD CONSTRAINT perfil_permissoes_permissao_id_fkey FOREIGN KEY (permissao_id) REFERENCES public.permissoes(permissao_id) ON DELETE CASCADE;


--
-- TOC entry 5310 (class 2606 OID 16958)
-- Name: perfis_alunos perfis_alunos_usuario_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.perfis_alunos
    ADD CONSTRAINT perfis_alunos_usuario_id_fkey FOREIGN KEY (usuario_id) REFERENCES public.usuarios(usuario_id) ON DELETE CASCADE;


--
-- TOC entry 5325 (class 2606 OID 17148)
-- Name: prontuarios_eletronicos prontuarios_eletronicos_agendamento_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.prontuarios_eletronicos
    ADD CONSTRAINT prontuarios_eletronicos_agendamento_id_fkey FOREIGN KEY (agendamento_id) REFERENCES public.agendamentos(agendamento_id) ON DELETE CASCADE;


--
-- TOC entry 5326 (class 2606 OID 17158)
-- Name: prontuarios_eletronicos prontuarios_eletronicos_aluno_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.prontuarios_eletronicos
    ADD CONSTRAINT prontuarios_eletronicos_aluno_id_fkey FOREIGN KEY (aluno_id) REFERENCES public.usuarios(usuario_id);


--
-- TOC entry 5327 (class 2606 OID 17153)
-- Name: prontuarios_eletronicos prontuarios_eletronicos_clinica_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.prontuarios_eletronicos
    ADD CONSTRAINT prontuarios_eletronicos_clinica_id_fkey FOREIGN KEY (clinica_id) REFERENCES public.clinicas(clinica_id);


--
-- TOC entry 5328 (class 2606 OID 17163)
-- Name: prontuarios_eletronicos prontuarios_eletronicos_coordenador_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.prontuarios_eletronicos
    ADD CONSTRAINT prontuarios_eletronicos_coordenador_id_fkey FOREIGN KEY (coordenador_id) REFERENCES public.usuarios(usuario_id);


--
-- TOC entry 5329 (class 2606 OID 17177)
-- Name: prontuarios_eletronicos_versoes prontuarios_eletronicos_versoes_prontuario_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.prontuarios_eletronicos_versoes
    ADD CONSTRAINT prontuarios_eletronicos_versoes_prontuario_id_fkey FOREIGN KEY (prontuario_id) REFERENCES public.prontuarios_eletronicos(prontuario_id) ON DELETE CASCADE;


--
-- TOC entry 5331 (class 2606 OID 17210)
-- Name: registros_presenca registros_presenca_agendamento_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.registros_presenca
    ADD CONSTRAINT registros_presenca_agendamento_id_fkey FOREIGN KEY (agendamento_id) REFERENCES public.agendamentos(agendamento_id);


--
-- TOC entry 5332 (class 2606 OID 17205)
-- Name: registros_presenca registros_presenca_aluno_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.registros_presenca
    ADD CONSTRAINT registros_presenca_aluno_id_fkey FOREIGN KEY (aluno_id) REFERENCES public.usuarios(usuario_id);


--
-- TOC entry 5313 (class 2606 OID 17020)
-- Name: responsaveis_legais responsaveis_legais_paciente_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.responsaveis_legais
    ADD CONSTRAINT responsaveis_legais_paciente_id_fkey FOREIGN KEY (paciente_id) REFERENCES public.pacientes(paciente_id) ON DELETE CASCADE;


--
-- TOC entry 5312 (class 2606 OID 16996)
-- Name: salas salas_clinica_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.salas
    ADD CONSTRAINT salas_clinica_id_fkey FOREIGN KEY (clinica_id) REFERENCES public.clinicas(clinica_id);


--
-- TOC entry 5311 (class 2606 OID 16983)
-- Name: servicos servicos_clinica_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.servicos
    ADD CONSTRAINT servicos_clinica_id_fkey FOREIGN KEY (clinica_id) REFERENCES public.clinicas(clinica_id) ON DELETE CASCADE;


--
-- TOC entry 5362 (class 2606 OID 17672)
-- Name: usuario_logacesso usuario_logacesso_usuario_id_f8ad5375_fk_usuario_u; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuario_logacesso
    ADD CONSTRAINT usuario_logacesso_usuario_id_f8ad5375_fk_usuario_u FOREIGN KEY (usuario_id) REFERENCES public.usuario_usuario(usuario_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5363 (class 2606 OID 17678)
-- Name: usuario_logauditoria usuario_logauditoria_usuario_id_596cd4d4_fk_usuario_u; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuario_logauditoria
    ADD CONSTRAINT usuario_logauditoria_usuario_id_596cd4d4_fk_usuario_u FOREIGN KEY (usuario_id) REFERENCES public.usuario_usuario(usuario_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5361 (class 2606 OID 17666)
-- Name: usuario_perfilaluno usuario_perfilaluno_usuario_id_98901a9e_fk_usuario_u; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuario_perfilaluno
    ADD CONSTRAINT usuario_perfilaluno_usuario_id_98901a9e_fk_usuario_u FOREIGN KEY (usuario_id) REFERENCES public.usuario_usuario(usuario_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5357 (class 2606 OID 17640)
-- Name: usuario_usuario_groups usuario_usuario_grou_usuario_id_62de76a1_fk_usuario_u; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuario_usuario_groups
    ADD CONSTRAINT usuario_usuario_grou_usuario_id_62de76a1_fk_usuario_u FOREIGN KEY (usuario_id) REFERENCES public.usuario_usuario(usuario_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5358 (class 2606 OID 17645)
-- Name: usuario_usuario_groups usuario_usuario_groups_group_id_b9c090f8_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuario_usuario_groups
    ADD CONSTRAINT usuario_usuario_groups_group_id_b9c090f8_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5359 (class 2606 OID 17659)
-- Name: usuario_usuario_user_permissions usuario_usuario_user_permission_id_5cad0a4b_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuario_usuario_user_permissions
    ADD CONSTRAINT usuario_usuario_user_permission_id_5cad0a4b_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5360 (class 2606 OID 17654)
-- Name: usuario_usuario_user_permissions usuario_usuario_user_usuario_id_5969a193_fk_usuario_u; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuario_usuario_user_permissions
    ADD CONSTRAINT usuario_usuario_user_usuario_id_5969a193_fk_usuario_u FOREIGN KEY (usuario_id) REFERENCES public.usuario_usuario(usuario_id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 5309 (class 2606 OID 16944)
-- Name: usuarios usuarios_perfil_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_perfil_id_fkey FOREIGN KEY (perfil_id) REFERENCES public.perfis(perfil_id);


-- Completed on 2025-07-14 17:33:59

--
-- PostgreSQL database dump complete
--

-- Completed on 2025-07-14 17:33:59

--
-- PostgreSQL database cluster dump complete
--

