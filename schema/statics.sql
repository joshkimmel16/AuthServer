CREATE DATABASE statics;

\c statics

/*
asset_key = name of the static asset in question.
asset_value = value of the static asset in question (type conversion should be done on the front end)
*/
DROP TABLE IF EXISTS assets;
CREATE TABLE assets (
    page text NOT NULL,
    component text NOT NULL,
    asset_key text NOT NULL,
    asset_value text NOT NULL
);

/* STORED PROCEDURES */

/*create an asset*/
CREATE OR REPLACE FUNCTION create_asset (pg text, comp text, name text, val text)
    RETURNS void AS
$$
BEGIN
    INSERT INTO assets (page, component, asset_key, asset_value) VALUES (pg, comp, name, val);
END; $$
LANGUAGE PLPGSQL;

/*retrieve all assets as JSON string*/
CREATE OR REPLACE FUNCTION get_assets (pg text)
    RETURNS table (
        result json
    ) AS
$$
BEGIN
    RETURN QUERY
    SELECT row_to_json(assets) FROM assets WHERE assets.page=pg;
END; $$
LANGUAGE PLPGSQL;