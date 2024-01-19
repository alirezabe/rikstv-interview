import random
from json import dumps
from typing import List

from kafka import KafkaProducer
from kafka.admin import KafkaAdminClient, NewTopic

from config import get_settings


def check_has_topic(topic_name: str, boostrap_servers: List[str]) -> bool:
    admin_client = KafkaAdminClient(
        bootstrap_servers=boostrap_servers,
    )
    topic_list = admin_client.list_topics()
    print(f'Topics: {topic_list}')
    if topic_name in topic_list:
        return True
    return False


def create_topic(topic_name: str, partitions: int, replication_factor: int, boostrap_servers: List[str]) -> None:
    admin_client = KafkaAdminClient(
        bootstrap_servers=boostrap_servers,
    )
    new_topic = [NewTopic(name=topic_name, num_partitions=partitions,
                          replication_factor=replication_factor)]
    admin_client.create_topics(new_topics=new_topic, validate_only=False)
    print(f'topic created: {new_topic}')


def create_producer(boostrap_servers) -> KafkaProducer | None:
    print(f'creating producer')
    try:
        my_producer = KafkaProducer(
            bootstrap_servers=boostrap_servers,
            value_serializer=lambda x: dumps(x).encode('utf-8'),
            key_serializer=lambda x: x.encode('utf-8')
        )
        print(f'producer created')
        return my_producer
    except:
        return None


def collatz_conjecture(number: int, topic: str, partition_size: int, my_producer: KafkaProducer):
    print(f' calling collatz_conjecture with {number}')
    initial_number = number
    step = 0

    data = {'Number': initial_number, 'Step': step, 'Value': number}
    my_producer.send(topic, key=str(initial_number), value=data, partition=int(initial_number % partition_size))
    while number != 1:
        if number % 2 == 0:
            number = number // 2
        else:
            number = (number * 3) + 1
        step += 1
        data = {'Number': initial_number, 'Step': step, 'Value': number}
        my_producer.send(topic, key=str(initial_number), value=data, partition=int(initial_number % partition_size))


if __name__ == "__main__":
    print(f'start producer')
    settings = get_settings()
    has_topic = check_has_topic(settings.kafka_topic_name, settings.bootstrap_servers.split(','))
    if not has_topic:
        create_topic(settings.kafka_topic_name, settings.partitions, settings.replication_factor,
                     settings.bootstrap_servers.split(','))

    producer = create_producer(settings.bootstrap_servers.split(','))
    if not producer:
        exit(-1)
    p_size = len(producer.partitions_for(settings.kafka_topic_name))
    print(f'partition size: {p_size}, topic: {settings.kafka_topic_name}')
    while True:
        random_number = random.randint(1, 99999999999999)
        collatz_conjecture(number=random_number, topic=settings.kafka_topic_name, partition_size=p_size,
                           my_producer=producer)
        producer.flush()
    producer.close()
