import datetime
from json import loads
from typing import List

import clickhouse_connect
from clickhouse_connect.driver.client import Client
from kafka import KafkaConsumer

from config import get_settings


def create_db_client(host: str, port: int, username: str, password: str) -> Client:
    client = clickhouse_connect.get_client(host=host, port=port, username=username, password=password)
    print(f'Connected to clickhouse_connect')
    return client


def setup_db(client: Client, db_name: str, table_name: str) -> None:
    client.command(f'CREATE DATABASE IF NOT EXISTS {db_name}')
    client.command(f"""
    CREATE TABLE IF NOT EXISTS {db_name}.{table_name}
    (
        number UInt64,
        step UInt64,
        value UInt64,
        timestamp DateTime           
    ) 
                   ENGINE = MergeTree()
                   PRIMARY KEY (number, timestamp)
    """)
    print(f'Table created')


def create_kafka_consumer(topic_name: str, group_id: str, bootstrap_servers: List[str]) -> KafkaConsumer:
    my_consumer = KafkaConsumer(
        topic_name,
        bootstrap_servers=bootstrap_servers,
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id=group_id,
        value_deserializer=lambda x: loads(x.decode('utf-8')),
    )
    print(f'Consumer created')
    return my_consumer


if __name__ == "__main__":
    settings = get_settings()
    my_consumer = create_kafka_consumer(topic_name=settings.kafka_topic_name, group_id=settings.kafka_group_id,
                                        bootstrap_servers=settings.bootstrap_servers)
    client = create_db_client(settings.clickhouse_host, settings.clickhouse_port, settings.clickhouse_user,
                              settings.clickhouse_password)
    setup_db(client, settings.clickhouse_db, settings.clickhouse_table)
    for message in my_consumer:
        data = message.value
        client.insert(f'{settings.clickhouse_db}.{settings.clickhouse_table}', [
            [data['Number'], data['Step'], data['Value'], datetime.datetime.fromtimestamp(message.timestamp / 1e3)]],
                      column_names=['number', 'step', 'value', 'timestamp'])
