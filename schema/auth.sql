CREATE DATABASE auth;

/*
username = username for the given user. This should be unique on a per-application basis.
password = password for the given user.
salt = salt used for password hashing.
usermetadata = JSON blob describing the user. Need to figure out best data type for this.
INDEXED on username
*/
CREATE TABLE users (
    username VARCHAR(80) NOT NULL,
    password VARCHAR(80) NOT NULL,
    usermetadata VARCHAR(1000)
    PRIMARY KEY (username)
);

/*
app_name = name of application using Auth server as SSO platform. This should be unique.
secret = private key passed to application for JWT signature validation.
algorithm = hashing algorithm to use for JWT signature generation.
INDEXED on app_name
*/
CREATE TABLE applications (
    app_name VARCHAR(100) NOT NULL,
    secret VARCHAR(1000) NOT NULL,
    algorithm VARCHAR(10) NOT NULL
    PRIMARY KEY (app_name)
);