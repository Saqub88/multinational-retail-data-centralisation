SELECT
	year,
	signature,
	new,
	strftime('%s', new)-strftime('%s', signature) AS diff
FROM
	(SELECT
		year,
		strftime(signature) AS signature,
		strftime(LEAD(signature) OVER (ORDER BY signature ASC)) as new
	FROM
		(SELECT
			year,
			datetime(year||'-'||month||'-'||day||' '||timestamp) as signature
		FROM x_dim_date_times))
--GROUP BY
	--year