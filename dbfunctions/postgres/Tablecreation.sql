CREATE OR REPLACE FUNCTION create_if_not_exists (table_name text, create_stmt text)
RETURNS text AS
$_$
BEGIN

IF EXISTS (
    SELECT *
    FROM   pg_catalog.pg_tables 
    WHERE    tablename  = table_name
    ) THEN
   RETURN 'TABLE ' || '''' || table_name || '''' || ' ALREADY EXISTS';
ELSE
   EXECUTE create_stmt;
   RETURN 'CREATED';
END IF;

END;
$_$ LANGUAGE plpgsql;