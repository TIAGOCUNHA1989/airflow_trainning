from airflow import DAG
from datetime import datetime
from airflow.providers.http.sensors.http import HttpSensor
from airflow.providers.postgres.operators.postgres import PostgresOperator
# import here

with DAG(
    dag_id="user_processing",
    start_date=datetime(2023, 1, 1),
    schedule_interval="@daily",
    catchup=False
) as dag:
    
    create_table = PostgresOperator(
        task_id='create_table',
        postgres_conn_id='postgres',
        sql='''
            CREATE TABLE IF NOT EXISTS users (
                firstname TEXT NOT NULL,
                lastname TEXT NOT NULL,
                country TEXT NOT NULL,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                email TEXT NOT NULL
            );
        ''')
        

    # task here
    is_api_available = HttpSensor(
        task_id='is_api_available',
        http_conn_id='user_api',
        endpoint='api/',
        method='GET',
        response_check=lambda response: response.status_code == 200,
        poke_interval=5,
        timeout=20
    )
    