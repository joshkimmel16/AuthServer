CREATE DATABASE auth;

\c auth

/*
username = username for the given user. This should be unique on a per-application basis.
password = password for the given user.
salt = salt used for password hashing.
usermetadata = JSON blob describing the user. Need to figure out best data type for this.
INDEXED on id
*/
CREATE TABLE users (
    id bigint,
    username text NOT NULL,
    password text NOT NULL,
    salt text NOT NULL,
    usermetadata text,
    PRIMARY KEY (id)
);

/*
app_name = name of application using Auth server as SSO platform. This should be unique.
secret = private key passed to application for JWT signature validation.
algorithm = hashing algorithm to use for JWT signature generation.
INDEXED on id
*/
CREATE TABLE applications (
    id bigint,
    app_name text NOT NULL,
    secret text NOT NULL,
    algorithm text NOT NULL,
    PRIMARY KEY (app_name)
);

/* STORED PROCEDURES */

/* CREATE */

/*create user*/
CREATE OR REPLACE FUNCTION create_user (name text, pass text, slt text, meta text)
    RETURNS bigint AS 
$$
DECLARE 
    var_count integer; 
    var_max bigint;
BEGIN
    SELECT COUNT(*) INTO var_count FROM users;
    IF var_count = 0 THEN
        INSERT INTO users (id, username, password, salt, usermetadata) VALUES (1, name, pass, slt, meta);
        RETURN 1;
    ELSE
        SELECT MAX(id) INTO var_max FROM users;
        INSERT INTO users (id, username, password, salt, usermetadata) VALUES ((var_max + 1), name, pass, slt, meta);
        RETURN (var_max + 1);
    END IF;
END; $$
LANGUAGE PLPGSQL;

/*create application*/
CREATE OR REPLACE FUNCTION create_application (name text, sec text, alg text)
    RETURNS bigint AS 
$$
DECLARE 
    var_count integer; 
    var_max bigint;
BEGIN
    SELECT COUNT(*) INTO var_count FROM applications;
    IF var_count = 0 THEN
        INSERT INTO applications (id, app_name, secret, algorithm) VALUES (1, name, sec, alg);
        RETURN 1;
    ELSE
        SELECT MAX(id) INTO var_max FROM applications;
        INSERT INTO applications (id, app_name, secret, algorithm) VALUES ((var_max + 1), name, sec, alg);
        RETURN (var_max + 1);
    END IF;
END; $$
LANGUAGE PLPGSQL;


/* UPDATE */

/*update username*/
CREATE OR REPLACE FUNCTION update_username (var_id bigint, var_name text)
    RETURNS void AS 
$$
BEGIN
    UPDATE users SET username=var_name WHERE id=var_id;
END; $$
LANGUAGE PLPGSQL;

/*update password*/
CREATE OR REPLACE FUNCTION update_password (var_id bigint, var_pass text, var_salt text)
    RETURNS void AS 
$$
BEGIN
    UPDATE users SET password=var_pass, salt=var_salt WHERE id=var_id;
END; $$
LANGUAGE PLPGSQL;

/*update metadata*/
CREATE OR REPLACE FUNCTION update_usermetadata (var_id bigint, var_meta text)
    RETURNS void AS 
$$
BEGIN
    UPDATE users SET usermetadata=var_meta WHERE id=var_id;
END; $$
LANGUAGE PLPGSQL;

/*update appname*/
CREATE OR REPLACE FUNCTION update_appname (var_id bigint, var_name text)
    RETURNS void AS 
$$
BEGIN
    UPDATE applications SET app_name=var_name WHERE id=var_id;
END; $$
LANGUAGE PLPGSQL;

/*update algorithm*/
CREATE OR REPLACE FUNCTION update_appalgorithm (var_id bigint, var_alg text)
    RETURNS void AS 
$$
BEGIN
    UPDATE applications SET algorithm=var_alg WHERE id=var_id;
END; $$
LANGUAGE PLPGSQL;


/* DELETE */

/*delete user*/
CREATE OR REPLACE FUNCTION delete_user (var_id bigint)
    RETURNS void AS 
$$
BEGIN
    DELETE FROM users WHERE id=var_id;
END; $$
LANGUAGE PLPGSQL;

/*delete application*/
CREATE OR REPLACE FUNCTION delete_application (var_id bigint)
    RETURNS void AS 
$$
BEGIN
    DELETE FROM applications WHERE id=var_id;
END; $$
LANGUAGE PLPGSQL;