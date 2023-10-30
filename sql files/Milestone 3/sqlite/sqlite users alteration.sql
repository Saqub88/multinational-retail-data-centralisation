ALTER TABLE dim_users RENAME TO x_dim_users;

CREATE TABLE dim_users(
	first_name VARCHAR(255),
	last_name VARCHAR(255),
	date_of_birth DATE,
	country_code VARCHAR(2),
	user_uuid UUID PRIMARY KEY,
	join_date DATE);

INSERT INTO dim_users(first_name, last_name, date_of_birth, country_code, user_uuid, join_date)
SELECT first_name, last_name, date_of_birth, country_code, user_uuid, join_date
FROM x_dim_users