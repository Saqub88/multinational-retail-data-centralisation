SELECT
	ROUND(TOTAL(p."product_price (£)" * o.product_quantity),2) AS total_sales,
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
	d.month
ORDER BY
	total_sales DESC
LIMIT 6