-- Table: public.sizes

-- DROP TABLE public.sizes;

CREATE TABLE public.sizes
(
    sizes_id integer NOT NULL GENERATED BY DEFAULT AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    sizes_length numeric(10,2) NOT NULL,
    sizes_wings_spread numeric(10,2) NOT NULL,
    sizes_hull_width numeric(10,2),
    sizes_wings_thicc numeric(10,2),
    sizes_mass_empty numeric(10,2),
    sizes_mass_full numeric(10,2),
    CONSTRAINT sizes_pkey PRIMARY KEY (sizes_id)
)

TABLESPACE pg_default;

ALTER TABLE public.sizes
    OWNER to postgres;