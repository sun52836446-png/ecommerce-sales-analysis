import sqlite3
import pandas as pd
import os

# ---------- 1. 连接数据库 ----------
db_path = "C:\\Users\\86159\\Desktop\\Business Data Analysis\\sql\\ecommerce.db"
conn = sqlite3.connect(db_path)

# ---------- 2. 导入 CSV 数据 ----------
csv_folder = "C:\\Users\\86159\\Desktop\\Business Data Analysis\\data"

tables = [
    "customers", "orders", "order_payments", "products", "sellers",
    "category", "order_items", "order_reviews", "geolocation"
]

for table in tables:
    file_path = os.path.join(csv_folder, f"{table}.csv")
    if os.path.exists(file_path):
        # ---------- 清空表 ----------
        conn.execute(f"DELETE FROM {table};")
        conn.commit()

        df = pd.read_csv(file_path)

        # ---------- 修正 products 列名 ----------
        if table == "products":
            df.rename(columns={
                "product_name_lenght": "product_name_length",
                "product_description_lenght": "product_description_length"
            }, inplace=True)

        # ---------- 去重（以防 CSV 内部有重复主键） ----------
        if table == "customers":
            df = df.drop_duplicates(subset=['customer_id'])
        elif table == "orders":
            df = df.drop_duplicates(subset=['order_id'])
        elif table == "products":
            df = df.drop_duplicates(subset=['product_id'])
        elif table == "sellers":
            df = df.drop_duplicates(subset=['seller_id'])

        # ---------- 导入数据库 ----------
        df.to_sql(table, conn, if_exists='append', index=False)
        print(f"✅ {table} 导入完成, {len(df)} 条数据")
    else:
        print(f"⚠️ {table}.csv 文件不存在")

# ---------- 3. 分析指标 ----------
print("\n--- 分析结果 ---")

# 1️⃣ 总 GMV
total_gmv = pd.read_sql_query(
    "SELECT ROUND(SUM(payment_value),2) AS total_gmv FROM order_payments;", conn
)
print("总 GMV:", total_gmv['total_gmv'][0])

# 2️⃣ 客单价
avg_order_value = pd.read_sql_query(
    "SELECT ROUND(SUM(payment_value)/COUNT(DISTINCT order_id),2) AS avg_order_value FROM order_payments;", conn
)
print("客单价:", avg_order_value['avg_order_value'][0])

# 3️⃣ 每月销售趋势
monthly_gmv = pd.read_sql_query("""
SELECT strftime('%Y-%m', o.order_purchase_timestamp) AS month,
       ROUND(SUM(p.payment_value),2) AS monthly_gmv
FROM orders o
JOIN order_payments p ON o.order_id = p.order_id
GROUP BY month
ORDER BY month;
""", conn)
print("\n每月销售趋势:")
print(monthly_gmv)

# 4️⃣ 各州销售额排行
state_gmv = pd.read_sql_query("""
SELECT c.customer_state,
       ROUND(SUM(p.payment_value),2) AS state_gmv
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN order_payments p ON o.order_id = p.order_id
GROUP BY c.customer_state
ORDER BY state_gmv DESC;
""", conn)
print("\n各州销售额排行:")
print(state_gmv)

# 5️⃣ 活跃客户数
active_customers = pd.read_sql_query(
    "SELECT COUNT(DISTINCT customer_id) AS active_customers FROM orders;", conn
)
print("\n活跃客户数:", active_customers['active_customers'][0])

# ---------- 4. 关闭数据库 ----------
conn.close()
print("\n✅ 数据库连接关闭")
