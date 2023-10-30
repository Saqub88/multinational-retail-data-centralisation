SELECT
	TOTAL(p."product_price (£)" * o.product_quantity) AS total_sales,
	d.year,
	d.month
FROM
	orders_table AS o
JOIN
	dim_date_times AS d
ON
	o.date_uuid = d.date_uuid
JOIN
	dim_products AS p
ON
	o.product_code = p.product_code
GROUP BY
	d.year, d.month
ORDER BY
	total_sales DESC
LIMIT 10