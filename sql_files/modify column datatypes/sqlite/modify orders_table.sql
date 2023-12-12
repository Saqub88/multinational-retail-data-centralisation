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