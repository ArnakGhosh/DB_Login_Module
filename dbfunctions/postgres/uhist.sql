CREATE TABLE UHIST (
u_id character varying (20) not null,
u_pass character varying (100) not null,
u_valid_from timestamp without time zone not null,
u_valid_till timestamp without time zone not null,
PRIMARY KEY (u_id, u_pass, u_valid_from)
);