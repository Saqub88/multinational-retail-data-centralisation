ALTER TABLE dim_products RENAME TO x_products;

CREATE TABLE dim_products(
	"product_price (£)" FLOAT,
	"weight (kg)" FLOAT,
	EAN varchar(13),
	product_code varchar(255),
	date_added date,
	uuid uuid,
	still_available boolean,
	weight_class varchar(14));

INSERT INTO
	dim_products("product_price (£)", "weight (kg)", EAN, product_code, date_added, uuid, still_available, weight_class)
SELECT
	"product_price (£)",
	"weight (kg)",
	EAN,
	product_code,
	date_added,
	uuid,
	still_available,
	CASE
	WHEN "weight (kg)" < 2 THEN 'Light'
	WHEN "weight (kg)" >= 2 AND "weight (kg)" < 40 THEN 'Mid_Sized'
	WHEN "weight (kg)" >= 40 AND "weight (kg)" < 140 THEN 'Heavy'
	ELSE 'Truck_Required' 
	END AS weight_class
FROM
	x_products