ALTER TABLE dim_products RENAME TO x_dim_products;

CREATE TABLE dim_products(
	product_price FLOAT,
	weight FLOAT,
	EAN varchar(17),
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