//calling create table procedure
select create_if_not_exists('uhist', 'CREATE TABLE UHIST (
u_id character varying (20) not null,
u_pass character varying (100) not null,
u_valid_from timestamp without time zone not null,
u_valid_till timestamp without time zone not null,
PRIMARY KEY (u_id, u_pass)
);');

//Madatory Data for running of application
INSERT INTO UOPS (op_id, op_desc, op_inac) values (1, 'New User Insert', 0);
INSERT INTO UOPS (op_id, op_desc, op_inac) values (2, 'Existing User Update', 0);
INSERT INTO UOPS (op_id, op_desc, op_inac) values (3, 'Existing User Deletion', 0);
INSERT INTO UOPS (op_id, op_desc, op_inac) values (4, 'Clearing History of logs', 0);

//Sample data, can be deleted afterwards
INSERT INTO UDET (u_id, u_name, u_doj, u_valid, u_mail, u_cont) values ('doejohn01','John Doe',Now()::timestamp,Now()::timestamp + interval '99999 days','johndoe1991@mail.com','+00-000-000-0000');
INSERT INTO UDET (u_id, u_name, u_doj, u_valid, u_mail, u_cont) values ('doejane01','Jane Doe',Now()::timestamp,Now()::timestamp + interval '99999 days','janedoe1991@mail.com','+00-000-000-0000');

INSERT INTO UCRED (u_id, u_pass, u_retry, u_reset) values ('doejohn01','S29sa2F0YUAxMjM=',0,0);
INSERT INTO UCRED (u_id, u_pass, u_retry, u_reset) values ('doejane01','S29sa2F0YUAxMjM=',0,0);

INSERT INTO UHIST (u_id, u_pass, u_valid_from, u_valid_till) values ('doejohn01','S29sa2F0YUAxMjM=',Now()::timestamp,Now()::timestamp + interval '2 days');
INSERT INTO UHIST (u_id, u_pass, u_valid_from, u_valid_till) values ('doejohn01','S29sa2F0YUAxMjM=',Now()::timestamp,Now()::timestamp + interval '2 days');