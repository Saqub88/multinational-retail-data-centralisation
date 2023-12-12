CREATE TEMP VIEW tempview_avg_intervals_between_orders AS
SELECT
	year,
	LEAD(date_time) OVER (ORDER BY date_time ASC) - date_time AS time_diff_between_orders
FROM(
	SELECT
		*,
		CAST(year||'-'||month||'-'||day||' '||"timestamp" as timestamp) AS date_time
	FROM
		dim_date_times
	);

SELECT
	year,
	'"hours": '||SUBSTR(AVG_time,2,1)||', "minutes": '||SUBSTR(AVG_time,4,2)||', "seconds": '||SUBSTR(AVG_time,7,2)||', "milliseconds": '||SUBSTR(AVG_time,10,2) AS actual_time_taken
FROM
	(SELECT
		year,
		CAST(AVG(time_diff_between_orders) AS text) AS AVG_time,
	 	AVG(time_diff_between_orders) AS time_taken
	FROM
		tempview_avg_intervals_between_orders
	GROUP BY
		year)
ORDER BY
	time_taken DESC