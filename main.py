import random
import clickhouse_connect
import datetime
client = clickhouse_connect.get_client(host='172.16.40.40',port=18123, username='default', password='')

client.command('CREATE DATABASE IF NOT EXISTS helloworld')
client.command("""
CREATE TABLE IF NOT EXISTS helloworld.my_first_table
(
    number UInt64,
    step UInt64,
    value UInt64,
    timestamp DateTime           
) 
               ENGINE = MergeTree()
               PRIMARY KEY (number, timestamp)
""")


def collatz_conjecture(number):
    initial_number = number
    step = 0
    print(f"Number: {initial_number}, Step: {step}, Value: {number}")
    while number != 1:
        if number % 2 == 0:
            number = number // 2
        else:
            number = (number * 3) + 1
        step += 1
        print(f"Number: {initial_number}, Step: {step}, Value: {number}")
        client.insert('helloworld.my_first_table', [[initial_number,step,number,datetime.datetime.now()]], column_names=['number','step', 'value', 'timestamp'])

if __name__ == "__main__":
    while True:
        random_number = random.randint(1, 99999999999999)
        collatz_conjecture(random_number)