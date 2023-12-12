Create temp view total_sales_view AS
SELECT
	SUM(p.product_price * o.product_quantity) AS total_sales
FROM 
	orders_table AS o
JOIN
	dim_products AS p
ON
	o.product_code = p.product_code;

SELECT
	s.store_type,
	ROUND(CAST(SUM(p.product_price * o.product_quantity)as numeric),2) AS total_sales,
	ROUND(CAST((SUM(p.product_price * o.product_quantity)/(SELECT total_sales FROM total_sales_view)*100) as numeric),2) AS "percentage_total(%)"
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
	total_sales DESC;