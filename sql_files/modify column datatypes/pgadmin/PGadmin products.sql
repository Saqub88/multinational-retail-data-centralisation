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
ALTER COLUMN "EAN" TYPE varchar(17),
ALTER COLUMN product_code TYPE varchar(255),
ALTER COLUMN date_added TYPE date,
ALTER COLUMN uuid TYPE uuid USING uuid::uuid,
DROP COLUMN removed;