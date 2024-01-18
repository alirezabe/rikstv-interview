from time import sleep
from json import dumps
from kafka import KafkaProducer

# initializing the Kafka producer
my_producer = KafkaProducer(
    bootstrap_servers = ['127.0.0.1:9092'],
    value_serializer = lambda x:dumps(x).encode('utf-8')
    )

for n in range(1600):
    my_data = {'num' : n}
    p_size = len(my_producer.partitions_for('test.python'))  
    print(f'partition_size: {p_size}')  
    a = my_producer.send('test.python', value = my_data, partition=int(n%p_size))
    print(my_data)
    # meta = a.get()
    # print(meta.topic)
    sleep(1)

my_producer.flush()
my_producer.close()
