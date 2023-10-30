SELECT
	year,
	'"hours": '||diff_hours||', "minutes": '||diff_mins||', "seconds": '||diff_secs||', "milliseconds": '||diff_milsecs AS ATT
FROM
	(SELECT
		year,
		AVG(new-signature) AS sigsig,
		CAST(AVG(new-signature)*365*24%24 AS INT) AS diff_hours,
		CAST(AVG(new-signature)*365*24*60%60 AS INT) AS diff_mins,
		CAST(AVG(new-signature)*365*24*60*60%60 AS INT) AS diff_secs,
		CAST(AVG(new-signature)*365*24*60*60*100%100 AS INT) AS diff_milsecs
	FROM
		(SELECT year, signature,	LEAD(signature) OVER (ORDER BY signature ASC) as new
		FROM (SELECT	year, datetime(year||'-'||month||'-'||day||' '||timestamp) as signature FROM x_dim_date_times))
	GROUP BY year)
ORDER BY
	sigsig ASC