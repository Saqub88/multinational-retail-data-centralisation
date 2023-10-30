ALTER TABLE public.orders_table
ADD CONSTRAINT fk_date FOREIGN KEY (date_uuid) REFERENCES public.dim_date_times (date_uuid),
ADD CONSTRAINT fk_users FOREIGN KEY (user_uuid) REFERENCES public.dim_users (user_uuid) NOT VALID,
ADD CONSTRAINT fk_cards FOREIGN KEY (card_number) REFERENCES public.dim_card_details (card_number) NOT VALID,
ADD CONSTRAINT fk_store FOREIGN KEY (store_code) REFERENCES public.dim_store_details (store_code) NOT VALID,
ADD CONSTRAINT fk_product FOREIGN KEY (product_code) REFERENCES public.dim_products (product_code) NOT VALID;