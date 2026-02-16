
 --GMV(总销售额）
SELECT 
    ROUND(SUM(payment_value),2) AS total_gmv
FROM order_payments;

 --总订单数
SELECT 
    COUNT(*) AS total_orders
FROM orders;

 --客单价（平均每笔订单支付金额）
SELECT 
    ROUND(AVG(payment_value),2) AS avg_order_value
FROM order_payments;

 --每月销售趋势（按月 GMV）
SELECT
    strftime('%Y-%m', o.order_purchase_timestamp) AS month,
    ROUND(SUM(p.payment_value),2) AS monthly_gmv
FROM orders o
JOIN order_payments p ON o.order_id = p.order_id
GROUP BY month
ORDER BY month;

 --各州销售额排行
SELECT
    c.customer_state,
    ROUND(SUM(p.payment_value),2) AS state_gmv
FROM customers c 
JOIN orders o ON c.customer_id = o.customer_id
JOIN order_payments p ON o.order_id = p.order_id
GROUP BY c.customer_state
ORDER BY state_gmv DESC;

SELECT * FROM order_payments LIMIT 5;
SELECT * FROM orders LIMIT 5;
SELECT * FROM customers LIMIT 5;
