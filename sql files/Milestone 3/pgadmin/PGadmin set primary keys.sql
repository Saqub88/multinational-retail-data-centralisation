ALTER TABLE public.dim_date_times ADD PRIMARY KEY (date_uuid);
ALTER TABLE public.dim_users ADD PRIMARY KEY (user_uuid);
ALTER TABLE public.dim_card_details ADD PRIMARY KEY (card_number);
ALTER TABLE public.dim_store_details ADD PRIMARY KEY (store_code);
ALTER TABLE public.dim_products ADD PRIMARY KEY (product_code);