ALTER TABLE dim_card_details RENAME TO x_dim_card_details;

CREATE TABLE dim_card_details(
	card_number varchar(19) PRIMARY KEY,
	expiry_date varchar(5),
	date_payment_confirmed date);

INSERT INTO dim_card_details(card_number, expiry_date, date_payment_confirmed)
SELECT card_number, expiry_date, date_payment_confirmed
FROM x_dim_card_details;

ALTER TABLE dim_date_times RENAME TO x_dim_date_times;

CREATE TABLE dim_date_times(
	month varchar(2),
	year varchar(4),
	day varchar(2),
	time_period varchar(10),
	date_uuid uuid PRIMARY KEY);

INSERT INTO dim_date_times(month, year, day, time_period, date_uuid)
SELECT
	month, year, day, time_period, date_uuid
FROM
	x_dim_date_times;

ALTER TABLE dim_products RENAME TO x_dim_products;

CREATE TABLE dim_products(
	product_price FLOAT,
	weight FLOAT,
	EAN varchar(13),
	product_code varchar(255) PRIMARY KEY,
	date_added date,
	uuid uuid,
	still_available boolean,
	weight_class varchar(14));

INSERT INTO
	dim_products(product_price, weight, EAN, product_code, date_added, uuid, still_available, weight_class)
SELECT
	product_price,
	weight,
	EAN,
	product_code,
	date_added,
	uuid,
	CASE
	WHEN removed = 'Still_available' THEN 1
	ELSE 0
	END AS still_available,
	CASE
	WHEN "weight" < 2 THEN 'Light'
	WHEN "weight" >= 2 AND "weight" < 40 THEN 'Mid_Sized'
	WHEN "weight" >= 40 AND "weight" < 140 THEN 'Heavy'
	ELSE 'Truck_Required' 
	END AS weight_class
FROM
	x_dim_products;

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
	store_type = 'Web Portal';

ALTER TABLE dim_users RENAME TO x_dim_users;

CREATE TABLE dim_users(
	first_name VARCHAR(255),
	last_name VARCHAR(255),
	date_of_birth DATE,
	country_code VARCHAR(2),
	user_uuid UUID PRIMARY KEY,
	join_date DATE);

INSERT INTO dim_users(first_name, last_name, date_of_birth, country_code, user_uuid, join_date)
SELECT first_name, last_name, date_of_birth, country_code, user_uuid, join_date
FROM x_dim_users;

PRAGMA foreign_keys = OFF;

ALTER TABLE orders_table RENAME TO x_orders_table;

CREATE TABLE orders_table(
	date_uuid uuid,
	user_uuid uuid,
	card_number varchar(19),
	store_code varchar(12),
	product_code varchar(11),
	product_quantity smallint,
	CONSTRAINT fk_date FOREIGN KEY (date_uuid) REFERENCES dim_date_times(date_uuid),
	CONSTRAINT fk_user FOREIGN KEY (user_uuid) REFERENCES dim_users(user_uuid),
	CONSTRAINT fk_card FOREIGN KEY (card_number) REFERENCES dim_card_details(card_number),
	CONSTRAINT fk_store FOREIGN KEY (store_code) REFERENCES dim_store_details(store_code),
	CONSTRAINT fk_product FOREIGN KEY (product_code) REFERENCES dim_products(product_code));

INSERT INTO orders_table(date_uuid, user_uuid, card_number, store_code, product_code, product_quantity)
SELECT
	date_uuid, user_uuid, card_number, store_code, product_code, product_quantity
FROM
	x_orders_table;

PRAGMA foreign_keys=on;