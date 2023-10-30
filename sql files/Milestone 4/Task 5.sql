SELECT
	s.store_type,
	ROUND(TOTAL(p."product_price (£)" * o.product_quantity),2) AS total_sales,
	ROUND((TOTAL(p."product_price (£)" * o.product_quantity) / (SELECT TOTAL(p."product_price (£)" * o.product_quantity) FROM orders_table AS o JOIN dim_products AS p ON o.product_code = p.product_code) *100),2) AS "percentage_total(%)"
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
GROUP BY
	s.store_type
ORDER BY
	total_sales DESC