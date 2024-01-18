from json import loads
from kafka import KafkaConsumer


my_consumer = KafkaConsumer(
    'test.python',
     bootstrap_servers = ['127.0.0.1 : 9092'],
     auto_offset_reset = 'earliest',
     enable_auto_commit = True,
     group_id = 'matine',
     value_deserializer = lambda x : loads(x.decode('utf-8')),
     )
# my_consumer.close()
print(f'init --> {my_consumer.topics()}')
for message in my_consumer:
    # print(f'hello --> {message}, {type(message)}')

    # message_val = message.value
    # print(f' added to {message_val}')

    print(f'partition:{message.partition}, offset: {message.offset}, message:{message.value}')
