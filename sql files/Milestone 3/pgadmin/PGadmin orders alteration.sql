ALTER TABLE public.orders_table
ALTER COLUMN index TYPE bigint,
ALTER COLUMN date_uuid TYPE uuid USING date_uuid::uuid,
ALTER COLUMN user_uuid TYPE uuid USING user_uuid::uuid,
ALTER COLUMN card_number TYPE varchar(19),
ALTER COLUMN store_code TYPE varchar(12),
ALTER COLUMN product_code TYPE varchar(11),
ALTER COLUMN product_quantity TYPE smallint
