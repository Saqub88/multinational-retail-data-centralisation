ALTER TABLE dim_date_times RENAME TO x_dim_date_times;

CREATE TABLE dim_date_times(
	month varchar(2),
	year varchar(4),
	day varchar(2),
	time_period varchar(10),
	date_uuid uuid PRIMARY KEY);

INSERT INTO dim_date_times(month, year, day, time_period, date_uuid)
SELECT
	month, year, day, time_period, date_uuid
FROM
	x_dim_date_times
