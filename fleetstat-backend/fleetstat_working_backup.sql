--
-- PostgreSQL database dump
--

\restrict 87bLNqGxPQDok9nQ4cnTPaQSnNpEDJlxf5ORAWdafxQaF2YQ4Z5kbeYgwmkdD3z

-- Dumped from database version 16.13 (Debian 16.13-1.pgdg13+1)
-- Dumped by pg_dump version 16.13 (Debian 16.13-1.pgdg13+1)

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

--
-- Name: update_updated_at_column(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.update_updated_at_column() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$;


ALTER FUNCTION public.update_updated_at_column() OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: container_assignments; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.container_assignments (
    assignment_id integer NOT NULL,
    trip_id integer NOT NULL,
    container_id integer NOT NULL,
    assigned_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.container_assignments OWNER TO postgres;

--
-- Name: container_assignments_assignment_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.container_assignments_assignment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.container_assignments_assignment_id_seq OWNER TO postgres;

--
-- Name: container_assignments_assignment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.container_assignments_assignment_id_seq OWNED BY public.container_assignments.assignment_id;


--
-- Name: containers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.containers (
    container_id integer NOT NULL,
    container_code character varying(50) NOT NULL,
    container_type character varying(50),
    capacity_kg numeric(10,2),
    status character varying(20) DEFAULT 'AVAILABLE'::character varying,
    description text,
    is_active boolean DEFAULT true,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT containers_status_check CHECK (((status)::text = ANY (ARRAY[('AVAILABLE'::character varying)::text, ('IN_USE'::character varying)::text, ('MAINTENANCE'::character varying)::text])))
);


ALTER TABLE public.containers OWNER TO postgres;

--
-- Name: container_utilization; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.container_utilization AS
 SELECT c.container_id,
    c.container_code,
    count(ca.assignment_id) AS usage_count
   FROM (public.containers c
     LEFT JOIN public.container_assignments ca ON ((c.container_id = ca.container_id)))
  GROUP BY c.container_id, c.container_code;


ALTER VIEW public.container_utilization OWNER TO postgres;

--
-- Name: containers_container_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.containers_container_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.containers_container_id_seq OWNER TO postgres;

--
-- Name: containers_container_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.containers_container_id_seq OWNED BY public.containers.container_id;


--
-- Name: customers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.customers (
    customer_id integer NOT NULL,
    customer_type character varying(20) NOT NULL,
    customer_name character varying(150) NOT NULL,
    gst_number character varying(50),
    email character varying(100),
    phone_number character varying(20),
    address text,
    is_active boolean DEFAULT true,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT customers_customer_type_check CHECK (((customer_type)::text = ANY (ARRAY[('BUSINESS'::character varying)::text, ('INDIVIDUAL'::character varying)::text])))
);


ALTER TABLE public.customers OWNER TO postgres;

--
-- Name: payments; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.payments (
    payment_id integer NOT NULL,
    shipment_id integer NOT NULL,
    amount numeric(12,2) NOT NULL,
    payment_method character varying(50),
    payment_status character varying(20) DEFAULT 'PENDING'::character varying,
    payment_date timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    remarks text,
    CONSTRAINT payments_payment_status_check CHECK (((payment_status)::text = ANY (ARRAY[('PENDING'::character varying)::text, ('SUCCESS'::character varying)::text, ('FAILED'::character varying)::text, ('REFUNDED'::character varying)::text])))
);


ALTER TABLE public.payments OWNER TO postgres;

--
-- Name: shipments; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.shipments (
    shipment_id integer NOT NULL,
    container_id integer NOT NULL,
    sender_customer_id integer NOT NULL,
    receiver_customer_id integer NOT NULL,
    shipment_status character varying(20) DEFAULT 'RECEIVED'::character varying,
    received_date date,
    shipped_date date,
    delivered_date date,
    notes text,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    trip_id integer NOT NULL,
    CONSTRAINT shipments_shipment_status_check CHECK (((shipment_status)::text = ANY (ARRAY[('RECEIVED'::character varying)::text, ('IN_TRANSIT'::character varying)::text, ('DELIVERED'::character varying)::text, ('DAMAGED'::character varying)::text, ('CANCELLED'::character varying)::text])))
);


ALTER TABLE public.shipments OWNER TO postgres;

--
-- Name: customer_revenue; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.customer_revenue AS
 SELECT c.customer_id,
    c.customer_name,
    COALESCE(sum(p.amount), (0)::numeric) AS total_revenue
   FROM ((public.customers c
     LEFT JOIN public.shipments s ON ((c.customer_id = s.sender_customer_id)))
     LEFT JOIN public.payments p ON (((s.shipment_id = p.shipment_id) AND ((p.payment_status)::text = 'SUCCESS'::text))))
  GROUP BY c.customer_id, c.customer_name;


ALTER VIEW public.customer_revenue OWNER TO postgres;

--
-- Name: customers_customer_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.customers_customer_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.customers_customer_id_seq OWNER TO postgres;

--
-- Name: customers_customer_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.customers_customer_id_seq OWNED BY public.customers.customer_id;


--
-- Name: damage_reports; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.damage_reports (
    damage_id integer NOT NULL,
    shipment_id integer NOT NULL,
    damage_percentage numeric(5,2),
    description text,
    reported_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    status character varying(20) DEFAULT 'PENDING'::character varying,
    CONSTRAINT damage_reports_damage_percentage_check CHECK (((damage_percentage >= (0)::numeric) AND (damage_percentage <= (100)::numeric))),
    CONSTRAINT damage_status_check CHECK (((status)::text = ANY (ARRAY[('PENDING'::character varying)::text, ('UNDER_REVIEW'::character varying)::text, ('RESOLVED'::character varying)::text])))
);


ALTER TABLE public.damage_reports OWNER TO postgres;

--
-- Name: damage_reports_damage_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.damage_reports_damage_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.damage_reports_damage_id_seq OWNER TO postgres;

--
-- Name: damage_reports_damage_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.damage_reports_damage_id_seq OWNED BY public.damage_reports.damage_id;


--
-- Name: drivers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.drivers (
    driver_id integer NOT NULL,
    full_name character varying(100) NOT NULL,
    date_of_birth date NOT NULL,
    avatar_url text,
    address text,
    license_number character varying(100) NOT NULL,
    email character varying(100),
    phone_number character varying(20) NOT NULL,
    prior_experience_years integer DEFAULT 0,
    employment_status character varying(20) DEFAULT 'active'::character varying,
    availability_status character varying(20) DEFAULT 'idle'::character varying,
    joining_date date NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    user_id integer NOT NULL,
    is_active boolean DEFAULT true,
    CONSTRAINT driver_availability_status_check CHECK (((availability_status)::text = ANY (ARRAY[('idle'::character varying)::text, ('on_trip'::character varying)::text, ('off_duty'::character varying)::text]))),
    CONSTRAINT driver_employment_status_check CHECK (((employment_status)::text = ANY (ARRAY[('active'::character varying)::text, ('inactive'::character varying)::text, ('suspended'::character varying)::text]))),
    CONSTRAINT driver_prior_experience_years_check CHECK ((prior_experience_years >= 0))
);


ALTER TABLE public.drivers OWNER TO postgres;

--
-- Name: driver_driver_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.driver_driver_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.driver_driver_id_seq OWNER TO postgres;

--
-- Name: driver_driver_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.driver_driver_id_seq OWNED BY public.drivers.driver_id;


--
-- Name: trip_assignments; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.trip_assignments (
    assignment_id integer NOT NULL,
    trip_id integer NOT NULL,
    driver_id integer NOT NULL,
    assigned_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.trip_assignments OWNER TO postgres;

--
-- Name: trips; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.trips (
    trip_id integer NOT NULL,
    truck_id integer NOT NULL,
    start_location text NOT NULL,
    end_location text NOT NULL,
    trip_distance numeric(12,2) NOT NULL,
    fuel_used numeric(10,2),
    start_time timestamp without time zone NOT NULL,
    end_time timestamp without time zone,
    trip_status character varying(20) DEFAULT 'PLANNED'::character varying,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    actual_start_time timestamp without time zone,
    actual_end_time timestamp without time zone,
    CONSTRAINT trips_trip_status_check CHECK (((trip_status)::text = ANY (ARRAY[('PLANNED'::character varying)::text, ('IN_PROGRESS'::character varying)::text, ('COMPLETED'::character varying)::text, ('CANCELLED'::character varying)::text])))
);


ALTER TABLE public.trips OWNER TO postgres;

--
-- Name: driver_performance; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.driver_performance AS
 SELECT d.driver_id,
    d.full_name,
    count(DISTINCT ta.trip_id) AS total_trips,
    COALESCE(sum(t.trip_distance), (0)::numeric) AS total_distance
   FROM ((public.drivers d
     LEFT JOIN public.trip_assignments ta ON ((d.driver_id = ta.driver_id)))
     LEFT JOIN public.trips t ON ((ta.trip_id = t.trip_id)))
  GROUP BY d.driver_id, d.full_name;


ALTER VIEW public.driver_performance OWNER TO postgres;

--
-- Name: driver_ranking; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.driver_ranking AS
 SELECT driver_id,
    full_name,
    total_trips,
    total_distance,
    rank() OVER (ORDER BY total_distance DESC) AS driver_rank
   FROM public.driver_performance;


ALTER VIEW public.driver_ranking OWNER TO postgres;

--
-- Name: fuel_logs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.fuel_logs (
    fuel_log_id integer NOT NULL,
    truck_id integer NOT NULL,
    trip_id integer,
    fuel_amount numeric(10,2) NOT NULL,
    fuel_cost numeric(12,2) NOT NULL,
    filled_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.fuel_logs OWNER TO postgres;

--
-- Name: fuel_logs_fuel_log_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.fuel_logs_fuel_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.fuel_logs_fuel_log_id_seq OWNER TO postgres;

--
-- Name: fuel_logs_fuel_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.fuel_logs_fuel_log_id_seq OWNED BY public.fuel_logs.fuel_log_id;


--
-- Name: payments_payment_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.payments_payment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.payments_payment_id_seq OWNER TO postgres;

--
-- Name: payments_payment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.payments_payment_id_seq OWNED BY public.payments.payment_id;


--
-- Name: revenue_summary; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.revenue_summary AS
 SELECT date_trunc('month'::text, payment_date) AS month,
    sum(amount) AS revenue
   FROM public.payments
  WHERE ((payment_status)::text = 'SUCCESS'::text)
  GROUP BY (date_trunc('month'::text, payment_date));


ALTER VIEW public.revenue_summary OWNER TO postgres;

--
-- Name: shipment_items; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.shipment_items (
    item_id integer NOT NULL,
    shipment_id integer NOT NULL,
    item_name character varying(150) NOT NULL,
    quantity integer NOT NULL,
    weight_kg numeric(10,2),
    declared_value numeric(12,2),
    temperature_required numeric(5,2)
);


ALTER TABLE public.shipment_items OWNER TO postgres;

--
-- Name: shipment_items_item_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.shipment_items_item_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.shipment_items_item_id_seq OWNER TO postgres;

--
-- Name: shipment_items_item_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.shipment_items_item_id_seq OWNED BY public.shipment_items.item_id;


--
-- Name: shipment_summary; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.shipment_summary AS
 SELECT s.shipment_id,
    sender.customer_name AS sender,
    receiver.customer_name AS receiver,
    s.shipment_status,
    count(si.item_id) AS total_items
   FROM (((public.shipments s
     LEFT JOIN public.customers sender ON ((s.sender_customer_id = sender.customer_id)))
     LEFT JOIN public.customers receiver ON ((s.receiver_customer_id = receiver.customer_id)))
     LEFT JOIN public.shipment_items si ON ((s.shipment_id = si.shipment_id)))
  GROUP BY s.shipment_id, sender.customer_name, receiver.customer_name, s.shipment_status;


ALTER VIEW public.shipment_summary OWNER TO postgres;

--
-- Name: shipments_shipment_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.shipments_shipment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.shipments_shipment_id_seq OWNER TO postgres;

--
-- Name: shipments_shipment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.shipments_shipment_id_seq OWNED BY public.shipments.shipment_id;


--
-- Name: trip_assignments_assignment_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.trip_assignments_assignment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.trip_assignments_assignment_id_seq OWNER TO postgres;

--
-- Name: trip_assignments_assignment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.trip_assignments_assignment_id_seq OWNED BY public.trip_assignments.assignment_id;


--
-- Name: trips_trip_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.trips_trip_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.trips_trip_id_seq OWNER TO postgres;

--
-- Name: trips_trip_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.trips_trip_id_seq OWNED BY public.trips.trip_id;


--
-- Name: trucks; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.trucks (
    truck_id integer NOT NULL,
    license_plate character varying(20) NOT NULL,
    manufacturer character varying(100) NOT NULL,
    model character varying(100) NOT NULL,
    purchase_date date,
    purchase_cost numeric(12,2),
    capacity_tons numeric(10,2) NOT NULL,
    total_distance_travelled numeric(12,2) DEFAULT 0,
    truck_condition character varying(20) DEFAULT 'GOOD'::character varying,
    status character varying(20) DEFAULT 'ACTIVE'::character varying,
    last_service_date date,
    description text,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    is_active boolean DEFAULT true,
    CONSTRAINT trucks_status_check CHECK (((status)::text = ANY (ARRAY[('ACTIVE'::character varying)::text, ('ON_TRIP'::character varying)::text, ('MAINTENANCE'::character varying)::text, ('OUT_OF_SERVICE'::character varying)::text]))),
    CONSTRAINT trucks_truck_condition_check CHECK (((truck_condition)::text = ANY (ARRAY[('EXCELLENT'::character varying)::text, ('GOOD'::character varying)::text, ('FAIR'::character varying)::text, ('POOR'::character varying)::text])))
);


ALTER TABLE public.trucks OWNER TO postgres;

--
-- Name: truck_analytics; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.truck_analytics AS
 SELECT t.truck_id,
    t.license_plate,
    COALESCE(sum(f.fuel_amount), (0)::numeric) AS total_fuel,
    COALESCE(sum(tr.trip_distance), (0)::numeric) AS total_distance
   FROM ((public.trucks t
     LEFT JOIN public.fuel_logs f ON ((t.truck_id = f.truck_id)))
     LEFT JOIN public.trips tr ON ((t.truck_id = tr.truck_id)))
  GROUP BY t.truck_id, t.license_plate;


ALTER VIEW public.truck_analytics OWNER TO postgres;

--
-- Name: truck_services; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.truck_services (
    service_id integer NOT NULL,
    truck_id integer NOT NULL,
    service_center character varying(150),
    service_date date NOT NULL,
    service_cost numeric(12,2),
    next_due_date date,
    description text,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.truck_services OWNER TO postgres;

--
-- Name: truck_maintenance_analytics; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.truck_maintenance_analytics AS
 SELECT t.truck_id,
    t.license_plate,
    count(ts.service_id) AS service_count,
    COALESCE(sum(ts.service_cost), (0)::numeric) AS total_service_cost
   FROM (public.trucks t
     LEFT JOIN public.truck_services ts ON ((t.truck_id = ts.truck_id)))
  GROUP BY t.truck_id, t.license_plate;


ALTER VIEW public.truck_maintenance_analytics OWNER TO postgres;

--
-- Name: truck_services_service_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.truck_services_service_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.truck_services_service_id_seq OWNER TO postgres;

--
-- Name: truck_services_service_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.truck_services_service_id_seq OWNED BY public.truck_services.service_id;


--
-- Name: trucks_truck_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.trucks_truck_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.trucks_truck_id_seq OWNER TO postgres;

--
-- Name: trucks_truck_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.trucks_truck_id_seq OWNED BY public.trucks.truck_id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    user_id integer NOT NULL,
    username character varying(50) NOT NULL,
    email character varying(100) NOT NULL,
    password_hash text NOT NULL,
    role character varying(20) NOT NULL,
    is_active boolean DEFAULT true,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT users_role_check CHECK (((role)::text = ANY (ARRAY[('admin'::character varying)::text, ('driver'::character varying)::text])))
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: users_user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_user_id_seq OWNER TO postgres;

--
-- Name: users_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_user_id_seq OWNED BY public.users.user_id;


--
-- Name: vehicles; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.vehicles (
    vehicle_id integer NOT NULL,
    registration_number character varying(20) NOT NULL,
    vehicle_type character varying(50) NOT NULL,
    manufacturer character varying(50) NOT NULL,
    model character varying(50) NOT NULL,
    year integer NOT NULL,
    fuel_type character varying(20) NOT NULL,
    capacity integer NOT NULL,
    status character varying(20) DEFAULT 'active'::character varying,
    created_at timestamp without time zone DEFAULT now(),
    updated_at timestamp without time zone DEFAULT now()
);


ALTER TABLE public.vehicles OWNER TO postgres;

--
-- Name: vehicles_vehicle_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.vehicles_vehicle_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.vehicles_vehicle_id_seq OWNER TO postgres;

--
-- Name: vehicles_vehicle_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.vehicles_vehicle_id_seq OWNED BY public.vehicles.vehicle_id;


--
-- Name: container_assignments assignment_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.container_assignments ALTER COLUMN assignment_id SET DEFAULT nextval('public.container_assignments_assignment_id_seq'::regclass);


--
-- Name: containers container_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.containers ALTER COLUMN container_id SET DEFAULT nextval('public.containers_container_id_seq'::regclass);


--
-- Name: customers customer_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.customers ALTER COLUMN customer_id SET DEFAULT nextval('public.customers_customer_id_seq'::regclass);


--
-- Name: damage_reports damage_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.damage_reports ALTER COLUMN damage_id SET DEFAULT nextval('public.damage_reports_damage_id_seq'::regclass);


--
-- Name: drivers driver_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.drivers ALTER COLUMN driver_id SET DEFAULT nextval('public.driver_driver_id_seq'::regclass);


--
-- Name: fuel_logs fuel_log_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fuel_logs ALTER COLUMN fuel_log_id SET DEFAULT nextval('public.fuel_logs_fuel_log_id_seq'::regclass);


--
-- Name: payments payment_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.payments ALTER COLUMN payment_id SET DEFAULT nextval('public.payments_payment_id_seq'::regclass);


--
-- Name: shipment_items item_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.shipment_items ALTER COLUMN item_id SET DEFAULT nextval('public.shipment_items_item_id_seq'::regclass);


--
-- Name: shipments shipment_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.shipments ALTER COLUMN shipment_id SET DEFAULT nextval('public.shipments_shipment_id_seq'::regclass);


--
-- Name: trip_assignments assignment_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.trip_assignments ALTER COLUMN assignment_id SET DEFAULT nextval('public.trip_assignments_assignment_id_seq'::regclass);


--
-- Name: trips trip_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.trips ALTER COLUMN trip_id SET DEFAULT nextval('public.trips_trip_id_seq'::regclass);


--
-- Name: truck_services service_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.truck_services ALTER COLUMN service_id SET DEFAULT nextval('public.truck_services_service_id_seq'::regclass);


--
-- Name: trucks truck_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.trucks ALTER COLUMN truck_id SET DEFAULT nextval('public.trucks_truck_id_seq'::regclass);


--
-- Name: users user_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN user_id SET DEFAULT nextval('public.users_user_id_seq'::regclass);


--
-- Name: vehicles vehicle_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.vehicles ALTER COLUMN vehicle_id SET DEFAULT nextval('public.vehicles_vehicle_id_seq'::regclass);


--
-- Data for Name: container_assignments; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.container_assignments (assignment_id, trip_id, container_id, assigned_at) FROM stdin;
1	1	1	2026-06-10 09:26:44.120282
2	1	2	2026-06-10 09:26:44.120282
3	2	3	2026-06-10 09:26:44.120282
4	2	4	2026-06-10 09:26:44.120282
5	3	5	2026-06-10 09:26:44.120282
6	4	6	2026-06-10 09:26:44.120282
7	4	7	2026-06-10 09:26:44.120282
8	5	8	2026-06-10 09:26:44.120282
9	6	9	2026-06-10 09:26:44.120282
10	7	10	2026-06-10 09:26:44.120282
11	8	11	2026-06-10 09:26:44.120282
12	8	12	2026-06-10 09:26:44.120282
13	9	13	2026-06-10 09:26:44.120282
14	10	14	2026-06-10 09:26:44.120282
15	10	15	2026-06-10 09:26:44.120282
16	11	1	2026-06-10 09:26:44.120282
17	12	2	2026-06-10 09:26:44.120282
18	13	3	2026-06-10 09:26:44.120282
19	14	4	2026-06-10 09:26:44.120282
20	15	5	2026-06-10 09:26:44.120282
21	16	6	2026-06-10 09:26:44.120282
22	17	7	2026-06-10 09:26:44.120282
23	18	8	2026-06-10 09:26:44.120282
24	19	9	2026-06-10 09:26:44.120282
25	20	10	2026-06-10 09:26:44.120282
26	21	11	2026-06-10 09:26:44.120282
27	22	12	2026-06-10 09:26:44.120282
28	23	13	2026-06-10 09:26:44.120282
29	24	14	2026-06-10 09:26:44.120282
30	25	15	2026-06-10 09:26:44.120282
31	26	1	2026-06-10 09:26:44.120282
32	27	2	2026-06-10 09:26:44.120282
33	28	3	2026-06-10 09:26:44.120282
34	29	4	2026-06-10 09:26:44.120282
35	30	5	2026-06-10 09:26:44.120282
\.


--
-- Data for Name: containers; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.containers (container_id, container_code, container_type, capacity_kg, status, description, is_active, created_at, updated_at) FROM stdin;
1	CONT001	REFRIGERATED	5000.00	AVAILABLE	\N	t	2026-06-10 09:26:03.075148	2026-06-10 09:26:03.075148
2	CONT002	REFRIGERATED	5000.00	AVAILABLE	\N	t	2026-06-10 09:26:03.075148	2026-06-10 09:26:03.075148
3	CONT003	REFRIGERATED	6000.00	AVAILABLE	\N	t	2026-06-10 09:26:03.075148	2026-06-10 09:26:03.075148
4	CONT004	REFRIGERATED	7000.00	AVAILABLE	\N	t	2026-06-10 09:26:03.075148	2026-06-10 09:26:03.075148
5	CONT005	REFRIGERATED	8000.00	AVAILABLE	\N	t	2026-06-10 09:26:03.075148	2026-06-10 09:26:03.075148
6	CONT006	REFRIGERATED	5000.00	AVAILABLE	\N	t	2026-06-10 09:26:03.075148	2026-06-10 09:26:03.075148
7	CONT007	REFRIGERATED	5000.00	AVAILABLE	\N	t	2026-06-10 09:26:03.075148	2026-06-10 09:26:03.075148
8	CONT008	REFRIGERATED	6000.00	AVAILABLE	\N	t	2026-06-10 09:26:03.075148	2026-06-10 09:26:03.075148
9	CONT009	REFRIGERATED	7000.00	AVAILABLE	\N	t	2026-06-10 09:26:03.075148	2026-06-10 09:26:03.075148
10	CONT010	REFRIGERATED	8000.00	AVAILABLE	\N	t	2026-06-10 09:26:03.075148	2026-06-10 09:26:03.075148
11	CONT011	REFRIGERATED	5000.00	AVAILABLE	\N	t	2026-06-10 09:26:03.075148	2026-06-10 09:26:03.075148
12	CONT012	REFRIGERATED	6000.00	AVAILABLE	\N	t	2026-06-10 09:26:03.075148	2026-06-10 09:26:03.075148
13	CONT013	REFRIGERATED	7000.00	AVAILABLE	\N	t	2026-06-10 09:26:03.075148	2026-06-10 09:26:03.075148
14	CONT014	REFRIGERATED	8000.00	AVAILABLE	\N	t	2026-06-10 09:26:03.075148	2026-06-10 09:26:03.075148
15	CONT015	REFRIGERATED	9000.00	AVAILABLE	\N	t	2026-06-10 09:26:03.075148	2026-06-10 09:26:03.075148
\.


--
-- Data for Name: customers; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.customers (customer_id, customer_type, customer_name, gst_number, email, phone_number, address, is_active, created_at, updated_at) FROM stdin;
1	BUSINESS	Amul	GST1001	contact@amul.com	9000000001	Ahmedabad	t	2026-06-10 09:25:55.671736	2026-06-10 09:25:55.671736
2	BUSINESS	Mother Dairy	GST1002	contact@motherdairy.com	9000000002	Delhi	t	2026-06-10 09:25:55.671736	2026-06-10 09:25:55.671736
3	BUSINESS	Fresh Foods Pvt Ltd	GST1003	contact@freshfoods.com	9000000003	Jaipur	t	2026-06-10 09:25:55.671736	2026-06-10 09:25:55.671736
4	BUSINESS	Frozen Mart	GST1004	contact@frozenmart.com	9000000004	Mumbai	t	2026-06-10 09:25:55.671736	2026-06-10 09:25:55.671736
5	BUSINESS	IceCube Logistics	GST1005	contact@icecube.com	9000000005	Ahmedabad	t	2026-06-10 09:25:55.671736	2026-06-10 09:25:55.671736
6	BUSINESS	Cold Chain India	GST1006	contact@coldchain.com	9000000006	Pune	t	2026-06-10 09:25:55.671736	2026-06-10 09:25:55.671736
7	BUSINESS	Nestle India	GST1007	contact@nestle.com	9000000007	Delhi	t	2026-06-10 09:25:55.671736	2026-06-10 09:25:55.671736
8	BUSINESS	Britannia	GST1008	contact@britannia.com	9000000008	Bengaluru	t	2026-06-10 09:25:55.671736	2026-06-10 09:25:55.671736
9	BUSINESS	Haldiram	GST1009	contact@haldiram.com	9000000009	Nagpur	t	2026-06-10 09:25:55.671736	2026-06-10 09:25:55.671736
10	BUSINESS	ITC Foods	GST1010	contact@itcfoods.com	9000000010	Kolkata	t	2026-06-10 09:25:55.671736	2026-06-10 09:25:55.671736
\.


--
-- Data for Name: damage_reports; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.damage_reports (damage_id, shipment_id, damage_percentage, description, reported_at, status) FROM stdin;
1	1	25.00	Front side dent	2026-06-14 20:44:54.242252	RESOLVED
\.


--
-- Data for Name: drivers; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.drivers (driver_id, full_name, date_of_birth, avatar_url, address, license_number, email, phone_number, prior_experience_years, employment_status, availability_status, joining_date, created_at, updated_at, user_id, is_active) FROM stdin;
2	Rohit Singh	1995-05-10	\N	Jaipur	RJDRV1001	rohit@fleetstat.com	9876543201	5	active	idle	2024-01-10	2026-06-10 09:22:33.02691	2026-06-10 09:22:33.02691	2	t
3	Aman Verma	1997-02-15	\N	Delhi	RJDRV1002	aman@fleetstat.com	9876543202	3	active	idle	2024-02-12	2026-06-10 09:22:33.02691	2026-06-10 09:22:33.02691	3	t
4	Karan Sharma	1993-08-20	\N	Mumbai	RJDRV1003	karan@fleetstat.com	9876543203	8	active	idle	2023-11-05	2026-06-10 09:22:33.02691	2026-06-10 09:22:33.02691	4	t
5	Raj Meena	1998-11-11	\N	Ajmer	RJDRV1004	raj@fleetstat.com	9876543204	2	active	idle	2024-03-20	2026-06-10 09:22:33.02691	2026-06-10 09:22:33.02691	5	t
6	Vikas Kumar	1994-07-14	\N	Kota	RJDRV1005	vikas@fleetstat.com	9876543205	6	active	idle	2023-09-15	2026-06-10 09:22:33.02691	2026-06-10 09:22:33.02691	6	t
7	Suresh Yadav	1992-01-25	\N	Udaipur	RJDRV1006	suresh@fleetstat.com	9876543206	10	active	idle	2023-06-01	2026-06-10 09:22:33.02691	2026-06-10 09:22:33.02691	7	t
8	Deepak Joshi	1996-06-18	\N	Jodhpur	RJDRV1007	deepak@fleetstat.com	9876543207	4	active	idle	2024-01-18	2026-06-10 09:22:33.02691	2026-06-10 09:22:33.02691	8	t
9	Manoj Gupta	1991-12-30	\N	Bikaner	RJDRV1008	manoj@fleetstat.com	9876543208	12	active	idle	2023-04-12	2026-06-10 09:22:33.02691	2026-06-10 09:22:33.02691	9	t
33	Rahul Sharma	1995-05-20	\N	Jaipur	DL123456789	rahul@example.com	9876543210	5	inactive	idle	2025-01-01	2026-06-12 17:57:41.37555	2026-06-12 18:02:20.784436	1	f
36	John	2000-01-01	\N	\N	DL-JOHN-001	\N	9999999999	0	active	idle	2019-01-01	2026-06-14 11:17:21.32786	2026-06-14 11:17:21.32786	23	t
\.


--
-- Data for Name: fuel_logs; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.fuel_logs (fuel_log_id, truck_id, trip_id, fuel_amount, fuel_cost, filled_at) FROM stdin;
1	1	1	42.00	4200.00	2026-06-10 09:30:41.273513
2	2	2	210.00	21000.00	2026-06-10 09:30:41.273513
3	3	3	24.00	2400.00	2026-06-10 09:30:41.273513
4	4	4	95.00	9500.00	2026-06-10 09:30:41.273513
5	5	5	75.00	7500.00	2026-06-10 09:30:41.273513
6	6	6	60.00	6000.00	2026-06-10 09:30:41.273513
7	7	7	38.00	3800.00	2026-06-10 09:30:41.273513
8	8	8	125.00	12500.00	2026-06-10 09:30:41.273513
9	9	9	76.00	7600.00	2026-06-10 09:30:41.273513
10	10	10	86.00	8600.00	2026-06-10 09:30:41.273513
11	1	11	41.00	4100.00	2026-06-10 09:30:41.273513
12	2	12	212.00	21200.00	2026-06-10 09:30:41.273513
13	3	13	25.00	2500.00	2026-06-10 09:30:41.273513
14	4	14	96.00	9600.00	2026-06-10 09:30:41.273513
15	5	15	74.00	7400.00	2026-06-10 09:30:41.273513
16	6	16	59.00	5900.00	2026-06-10 09:30:41.273513
17	7	17	37.00	3700.00	2026-06-10 09:30:41.273513
18	8	18	126.00	12600.00	2026-06-10 09:30:41.273513
19	9	19	77.00	7700.00	2026-06-10 09:30:41.273513
20	10	20	85.00	8500.00	2026-06-10 09:30:41.273513
21	1	21	20.00	2000.00	2026-06-10 09:30:41.273513
22	2	22	21.00	2100.00	2026-06-10 09:30:41.273513
23	3	23	34.00	3400.00	2026-06-10 09:30:41.273513
24	4	24	35.00	3500.00	2026-06-10 09:30:41.273513
25	5	25	32.00	3200.00	2026-06-10 09:30:41.273513
26	6	26	31.00	3100.00	2026-06-10 09:30:41.273513
27	7	27	36.00	3600.00	2026-06-10 09:30:41.273513
28	8	28	37.00	3700.00	2026-06-10 09:30:41.273513
29	9	29	82.00	8200.00	2026-06-10 09:30:41.273513
30	10	30	83.00	8300.00	2026-06-10 09:30:41.273513
31	1	33	40.00	4200.00	2026-06-14 19:05:25.895951
\.


--
-- Data for Name: payments; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.payments (payment_id, shipment_id, amount, payment_method, payment_status, payment_date, remarks) FROM stdin;
1	1	25000.00	BANK_TRANSFER	SUCCESS	2026-06-10 09:30:32.692318	\N
2	1	25000.00	BANK_TRANSFER	SUCCESS	2026-06-10 09:30:32.692318	\N
3	2	30000.00	UPI	SUCCESS	2026-06-10 09:30:32.692318	\N
4	2	30000.00	UPI	SUCCESS	2026-06-10 09:30:32.692318	\N
5	3	40000.00	BANK_TRANSFER	SUCCESS	2026-06-10 09:30:32.692318	\N
6	3	45000.00	BANK_TRANSFER	SUCCESS	2026-06-10 09:30:32.692318	\N
7	4	25000.00	UPI	SUCCESS	2026-06-10 09:30:32.692318	\N
8	4	22000.00	UPI	SUCCESS	2026-06-10 09:30:32.692318	\N
9	5	35000.00	BANK_TRANSFER	SUCCESS	2026-06-10 09:30:32.692318	\N
10	5	28000.00	BANK_TRANSFER	SUCCESS	2026-06-10 09:30:32.692318	\N
11	6	300000.00	BANK_TRANSFER	SUCCESS	2026-06-10 09:30:32.692318	\N
12	6	400000.00	BANK_TRANSFER	SUCCESS	2026-06-10 09:30:32.692318	\N
13	7	50000.00	UPI	SUCCESS	2026-06-10 09:30:32.692318	\N
14	7	62000.00	BANK_TRANSFER	SUCCESS	2026-06-10 09:30:32.692318	\N
15	8	35000.00	BANK_TRANSFER	SUCCESS	2026-06-10 09:30:32.692318	\N
16	8	45000.00	BANK_TRANSFER	SUCCESS	2026-06-10 09:30:32.692318	\N
17	9	45000.00	UPI	SUCCESS	2026-06-10 09:30:32.692318	\N
18	9	35000.00	UPI	SUCCESS	2026-06-10 09:30:32.692318	\N
19	10	28000.00	BANK_TRANSFER	SUCCESS	2026-06-10 09:30:32.692318	\N
20	10	30000.00	BANK_TRANSFER	SUCCESS	2026-06-10 09:30:32.692318	\N
21	11	48000.00	BANK_TRANSFER	SUCCESS	2026-06-10 09:30:32.692318	\N
22	11	65000.00	BANK_TRANSFER	SUCCESS	2026-06-10 09:30:32.692318	\N
23	12	26000.00	UPI	SUCCESS	2026-06-10 09:30:32.692318	\N
24	12	22000.00	UPI	SUCCESS	2026-06-10 09:30:32.692318	\N
25	13	30000.00	BANK_TRANSFER	SUCCESS	2026-06-10 09:30:32.692318	\N
26	13	36000.00	BANK_TRANSFER	SUCCESS	2026-06-10 09:30:32.692318	\N
27	14	60000.00	BANK_TRANSFER	SUCCESS	2026-06-10 09:30:32.692318	\N
28	14	30000.00	BANK_TRANSFER	SUCCESS	2026-06-10 09:30:32.692318	\N
29	15	300000.00	BANK_TRANSFER	SUCCESS	2026-06-10 09:30:32.692318	\N
30	15	300000.00	BANK_TRANSFER	SUCCESS	2026-06-10 09:30:32.692318	\N
31	16	62000.00	UPI	SUCCESS	2026-06-10 09:30:32.692318	\N
32	16	52000.00	UPI	SUCCESS	2026-06-10 09:30:32.692318	\N
33	17	55000.00	BANK_TRANSFER	SUCCESS	2026-06-10 09:30:32.692318	\N
34	17	26000.00	BANK_TRANSFER	SUCCESS	2026-06-10 09:30:32.692318	\N
35	18	38000.00	UPI	SUCCESS	2026-06-10 09:30:32.692318	\N
36	18	32000.00	UPI	SUCCESS	2026-06-10 09:30:32.692318	\N
37	19	35000.00	BANK_TRANSFER	SUCCESS	2026-06-10 09:30:32.692318	\N
38	19	45000.00	BANK_TRANSFER	SUCCESS	2026-06-10 09:30:32.692318	\N
39	20	300000.00	BANK_TRANSFER	SUCCESS	2026-06-10 09:30:32.692318	\N
40	20	300000.00	BANK_TRANSFER	SUCCESS	2026-06-10 09:30:32.692318	\N
\.


--
-- Data for Name: shipment_items; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.shipment_items (item_id, shipment_id, item_name, quantity, weight_kg, declared_value, temperature_required) FROM stdin;
1	1	Milk Crates	50	1000.00	50000.00	4.00
2	1	Butter Boxes	20	400.00	20000.00	4.00
3	2	Ice Cream	100	800.00	60000.00	-18.00
4	2	Frozen Pizza	50	600.00	45000.00	-18.00
5	3	Milk Crates	60	1200.00	55000.00	4.00
6	3	Cheese Packs	40	300.00	30000.00	4.00
7	4	Yogurt Cups	200	500.00	25000.00	4.00
8	4	Butter Boxes	25	450.00	22000.00	4.00
9	5	Frozen Peas	150	900.00	35000.00	-18.00
10	5	Frozen Corn	100	700.00	28000.00	-18.00
11	6	Vaccines	10	50.00	500000.00	2.00
12	6	Medical Samples	20	20.00	200000.00	2.00
13	7	Ice Cream	120	850.00	62000.00	-18.00
14	7	Frozen Pizza	70	650.00	50000.00	-18.00
15	8	Milk Crates	40	900.00	45000.00	4.00
16	8	Cheese Packs	50	350.00	35000.00	4.00
17	9	Frozen Berries	100	500.00	45000.00	-18.00
18	9	Frozen Vegetables	120	700.00	35000.00	-18.00
19	10	Butter Boxes	40	500.00	28000.00	4.00
20	10	Milk Crates	30	700.00	30000.00	4.00
21	11	Frozen Pizza	60	700.00	48000.00	-18.00
22	11	Ice Cream	90	800.00	65000.00	-18.00
23	12	Yogurt Cups	250	600.00	26000.00	4.00
24	12	Butter Boxes	30	450.00	22000.00	4.00
25	13	Frozen Corn	120	750.00	30000.00	-18.00
26	13	Frozen Peas	140	850.00	36000.00	-18.00
27	14	Milk Crates	70	1300.00	60000.00	4.00
28	14	Cheese Packs	40	350.00	30000.00	4.00
29	15	Vaccines	8	40.00	450000.00	2.00
30	15	Medical Samples	15	15.00	150000.00	2.00
31	16	Ice Cream	100	750.00	62000.00	-18.00
32	16	Frozen Pizza	80	700.00	52000.00	-18.00
33	17	Milk Crates	60	1200.00	55000.00	4.00
34	17	Butter Boxes	35	500.00	26000.00	4.00
35	18	Frozen Vegetables	130	850.00	38000.00	-18.00
36	18	Frozen Corn	120	700.00	32000.00	-18.00
37	19	Cheese Packs	50	400.00	35000.00	4.00
38	19	Milk Crates	40	900.00	45000.00	4.00
39	20	Vaccines	12	60.00	600000.00	2.00
40	20	Medical Samples	25	25.00	250000.00	2.00
\.


--
-- Data for Name: shipments; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.shipments (shipment_id, container_id, sender_customer_id, receiver_customer_id, shipment_status, received_date, shipped_date, delivered_date, notes, created_at, updated_at, trip_id) FROM stdin;
1	1	1	2	DELIVERED	2026-01-01	2026-01-01	2026-01-01	\N	2026-06-10 09:29:44.314995	2026-06-10 09:29:44.314995	1
2	2	3	4	DELIVERED	2026-01-01	2026-01-01	2026-01-01	\N	2026-06-10 09:29:44.314995	2026-06-10 09:29:44.314995	1
3	3	5	6	DELIVERED	2026-01-02	2026-01-02	2026-01-03	\N	2026-06-10 09:29:44.314995	2026-06-10 09:29:44.314995	2
4	4	7	8	DELIVERED	2026-01-02	2026-01-02	2026-01-03	\N	2026-06-10 09:29:44.314995	2026-06-10 09:29:44.314995	2
5	5	9	10	DELIVERED	2026-01-03	2026-01-03	2026-01-03	\N	2026-06-10 09:29:44.314995	2026-06-10 09:29:44.314995	3
6	6	1	3	DELIVERED	2026-01-04	2026-01-04	2026-01-04	\N	2026-06-10 09:29:44.314995	2026-06-10 09:29:44.314995	4
7	7	2	5	DELIVERED	2026-01-04	2026-01-04	2026-01-04	\N	2026-06-10 09:29:44.314995	2026-06-10 09:29:44.314995	4
8	8	4	6	DELIVERED	2026-01-05	2026-01-05	2026-01-05	\N	2026-06-10 09:29:44.314995	2026-06-10 09:29:44.314995	5
9	9	7	9	DELIVERED	2026-01-06	2026-01-06	2026-01-06	\N	2026-06-10 09:29:44.314995	2026-06-10 09:29:44.314995	6
10	10	8	10	DELIVERED	2026-01-07	2026-01-07	2026-01-07	\N	2026-06-10 09:29:44.314995	2026-06-10 09:29:44.314995	7
11	11	1	8	DELIVERED	2026-01-08	2026-01-08	2026-01-08	\N	2026-06-10 09:29:44.314995	2026-06-10 09:29:44.314995	8
12	12	2	9	DELIVERED	2026-01-08	2026-01-08	2026-01-08	\N	2026-06-10 09:29:44.314995	2026-06-10 09:29:44.314995	8
13	13	3	10	DELIVERED	2026-01-09	2026-01-09	2026-01-09	\N	2026-06-10 09:29:44.314995	2026-06-10 09:29:44.314995	9
14	14	4	1	DELIVERED	2026-01-10	2026-01-10	2026-01-10	\N	2026-06-10 09:29:44.314995	2026-06-10 09:29:44.314995	10
15	15	5	2	DELIVERED	2026-01-10	2026-01-10	2026-01-10	\N	2026-06-10 09:29:44.314995	2026-06-10 09:29:44.314995	10
16	1	6	3	DELIVERED	2026-01-11	2026-01-11	2026-01-11	\N	2026-06-10 09:29:44.314995	2026-06-10 09:29:44.314995	11
17	2	7	4	DELIVERED	2026-01-12	2026-01-12	2026-01-12	\N	2026-06-10 09:29:44.314995	2026-06-10 09:29:44.314995	12
18	3	8	5	DELIVERED	2026-01-13	2026-01-13	2026-01-13	\N	2026-06-10 09:29:44.314995	2026-06-10 09:29:44.314995	13
19	4	9	6	DELIVERED	2026-01-14	2026-01-14	2026-01-14	\N	2026-06-10 09:29:44.314995	2026-06-10 09:29:44.314995	14
20	5	10	7	DELIVERED	2026-01-15	2026-01-15	2026-01-15	\N	2026-06-10 09:29:44.314995	2026-06-10 09:29:44.314995	15
21	1	1	2	CANCELLED	2026-06-12	2026-06-13	2026-06-15	Updated shipment details	2026-06-12 19:59:21.745921	2026-06-12 20:29:54.534769	1
\.


--
-- Data for Name: trip_assignments; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.trip_assignments (assignment_id, trip_id, driver_id, assigned_at) FROM stdin;
82	2	3	2026-06-10 10:28:17.17458
83	3	4	2026-06-10 10:28:17.17458
84	4	5	2026-06-10 10:28:17.17458
85	5	6	2026-06-10 10:28:17.17458
86	6	7	2026-06-10 10:28:17.17458
87	7	8	2026-06-10 10:28:17.17458
88	8	9	2026-06-10 10:28:17.17458
89	9	2	2026-06-10 10:28:17.17458
90	10	3	2026-06-10 10:28:17.17458
91	11	4	2026-06-10 10:28:17.17458
92	12	5	2026-06-10 10:28:17.17458
93	13	6	2026-06-10 10:28:17.17458
94	14	7	2026-06-10 10:28:17.17458
95	15	8	2026-06-10 10:28:17.17458
96	16	9	2026-06-10 10:28:17.17458
97	17	2	2026-06-10 10:28:17.17458
98	18	3	2026-06-10 10:28:17.17458
99	19	4	2026-06-10 10:28:17.17458
100	20	5	2026-06-10 10:28:17.17458
101	21	6	2026-06-10 10:28:17.17458
102	22	7	2026-06-10 10:28:17.17458
103	23	8	2026-06-10 10:28:17.17458
104	24	9	2026-06-10 10:28:17.17458
105	25	2	2026-06-10 10:28:17.17458
106	26	3	2026-06-10 10:28:17.17458
107	27	4	2026-06-10 10:28:17.17458
108	28	5	2026-06-10 10:28:17.17458
109	29	6	2026-06-10 10:28:17.17458
110	30	7	2026-06-10 10:28:17.17458
111	2	4	2026-06-10 10:28:17.17458
112	4	6	2026-06-10 10:28:17.17458
113	8	8	2026-06-10 10:28:17.17458
114	10	9	2026-06-10 10:28:17.17458
115	12	2	2026-06-10 10:28:17.17458
116	14	3	2026-06-10 10:28:17.17458
117	18	5	2026-06-10 10:28:17.17458
118	20	7	2026-06-10 10:28:17.17458
119	24	8	2026-06-10 10:28:17.17458
120	30	9	2026-06-10 10:28:17.17458
123	1	2	2026-06-12 20:39:55.597594
124	1	36	2026-06-14 16:26:07.585258
125	32	36	2026-06-14 18:21:23.508337
126	33	36	2026-06-14 18:52:57.247519
\.


--
-- Data for Name: trips; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.trips (trip_id, truck_id, start_location, end_location, trip_distance, fuel_used, start_time, end_time, trip_status, created_at, updated_at, actual_start_time, actual_end_time) FROM stdin;
1	1	Jaipur	Delhi	280.00	42.00	2026-01-01 06:00:00	2026-01-01 12:00:00	COMPLETED	2026-06-10 09:26:29.59422	2026-06-10 09:26:29.59422	\N	\N
2	2	Delhi	Mumbai	1400.00	210.00	2026-01-02 05:00:00	2026-01-03 04:00:00	COMPLETED	2026-06-10 09:26:29.59422	2026-06-10 09:26:29.59422	\N	\N
3	3	Mumbai	Pune	160.00	24.00	2026-01-03 08:00:00	2026-01-03 12:00:00	COMPLETED	2026-06-10 09:26:29.59422	2026-06-10 09:26:29.59422	\N	\N
4	4	Ahmedabad	Jaipur	660.00	95.00	2026-01-04 05:30:00	2026-01-04 18:00:00	COMPLETED	2026-06-10 09:26:29.59422	2026-06-10 09:26:29.59422	\N	\N
5	5	Kota	Delhi	500.00	75.00	2026-01-05 06:00:00	2026-01-05 16:00:00	COMPLETED	2026-06-10 09:26:29.59422	2026-06-10 09:26:29.59422	\N	\N
6	6	Jaipur	Udaipur	400.00	60.00	2026-01-06 07:00:00	2026-01-06 15:00:00	COMPLETED	2026-06-10 09:26:29.59422	2026-06-10 09:26:29.59422	\N	\N
7	7	Delhi	Chandigarh	250.00	38.00	2026-01-07 08:00:00	2026-01-07 13:00:00	COMPLETED	2026-06-10 09:26:29.59422	2026-06-10 09:26:29.59422	\N	\N
8	8	Mumbai	Nagpur	820.00	125.00	2026-01-08 05:00:00	2026-01-08 19:00:00	COMPLETED	2026-06-10 09:26:29.59422	2026-06-10 09:26:29.59422	\N	\N
9	9	Nagpur	Hyderabad	500.00	76.00	2026-01-09 07:00:00	2026-01-09 17:00:00	COMPLETED	2026-06-10 09:26:29.59422	2026-06-10 09:26:29.59422	\N	\N
10	10	Hyderabad	Bengaluru	570.00	86.00	2026-01-10 06:00:00	2026-01-10 17:00:00	COMPLETED	2026-06-10 09:26:29.59422	2026-06-10 09:26:29.59422	\N	\N
11	1	Delhi	Jaipur	280.00	41.00	2026-01-11 06:00:00	2026-01-11 12:00:00	COMPLETED	2026-06-10 09:26:29.59422	2026-06-10 09:26:29.59422	\N	\N
12	2	Mumbai	Delhi	1400.00	212.00	2026-01-12 05:00:00	2026-01-13 04:00:00	COMPLETED	2026-06-10 09:26:29.59422	2026-06-10 09:26:29.59422	\N	\N
13	3	Pune	Mumbai	160.00	25.00	2026-01-13 08:00:00	2026-01-13 12:00:00	COMPLETED	2026-06-10 09:26:29.59422	2026-06-10 09:26:29.59422	\N	\N
14	4	Jaipur	Ahmedabad	660.00	96.00	2026-01-14 05:30:00	2026-01-14 18:00:00	COMPLETED	2026-06-10 09:26:29.59422	2026-06-10 09:26:29.59422	\N	\N
15	5	Delhi	Kota	500.00	74.00	2026-01-15 06:00:00	2026-01-15 16:00:00	COMPLETED	2026-06-10 09:26:29.59422	2026-06-10 09:26:29.59422	\N	\N
16	6	Udaipur	Jaipur	400.00	59.00	2026-01-16 07:00:00	2026-01-16 15:00:00	COMPLETED	2026-06-10 09:26:29.59422	2026-06-10 09:26:29.59422	\N	\N
17	7	Chandigarh	Delhi	250.00	37.00	2026-01-17 08:00:00	2026-01-17 13:00:00	COMPLETED	2026-06-10 09:26:29.59422	2026-06-10 09:26:29.59422	\N	\N
18	8	Nagpur	Mumbai	820.00	126.00	2026-01-18 05:00:00	2026-01-18 19:00:00	COMPLETED	2026-06-10 09:26:29.59422	2026-06-10 09:26:29.59422	\N	\N
19	9	Hyderabad	Nagpur	500.00	77.00	2026-01-19 07:00:00	2026-01-19 17:00:00	COMPLETED	2026-06-10 09:26:29.59422	2026-06-10 09:26:29.59422	\N	\N
20	10	Bengaluru	Hyderabad	570.00	85.00	2026-01-20 06:00:00	2026-01-20 17:00:00	COMPLETED	2026-06-10 09:26:29.59422	2026-06-10 09:26:29.59422	\N	\N
21	1	Jaipur	Ajmer	140.00	20.00	2026-01-21 08:00:00	2026-01-21 11:00:00	COMPLETED	2026-06-10 09:26:29.59422	2026-06-10 09:26:29.59422	\N	\N
22	2	Ajmer	Jaipur	140.00	21.00	2026-01-22 08:00:00	2026-01-22 11:00:00	COMPLETED	2026-06-10 09:26:29.59422	2026-06-10 09:26:29.59422	\N	\N
23	3	Delhi	Agra	230.00	34.00	2026-01-23 07:00:00	2026-01-23 12:00:00	COMPLETED	2026-06-10 09:26:29.59422	2026-06-10 09:26:29.59422	\N	\N
24	4	Agra	Delhi	230.00	35.00	2026-01-24 07:00:00	2026-01-24 12:00:00	COMPLETED	2026-06-10 09:26:29.59422	2026-06-10 09:26:29.59422	\N	\N
25	5	Pune	Nashik	210.00	32.00	2026-01-25 08:00:00	2026-01-25 13:00:00	COMPLETED	2026-06-10 09:26:29.59422	2026-06-10 09:26:29.59422	\N	\N
26	6	Nashik	Pune	210.00	31.00	2026-01-26 08:00:00	2026-01-26 13:00:00	COMPLETED	2026-06-10 09:26:29.59422	2026-06-10 09:26:29.59422	\N	\N
27	7	Jaipur	Kota	250.00	36.00	2026-01-27 07:00:00	2026-01-27 12:00:00	COMPLETED	2026-06-10 09:26:29.59422	2026-06-10 09:26:29.59422	\N	\N
28	8	Kota	Jaipur	250.00	37.00	2026-01-28 07:00:00	2026-01-28 12:00:00	COMPLETED	2026-06-10 09:26:29.59422	2026-06-10 09:26:29.59422	\N	\N
29	9	Delhi	Lucknow	550.00	82.00	2026-01-29 05:00:00	2026-01-29 16:00:00	COMPLETED	2026-06-10 09:26:29.59422	2026-06-10 09:26:29.59422	\N	\N
30	10	Lucknow	Delhi	550.00	83.00	2026-01-30 05:00:00	2026-01-30 16:00:00	COMPLETED	2026-06-10 09:26:29.59422	2026-06-10 09:26:29.59422	\N	\N
31	1	Jaipur	Delhi	280.00	35.00	2026-06-12 08:00:00	2026-06-12 13:30:00	CANCELLED	2026-06-12 18:33:31.094237	2026-06-12 19:26:18.106108	\N	\N
32	1	Jaipur	Delhi	280.00	0.00	2026-06-14 18:21:09.50664	2026-06-15 00:21:09.50664	COMPLETED	2026-06-14 18:21:09.50664	2026-06-14 18:21:09.50664	2026-06-14 18:23:56.868695	2026-06-14 18:25:25.744545
33	1	Jaipur	Delhi	280.00	0.00	2026-06-14 18:52:06.734452	2026-06-15 00:52:06.734452	IN_PROGRESS	2026-06-14 18:52:06.734452	2026-06-14 18:52:06.734452	2026-06-14 18:53:05.216035	\N
\.


--
-- Data for Name: truck_services; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.truck_services (service_id, truck_id, service_center, service_date, service_cost, next_due_date, description, created_at) FROM stdin;
1	1	Tata Service Jaipur	2026-01-15	12000.00	2026-07-15	Routine maintenance	2026-06-10 09:30:49.975446
2	2	Leyland Service Delhi	2026-01-16	18000.00	2026-07-16	Engine inspection	2026-06-10 09:30:49.975446
3	3	Eicher Service Mumbai	2026-01-17	10000.00	2026-07-17	Oil change	2026-06-10 09:30:49.975446
4	4	Tata Service Ahmedabad	2026-01-18	22000.00	2026-07-18	Brake servicing	2026-06-10 09:30:49.975446
5	5	BharatBenz Service Delhi	2026-01-19	15000.00	2026-07-19	General maintenance	2026-06-10 09:30:49.975446
6	6	Mahindra Service Jaipur	2026-01-20	13000.00	2026-07-20	Filter replacement	2026-06-10 09:30:49.975446
7	7	Leyland Service Chandigarh	2026-01-21	11000.00	2026-07-21	Tyre inspection	2026-06-10 09:30:49.975446
8	8	Tata Service Mumbai	2026-01-22	16000.00	2026-07-22	Cooling system check	2026-06-10 09:30:49.975446
9	9	Eicher Service Nagpur	2026-01-23	25000.00	2026-07-23	Major maintenance	2026-06-10 09:30:49.975446
10	10	BharatBenz Service Bengaluru	2026-01-24	21000.00	2026-07-24	Engine overhaul	2026-06-10 09:30:49.975446
11	1	Tata Service Jaipur	2026-03-15	9000.00	2026-09-15	Oil change	2026-06-10 09:30:49.975446
12	2	Leyland Service Delhi	2026-03-18	14000.00	2026-09-18	Tyre replacement	2026-06-10 09:30:49.975446
13	5	BharatBenz Service Delhi	2026-03-20	12000.00	2026-09-20	Brake inspection	2026-06-10 09:30:49.975446
14	8	Tata Service Mumbai	2026-03-22	15000.00	2026-09-22	Cooling service	2026-06-10 09:30:49.975446
15	10	BharatBenz Service Bengaluru	2026-03-25	17000.00	2026-09-25	Routine maintenance	2026-06-10 09:30:49.975446
\.


--
-- Data for Name: trucks; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.trucks (truck_id, license_plate, manufacturer, model, purchase_date, purchase_cost, capacity_tons, total_distance_travelled, truck_condition, status, last_service_date, description, created_at, updated_at, is_active) FROM stdin;
1	RJ14TR1001	Tata	Ultra T16	2023-01-10	2500000.00	16.00	45000.00	GOOD	ACTIVE	\N	\N	2026-06-10 09:22:39.660724	2026-06-10 09:22:39.660724	t
2	RJ14TR1002	Ashok Leyland	AVTR 1920	2023-03-15	3200000.00	20.00	52000.00	GOOD	ACTIVE	\N	\N	2026-06-10 09:22:39.660724	2026-06-10 09:22:39.660724	t
3	RJ14TR1003	Eicher	Pro 3015	2023-05-12	2400000.00	15.00	38000.00	GOOD	ACTIVE	\N	\N	2026-06-10 09:22:39.660724	2026-06-10 09:22:39.660724	t
4	RJ14TR1004	Tata	Signa 2823	2022-11-10	4200000.00	28.00	68000.00	GOOD	ACTIVE	\N	\N	2026-06-10 09:22:39.660724	2026-06-10 09:22:39.660724	t
5	RJ14TR1005	BharatBenz	1923R	2023-02-20	3600000.00	19.00	47000.00	GOOD	ACTIVE	\N	\N	2026-06-10 09:22:39.660724	2026-06-10 09:22:39.660724	t
6	RJ14TR1006	Mahindra	Blazo X	2023-06-01	3000000.00	18.00	41000.00	GOOD	ACTIVE	\N	\N	2026-06-10 09:22:39.660724	2026-06-10 09:22:39.660724	t
7	RJ14TR1007	Ashok Leyland	Boss 1415	2023-04-10	2700000.00	14.00	36000.00	GOOD	ACTIVE	\N	\N	2026-06-10 09:22:39.660724	2026-06-10 09:22:39.660724	t
8	RJ14TR1008	Tata	Ultra 1518	2022-12-15	2900000.00	15.00	56000.00	GOOD	ACTIVE	\N	\N	2026-06-10 09:22:39.660724	2026-06-10 09:22:39.660724	t
9	RJ14TR1009	Eicher	Pro 6048	2023-01-25	5000000.00	40.00	72000.00	GOOD	ACTIVE	\N	\N	2026-06-10 09:22:39.660724	2026-06-10 09:22:39.660724	t
10	RJ14TR1010	BharatBenz	2823C	2023-07-01	4500000.00	28.00	31000.00	GOOD	ACTIVE	\N	\N	2026-06-10 09:22:39.660724	2026-06-10 09:22:39.660724	t
20	RJ14TR1067	Tata	Ultra T16 Updated	2023-01-10	2600000.00	16.00	50000.00	GOOD	OUT_OF_SERVICE	2026-06-01	Updated truck details	2026-06-12 14:18:29.88403	2026-06-12 15:23:53.88082	f
21	RJ14TR2001	Tata	Ultra T16	2025-01-01	2500000.00	16.00	0.00	GOOD	OUT_OF_SERVICE	\N	\N	2026-06-12 18:03:18.620772	2026-06-12 18:04:21.876195	f
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (user_id, username, email, password_hash, role, is_active, created_at, updated_at) FROM stdin;
2	rohit_driver	rohit@fleetstat.com	$2b$12$B1b2C3d4E5f6G7h8I9j0K1LmNoPqRsTuVwXyZ123456	driver	t	2026-06-10 09:22:25.88082	2026-06-10 09:22:25.88082
3	aman_driver	aman@fleetstat.com	$2b$12$C1b2C3d4E5f6G7h8I9j0K1LmNoPqRsTuVwXyZ123456	driver	t	2026-06-10 09:22:25.88082	2026-06-10 09:22:25.88082
4	karan_driver	karan@fleetstat.com	$2b$12$D1b2C3d4E5f6G7h8I9j0K1LmNoPqRsTuVwXyZ123456	driver	t	2026-06-10 09:22:25.88082	2026-06-10 09:22:25.88082
5	raj_driver	raj@fleetstat.com	$2b$12$E1b2C3d4E5f6G7h8I9j0K1LmNoPqRsTuVwXyZ123456	driver	t	2026-06-10 09:22:25.88082	2026-06-10 09:22:25.88082
6	vikas_driver	vikas@fleetstat.com	$2b$12$F1b2C3d4E5f6G7h8I9j0K1LmNoPqRsTuVwXyZ123456	driver	t	2026-06-10 09:22:25.88082	2026-06-10 09:22:25.88082
7	suresh_driver	suresh@fleetstat.com	$2b$12$G1b2C3d4E5f6G7h8I9j0K1LmNoPqRsTuVwXyZ123456	driver	t	2026-06-10 09:22:25.88082	2026-06-10 09:22:25.88082
8	deepak_driver	deepak@fleetstat.com	$2b$12$H1b2C3d4E5f6G7h8I9j0K1LmNoPqRsTuVwXyZ123456	driver	t	2026-06-10 09:22:25.88082	2026-06-10 09:22:25.88082
9	manoj_driver	manoj@fleetstat.com	$2b$12$I1b2C3d4E5f6G7h8I9j0K1LmNoPqRsTuVwXyZ123456	driver	t	2026-06-10 09:22:25.88082	2026-06-10 09:22:25.88082
10	support_admin	support@fleetstat.com	$2b$12$J1b2C3d4E5f6G7h8I9j0K1LmNoPqRsTuVwXyZ123456	admin	t	2026-06-10 09:22:25.88082	2026-06-10 09:22:25.88082
12	mayank_driver	mayankdriver@fleetstat.com	dummyhash	driver	t	2026-06-11 19:00:15.308038	2026-06-11 19:00:15.308038
17	john_doe	john@example.com	johnpassword123	driver	f	2026-06-13 11:17:17.583299	2026-06-13 11:27:22.715669
23	john	john2@example.com	$2b$12$8vX2LXzmH6H6jSUxzSNNS.VGIdNrJWQiSsYj3HNGyD6h3Qw72w1nO	driver	t	2026-06-13 22:26:36.419176	2026-06-13 22:26:36.419176
1	mayank	mayank@gmail.com	$2b$12$xisu7AaEEM5G6J.TairrgONMCzrc/v6dXSaOfdPAOrXBiOMNqf73a	admin	t	2026-06-10 09:22:25.88082	2026-06-15 06:41:10.092544
\.


--
-- Data for Name: vehicles; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.vehicles (vehicle_id, registration_number, vehicle_type, manufacturer, model, year, fuel_type, capacity, status, created_at, updated_at) FROM stdin;
1	RJ14AB1234	Truck	Tata	Ace Gold	2024	Diesel	1500	active	2026-06-11 20:34:07.052357	2026-06-11 20:34:07.052357
\.


--
-- Name: container_assignments_assignment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.container_assignments_assignment_id_seq', 35, true);


--
-- Name: containers_container_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.containers_container_id_seq', 15, true);


--
-- Name: customers_customer_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.customers_customer_id_seq', 10, true);


--
-- Name: damage_reports_damage_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.damage_reports_damage_id_seq', 1, true);


--
-- Name: driver_driver_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.driver_driver_id_seq', 36, true);


--
-- Name: fuel_logs_fuel_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.fuel_logs_fuel_log_id_seq', 31, true);


--
-- Name: payments_payment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.payments_payment_id_seq', 40, true);


--
-- Name: shipment_items_item_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.shipment_items_item_id_seq', 40, true);


--
-- Name: shipments_shipment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.shipments_shipment_id_seq', 21, true);


--
-- Name: trip_assignments_assignment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.trip_assignments_assignment_id_seq', 126, true);


--
-- Name: trips_trip_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.trips_trip_id_seq', 33, true);


--
-- Name: truck_services_service_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.truck_services_service_id_seq', 15, true);


--
-- Name: trucks_truck_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.trucks_truck_id_seq', 21, true);


--
-- Name: users_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_user_id_seq', 23, true);


--
-- Name: vehicles_vehicle_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.vehicles_vehicle_id_seq', 1, true);


--
-- Name: container_assignments container_assignments_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.container_assignments
    ADD CONSTRAINT container_assignments_pkey PRIMARY KEY (assignment_id);


--
-- Name: containers containers_container_code_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.containers
    ADD CONSTRAINT containers_container_code_key UNIQUE (container_code);


--
-- Name: containers containers_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.containers
    ADD CONSTRAINT containers_pkey PRIMARY KEY (container_id);


--
-- Name: customers customers_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.customers
    ADD CONSTRAINT customers_pkey PRIMARY KEY (customer_id);


--
-- Name: damage_reports damage_reports_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.damage_reports
    ADD CONSTRAINT damage_reports_pkey PRIMARY KEY (damage_id);


--
-- Name: drivers driver_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.drivers
    ADD CONSTRAINT driver_email_key UNIQUE (email);


--
-- Name: drivers driver_licence_number_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.drivers
    ADD CONSTRAINT driver_licence_number_key UNIQUE (license_number);


--
-- Name: drivers driver_phone_no_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.drivers
    ADD CONSTRAINT driver_phone_no_key UNIQUE (phone_number);


--
-- Name: drivers driver_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.drivers
    ADD CONSTRAINT driver_pkey PRIMARY KEY (driver_id);


--
-- Name: drivers drivers_user_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.drivers
    ADD CONSTRAINT drivers_user_id_key UNIQUE (user_id);


--
-- Name: fuel_logs fuel_logs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fuel_logs
    ADD CONSTRAINT fuel_logs_pkey PRIMARY KEY (fuel_log_id);


--
-- Name: payments payments_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.payments
    ADD CONSTRAINT payments_pkey PRIMARY KEY (payment_id);


--
-- Name: shipment_items shipment_items_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.shipment_items
    ADD CONSTRAINT shipment_items_pkey PRIMARY KEY (item_id);


--
-- Name: shipments shipments_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.shipments
    ADD CONSTRAINT shipments_pkey PRIMARY KEY (shipment_id);


--
-- Name: trip_assignments trip_assignments_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.trip_assignments
    ADD CONSTRAINT trip_assignments_pkey PRIMARY KEY (assignment_id);


--
-- Name: trips trips_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.trips
    ADD CONSTRAINT trips_pkey PRIMARY KEY (trip_id);


--
-- Name: truck_services truck_services_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.truck_services
    ADD CONSTRAINT truck_services_pkey PRIMARY KEY (service_id);


--
-- Name: trucks trucks_license_plate_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.trucks
    ADD CONSTRAINT trucks_license_plate_key UNIQUE (license_plate);


--
-- Name: trucks trucks_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.trucks
    ADD CONSTRAINT trucks_pkey PRIMARY KEY (truck_id);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- Name: vehicles vehicles_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.vehicles
    ADD CONSTRAINT vehicles_pkey PRIMARY KEY (vehicle_id);


--
-- Name: vehicles vehicles_registration_number_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.vehicles
    ADD CONSTRAINT vehicles_registration_number_key UNIQUE (registration_number);


--
-- Name: idx_assignment_driver; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_assignment_driver ON public.trip_assignments USING btree (driver_id);


--
-- Name: idx_assignment_trip; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_assignment_trip ON public.trip_assignments USING btree (trip_id);


--
-- Name: idx_container_assignments_container; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_container_assignments_container ON public.container_assignments USING btree (container_id);


--
-- Name: idx_container_assignments_trip; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_container_assignments_trip ON public.container_assignments USING btree (trip_id);


--
-- Name: idx_damage_reports_shipment; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_damage_reports_shipment ON public.damage_reports USING btree (shipment_id);


--
-- Name: idx_drivers_user; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_drivers_user ON public.drivers USING btree (user_id);


--
-- Name: idx_fuel_logs_trip; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_fuel_logs_trip ON public.fuel_logs USING btree (trip_id);


--
-- Name: idx_fuel_logs_truck; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_fuel_logs_truck ON public.fuel_logs USING btree (truck_id);


--
-- Name: idx_payment_shipment; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_payment_shipment ON public.payments USING btree (shipment_id);


--
-- Name: idx_payments_shipment; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_payments_shipment ON public.payments USING btree (shipment_id);


--
-- Name: idx_shipment_items_shipment; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_shipment_items_shipment ON public.shipment_items USING btree (shipment_id);


--
-- Name: idx_shipment_receiver; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_shipment_receiver ON public.shipments USING btree (receiver_customer_id);


--
-- Name: idx_shipment_sender; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_shipment_sender ON public.shipments USING btree (sender_customer_id);


--
-- Name: idx_shipments_container; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_shipments_container ON public.shipments USING btree (container_id);


--
-- Name: idx_shipments_receiver; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_shipments_receiver ON public.shipments USING btree (receiver_customer_id);


--
-- Name: idx_shipments_sender; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_shipments_sender ON public.shipments USING btree (sender_customer_id);


--
-- Name: idx_trip_assignments_driver; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_trip_assignments_driver ON public.trip_assignments USING btree (driver_id);


--
-- Name: idx_trip_assignments_trip; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_trip_assignments_trip ON public.trip_assignments USING btree (trip_id);


--
-- Name: idx_trip_truck; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_trip_truck ON public.trips USING btree (truck_id);


--
-- Name: idx_trips_truck; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_trips_truck ON public.trips USING btree (truck_id);


--
-- Name: idx_truck_services_truck; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_truck_services_truck ON public.truck_services USING btree (truck_id);


--
-- Name: containers trg_containers_updated_at; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trg_containers_updated_at BEFORE UPDATE ON public.containers FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


--
-- Name: customers trg_customers_updated_at; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trg_customers_updated_at BEFORE UPDATE ON public.customers FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


--
-- Name: drivers trg_drivers_updated_at; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trg_drivers_updated_at BEFORE UPDATE ON public.drivers FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


--
-- Name: shipments trg_shipments_updated_at; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trg_shipments_updated_at BEFORE UPDATE ON public.shipments FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


--
-- Name: trucks trg_trucks_updated_at; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trg_trucks_updated_at BEFORE UPDATE ON public.trucks FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


--
-- Name: users trg_users_updated_at; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER trg_users_updated_at BEFORE UPDATE ON public.users FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


--
-- Name: container_assignments container_assignments_container_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.container_assignments
    ADD CONSTRAINT container_assignments_container_id_fkey FOREIGN KEY (container_id) REFERENCES public.containers(container_id) ON DELETE CASCADE;


--
-- Name: container_assignments container_assignments_trip_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.container_assignments
    ADD CONSTRAINT container_assignments_trip_id_fkey FOREIGN KEY (trip_id) REFERENCES public.trips(trip_id) ON DELETE CASCADE;


--
-- Name: damage_reports damage_reports_shipment_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.damage_reports
    ADD CONSTRAINT damage_reports_shipment_id_fkey FOREIGN KEY (shipment_id) REFERENCES public.shipments(shipment_id) ON DELETE CASCADE;


--
-- Name: drivers fk_driver_user; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.drivers
    ADD CONSTRAINT fk_driver_user FOREIGN KEY (user_id) REFERENCES public.users(user_id) ON DELETE CASCADE;


--
-- Name: shipments fk_shipment_trip; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.shipments
    ADD CONSTRAINT fk_shipment_trip FOREIGN KEY (trip_id) REFERENCES public.trips(trip_id);


--
-- Name: fuel_logs fuel_logs_trip_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fuel_logs
    ADD CONSTRAINT fuel_logs_trip_id_fkey FOREIGN KEY (trip_id) REFERENCES public.trips(trip_id);


--
-- Name: fuel_logs fuel_logs_truck_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fuel_logs
    ADD CONSTRAINT fuel_logs_truck_id_fkey FOREIGN KEY (truck_id) REFERENCES public.trucks(truck_id);


--
-- Name: payments payments_shipment_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.payments
    ADD CONSTRAINT payments_shipment_id_fkey FOREIGN KEY (shipment_id) REFERENCES public.shipments(shipment_id) ON DELETE CASCADE;


--
-- Name: shipment_items shipment_items_shipment_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.shipment_items
    ADD CONSTRAINT shipment_items_shipment_id_fkey FOREIGN KEY (shipment_id) REFERENCES public.shipments(shipment_id) ON DELETE CASCADE;


--
-- Name: shipments shipments_container_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.shipments
    ADD CONSTRAINT shipments_container_id_fkey FOREIGN KEY (container_id) REFERENCES public.containers(container_id);


--
-- Name: shipments shipments_receiver_customer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.shipments
    ADD CONSTRAINT shipments_receiver_customer_id_fkey FOREIGN KEY (receiver_customer_id) REFERENCES public.customers(customer_id);


--
-- Name: shipments shipments_sender_customer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.shipments
    ADD CONSTRAINT shipments_sender_customer_id_fkey FOREIGN KEY (sender_customer_id) REFERENCES public.customers(customer_id);


--
-- Name: trip_assignments trip_assignments_driver_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.trip_assignments
    ADD CONSTRAINT trip_assignments_driver_id_fkey FOREIGN KEY (driver_id) REFERENCES public.drivers(driver_id) ON DELETE CASCADE;


--
-- Name: trip_assignments trip_assignments_trip_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.trip_assignments
    ADD CONSTRAINT trip_assignments_trip_id_fkey FOREIGN KEY (trip_id) REFERENCES public.trips(trip_id) ON DELETE CASCADE;


--
-- Name: trips trips_truck_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.trips
    ADD CONSTRAINT trips_truck_id_fkey FOREIGN KEY (truck_id) REFERENCES public.trucks(truck_id);


--
-- Name: truck_services truck_services_truck_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.truck_services
    ADD CONSTRAINT truck_services_truck_id_fkey FOREIGN KEY (truck_id) REFERENCES public.trucks(truck_id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

\unrestrict 87bLNqGxPQDok9nQ4cnTPaQSnNpEDJlxf5ORAWdafxQaF2YQ4Z5kbeYgwmkdD3z

