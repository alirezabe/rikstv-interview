
import clickhouse_connect
import datetime
client = clickhouse_connect.get_client(host='172.16.40.40',port=18123, username='default', password='')
client.command('Drop DAtabase helloworld')
# client.command('CREATE DATABASE IF NOT EXISTS helloworld')
# client.command("""
# CREATE TABLE IF NOT EXISTS helloworld.my_first_table
# (
#     initial_number UInt64,
#     step UInt64,
#     number UInt64,
#     timestamp DateTime           
# ) 
#                ENGINE = MergeTree()
# """)

# client.insert('helloworld.my_first_table', [[6437039977267,71,358826102,datetime.datetime.now()]], column_names=['number','step', 'value', 'timestamp'])

result = client.query('SELECT max(number), avg(value), count(value) FROM helloworld.my_first_table')
print(result.result_rows)


## Which number had the longest step chain.
## SELECT number , count(step) as cnt FROM helloworld.my_first_table group by number order by cnt desc
result = client.query('SELECT number , count(distinct(step)) FROM helloworld.my_first_table group by number')
print(result.result_rows)

## Which number had the biggest step chain.
## SELECT number , step as cnt FROM helloworld.my_first_table order by step desc

## Which number went to the highest value.
## SELECT number , step, value as cnt FROM helloworld.my_first_table order by value desc

## is number x part of the step chain of another number.