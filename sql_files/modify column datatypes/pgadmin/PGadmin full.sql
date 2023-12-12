ALTER TABLE public.dim_users
ALTER COLUMN first_name TYPE VARCHAR(255),
ALTER COLUMN last_name TYPE VARCHAR(255),
ALTER COLUMN date_of_birth TYPE date,
ALTER COLUMN country_code TYPE VARCHAR(2),
ALTER COLUMN user_uuid TYPE uuid USING user_uuid::uuid,
ALTER COLUMN join_date TYPE date;

ALTER TABLE public.dim_card_details
ALTER COLUMN card_number TYPE VARCHAR(19),
ALTER COLUMN expiry_date TYPE VARCHAR(5),
ALTER COLUMN date_payment_confirmed TYPE date;

ALTER TABLE public.dim_date_times
ALTER COLUMN month TYPE VARCHAR(2),
ALTER COLUMN year TYPE VARCHAR(4),
ALTER COLUMN day TYPE VARCHAR(2),
ALTER COLUMN time_period TYPE VARCHAR(10),
ALTER COLUMN date_uuid TYPE uuid USING date_uuid::uuid;

ALTER TABLE public.orders_table
ALTER COLUMN index TYPE bigint,
ALTER COLUMN date_uuid TYPE uuid USING date_uuid::uuid,
ALTER COLUMN user_uuid TYPE uuid USING user_uuid::uuid,
ALTER COLUMN card_number TYPE varchar(19),
ALTER COLUMN store_code TYPE varchar(12),
ALTER COLUMN product_code TYPE varchar(11),
ALTER COLUMN product_quantity TYPE smallint;

ALTER TABLE public.dim_products
ADD COLUMN weight_class varchar(14),
ADD COLUMN still_available boolean;

UPDATE public.dim_products 
SET weight_class = CASE
	WHEN weight < 2 THEN 'Light'
	WHEN weight >= 2 AND weight < 40 THEN 'Mid_Sized'
	WHEN weight >= 40 AND weight < 140 THEN 'Heavy'
	ELSE 'Truck_Required' 
    END;

UPDATE public.dim_products
SET still_available = CASE
	WHEN "removed" = 'Still_available' THEN True
	WHEN "removed" = 'Removed' THEN False
    END;

ALTER TABLE public.dim_products
ALTER COLUMN product_price TYPE FLOAT,
ALTER COLUMN weight TYPE FLOAT,
ALTER COLUMN "EAN" TYPE varchar(13),
ALTER COLUMN product_code TYPE varchar(255),
ALTER COLUMN date_added TYPE date,
ALTER COLUMN uuid TYPE uuid USING uuid::uuid,
DROP COLUMN removed;

ALTER TABLE public.dim_store_details
ALTER COLUMN longitude TYPE float,
ALTER COLUMN locality TYPE varchar(255),
ALTER COLUMN store_code TYPE varchar(12),
ALTER COLUMN staff_numbers TYPE smallint,
ALTER COLUMN opening_date TYPE date,
ALTER COLUMN store_type TYPE varchar(255),
ALTER COLUMN store_type DROP NOT NULL,
ALTER COLUMN latitude TYPE float,
ALTER COLUMN country_code TYPE varchar(2),
ALTER COLUMN continent TYPE varchar(255);

UPDATE
	dim_store_details
SET
	longitude = NULL,
	latitude = Null
	locality = 'N/A'
WHERE
	store_type = 'Web Portal';

ALTER TABLE public.dim_date_times ADD PRIMARY KEY (date_uuid);
ALTER TABLE public.dim_users ADD PRIMARY KEY (user_uuid);
ALTER TABLE public.dim_card_details ADD PRIMARY KEY (card_number);
ALTER TABLE public.dim_store_details ADD PRIMARY KEY (store_code);
ALTER TABLE public.dim_products ADD PRIMARY KEY (product_code);

ALTER TABLE public.orders_table
ADD CONSTRAINT fk_date FOREIGN KEY (date_uuid) REFERENCES public.dim_date_times (date_uuid),
ADD CONSTRAINT fk_users FOREIGN KEY (user_uuid) REFERENCES public.dim_users (user_uuid) NOT VALID,
ADD CONSTRAINT fk_cards FOREIGN KEY (card_number) REFERENCES public.dim_card_details (card_number) NOT VALID,
ADD CONSTRAINT fk_store FOREIGN KEY (store_code) REFERENCES public.dim_store_details (store_code) NOT VALID,
ADD CONSTRAINT fk_product FOREIGN KEY (product_code) REFERENCES public.dim_products (product_code) NOT VALID;