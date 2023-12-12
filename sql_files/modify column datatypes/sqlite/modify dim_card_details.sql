ALTER TABLE dim_card_details RENAME TO x_dim_card_details;

CREATE TABLE dim_card_details(
	card_number varchar(19) PRIMARY KEY,
	expiry_date varchar(5),
	date_payment_confirmed date);

INSERT INTO dim_card_details(card_number, expiry_date, date_payment_confirmed)
SELECT card_number, expiry_date, date_payment_confirmed
FROM x_dim_card_details;