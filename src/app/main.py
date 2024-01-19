import logging
from typing import Union
import matplotlib.pyplot as plt
import clickhouse_connect
from clickhouse_connect.driver.client import Client
from clickhouse_connect.driver.query import QueryResult
from fastapi import FastAPI, Depends, Response, BackgroundTasks
from pydantic import BaseModel
import io
from starlette.responses import StreamingResponse

app = FastAPI()


def create_img(result, number):
    steps = [record[0] for record in result.result_rows]
    values = [record[1] for record in result.result_rows]
    # steps= [1,2,3,4,5,6,7,8,9,10,11,12,13]
    # values = [17,52,26,13,40,20,10,5,16,8,4,2,1]

    plt.switch_backend('Agg')
    plt.title(f'Plot of Steps for Number {number}')
    plt.xlabel('Step Number')
    plt.ylabel('Value')
    plt.plot(steps, values)
    plt.rcParams['figure.figsize'] = [7.50, 3.50]
    plt.rcParams['figure.autolayout'] = True


    img_buf = io.BytesIO()
    plt.savefig(img_buf, format='png')
    plt.close('all')
    return img_buf


def get_db() -> Client:
    client = clickhouse_connect.get_client(host='172.16.40.40', port=18123, username='default', password='')
    try:
        yield client
    finally:
        client.close()


def setup_db(client: Client):
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


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


# Which number had the longest step chain
@app.get("/longest_step_chain")
def longest_step_chain(db=Depends(get_db)):
    result: QueryResult = db.query('SELECT number , count(step) FROM helloworld.my_first_table group by number limit 1')
    print(result.result_rows)
    return {"longest": result.result_rows[0][0]}


# Which number went to the highest value
@app.get("/highest_value")
def highest_value(db=Depends(get_db)):
    result: QueryResult = db.query(
        'SELECT number , step, value as cnt FROM helloworld.my_first_table order by value desc limit 1')
    print(result.result_rows)
    return {"longest": result.result_rows[0][0]}


# is number x part of the step chain of another number.
@app.get("/part/{number}")
def part_number(number: int, db=Depends(get_db)):
    result: QueryResult = db.query(
        f'select number from helloworld.my_first_table where value = {number}')
    print(result.result_rows)
    return result.result_rows


# Create a plot of all steps of number
@app.get('/plot/{number}')
def get_plot(number: int,background_tasks: BackgroundTasks, db=Depends(get_db)):
    result: QueryResult = db.query(
        f'select step ,value from helloworld.my_first_table where number = {number}')
    print(result.result_rows)
    # return result.result_rows

    img_buf = create_img(result,number)
    background_tasks.add_task(img_buf.close)
    headers = {'Content-Disposition': 'inline; filename="out.png"'}
    return Response(img_buf.getvalue(), headers=headers, media_type='image/png')
