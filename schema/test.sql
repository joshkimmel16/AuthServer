CREATE DATABASE IF NOT EXISTS unittests;

\c unittests

/*
this table is used to run unit tests for the data layer.
*/
DROP TABLE IF EXISTS testing;
CREATE TABLE testing (
    col1 text,
    col2 text
);

/*
this function is used for testing in data layer
*/
CREATE OR REPLACE FUNCTION test_function (c1 text, c2 text)
    RETURNS integer AS 
$$
DECLARE 
    var_count integer; 
BEGIN
    SELECT COUNT(*) INTO var_count FROM testing;
    INSERT INTO testing (col1, col2) VALUES (c1, c2);
    RETURN var_count;
END; $$
LANGUAGE PLPGSQL;