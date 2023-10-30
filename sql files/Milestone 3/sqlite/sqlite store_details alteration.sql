ALTER TABLE dim_store_details RENAME TO x_dim_store_details;

CREATE TABLE dim_store_details(
    longitude FLOAT,
    locality varchar(255),
    store_code varchar(12) PRIMARY KEY,
    staff_numbers smallint,
    opening_date date,
    store_type varchar(255) DEFAULT(NULL),
    latitude FLOAT,
    country_code varchar(2),
    continent varchar(255));

INSERT INTO dim_store_details(
    longitude, locality, store_code, staff_numbers, opening_date, store_type, latitude, country_code, continent)
SELECT
    longitude, locality, store_code, staff_numbers, opening_date, store_type, latitude, country_code, continent
FROM
    x_dim_store_details;

UPDATE
	dim_store_details
SET
	longitude = 'N/A',
    latitude = 'N/A'
WHERE
	store_type = 'Web Portal'