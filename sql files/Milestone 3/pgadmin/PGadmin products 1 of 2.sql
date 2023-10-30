ALTER TABLE public.dim_products
ADD COLUMN weight_class varchar(14);

UPDATE public.dim_products SET "weight_class" = 'Light' WHERE "weight (kg)" < 2;
UPDATE public.dim_products SET "weight_class" = 'Mid_Sized' WHERE "weight (kg)" >= 2 AND "weight (kg)" < 40;
UPDATE public.dim_products SET "weight_class" = 'Heavy' WHERE "weight (kg)" >= 40 AND "weight (kg)" < 140;
UPDATE public.dim_products SET "weight_class" = 'Truck_Required' WHERE "weight (kg)" >= 140;

ALTER TABLE public.dim_products
ALTER COLUMN product_price TYPE FLOAT,
ALTER COLUMN "weight (kg)" TYPE FLOAT,
ALTER COLUMN EAN TYPE varchar(13),
ALTER COLUMN product_code TYPE varchar(255),
ALTER COLUMN date_added TYPE date,
ALTER COLUMN uuid TYPE uuid,
ALTER COLUMN weight_class TYPE varchar(14);