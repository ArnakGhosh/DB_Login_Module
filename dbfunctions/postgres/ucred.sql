CREATE TABLE UCRED (
u_id character varying (20) REFERENCES UDET(u_id),
u_pass character varying (100) not null,
u_retry integer,
u_reset integer
);