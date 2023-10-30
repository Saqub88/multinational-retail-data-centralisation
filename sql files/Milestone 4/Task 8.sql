SELECT
	ROUND(TOTAL(p."product_price (£)" * o.product_quantity),2) AS total_sales,
	s.store_type,
	s.country_code
FROM
	orders_table AS o
JOIN
	dim_store_details AS s
ON
	o.store_code = s.store_code
JOIN
	dim_products AS p
ON
	o.product_code = p.product_code
WHERE
	s.country_code = 'DE'
GROUP BY
	s.store_type
ORDER BY
	total_sales ASC