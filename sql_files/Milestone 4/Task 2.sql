SELECT
	locality,
    count(*) AS total_no_stores
FROM
	dim_store_details
GROUP BY
	locality
HAVING
	count(*) >= 10
ORDER BY
	total_no_stores DESC;

/*

SQlite

SELECT
	locality,
    count(*) AS total_no_stores
FROM
	dim_store_details
GROUP BY
	locality
HAVING
	count(*) >= 10
ORDER BY
	total_no_stores DESC
*/