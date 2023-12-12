SELECT
	COUNT(*) as number_of_sales,
	CAST(SUM(product_quantity) AS INT) AS product_quantity_count,
	CASE
	WHEN store_code = 'WEB-1388012W' THEN 'Web'
	else 'Offline'
	END AS location
FROM
	orders_table
GROUP BY
	location
ORDER BY
	product_quantity_count ASC
