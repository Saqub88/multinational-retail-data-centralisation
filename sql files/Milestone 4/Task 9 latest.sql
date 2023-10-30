SELECT
	year,
	count(*) AS num_orders,
	AVG(strftime('%s', new)-strftime('%s', signature)) AS diff
/*
	CAST(AVG(strftime('%s', new)-strftime('%s', signature))/3600 AS INT) AS diff_hours,
	CAST(AVG(strftime('%s', new)-strftime('%s', signature))%3600/60 AS INT) AS diff_mins,
	CAST(AVG(strftime('%s', new)-strftime('%s', signature))%3600%60 AS INT) AS diff_secs,
	CAST(AVG(strftime('%s', new)-strftime('%s', signature))*365*24*60*60*100%100 AS INT) AS diff_milsecs	
*/	
FROM
	(SELECT
		year,
		signature,
		LEAD(signature) OVER (ORDER BY signature ASC) as new
	FROM
		(SELECT
			year,
			datetime(year||'-'||month||'-'||day) as signature
		FROM dim_date_times))
GROUP BY
	year
--ORDER BY
--	diff DESC