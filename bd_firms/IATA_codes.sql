-- Table: public.routes

-- DROP TABLE public.routes;

CREATE TABLE public.IATA_codes
(
    IATA_id integer NOT NULL GENERATED BY DEFAULT AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    IATA_dep character varying(3) COLLATE pg_catalog."default",
    IATA_arr character varying(3) COLLATE pg_catalog."default",
    CONSTRAINT pk_IATA_codes PRIMARY KEY (IATA_id)
)

TABLESPACE pg_default;

ALTER TABLE public.IATA_codes
    OWNER to postgres;