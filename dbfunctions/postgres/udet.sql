CREATE TABLE UDET (
u_id character varying (20) PRIMARY KEY not null,
u_name character varying (50) not null,
u_doj timestamp without time zone not null,
u_valid timestamp without time zone not null,
u_mail character varying (75),
u_cont character varying (25)
);