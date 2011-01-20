--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = off;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET escape_string_warning = off;

--
-- Name: plpgsql; Type: PROCEDURAL LANGUAGE; Schema: -; Owner: postgres
--

CREATE OR REPLACE PROCEDURAL LANGUAGE plpgsql;


ALTER PROCEDURAL LANGUAGE plpgsql OWNER TO postgres;

SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE auth_group (
    id integer NOT NULL,
    name character varying(80) NOT NULL
);


ALTER TABLE public.auth_group OWNER TO postgres;

--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE auth_group_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_id_seq OWNER TO postgres;

--
-- Name: auth_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE auth_group_id_seq OWNED BY auth_group.id;


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('auth_group_id_seq', 12, true);


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE auth_group_permissions (
    id integer NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_group_permissions OWNER TO postgres;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE auth_group_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_permissions_id_seq OWNER TO postgres;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE auth_group_permissions_id_seq OWNED BY auth_group_permissions.id;


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('auth_group_permissions_id_seq', 183, true);


--
-- Name: auth_message; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE auth_message (
    id integer NOT NULL,
    user_id integer NOT NULL,
    message text NOT NULL
);


ALTER TABLE public.auth_message OWNER TO postgres;

--
-- Name: auth_message_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE auth_message_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_message_id_seq OWNER TO postgres;

--
-- Name: auth_message_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE auth_message_id_seq OWNED BY auth_message.id;


--
-- Name: auth_message_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('auth_message_id_seq', 1, false);


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE auth_permission (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE public.auth_permission OWNER TO postgres;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE auth_permission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_permission_id_seq OWNER TO postgres;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE auth_permission_id_seq OWNED BY auth_permission.id;


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('auth_permission_id_seq', 117, true);


--
-- Name: auth_user; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE auth_user (
    id integer NOT NULL,
    username character varying(30) NOT NULL,
    first_name character varying(30) NOT NULL,
    last_name character varying(30) NOT NULL,
    email character varying(75) NOT NULL,
    password character varying(128) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    is_superuser boolean NOT NULL,
    last_login timestamp with time zone NOT NULL,
    date_joined timestamp with time zone NOT NULL
);


ALTER TABLE public.auth_user OWNER TO postgres;

--
-- Name: auth_user_groups; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE auth_user_groups (
    id integer NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public.auth_user_groups OWNER TO postgres;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE auth_user_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_groups_id_seq OWNER TO postgres;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE auth_user_groups_id_seq OWNED BY auth_user_groups.id;


--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('auth_user_groups_id_seq', 1, false);


--
-- Name: auth_user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE auth_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_id_seq OWNER TO postgres;

--
-- Name: auth_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE auth_user_id_seq OWNED BY auth_user.id;


--
-- Name: auth_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('auth_user_id_seq', 1, true);


--
-- Name: auth_user_user_permissions; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE auth_user_user_permissions (
    id integer NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_user_user_permissions OWNER TO postgres;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE auth_user_user_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_user_permissions_id_seq OWNER TO postgres;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE auth_user_user_permissions_id_seq OWNED BY auth_user_user_permissions.id;


--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('auth_user_user_permissions_id_seq', 1, false);


--
-- Name: common_burial; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE common_burial (
    order_ptr_id character varying(36) NOT NULL,
    person_id character varying(36) NOT NULL,
    account_book_n character varying(9) NOT NULL
);


ALTER TABLE public.common_burial OWNER TO postgres;

--
-- Name: common_burial1; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW common_burial1 AS
    SELECT common_burial.order_ptr_id, common_burial.person_id, common_burial.account_book_n, "substring"((common_burial.account_book_n)::text, '([^[:digit:]]*)[[:digit:]]*.*'::text) AS s1, to_number("substring"((common_burial.account_book_n)::text, '[^[:digit:]]*([[:digit:]]*).*'::text), '9999999999'::text) AS s2, "substring"((common_burial.account_book_n)::text, '[^[:digit:]]*[[:digit:]]*(.*)'::text) AS s3 FROM common_burial;


ALTER TABLE public.common_burial1 OWNER TO postgres;

--
-- Name: common_cemetery; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE common_cemetery (
    uuid character varying(36) NOT NULL,
    organization_id character varying(36) NOT NULL,
    location_id character varying(36),
    name character varying(99) NOT NULL,
    creator_id integer NOT NULL,
    date_of_creation timestamp with time zone NOT NULL
);


ALTER TABLE public.common_cemetery OWNER TO postgres;

--
-- Name: common_deathcertificate; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE common_deathcertificate (
    uuid character varying(36) NOT NULL,
    soul_id character varying(36) NOT NULL,
    s_number character varying(30) NOT NULL
);


ALTER TABLE public.common_deathcertificate OWNER TO postgres;

--
-- Name: common_email; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE common_email (
    uuid character varying(36) NOT NULL,
    soul_id character varying(36) NOT NULL,
    e_addr character varying(75) NOT NULL
);


ALTER TABLE public.common_email OWNER TO postgres;

--
-- Name: common_geocity; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE common_geocity (
    uuid character varying(36) NOT NULL,
    country_id character varying(36) NOT NULL,
    region_id character varying(36) NOT NULL,
    name character varying(36) NOT NULL
);


ALTER TABLE public.common_geocity OWNER TO postgres;

--
-- Name: common_geocountry; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE common_geocountry (
    uuid character varying(36) NOT NULL,
    name character varying(24) NOT NULL
);


ALTER TABLE public.common_geocountry OWNER TO postgres;

--
-- Name: common_georegion; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE common_georegion (
    uuid character varying(36) NOT NULL,
    country_id character varying(36) NOT NULL,
    name character varying(36) NOT NULL
);


ALTER TABLE public.common_georegion OWNER TO postgres;

--
-- Name: common_location; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE common_location (
    uuid character varying(36) NOT NULL,
    street_id character varying(36),
    house character varying(16) NOT NULL,
    block character varying(16) NOT NULL,
    building character varying(16) NOT NULL,
    flat character varying(16) NOT NULL,
    gps_x double precision,
    gps_y double precision,
    gps_z double precision
);


ALTER TABLE public.common_location OWNER TO postgres;

--
-- Name: common_metro; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE common_metro (
    uuid character varying(36) NOT NULL,
    city_id character varying(36) NOT NULL,
    name character varying(99) NOT NULL
);


ALTER TABLE public.common_metro OWNER TO postgres;

--
-- Name: common_operation; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE common_operation (
    id integer NOT NULL,
    op_type character varying(100) NOT NULL
);


ALTER TABLE public.common_operation OWNER TO postgres;

--
-- Name: common_operation_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE common_operation_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.common_operation_id_seq OWNER TO postgres;

--
-- Name: common_operation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE common_operation_id_seq OWNED BY common_operation.id;


--
-- Name: common_operation_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('common_operation_id_seq', 4, true);


--
-- Name: common_order; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE common_order (
    uuid character varying(36) NOT NULL,
    responsible_id character varying(36) NOT NULL,
    customer_id character varying(36) NOT NULL,
    doer_id character varying(36),
    date_plan timestamp with time zone,
    date_fact timestamp with time zone,
    product_id character varying(36) NOT NULL,
    operation_id integer NOT NULL,
    is_trash boolean NOT NULL,
    creator_id integer NOT NULL,
    date_of_creation timestamp with time zone NOT NULL,
    all_comments text NOT NULL
);


ALTER TABLE public.common_order OWNER TO postgres;

--
-- Name: common_ordercomments; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE common_ordercomments (
    uuid character varying(36) NOT NULL,
    order_id character varying(36) NOT NULL,
    comment text NOT NULL,
    creator_id integer NOT NULL,
    date_of_creation timestamp with time zone NOT NULL
);


ALTER TABLE public.common_ordercomments OWNER TO postgres;

--
-- Name: common_orderfiles; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE common_orderfiles (
    uuid character varying(36) NOT NULL,
    order_id character varying(36) NOT NULL,
    ofile character varying(100) NOT NULL,
    comment character varying(96) NOT NULL,
    creator_id integer,
    date_of_creation timestamp with time zone NOT NULL
);


ALTER TABLE public.common_orderfiles OWNER TO postgres;

--
-- Name: common_organization; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE common_organization (
    soul_ptr_id character varying(36) NOT NULL,
    ogrn character varying(15) NOT NULL,
    inn character varying(15) NOT NULL,
    name character varying(99) NOT NULL
);


ALTER TABLE public.common_organization OWNER TO postgres;

--
-- Name: common_person; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE common_person (
    soul_ptr_id character varying(36) NOT NULL,
    first_name character varying(30) NOT NULL,
    last_name character varying(30) NOT NULL,
    patronymic character varying(30) NOT NULL
);


ALTER TABLE public.common_person OWNER TO postgres;

--
-- Name: common_personrole; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE common_personrole (
    id integer NOT NULL,
    person_id character varying(36) NOT NULL,
    role_id character varying(36) NOT NULL,
    hire_date date,
    discharge_date date,
    creator_id integer NOT NULL,
    date_of_creation timestamp with time zone NOT NULL
);


ALTER TABLE public.common_personrole OWNER TO postgres;

--
-- Name: common_personrole_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE common_personrole_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.common_personrole_id_seq OWNER TO postgres;

--
-- Name: common_personrole_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE common_personrole_id_seq OWNED BY common_personrole.id;


--
-- Name: common_personrole_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('common_personrole_id_seq', 1, false);


--
-- Name: common_phone; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE common_phone (
    uuid character varying(36) NOT NULL,
    soul_id character varying(36) NOT NULL,
    f_number character varying(15) NOT NULL
);


ALTER TABLE public.common_phone OWNER TO postgres;

--
-- Name: common_place; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE common_place (
    product_ptr_id character varying(36) NOT NULL,
    cemetery_id character varying(36) NOT NULL,
    area character varying(9) NOT NULL,
    "row" character varying(9) NOT NULL,
    seat character varying(9) NOT NULL,
    gps_x double precision,
    gps_y double precision,
    gps_z double precision,
    creator_id integer NOT NULL,
    date_of_creation timestamp with time zone NOT NULL
);


ALTER TABLE public.common_place OWNER TO postgres;

--
-- Name: common_place1; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW common_place1 AS
    SELECT common_place.product_ptr_id, common_place.cemetery_id, common_place.area, common_place."row", common_place.seat, common_place.gps_x, common_place.gps_y, common_place.gps_z, common_place.creator_id, common_place.date_of_creation, "substring"((common_place.area)::text, '([^[:digit:]]*)[[:digit:]]*.*'::text) AS s1, to_number("substring"((common_place.area)::text, '[^[:digit:]]*([[:digit:]]*).*'::text), '9999999999'::text) AS s2, "substring"((common_place.area)::text, '[^[:digit:]]*[[:digit:]]*(.*)'::text) AS s3, "substring"((common_place."row")::text, '([^[:digit:]]*)[[:digit:]]*.*'::text) AS s4, to_number("substring"((common_place."row")::text, '[^[:digit:]]*([[:digit:]]*).*'::text), '9999999999'::text) AS s5, "substring"((common_place."row")::text, '[^[:digit:]]*[[:digit:]]*(.*)'::text) AS s6, "substring"((common_place.seat)::text, '([^[:digit:]]*)[[:digit:]]*.*'::text) AS s7, to_number("substring"((common_place.seat)::text, '[^[:digit:]]*([[:digit:]]*).*'::text), '9999999999'::text) AS s8, "substring"((common_place.seat)::text, '[^[:digit:]]*[[:digit:]]*(.*)'::text) AS s9 FROM common_place;


ALTER TABLE public.common_place1 OWNER TO postgres;

--
-- Name: common_product; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE common_product (
    uuid character varying(36) NOT NULL,
    soul_id character varying(36) NOT NULL,
    name character varying(50) NOT NULL,
    measure character varying(50) NOT NULL,
    p_type_id integer NOT NULL,
    all_comments text NOT NULL
);


ALTER TABLE public.common_product OWNER TO postgres;

--
-- Name: common_productcomments; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE common_productcomments (
    uuid character varying(36) NOT NULL,
    product_id character varying(36) NOT NULL,
    comment text NOT NULL,
    creator_id integer NOT NULL,
    date_of_creation timestamp with time zone NOT NULL
);


ALTER TABLE public.common_productcomments OWNER TO postgres;

--
-- Name: common_productfiles; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE common_productfiles (
    uuid character varying(36) NOT NULL,
    product_id character varying(36) NOT NULL,
    pfile character varying(100) NOT NULL,
    creator_id integer,
    date_of_creation timestamp with time zone NOT NULL
);


ALTER TABLE public.common_productfiles OWNER TO postgres;

--
-- Name: common_producttype; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE common_producttype (
    id integer NOT NULL,
    name character varying(24) NOT NULL
);


ALTER TABLE public.common_producttype OWNER TO postgres;

--
-- Name: common_producttype_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE common_producttype_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.common_producttype_id_seq OWNER TO postgres;

--
-- Name: common_producttype_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE common_producttype_id_seq OWNED BY common_producttype.id;


--
-- Name: common_producttype_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('common_producttype_id_seq', 1, true);


--
-- Name: common_role; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE common_role (
    uuid character varying(36) NOT NULL,
    organization_id character varying(36) NOT NULL,
    name character varying(50) NOT NULL,
    creator_id integer NOT NULL,
    date_of_creation timestamp with time zone NOT NULL
);


ALTER TABLE public.common_role OWNER TO postgres;

--
-- Name: common_role_djgroups; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE common_role_djgroups (
    id integer NOT NULL,
    role_id character varying(36) NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public.common_role_djgroups OWNER TO postgres;

--
-- Name: common_role_djgroups_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE common_role_djgroups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.common_role_djgroups_id_seq OWNER TO postgres;

--
-- Name: common_role_djgroups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE common_role_djgroups_id_seq OWNED BY common_role_djgroups.id;


--
-- Name: common_role_djgroups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('common_role_djgroups_id_seq', 1, false);


--
-- Name: common_roletree; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE common_roletree (
    id integer NOT NULL,
    master_id character varying(36) NOT NULL,
    slave_id character varying(36) NOT NULL
);


ALTER TABLE public.common_roletree OWNER TO postgres;

--
-- Name: common_roletree_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE common_roletree_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.common_roletree_id_seq OWNER TO postgres;

--
-- Name: common_roletree_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE common_roletree_id_seq OWNED BY common_roletree.id;


--
-- Name: common_roletree_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('common_roletree_id_seq', 1, false);


--
-- Name: common_soul; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE common_soul (
    uuid character varying(36) NOT NULL,
    birth_date date,
    death_date date,
    location_id character varying(36),
    creator_id integer NOT NULL,
    date_of_creation timestamp with time zone NOT NULL
);


ALTER TABLE public.common_soul OWNER TO postgres;

--
-- Name: common_soulproducttypeoperation; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE common_soulproducttypeoperation (
    id integer NOT NULL,
    soul_id character varying(36) NOT NULL,
    p_type_id integer NOT NULL,
    operation_id integer NOT NULL
);


ALTER TABLE public.common_soulproducttypeoperation OWNER TO postgres;

--
-- Name: common_soulproducttypeoperation_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE common_soulproducttypeoperation_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.common_soulproducttypeoperation_id_seq OWNER TO postgres;

--
-- Name: common_soulproducttypeoperation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE common_soulproducttypeoperation_id_seq OWNED BY common_soulproducttypeoperation.id;


--
-- Name: common_soulproducttypeoperation_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('common_soulproducttypeoperation_id_seq', 1, false);


--
-- Name: common_street; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE common_street (
    uuid character varying(36) NOT NULL,
    city_id character varying(36) NOT NULL,
    name character varying(99) NOT NULL
);


ALTER TABLE public.common_street OWNER TO postgres;

--
-- Name: common_userprofile; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE common_userprofile (
    user_id integer NOT NULL,
    soul_id character varying(36) NOT NULL,
    default_cemetery_id character varying(36),
    default_operation_id integer,
    default_country_id character varying(36),
    default_region_id character varying(36),
    default_city_id character varying(36),
    records_per_page smallint,
    records_order_by character varying(50) NOT NULL,
    CONSTRAINT common_userprofile_records_per_page_check CHECK ((records_per_page >= 0))
);


ALTER TABLE public.common_userprofile OWNER TO postgres;

--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    user_id integer NOT NULL,
    content_type_id integer,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


ALTER TABLE public.django_admin_log OWNER TO postgres;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE django_admin_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_admin_log_id_seq OWNER TO postgres;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE django_admin_log_id_seq OWNED BY django_admin_log.id;


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('django_admin_log_id_seq', 27, true);


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE django_content_type (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE public.django_content_type OWNER TO postgres;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE django_content_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_content_type_id_seq OWNER TO postgres;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE django_content_type_id_seq OWNED BY django_content_type.id;


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('django_content_type_id_seq', 39, true);


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE public.django_session OWNER TO postgres;

--
-- Name: django_site; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE django_site (
    id integer NOT NULL,
    domain character varying(100) NOT NULL,
    name character varying(50) NOT NULL
);


ALTER TABLE public.django_site OWNER TO postgres;

--
-- Name: django_site_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE django_site_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_site_id_seq OWNER TO postgres;

--
-- Name: django_site_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE django_site_id_seq OWNED BY django_site.id;


--
-- Name: django_site_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('django_site_id_seq', 1, true);


--
-- Name: south_migrationhistory; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE south_migrationhistory (
    id integer NOT NULL,
    app_name character varying(255) NOT NULL,
    migration character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE public.south_migrationhistory OWNER TO postgres;

--
-- Name: south_migrationhistory_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE south_migrationhistory_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.south_migrationhistory_id_seq OWNER TO postgres;

--
-- Name: south_migrationhistory_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE south_migrationhistory_id_seq OWNED BY south_migrationhistory.id;


--
-- Name: south_migrationhistory_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('south_migrationhistory_id_seq', 1, false);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE auth_group ALTER COLUMN id SET DEFAULT nextval('auth_group_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('auth_group_permissions_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE auth_message ALTER COLUMN id SET DEFAULT nextval('auth_message_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE auth_permission ALTER COLUMN id SET DEFAULT nextval('auth_permission_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE auth_user ALTER COLUMN id SET DEFAULT nextval('auth_user_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE auth_user_groups ALTER COLUMN id SET DEFAULT nextval('auth_user_groups_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE auth_user_user_permissions ALTER COLUMN id SET DEFAULT nextval('auth_user_user_permissions_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE common_operation ALTER COLUMN id SET DEFAULT nextval('common_operation_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE common_personrole ALTER COLUMN id SET DEFAULT nextval('common_personrole_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE common_producttype ALTER COLUMN id SET DEFAULT nextval('common_producttype_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE common_role_djgroups ALTER COLUMN id SET DEFAULT nextval('common_role_djgroups_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE common_roletree ALTER COLUMN id SET DEFAULT nextval('common_roletree_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE common_soulproducttypeoperation ALTER COLUMN id SET DEFAULT nextval('common_soulproducttypeoperation_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE django_admin_log ALTER COLUMN id SET DEFAULT nextval('django_admin_log_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE django_content_type ALTER COLUMN id SET DEFAULT nextval('django_content_type_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE django_site ALTER COLUMN id SET DEFAULT nextval('django_site_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE south_migrationhistory ALTER COLUMN id SET DEFAULT nextval('south_migrationhistory_id_seq'::regclass);


--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY auth_group (id, name) FROM stdin;
1	management
2	journal
3	profile
4	management_cemetery
5	management_user
6	edit_burial
8	import_csv
10	management_edit_user
11	management_edit_cemetery
12	delete_orderfile
7	edit_bur_in_adm
9	adminka
\.


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY auth_group_permissions (id, group_id, permission_id) FROM stdin;
91	9	4
92	9	5
93	9	6
94	9	28
95	9	29
96	9	30
97	9	31
98	9	32
99	9	33
100	9	34
101	9	35
102	9	36
103	9	37
104	9	38
105	9	39
106	9	40
107	9	41
108	9	42
109	9	43
110	9	44
111	9	45
112	9	46
113	9	47
114	9	48
115	9	49
116	9	50
117	9	51
118	9	52
119	9	53
120	9	54
121	9	55
122	9	56
123	9	57
124	9	58
125	9	59
126	9	60
127	9	61
128	9	62
129	9	63
130	9	64
131	9	65
132	9	66
133	9	67
134	9	68
135	9	69
136	9	70
137	9	71
138	9	72
139	9	73
140	9	74
141	9	75
142	9	76
143	9	77
144	9	78
145	9	79
146	9	80
147	9	81
148	9	82
149	9	83
150	9	84
151	9	85
152	9	86
153	9	87
154	9	88
155	9	89
156	9	90
157	9	91
158	9	92
159	9	93
160	9	94
161	9	95
162	9	96
163	9	97
164	9	98
165	9	99
166	9	100
167	9	101
168	9	102
169	9	103
170	9	104
171	9	105
172	9	106
173	9	107
174	9	108
175	9	109
176	9	110
177	9	111
178	9	112
179	9	113
180	9	114
181	9	115
182	9	116
183	9	117
\.


--
-- Data for Name: auth_message; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY auth_message (id, user_id, message) FROM stdin;
\.


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add permission	1	add_permission
2	Can change permission	1	change_permission
3	Can delete permission	1	delete_permission
4	Can add group	2	add_group
5	Can change group	2	change_group
6	Can delete group	2	delete_group
7	Can add user	3	add_user
8	Can change user	3	change_user
9	Can delete user	3	delete_user
10	Can add message	4	add_message
11	Can change message	4	change_message
12	Can delete message	4	delete_message
13	Can add content type	5	add_contenttype
14	Can change content type	5	change_contenttype
15	Can delete content type	5	delete_contenttype
16	Can add session	6	add_session
17	Can change session	6	change_session
18	Can delete session	6	delete_session
19	Can add site	7	add_site
20	Can change site	7	change_site
21	Can delete site	7	delete_site
22	Can add log entry	8	add_logentry
23	Can change log entry	8	change_logentry
24	Can delete log entry	8	delete_logentry
25	Can add migration history	9	add_migrationhistory
26	Can change migration history	9	change_migrationhistory
27	Can delete migration history	9	delete_migrationhistory
28	Can add страна	10	add_geocountry
29	Can change страна	10	change_geocountry
30	Can delete страна	10	delete_geocountry
31	Can add регион	11	add_georegion
32	Can change регион	11	change_georegion
33	Can delete регион	11	delete_georegion
34	Can add населенный пункт	12	add_geocity
35	Can change населенный пункт	12	change_geocity
36	Can delete населенный пункт	12	delete_geocity
37	Can add metro	13	add_metro
38	Can change metro	13	change_metro
39	Can delete metro	13	delete_metro
40	Can add street	14	add_street
41	Can change street	14	change_street
42	Can delete street	14	delete_street
43	Can add location	15	add_location
44	Can change location	15	change_location
45	Can delete location	15	delete_location
46	Can add soul	16	add_soul
47	Can change soul	16	change_soul
48	Can delete soul	16	delete_soul
49	Can add phone	17	add_phone
50	Can change phone	17	change_phone
51	Can delete phone	17	delete_phone
52	Can add email	18	add_email
53	Can change email	18	change_email
54	Can delete email	18	delete_email
55	Can add физ. лицо	19	add_person
56	Can change физ. лицо	19	change_person
57	Can delete физ. лицо	19	delete_person
58	Can add свидетельство о смерти	20	add_deathcertificate
59	Can change свидетельство о смерти	20	change_deathcertificate
60	Can delete свидетельство о смерти	20	delete_deathcertificate
61	Can add юр. лицо	21	add_organization
62	Can change юр. лицо	21	change_organization
63	Can delete юр. лицо	21	delete_organization
64	Can add роль в организации	22	add_role
65	Can change роль в организации	22	change_role
66	Can delete роль в организации	22	delete_role
67	Can add role tree	23	add_roletree
68	Can change role tree	23	change_roletree
69	Can delete role tree	23	delete_roletree
70	Can add person role	24	add_personrole
71	Can change person role	24	change_personrole
72	Can delete person role	24	delete_personrole
73	Can add кладбище	25	add_cemetery
74	Can change кладбище	25	change_cemetery
75	Can delete кладбище	25	delete_cemetery
76	Can add тип продукта	26	add_producttype
77	Can change тип продукта	26	change_producttype
78	Can delete тип продукта	26	delete_producttype
79	Can add product	27	add_product
80	Can change product	27	change_product
81	Can delete product	27	delete_product
82	Can add product files	28	add_productfiles
83	Can change product files	28	change_productfiles
84	Can delete product files	28	delete_productfiles
85	Can add product comments	29	add_productcomments
86	Can change product comments	29	change_productcomments
87	Can delete product comments	29	delete_productcomments
88	Can add place	30	add_place
89	Can change place	30	change_place
90	Can delete place	30	delete_place
91	Can add place1	31	add_place1
92	Can change place1	31	change_place1
93	Can delete place1	31	delete_place1
94	Can add операция с продуктом	32	add_operation
95	Can change операция с продуктом	32	change_operation
96	Can delete операция с продуктом	32	delete_operation
97	Can add order	33	add_order
98	Can change order	33	change_order
99	Can delete order	33	delete_order
100	Can add order files	34	add_orderfiles
101	Can change order files	34	change_orderfiles
102	Can delete order files	34	delete_orderfiles
103	Can add order comments	35	add_ordercomments
104	Can change order comments	35	change_ordercomments
105	Can delete order comments	35	delete_ordercomments
106	Can add захоронение	36	add_burial
107	Can change захоронение	36	change_burial
108	Can delete захоронение	36	delete_burial
109	Can add burial1	37	add_burial1
110	Can change burial1	37	change_burial1
111	Can delete burial1	37	delete_burial1
112	Can add user profile	38	add_userprofile
113	Can change user profile	38	change_userprofile
114	Can delete user profile	38	delete_userprofile
115	Can add связь типа продукта с операцией	39	add_soulproducttypeoperation
116	Can change связь типа продукта с операцией	39	change_soulproducttypeoperation
117	Can delete связь типа продукта с операцией	39	delete_soulproducttypeoperation
\.


--
-- Data for Name: auth_user; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY auth_user (id, username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined) FROM stdin;
1	soul	Админ	Админов	pythonprogrammer@mail.ru	sha1$3dcf4$06f4af26cece81c8b657f1c5339fe1857007301a	t	t	t	2010-12-28 21:00:20.81031+03	2010-12-27 15:40:51+03
\.


--
-- Data for Name: auth_user_groups; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY auth_user_groups (id, user_id, group_id) FROM stdin;
\.


--
-- Data for Name: auth_user_user_permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY auth_user_user_permissions (id, user_id, permission_id) FROM stdin;
\.


--
-- Data for Name: common_burial; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY common_burial (order_ptr_id, person_id, account_book_n) FROM stdin;
\.


--
-- Data for Name: common_cemetery; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY common_cemetery (uuid, organization_id, location_id, name, creator_id, date_of_creation) FROM stdin;
\.


--
-- Data for Name: common_deathcertificate; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY common_deathcertificate (uuid, soul_id, s_number) FROM stdin;
\.


--
-- Data for Name: common_email; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY common_email (uuid, soul_id, e_addr) FROM stdin;
\.


--
-- Data for Name: common_geocity; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY common_geocity (uuid, country_id, region_id, name) FROM stdin;
b84399b0-11b7-11e0-9fee-485b39c96dfe	abae0096-11b7-11e0-9fee-485b39c96dfe	b2b61626-11b7-11e0-9fee-485b39c96dfe	НЕИЗВЕСТЕН
\.


--
-- Data for Name: common_geocountry; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY common_geocountry (uuid, name) FROM stdin;
abae0096-11b7-11e0-9fee-485b39c96dfe	НЕИЗВЕСТЕН
\.


--
-- Data for Name: common_georegion; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY common_georegion (uuid, country_id, name) FROM stdin;
b2b61626-11b7-11e0-9fee-485b39c96dfe	abae0096-11b7-11e0-9fee-485b39c96dfe	НЕИЗВЕСТЕН
\.


--
-- Data for Name: common_location; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY common_location (uuid, street_id, house, block, building, flat, gps_x, gps_y, gps_z) FROM stdin;
\.


--
-- Data for Name: common_metro; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY common_metro (uuid, city_id, name) FROM stdin;
\.


--
-- Data for Name: common_operation; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY common_operation (id, op_type) FROM stdin;
1	Захоронение
2	Захоронение в существующую могилу
3	Подзахоронение
4	Подзахоронение урны
\.


--
-- Data for Name: common_order; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY common_order (uuid, responsible_id, customer_id, doer_id, date_plan, date_fact, product_id, operation_id, is_trash, creator_id, date_of_creation, all_comments) FROM stdin;
\.


--
-- Data for Name: common_ordercomments; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY common_ordercomments (uuid, order_id, comment, creator_id, date_of_creation) FROM stdin;
\.


--
-- Data for Name: common_orderfiles; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY common_orderfiles (uuid, order_id, ofile, comment, creator_id, date_of_creation) FROM stdin;
\.


--
-- Data for Name: common_organization; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY common_organization (soul_ptr_id, ogrn, inn, name) FROM stdin;
\.


--
-- Data for Name: common_person; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY common_person (soul_ptr_id, first_name, last_name, patronymic) FROM stdin;
d0a7439a-11b6-11e0-9fee-485b39c96dfe	Админ	Админов	
\.


--
-- Data for Name: common_personrole; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY common_personrole (id, person_id, role_id, hire_date, discharge_date, creator_id, date_of_creation) FROM stdin;
\.


--
-- Data for Name: common_phone; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY common_phone (uuid, soul_id, f_number) FROM stdin;
\.


--
-- Data for Name: common_place; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY common_place (product_ptr_id, cemetery_id, area, "row", seat, gps_x, gps_y, gps_z, creator_id, date_of_creation) FROM stdin;
\.


--
-- Data for Name: common_product; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY common_product (uuid, soul_id, name, measure, p_type_id, all_comments) FROM stdin;
\.


--
-- Data for Name: common_productcomments; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY common_productcomments (uuid, product_id, comment, creator_id, date_of_creation) FROM stdin;
\.


--
-- Data for Name: common_productfiles; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY common_productfiles (uuid, product_id, pfile, creator_id, date_of_creation) FROM stdin;
\.


--
-- Data for Name: common_producttype; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY common_producttype (id, name) FROM stdin;
1	Место захоронения
\.


--
-- Data for Name: common_role; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY common_role (uuid, organization_id, name, creator_id, date_of_creation) FROM stdin;
\.


--
-- Data for Name: common_role_djgroups; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY common_role_djgroups (id, role_id, group_id) FROM stdin;
\.


--
-- Data for Name: common_roletree; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY common_roletree (id, master_id, slave_id) FROM stdin;
\.


--
-- Data for Name: common_soul; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY common_soul (uuid, birth_date, death_date, location_id, creator_id, date_of_creation) FROM stdin;
d0a7439a-11b6-11e0-9fee-485b39c96dfe	2010-12-27	\N	\N	1	2010-12-27 15:42:50.346172+03
\.


--
-- Data for Name: common_soulproducttypeoperation; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY common_soulproducttypeoperation (id, soul_id, p_type_id, operation_id) FROM stdin;
\.


--
-- Data for Name: common_street; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY common_street (uuid, city_id, name) FROM stdin;
\.


--
-- Data for Name: common_userprofile; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY common_userprofile (user_id, soul_id, default_cemetery_id, default_operation_id, default_country_id, default_region_id, default_city_id, records_per_page, records_order_by) FROM stdin;
1	d0a7439a-11b6-11e0-9fee-485b39c96dfe	\N	\N	\N	\N	\N	\N	
\.


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY django_admin_log (id, action_time, user_id, content_type_id, object_id, object_repr, action_flag, change_message) FROM stdin;
1	2010-12-27 15:42:50.354314+03	1	19	d0a7439a-11b6-11e0-9fee-485b39c96dfe	Админов А.	1	
2	2010-12-27 15:43:01.992777+03	1	38	1	soul	1	
3	2010-12-27 15:44:18.917976+03	1	3	1	soul	2	Изменен first_name и last_name.
4	2010-12-27 15:45:53.347775+03	1	2	1	management	1	
5	2010-12-27 15:45:59.2196+03	1	2	2	journal	1	
6	2010-12-27 15:46:04.281282+03	1	2	3	profile	1	
7	2010-12-27 15:46:08.646007+03	1	2	4	management_cemetery	1	
8	2010-12-27 15:46:12.887195+03	1	2	5	management_user	1	
9	2010-12-27 15:46:17.471195+03	1	2	6	edit_burial	1	
10	2010-12-27 15:46:22.449827+03	1	2	7	edtit_bur_in_adm	1	
11	2010-12-27 15:46:27.327846+03	1	2	8	import_csv	1	
12	2010-12-27 15:46:31.581014+03	1	2	9	adminka	1	
13	2010-12-27 15:46:47.599116+03	1	2	9	adminka	2	Изменен permissions.
14	2010-12-27 15:48:57.813088+03	1	10	abae0096-11b7-11e0-9fee-485b39c96dfe	НЕИЗВЕСТЕН	1	
15	2010-12-27 15:49:09.61124+03	1	11	b2b61626-11b7-11e0-9fee-485b39c96dfe	НЕИЗВЕСТЕН	1	
16	2010-12-27 15:49:18.927609+03	1	12	b84399b0-11b7-11e0-9fee-485b39c96dfe	НЕИЗВЕСТЕН	1	
17	2010-12-27 15:50:04.491709+03	1	32	1	Захоронение	1	
18	2010-12-27 15:50:17.618426+03	1	32	2	Захоронение в существующ	1	
19	2010-12-27 15:50:26.759143+03	1	32	3	Подзахоронение	1	
20	2010-12-27 15:50:36.457157+03	1	32	4	Подзахоронение урны	1	
21	2010-12-27 16:00:15.69967+03	1	26	1	Захоронение	1	
22	2010-12-27 16:12:33.056917+03	1	2	10	management_edit_user	1	
23	2010-12-27 16:12:51.071786+03	1	2	11	management_edit_cemetery	1	
24	2010-12-27 16:13:27.705733+03	1	2	12	delete_orderfile	1	
25	2010-12-27 16:14:14.789539+03	1	2	7	edit_bur_in_adm	2	Изменен name.
26	2010-12-27 16:23:31.138968+03	1	2	9	adminka	2	Изменен permissions.
27	2010-12-28 21:01:17.200782+03	1	26	1	Место захоронения	2	Изменен name.
\.


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY django_content_type (id, name, app_label, model) FROM stdin;
1	permission	auth	permission
2	group	auth	group
3	user	auth	user
4	message	auth	message
5	content type	contenttypes	contenttype
6	session	sessions	session
7	site	sites	site
8	log entry	admin	logentry
9	migration history	south	migrationhistory
10	страна	common	geocountry
11	регион	common	georegion
12	населенный пункт	common	geocity
13	metro	common	metro
14	street	common	street
15	location	common	location
16	soul	common	soul
17	phone	common	phone
18	email	common	email
19	физ. лицо	common	person
20	свидетельство о смерти	common	deathcertificate
21	юр. лицо	common	organization
22	роль в организации	common	role
23	role tree	common	roletree
24	person role	common	personrole
25	кладбище	common	cemetery
26	тип продукта	common	producttype
27	product	common	product
28	product files	common	productfiles
29	product comments	common	productcomments
30	place	common	place
31	place1	common	place1
32	операция с продуктом	common	operation
33	order	common	order
34	order files	common	orderfiles
35	order comments	common	ordercomments
36	захоронение	common	burial
37	burial1	common	burial1
38	user profile	common	userprofile
39	связь типа продукта с операцией	common	soulproducttypeoperation
\.


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY django_session (session_key, session_data, expire_date) FROM stdin;
e9c94437b986261241c2afd9f498780c	gAJ9cQEuMDZkMmE5Y2RhZTkxYjkwNjE2MzFjNTAyMTAwOTZiMjk=\n	2011-01-10 15:41:42.898455+03
6984c8fd2fb146df3241b306ee08d743	gAJ9cQEoVQp0ZXN0Y29va2llVQZ3b3JrZWRVEl9hdXRoX3VzZXJfYmFja2VuZHECVSlkamFuZ28u\nY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHEDVQ1fYXV0aF91c2VyX2lkcQRLAXUu\nZTE5YWE2ZDU4MGYzYzdjOTU2ZjJiOTc5ZGQ0MWMxMjk=\n	2011-01-10 15:54:46.69459+03
ebceb7463638a8d45153900dab25a6ab	gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEESwF1LjViYTdhMWYyYzY5ZmNjMTI0ZWYx\nNzc1NjNjNWRmMDUy\n	2011-01-10 16:11:33.698809+03
e6daaa2871aefb8740bbedeca64cdd44	gAJ9cQFVCnRlc3Rjb29raWVVBndvcmtlZHECcy5mMGYwYWQ2ZTJhZTk5NDdlYmY1ZGM5NjBhNGYz\nNTg1Yw==\n	2011-01-10 16:16:35.155981+03
b1271d21e619b5c8eeff619fe4f1ff4a	gAJ9cQEoVRJfYXV0aF91c2VyX2JhY2tlbmRxAlUpZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5k\ncy5Nb2RlbEJhY2tlbmRxA1UNX2F1dGhfdXNlcl9pZHEESwF1LjViYTdhMWYyYzY5ZmNjMTI0ZWYx\nNzc1NjNjNWRmMDUy\n	2011-01-11 21:00:20.830489+03
\.


--
-- Data for Name: django_site; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY django_site (id, domain, name) FROM stdin;
1	example.com	example.com
\.


--
-- Data for Name: south_migrationhistory; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY south_migrationhistory (id, app_name, migration, applied) FROM stdin;
\.


--
-- Name: auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions_group_id_permission_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_key UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_message_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY auth_message
    ADD CONSTRAINT auth_message_pkey PRIMARY KEY (id);


--
-- Name: auth_permission_content_type_id_codename_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_key UNIQUE (content_type_id, codename);


--
-- Name: auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups_user_id_group_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_group_id_key UNIQUE (user_id, group_id);


--
-- Name: auth_user_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions_user_id_permission_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_permission_id_key UNIQUE (user_id, permission_id);


--
-- Name: auth_user_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY auth_user
    ADD CONSTRAINT auth_user_username_key UNIQUE (username);


--
-- Name: common_burial_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY common_burial
    ADD CONSTRAINT common_burial_pkey PRIMARY KEY (order_ptr_id);


--
-- Name: common_cemetery_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY common_cemetery
    ADD CONSTRAINT common_cemetery_pkey PRIMARY KEY (uuid);


--
-- Name: common_deathcertificate_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY common_deathcertificate
    ADD CONSTRAINT common_deathcertificate_pkey PRIMARY KEY (uuid);


--
-- Name: common_deathcertificate_soul_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY common_deathcertificate
    ADD CONSTRAINT common_deathcertificate_soul_id_key UNIQUE (soul_id);


--
-- Name: common_email_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY common_email
    ADD CONSTRAINT common_email_pkey PRIMARY KEY (uuid);


--
-- Name: common_geocity_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY common_geocity
    ADD CONSTRAINT common_geocity_pkey PRIMARY KEY (uuid);


--
-- Name: common_geocity_region_id_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY common_geocity
    ADD CONSTRAINT common_geocity_region_id_name_key UNIQUE (region_id, name);


--
-- Name: common_geocountry_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY common_geocountry
    ADD CONSTRAINT common_geocountry_name_key UNIQUE (name);


--
-- Name: common_geocountry_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY common_geocountry
    ADD CONSTRAINT common_geocountry_pkey PRIMARY KEY (uuid);


--
-- Name: common_georegion_country_id_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY common_georegion
    ADD CONSTRAINT common_georegion_country_id_name_key UNIQUE (country_id, name);


--
-- Name: common_georegion_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY common_georegion
    ADD CONSTRAINT common_georegion_pkey PRIMARY KEY (uuid);


--
-- Name: common_location_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY common_location
    ADD CONSTRAINT common_location_pkey PRIMARY KEY (uuid);


--
-- Name: common_metro_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY common_metro
    ADD CONSTRAINT common_metro_pkey PRIMARY KEY (uuid);


--
-- Name: common_operation_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY common_operation
    ADD CONSTRAINT common_operation_pkey PRIMARY KEY (id);


--
-- Name: common_order_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY common_order
    ADD CONSTRAINT common_order_pkey PRIMARY KEY (uuid);


--
-- Name: common_ordercomments_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY common_ordercomments
    ADD CONSTRAINT common_ordercomments_pkey PRIMARY KEY (uuid);


--
-- Name: common_orderfiles_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY common_orderfiles
    ADD CONSTRAINT common_orderfiles_pkey PRIMARY KEY (uuid);


--
-- Name: common_organization_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY common_organization
    ADD CONSTRAINT common_organization_pkey PRIMARY KEY (soul_ptr_id);


--
-- Name: common_person_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY common_person
    ADD CONSTRAINT common_person_pkey PRIMARY KEY (soul_ptr_id);


--
-- Name: common_personrole_person_id_role_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY common_personrole
    ADD CONSTRAINT common_personrole_person_id_role_id_key UNIQUE (person_id, role_id);


--
-- Name: common_personrole_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY common_personrole
    ADD CONSTRAINT common_personrole_pkey PRIMARY KEY (id);


--
-- Name: common_phone_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY common_phone
    ADD CONSTRAINT common_phone_pkey PRIMARY KEY (uuid);


--
-- Name: common_phone_soul_id_f_number_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY common_phone
    ADD CONSTRAINT common_phone_soul_id_f_number_key UNIQUE (soul_id, f_number);


--
-- Name: common_place_cemetery_id_area_row_seat_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY common_place
    ADD CONSTRAINT common_place_cemetery_id_area_row_seat_key UNIQUE (cemetery_id, area, "row", seat);


--
-- Name: common_place_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY common_place
    ADD CONSTRAINT common_place_pkey PRIMARY KEY (product_ptr_id);


--
-- Name: common_product_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY common_product
    ADD CONSTRAINT common_product_pkey PRIMARY KEY (uuid);


--
-- Name: common_productcomments_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY common_productcomments
    ADD CONSTRAINT common_productcomments_pkey PRIMARY KEY (uuid);


--
-- Name: common_productfiles_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY common_productfiles
    ADD CONSTRAINT common_productfiles_pkey PRIMARY KEY (uuid);


--
-- Name: common_producttype_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY common_producttype
    ADD CONSTRAINT common_producttype_pkey PRIMARY KEY (id);


--
-- Name: common_role_djgroups_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY common_role_djgroups
    ADD CONSTRAINT common_role_djgroups_pkey PRIMARY KEY (id);


--
-- Name: common_role_djgroups_role_id_group_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY common_role_djgroups
    ADD CONSTRAINT common_role_djgroups_role_id_group_id_key UNIQUE (role_id, group_id);


--
-- Name: common_role_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY common_role
    ADD CONSTRAINT common_role_pkey PRIMARY KEY (uuid);


--
-- Name: common_roletree_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY common_roletree
    ADD CONSTRAINT common_roletree_pkey PRIMARY KEY (id);


--
-- Name: common_soul_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY common_soul
    ADD CONSTRAINT common_soul_pkey PRIMARY KEY (uuid);


--
-- Name: common_soulproducttypeoperati_soul_id_p_type_id_operation_i_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY common_soulproducttypeoperation
    ADD CONSTRAINT common_soulproducttypeoperati_soul_id_p_type_id_operation_i_key UNIQUE (soul_id, p_type_id, operation_id);


--
-- Name: common_soulproducttypeoperation_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY common_soulproducttypeoperation
    ADD CONSTRAINT common_soulproducttypeoperation_pkey PRIMARY KEY (id);


--
-- Name: common_street_city_id_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY common_street
    ADD CONSTRAINT common_street_city_id_name_key UNIQUE (city_id, name);


--
-- Name: common_street_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY common_street
    ADD CONSTRAINT common_street_pkey PRIMARY KEY (uuid);


--
-- Name: common_userprofile_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY common_userprofile
    ADD CONSTRAINT common_userprofile_pkey PRIMARY KEY (user_id);


--
-- Name: common_userprofile_soul_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY common_userprofile
    ADD CONSTRAINT common_userprofile_soul_id_key UNIQUE (soul_id);


--
-- Name: django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_content_type_app_label_model_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_key UNIQUE (app_label, model);


--
-- Name: django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: django_site_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY django_site
    ADD CONSTRAINT django_site_pkey PRIMARY KEY (id);


--
-- Name: south_migrationhistory_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY south_migrationhistory
    ADD CONSTRAINT south_migrationhistory_pkey PRIMARY KEY (id);


--
-- Name: auth_group_permissions_group_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX auth_group_permissions_group_id ON auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_permission_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX auth_group_permissions_permission_id ON auth_group_permissions USING btree (permission_id);


--
-- Name: auth_message_user_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX auth_message_user_id ON auth_message USING btree (user_id);


--
-- Name: auth_permission_content_type_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX auth_permission_content_type_id ON auth_permission USING btree (content_type_id);


--
-- Name: auth_user_groups_group_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX auth_user_groups_group_id ON auth_user_groups USING btree (group_id);


--
-- Name: auth_user_groups_user_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX auth_user_groups_user_id ON auth_user_groups USING btree (user_id);


--
-- Name: auth_user_user_permissions_permission_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX auth_user_user_permissions_permission_id ON auth_user_user_permissions USING btree (permission_id);


--
-- Name: auth_user_user_permissions_user_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX auth_user_user_permissions_user_id ON auth_user_user_permissions USING btree (user_id);


--
-- Name: common_burial_person_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX common_burial_person_id ON common_burial USING btree (person_id);


--
-- Name: common_burial_person_id_like; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX common_burial_person_id_like ON common_burial USING btree (person_id varchar_pattern_ops);


--
-- Name: common_cemetery_creator_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX common_cemetery_creator_id ON common_cemetery USING btree (creator_id);


--
-- Name: common_cemetery_location_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX common_cemetery_location_id ON common_cemetery USING btree (location_id);


--
-- Name: common_cemetery_location_id_like; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX common_cemetery_location_id_like ON common_cemetery USING btree (location_id varchar_pattern_ops);


--
-- Name: common_cemetery_organization_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX common_cemetery_organization_id ON common_cemetery USING btree (organization_id);


--
-- Name: common_cemetery_organization_id_like; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX common_cemetery_organization_id_like ON common_cemetery USING btree (organization_id varchar_pattern_ops);


--
-- Name: common_email_soul_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX common_email_soul_id ON common_email USING btree (soul_id);


--
-- Name: common_email_soul_id_like; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX common_email_soul_id_like ON common_email USING btree (soul_id varchar_pattern_ops);


--
-- Name: common_geocity_country_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX common_geocity_country_id ON common_geocity USING btree (country_id);


--
-- Name: common_geocity_country_id_like; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX common_geocity_country_id_like ON common_geocity USING btree (country_id varchar_pattern_ops);


--
-- Name: common_geocity_name; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX common_geocity_name ON common_geocity USING btree (name);


--
-- Name: common_geocity_name_like; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX common_geocity_name_like ON common_geocity USING btree (name varchar_pattern_ops);


--
-- Name: common_geocity_region_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX common_geocity_region_id ON common_geocity USING btree (region_id);


--
-- Name: common_geocity_region_id_like; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX common_geocity_region_id_like ON common_geocity USING btree (region_id varchar_pattern_ops);


--
-- Name: common_georegion_country_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX common_georegion_country_id ON common_georegion USING btree (country_id);


--
-- Name: common_georegion_country_id_like; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX common_georegion_country_id_like ON common_georegion USING btree (country_id varchar_pattern_ops);


--
-- Name: common_georegion_name; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX common_georegion_name ON common_georegion USING btree (name);


--
-- Name: common_georegion_name_like; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX common_georegion_name_like ON common_georegion USING btree (name varchar_pattern_ops);


--
-- Name: common_location_street_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX common_location_street_id ON common_location USING btree (street_id);


--
-- Name: common_location_street_id_like; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX common_location_street_id_like ON common_location USING btree (street_id varchar_pattern_ops);


--
-- Name: common_metro_city_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX common_metro_city_id ON common_metro USING btree (city_id);


--
-- Name: common_metro_city_id_like; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX common_metro_city_id_like ON common_metro USING btree (city_id varchar_pattern_ops);


--
-- Name: common_order_creator_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX common_order_creator_id ON common_order USING btree (creator_id);


--
-- Name: common_order_customer_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX common_order_customer_id ON common_order USING btree (customer_id);


--
-- Name: common_order_customer_id_like; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX common_order_customer_id_like ON common_order USING btree (customer_id varchar_pattern_ops);


--
-- Name: common_order_doer_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX common_order_doer_id ON common_order USING btree (doer_id);


--
-- Name: common_order_doer_id_like; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX common_order_doer_id_like ON common_order USING btree (doer_id varchar_pattern_ops);


--
-- Name: common_order_operation_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX common_order_operation_id ON common_order USING btree (operation_id);


--
-- Name: common_order_product_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX common_order_product_id ON common_order USING btree (product_id);


--
-- Name: common_order_product_id_like; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX common_order_product_id_like ON common_order USING btree (product_id varchar_pattern_ops);


--
-- Name: common_order_responsible_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX common_order_responsible_id ON common_order USING btree (responsible_id);


--
-- Name: common_order_responsible_id_like; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX common_order_responsible_id_like ON common_order USING btree (responsible_id varchar_pattern_ops);


--
-- Name: common_ordercomments_creator_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX common_ordercomments_creator_id ON common_ordercomments USING btree (creator_id);


--
-- Name: common_ordercomments_order_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX common_ordercomments_order_id ON common_ordercomments USING btree (order_id);


--
-- Name: common_ordercomments_order_id_like; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX common_ordercomments_order_id_like ON common_ordercomments USING btree (order_id varchar_pattern_ops);


--
-- Name: common_orderfiles_creator_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX common_orderfiles_creator_id ON common_orderfiles USING btree (creator_id);


--
-- Name: common_orderfiles_order_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX common_orderfiles_order_id ON common_orderfiles USING btree (order_id);


--
-- Name: common_orderfiles_order_id_like; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX common_orderfiles_order_id_like ON common_orderfiles USING btree (order_id varchar_pattern_ops);


--
-- Name: common_personrole_creator_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX common_personrole_creator_id ON common_personrole USING btree (creator_id);


--
-- Name: common_personrole_person_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX common_personrole_person_id ON common_personrole USING btree (person_id);


--
-- Name: common_personrole_person_id_like; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX common_personrole_person_id_like ON common_personrole USING btree (person_id varchar_pattern_ops);


--
-- Name: common_personrole_role_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX common_personrole_role_id ON common_personrole USING btree (role_id);


--
-- Name: common_personrole_role_id_like; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX common_personrole_role_id_like ON common_personrole USING btree (role_id varchar_pattern_ops);


--
-- Name: common_phone_soul_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX common_phone_soul_id ON common_phone USING btree (soul_id);


--
-- Name: common_phone_soul_id_like; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX common_phone_soul_id_like ON common_phone USING btree (soul_id varchar_pattern_ops);


--
-- Name: common_place_cemetery_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX common_place_cemetery_id ON common_place USING btree (cemetery_id);


--
-- Name: common_place_cemetery_id_like; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX common_place_cemetery_id_like ON common_place USING btree (cemetery_id varchar_pattern_ops);


--
-- Name: common_place_creator_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX common_place_creator_id ON common_place USING btree (creator_id);


--
-- Name: common_product_p_type_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX common_product_p_type_id ON common_product USING btree (p_type_id);


--
-- Name: common_product_soul_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX common_product_soul_id ON common_product USING btree (soul_id);


--
-- Name: common_product_soul_id_like; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX common_product_soul_id_like ON common_product USING btree (soul_id varchar_pattern_ops);


--
-- Name: common_productcomments_creator_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX common_productcomments_creator_id ON common_productcomments USING btree (creator_id);


--
-- Name: common_productcomments_product_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX common_productcomments_product_id ON common_productcomments USING btree (product_id);


--
-- Name: common_productcomments_product_id_like; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX common_productcomments_product_id_like ON common_productcomments USING btree (product_id varchar_pattern_ops);


--
-- Name: common_productfiles_creator_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX common_productfiles_creator_id ON common_productfiles USING btree (creator_id);


--
-- Name: common_productfiles_product_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX common_productfiles_product_id ON common_productfiles USING btree (product_id);


--
-- Name: common_productfiles_product_id_like; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX common_productfiles_product_id_like ON common_productfiles USING btree (product_id varchar_pattern_ops);


--
-- Name: common_role_creator_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX common_role_creator_id ON common_role USING btree (creator_id);


--
-- Name: common_role_djgroups_group_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX common_role_djgroups_group_id ON common_role_djgroups USING btree (group_id);


--
-- Name: common_role_djgroups_role_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX common_role_djgroups_role_id ON common_role_djgroups USING btree (role_id);


--
-- Name: common_role_djgroups_role_id_like; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX common_role_djgroups_role_id_like ON common_role_djgroups USING btree (role_id varchar_pattern_ops);


--
-- Name: common_role_organization_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX common_role_organization_id ON common_role USING btree (organization_id);


--
-- Name: common_role_organization_id_like; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX common_role_organization_id_like ON common_role USING btree (organization_id varchar_pattern_ops);


--
-- Name: common_roletree_master_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX common_roletree_master_id ON common_roletree USING btree (master_id);


--
-- Name: common_roletree_master_id_like; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX common_roletree_master_id_like ON common_roletree USING btree (master_id varchar_pattern_ops);


--
-- Name: common_roletree_slave_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX common_roletree_slave_id ON common_roletree USING btree (slave_id);


--
-- Name: common_roletree_slave_id_like; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX common_roletree_slave_id_like ON common_roletree USING btree (slave_id varchar_pattern_ops);


--
-- Name: common_soul_creator_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX common_soul_creator_id ON common_soul USING btree (creator_id);


--
-- Name: common_soul_location_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX common_soul_location_id ON common_soul USING btree (location_id);


--
-- Name: common_soul_location_id_like; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX common_soul_location_id_like ON common_soul USING btree (location_id varchar_pattern_ops);


--
-- Name: common_soulproducttypeoperation_operation_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX common_soulproducttypeoperation_operation_id ON common_soulproducttypeoperation USING btree (operation_id);


--
-- Name: common_soulproducttypeoperation_p_type_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX common_soulproducttypeoperation_p_type_id ON common_soulproducttypeoperation USING btree (p_type_id);


--
-- Name: common_soulproducttypeoperation_soul_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX common_soulproducttypeoperation_soul_id ON common_soulproducttypeoperation USING btree (soul_id);


--
-- Name: common_soulproducttypeoperation_soul_id_like; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX common_soulproducttypeoperation_soul_id_like ON common_soulproducttypeoperation USING btree (soul_id varchar_pattern_ops);


--
-- Name: common_street_city_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX common_street_city_id ON common_street USING btree (city_id);


--
-- Name: common_street_city_id_like; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX common_street_city_id_like ON common_street USING btree (city_id varchar_pattern_ops);


--
-- Name: common_street_name; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX common_street_name ON common_street USING btree (name);


--
-- Name: common_street_name_like; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX common_street_name_like ON common_street USING btree (name varchar_pattern_ops);


--
-- Name: common_userprofile_default_cemetery_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX common_userprofile_default_cemetery_id ON common_userprofile USING btree (default_cemetery_id);


--
-- Name: common_userprofile_default_cemetery_id_like; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX common_userprofile_default_cemetery_id_like ON common_userprofile USING btree (default_cemetery_id varchar_pattern_ops);


--
-- Name: common_userprofile_default_city_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX common_userprofile_default_city_id ON common_userprofile USING btree (default_city_id);


--
-- Name: common_userprofile_default_city_id_like; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX common_userprofile_default_city_id_like ON common_userprofile USING btree (default_city_id varchar_pattern_ops);


--
-- Name: common_userprofile_default_country_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX common_userprofile_default_country_id ON common_userprofile USING btree (default_country_id);


--
-- Name: common_userprofile_default_country_id_like; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX common_userprofile_default_country_id_like ON common_userprofile USING btree (default_country_id varchar_pattern_ops);


--
-- Name: common_userprofile_default_operation_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX common_userprofile_default_operation_id ON common_userprofile USING btree (default_operation_id);


--
-- Name: common_userprofile_default_region_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX common_userprofile_default_region_id ON common_userprofile USING btree (default_region_id);


--
-- Name: common_userprofile_default_region_id_like; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX common_userprofile_default_region_id_like ON common_userprofile USING btree (default_region_id varchar_pattern_ops);


--
-- Name: django_admin_log_content_type_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX django_admin_log_content_type_id ON django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_user_id; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX django_admin_log_user_id ON django_admin_log USING btree (user_id);


--
-- Name: auth_group_permissions_permission_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_permission_id_fkey FOREIGN KEY (permission_id) REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_message_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_message
    ADD CONSTRAINT auth_message_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_fkey FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions_permission_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_permission_id_fkey FOREIGN KEY (permission_id) REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_burial_order_ptr_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY common_burial
    ADD CONSTRAINT common_burial_order_ptr_id_fkey FOREIGN KEY (order_ptr_id) REFERENCES common_order(uuid) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_burial_person_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY common_burial
    ADD CONSTRAINT common_burial_person_id_fkey FOREIGN KEY (person_id) REFERENCES common_person(soul_ptr_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_cemetery_creator_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY common_cemetery
    ADD CONSTRAINT common_cemetery_creator_id_fkey FOREIGN KEY (creator_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_cemetery_location_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY common_cemetery
    ADD CONSTRAINT common_cemetery_location_id_fkey FOREIGN KEY (location_id) REFERENCES common_location(uuid) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_cemetery_organization_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY common_cemetery
    ADD CONSTRAINT common_cemetery_organization_id_fkey FOREIGN KEY (organization_id) REFERENCES common_organization(soul_ptr_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_deathcertificate_soul_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY common_deathcertificate
    ADD CONSTRAINT common_deathcertificate_soul_id_fkey FOREIGN KEY (soul_id) REFERENCES common_soul(uuid) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_email_soul_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY common_email
    ADD CONSTRAINT common_email_soul_id_fkey FOREIGN KEY (soul_id) REFERENCES common_soul(uuid) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_geocity_country_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY common_geocity
    ADD CONSTRAINT common_geocity_country_id_fkey FOREIGN KEY (country_id) REFERENCES common_geocountry(uuid) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_geocity_region_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY common_geocity
    ADD CONSTRAINT common_geocity_region_id_fkey FOREIGN KEY (region_id) REFERENCES common_georegion(uuid) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_georegion_country_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY common_georegion
    ADD CONSTRAINT common_georegion_country_id_fkey FOREIGN KEY (country_id) REFERENCES common_geocountry(uuid) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_location_street_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY common_location
    ADD CONSTRAINT common_location_street_id_fkey FOREIGN KEY (street_id) REFERENCES common_street(uuid) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_metro_city_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY common_metro
    ADD CONSTRAINT common_metro_city_id_fkey FOREIGN KEY (city_id) REFERENCES common_geocity(uuid) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_order_creator_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY common_order
    ADD CONSTRAINT common_order_creator_id_fkey FOREIGN KEY (creator_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_order_customer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY common_order
    ADD CONSTRAINT common_order_customer_id_fkey FOREIGN KEY (customer_id) REFERENCES common_soul(uuid) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_order_doer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY common_order
    ADD CONSTRAINT common_order_doer_id_fkey FOREIGN KEY (doer_id) REFERENCES common_soul(uuid) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_order_operation_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY common_order
    ADD CONSTRAINT common_order_operation_id_fkey FOREIGN KEY (operation_id) REFERENCES common_operation(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_order_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY common_order
    ADD CONSTRAINT common_order_product_id_fkey FOREIGN KEY (product_id) REFERENCES common_product(uuid) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_order_responsible_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY common_order
    ADD CONSTRAINT common_order_responsible_id_fkey FOREIGN KEY (responsible_id) REFERENCES common_soul(uuid) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_ordercomments_creator_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY common_ordercomments
    ADD CONSTRAINT common_ordercomments_creator_id_fkey FOREIGN KEY (creator_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_ordercomments_order_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY common_ordercomments
    ADD CONSTRAINT common_ordercomments_order_id_fkey FOREIGN KEY (order_id) REFERENCES common_order(uuid) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_orderfiles_creator_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY common_orderfiles
    ADD CONSTRAINT common_orderfiles_creator_id_fkey FOREIGN KEY (creator_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_orderfiles_order_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY common_orderfiles
    ADD CONSTRAINT common_orderfiles_order_id_fkey FOREIGN KEY (order_id) REFERENCES common_order(uuid) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_organization_soul_ptr_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY common_organization
    ADD CONSTRAINT common_organization_soul_ptr_id_fkey FOREIGN KEY (soul_ptr_id) REFERENCES common_soul(uuid) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_person_soul_ptr_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY common_person
    ADD CONSTRAINT common_person_soul_ptr_id_fkey FOREIGN KEY (soul_ptr_id) REFERENCES common_soul(uuid) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_personrole_creator_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY common_personrole
    ADD CONSTRAINT common_personrole_creator_id_fkey FOREIGN KEY (creator_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_personrole_person_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY common_personrole
    ADD CONSTRAINT common_personrole_person_id_fkey FOREIGN KEY (person_id) REFERENCES common_person(soul_ptr_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_personrole_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY common_personrole
    ADD CONSTRAINT common_personrole_role_id_fkey FOREIGN KEY (role_id) REFERENCES common_role(uuid) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_phone_soul_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY common_phone
    ADD CONSTRAINT common_phone_soul_id_fkey FOREIGN KEY (soul_id) REFERENCES common_soul(uuid) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_place_cemetery_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY common_place
    ADD CONSTRAINT common_place_cemetery_id_fkey FOREIGN KEY (cemetery_id) REFERENCES common_cemetery(uuid) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_place_creator_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY common_place
    ADD CONSTRAINT common_place_creator_id_fkey FOREIGN KEY (creator_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_place_product_ptr_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY common_place
    ADD CONSTRAINT common_place_product_ptr_id_fkey FOREIGN KEY (product_ptr_id) REFERENCES common_product(uuid) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_product_p_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY common_product
    ADD CONSTRAINT common_product_p_type_id_fkey FOREIGN KEY (p_type_id) REFERENCES common_producttype(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_product_soul_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY common_product
    ADD CONSTRAINT common_product_soul_id_fkey FOREIGN KEY (soul_id) REFERENCES common_soul(uuid) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_productcomments_creator_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY common_productcomments
    ADD CONSTRAINT common_productcomments_creator_id_fkey FOREIGN KEY (creator_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_productcomments_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY common_productcomments
    ADD CONSTRAINT common_productcomments_product_id_fkey FOREIGN KEY (product_id) REFERENCES common_product(uuid) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_productfiles_creator_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY common_productfiles
    ADD CONSTRAINT common_productfiles_creator_id_fkey FOREIGN KEY (creator_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_productfiles_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY common_productfiles
    ADD CONSTRAINT common_productfiles_product_id_fkey FOREIGN KEY (product_id) REFERENCES common_product(uuid) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_role_creator_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY common_role
    ADD CONSTRAINT common_role_creator_id_fkey FOREIGN KEY (creator_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_role_djgroups_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY common_role_djgroups
    ADD CONSTRAINT common_role_djgroups_group_id_fkey FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_role_organization_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY common_role
    ADD CONSTRAINT common_role_organization_id_fkey FOREIGN KEY (organization_id) REFERENCES common_organization(soul_ptr_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_roletree_master_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY common_roletree
    ADD CONSTRAINT common_roletree_master_id_fkey FOREIGN KEY (master_id) REFERENCES common_role(uuid) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_roletree_slave_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY common_roletree
    ADD CONSTRAINT common_roletree_slave_id_fkey FOREIGN KEY (slave_id) REFERENCES common_role(uuid) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_soul_creator_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY common_soul
    ADD CONSTRAINT common_soul_creator_id_fkey FOREIGN KEY (creator_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_soul_location_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY common_soul
    ADD CONSTRAINT common_soul_location_id_fkey FOREIGN KEY (location_id) REFERENCES common_location(uuid) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_soulproducttypeoperation_operation_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY common_soulproducttypeoperation
    ADD CONSTRAINT common_soulproducttypeoperation_operation_id_fkey FOREIGN KEY (operation_id) REFERENCES common_operation(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_soulproducttypeoperation_p_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY common_soulproducttypeoperation
    ADD CONSTRAINT common_soulproducttypeoperation_p_type_id_fkey FOREIGN KEY (p_type_id) REFERENCES common_producttype(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_soulproducttypeoperation_soul_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY common_soulproducttypeoperation
    ADD CONSTRAINT common_soulproducttypeoperation_soul_id_fkey FOREIGN KEY (soul_id) REFERENCES common_soul(uuid) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_street_city_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY common_street
    ADD CONSTRAINT common_street_city_id_fkey FOREIGN KEY (city_id) REFERENCES common_geocity(uuid) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_userprofile_default_cemetery_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY common_userprofile
    ADD CONSTRAINT common_userprofile_default_cemetery_id_fkey FOREIGN KEY (default_cemetery_id) REFERENCES common_cemetery(uuid) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_userprofile_default_city_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY common_userprofile
    ADD CONSTRAINT common_userprofile_default_city_id_fkey FOREIGN KEY (default_city_id) REFERENCES common_geocity(uuid) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_userprofile_default_country_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY common_userprofile
    ADD CONSTRAINT common_userprofile_default_country_id_fkey FOREIGN KEY (default_country_id) REFERENCES common_geocountry(uuid) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_userprofile_default_operation_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY common_userprofile
    ADD CONSTRAINT common_userprofile_default_operation_id_fkey FOREIGN KEY (default_operation_id) REFERENCES common_operation(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_userprofile_default_region_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY common_userprofile
    ADD CONSTRAINT common_userprofile_default_region_id_fkey FOREIGN KEY (default_region_id) REFERENCES common_georegion(uuid) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_userprofile_soul_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY common_userprofile
    ADD CONSTRAINT common_userprofile_soul_id_fkey FOREIGN KEY (soul_id) REFERENCES common_soul(uuid) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: common_userprofile_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY common_userprofile
    ADD CONSTRAINT common_userprofile_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: content_type_id_refs_id_728de91f; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT content_type_id_refs_id_728de91f FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log_content_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_fkey FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: group_id_refs_id_3cea63fe; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT group_id_refs_id_3cea63fe FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: role_id_refs_uuid_7648cce5; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY common_role_djgroups
    ADD CONSTRAINT role_id_refs_uuid_7648cce5 FOREIGN KEY (role_id) REFERENCES common_role(uuid) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: user_id_refs_id_831107f1; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT user_id_refs_id_831107f1 FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: user_id_refs_id_f2045483; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT user_id_refs_id_f2045483 FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

