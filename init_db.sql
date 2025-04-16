--
-- PostgreSQL database dump
--

-- Dumped from database version 16.0
-- Dumped by pg_dump version 16rc1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: favorites; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.favorites (
    id integer NOT NULL,
    user_id integer,
    product_id integer
);


ALTER TABLE public.favorites OWNER TO postgres;

--
-- Name: favorites_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.favorites_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.favorites_id_seq OWNER TO postgres;

--
-- Name: favorites_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.favorites_id_seq OWNED BY public.favorites.id;


--
-- Name: price_history; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.price_history (
    id integer NOT NULL,
    product_id integer,
    "timestamp" timestamp without time zone,
    price numeric
);


ALTER TABLE public.price_history OWNER TO postgres;

--
-- Name: price_history_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.price_history_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.price_history_id_seq OWNER TO postgres;

--
-- Name: price_history_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.price_history_id_seq OWNED BY public.price_history.id;


--
-- Name: products; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.products (
    id integer NOT NULL,
    name character varying,
    url character varying,
    latest_price numeric,
    last_checked timestamp without time zone
);


ALTER TABLE public.products OWNER TO postgres;

--
-- Name: products_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.products_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.products_id_seq OWNER TO postgres;

--
-- Name: products_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.products_id_seq OWNED BY public.products.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id integer NOT NULL,
    username character varying,
    password_hash character varying,
    telegram_username character varying,
    telegram_chat_id character varying
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: favorites id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.favorites ALTER COLUMN id SET DEFAULT nextval('public.favorites_id_seq'::regclass);


--
-- Name: price_history id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.price_history ALTER COLUMN id SET DEFAULT nextval('public.price_history_id_seq'::regclass);


--
-- Name: products id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.products ALTER COLUMN id SET DEFAULT nextval('public.products_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: favorites; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.favorites (id, user_id, product_id) FROM stdin;
1	1	3
2	1	4
8	1	8
9	1	9
10	1	10
11	1	11
13	2	12
14	2	12
15	2	12
\.


--
-- Data for Name: price_history; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.price_history (id, product_id, "timestamp", price) FROM stdin;
1	3	2025-04-10 21:47:33.67124	98980.0
2	2	2025-04-10 21:47:33.914799	80480.0
3	1	2025-04-10 21:47:34.718998	80480.0
4	3	2025-04-10 21:50:11.181196	98980.0
5	2	2025-04-10 21:50:11.426916	80480.0
6	1	2025-04-10 21:50:12.239054	80480.0
9	3	2025-04-12 01:36:08.853907	97490.0
10	2	2025-04-12 01:36:09.336805	80480.0
11	3	2025-04-12 14:36:20.664535	95490.0
12	2	2025-04-12 14:36:21.101837	80480.0
13	4	2025-04-12 14:43:23.533803	17480.0
14	3	2025-04-12 15:56:41.003704	95490.0
15	4	2025-04-12 15:56:55.025534	17480.0
16	5	2025-04-12 16:48:05.692653	0
17	5	2025-04-12 16:50:36.163344	0
18	5	2025-04-12 16:51:58.350418	0
19	6	2025-04-12 16:55:32.915606	0
20	7	2025-04-12 16:57:04.575373	1000.0
21	7	2025-04-12 17:08:38.881111	1500.0
23	7	2025-04-12 19:34:21.719409	0
24	8	2025-04-12 19:34:22.440368	95990.0
22	8	2025-04-12 19:30:14.201693	96490
25	9	2025-04-12 19:37:02.740421	112290.0
26	10	2025-04-12 19:43:03.996445	112990.0
27	11	2025-04-12 19:45:39.146199	10980.0
28	3	2025-04-13 15:59:53.826476	95190.0
29	8	2025-04-13 15:59:55.054388	94890.0
30	12	2025-04-13 16:05:02.494399	0
31	12	2025-04-13 16:07:38.879465	0
32	12	2025-04-13 16:09:17.621737	0
33	12	2025-04-13 16:13:49.473971	0
34	1	2025-04-13 18:42:50.119387	78880.0
35	2	2025-04-13 18:42:50.647975	78880.0
36	8	2025-04-15 17:48:43.329305	94190.0
37	4	2025-04-15 17:48:43.688563	17380.0
38	10	2025-04-15 17:48:44.238012	110990.0
39	3	2025-04-15 17:48:44.748685	94490.0
40	9	2025-04-15 17:48:45.21776	111790.0
\.


--
-- Data for Name: products; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.products (id, name, url, latest_price, last_checked) FROM stdin;
7	Quick Text - Easiest way of online text sharing 📠	https://qtext.io/flc9	0	2025-04-12 19:34:21.719409
11	Наушники накладные Bluetooth Marshall Major V, Brown купить в Москве. Цена, отзывы, доставка | МСК Каталог	https://msk-katalog.ru/naushniki-nakladnye-bluetooth-marshall-major-v-brown/	10980.0	2025-04-12 19:45:39.143199
12	ÐÐ¾ÑÑÑÐ¿ Ð¾Ð³ÑÐ°Ð½Ð¸ÑÐµÐ½	https://www.ozon.ru/product/kofevarka-rozhkovaya-s-avtokapuchinatorom-tuvio-tcm04ea-chernyy-serebristyy-1519096090/	0	2025-04-13 16:05:02.487399
1	Поиск - iphone 15 pro 128 nano	https://msk-katalog.ru/search/?search=iphone%2015%20pro%20128%20nano	78880.0	2025-04-13 18:42:50.119387
2	Смартфон Apple iPhone 15 Pro 128 ГБ, белый титан, Dual SIM (nano SIM+eSIM) купить в Москве. Цена, отзывы, доставка | МСК Каталог	https://msk-katalog.ru/smartfon-apple-iphone-15-pro-128-gb-belyj-titan-dual-sim-nano-simesim/	78880.0	2025-04-13 18:42:50.647975
8	Смартфон Apple iPhone 16 Pro 256 GB, Dual SIM (nano SIM+eSIM), Black Titanium купить в Москве. Цена, отзывы, доставка | МСК Каталог	https://msk-katalog.ru/smartfon-apple-iphone-16-pro-256-gb-dual-sim-nano-simesim-black-titanium/	94190.0	2025-04-15 17:48:43.329305
4	Беспроводные наушники Apple AirPods Pro 2 MagSafe USB-C (2023), белый купить в Москве. Цена, отзывы, доставка | МСК Каталог	https://msk-katalog.ru/besprovodnye-naushniki-apple-airpods-2-magsafe-usb-c-2023-belyj/	17380.0	2025-04-15 17:48:43.688563
10	Смартфон Apple iPhone 16 Pro 512 GB, Dual SIM (nano SIM+eSIM), Black Titanium купить в Москве. Цена, отзывы, доставка | МСК Каталог	https://msk-katalog.ru/smartfon-apple-iphone-16-pro-512-gb-dual-sim-nano-simesim-black-titanium/	110990.0	2025-04-15 17:48:44.238012
3	Смартфон Apple iPhone 16 Pro 256 GB, Dual SIM (nano SIM+eSIM), Natural Titanium купить в Москве. Цена, отзывы, доставка | МСК Каталог	https://msk-katalog.ru/smartfon-apple-iphone-16-pro-256-gb-dual-sim-nano-simesim-natural-titanium/	94490.0	2025-04-15 17:48:44.748685
9	Смартфон Apple iPhone 16 Pro 512 GB, Dual SIM (nano SIM+eSIM), Natural Titanium купить в Москве. Цена, отзывы, доставка | МСК Каталог	https://msk-katalog.ru/smartfon-apple-iphone-16-pro-512-gb-dual-sim-nano-simesim-natural-titanium/	111790.0	2025-04-15 17:48:45.21776
5	Без заголовка - Text-Host - текстовый хостинг	https://text-host.ru/bez-zagolovka-13956	0	2025-04-12 16:48:05.686652
6	ShareTXT -\n            greyson has already been claimed	https://sharetxt.live/greyson	0	2025-04-12 16:55:32.913606
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, username, password_hash, telegram_username, telegram_chat_id) FROM stdin;
1	admin	$2b$12$Ca6x.ypaUSsdHVBjstA8V.07zv7PFroKpSN4BW52gDY2iSxmjrN2W	SergeyGreyson	649320467
2	user1	$2b$12$RNpy/yrBwEVX1VAQVHTx9eCXpIJ6PCX.JBaRdrjzPCF2T/CmsjXci	\N	\N
\.


--
-- Name: favorites_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.favorites_id_seq', 15, true);


--
-- Name: price_history_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.price_history_id_seq', 40, true);


--
-- Name: products_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.products_id_seq', 12, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 2, true);


--
-- Name: favorites favorites_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.favorites
    ADD CONSTRAINT favorites_pkey PRIMARY KEY (id);


--
-- Name: price_history price_history_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.price_history
    ADD CONSTRAINT price_history_pkey PRIMARY KEY (id);


--
-- Name: products products_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_pkey PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- Name: favorites favorites_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.favorites
    ADD CONSTRAINT favorites_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(id);


--
-- Name: favorites favorites_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.favorites
    ADD CONSTRAINT favorites_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: price_history price_history_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.price_history
    ADD CONSTRAINT price_history_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(id);


--
-- PostgreSQL database dump complete
--

