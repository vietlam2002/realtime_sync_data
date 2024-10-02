from kafka import KafkaConsumer
import json
import psycopg2
from datetime import datetime, timedelta

# Config connector PostgreSQL
conn_params = {
    'dbname': 'postgres',
    'user': 'postgres',
    'password': 'password',
    'host': 'localhost',
    'port': '3000'
}
conn = psycopg2.connect(**conn_params)
cursor = conn.cursor()

# Create Kafka Consumer
consumer = KafkaConsumer(
    'demo.public.dev_data_integration_pipeline_load_data_from_postgres_v1',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='unique_consumer_group_test',
    value_deserializer=lambda x: json.loads(x.decode('utf-8')) if x is not None else None
)

print("Listening to topic...")

# Save to PostgreSQL
def save_to_postgres(data, operation):
    try:
        order_date_raw = data["order_date"]
        order_date = datetime(1970, 1, 1) + timedelta(days=order_date_raw)

        if operation == 'c' or operation == 'u':  
            insert_query = """
            INSERT INTO public.test_orders (order_id, customer_name, customer_phone, delivery_address, food_item, order_date, quantity, total_price) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (order_id) 
            DO UPDATE SET 
                customer_name = EXCLUDED.customer_name,
                customer_phone = EXCLUDED.customer_phone,
                delivery_address = EXCLUDED.delivery_address,
                food_item = EXCLUDED.food_item,
                order_date = EXCLUDED.order_date,
                quantity = EXCLUDED.quantity,
                total_price = EXCLUDED.total_price;
            """
            cursor.execute(insert_query, (data["order_id"], data["customer_name"], data["customer_phone"], data["delivery_address"], data["food_item"], order_date, data["quantity"], data["total_price"]))
        elif operation == 'd':  
            delete_query = """
            DELETE FROM public.test_orders WHERE order_id = %s;
            """
            cursor.execute(delete_query, (data["order_id"],))
        conn.commit()
        print(f"Saved data to Postgres: {data}")
    except Exception as e:
        print(f"Error saving to Postgres: {e}")
        conn.rollback()


# Data transform Kafka messages
for message in consumer:
    if message.value is not None:
        # print(f"Received message: {message.value}")
        # print(f"Partition: {message.partition}, Offset: {message.offset}, Timestamp: {message.timestamp}")
        
        operation = message.value.get('op') 
        after_data = message.value.get('after')  
        before_data = message.value.get('before')  
        
        if operation in ['c', 'u'] and after_data:
            save_to_postgres(after_data, operation)  
        elif operation == 'd' and before_data:
            save_to_postgres(before_data, operation)  

# Close connect
cursor.close()
conn.close()
