import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#连接数据库
db_path = r"C:\\Users\\86159\\Desktop\\Business Data Analysis\\sql\\ecommerce.db"
conn = sqlite3.connect(db_path)

#读取数据
monthly_sales = pd.read_sql_query("""
SELECT strftime('%Y-%m', o.order_purchase_timestamp) AS month,
       SUM(p.payment_value) AS monthly_gmv
FROM orders o
JOIN order_payments p ON o.order_id = p.order_id
GROUP BY month
ORDER BY month;
""", conn)

state_sales = pd.read_sql_query("""
SELECT c.customer_state,
       SUM(p.payment_value) AS state_gmv
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN order_payments p ON o.order_id = p.order_id
GROUP BY c.customer_state
ORDER BY state_gmv DESC;
""", conn)

conn.close()

#可视化（字体）设置
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
#sns.set(style="whitegrid")

#月销售趋势
plt.figure(figsize=(12,6))
sns.lineplot(data=monthly_sales, x="month", y="monthly_gmv", marker="o")

plt.title("每月销售趋势")
plt.xlabel("月份")
plt.ylabel("GMV")
plt.xticks(rotation=0)

plt.tight_layout()
plt.savefig('月销售折线图.png')
plt.show()

#州销售趋势

top10 = state_sales.head(10)

plt.figure(figsize=(12,6))
sns.barplot(data=top10, x="state_gmv", y="customer_state")

plt.title("各州销售额 TOP10")
plt.xlabel("销售额")
plt.ylabel("州")

plt.tight_layout()
plt.savefig('州销售柱状图.png')
plt.show()