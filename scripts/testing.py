import json
import psycopg2
from kafka import KafkaConsumer
from datetime import datetime, timedelta

# Cấu hình kết nối đến PostgreSQL
conn_params = {
    'dbname': 'postgres',
    'user': 'postgres',
    'password': 'password',
    'host': 'localhost',
    'port': '3000'  # Port PostgreSQL
}

# Kết nối tới PostgreSQL
try:
    conn = psycopg2.connect(**conn_params)
    cursor = conn.cursor()
    print("Kết nối tới PostgreSQL thành công.")
except Exception as e:
    print(f"Lỗi khi kết nối tới PostgreSQL: {e}")

# Tạo Kafka Consumer để lấy dữ liệu từ topic
consumer = KafkaConsumer(
    'demo.public.dev_data_integration_pipeline_load_data_from_postgres_v1',  # Tên Kafka topic
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',  # Đọc từ message đầu tiên
    enable_auto_commit=True,
    group_id='unique_consumer_group_test',
    value_deserializer=lambda x: json.loads(x.decode('utf-8')) if x is not None else None
)

print("Đang lắng nghe các message từ Kafka...")

# Hàm chèn dữ liệu vào PostgreSQL
def insert_data_to_postgres(data):
    try:
        # Chuyển đổi định dạng ngày từ timestamp (nếu có)
        order_date_raw = data.get("order_date", None)
        order_date = None
        if order_date_raw:
            order_date = datetime(1970, 1, 1) + timedelta(days=order_date_raw)

        # Câu truy vấn chèn dữ liệu vào PostgreSQL
        insert_query = """
        INSERT INTO public.test_orders (order_id, customer_name, customer_phone, delivery_address, food_item, order_date, quantity, total_price) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (
            data["order_id"], 
            data["customer_name"], 
            data["customer_phone"], 
            data["delivery_address"], 
            data["food_item"], 
            order_date, 
            data["quantity"], 
            data["total_price"]
        ))

        conn.commit()
        print(f"Đã chèn message vào Postgres: {data}")

    except Exception as e:
        print(f"Lỗi khi chèn dữ liệu vào Postgres: {e}")
        conn.rollback()

# Lắng nghe các message từ Kafka và lưu vào PostgreSQL
for message in consumer:
    if message.value is not None:
        print(f"Nhận được message: {message.value}")
        insert_data_to_postgres(message.value)  # Chèn dữ liệu vào PostgreSQL

# Đóng kết nối khi hoàn thành
cursor.close()
conn.close()
