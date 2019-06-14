CREATE TABLE ULOG (
op_id integer REFERENCES UOPS(op_id),
op_start timestamp without time zone,
op_end timestamp without time zone,
op_status character varying (10),
op_error character varying (200)
);