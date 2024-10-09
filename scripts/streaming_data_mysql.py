from kafka import KafkaComsumer
import json
import mysql.connector
from datetime import datetime, timedelta

def connect_to_mysql():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        port=6000
    )

#create Kafka consumer
consumer = KafkaConsumer(
    bootstrap_servers='localhost:9092',
    group_id='my-group',
    auto_offset_reset='earliest'
)

# I want a new function to transform from messages in kafka topic and return dataframe