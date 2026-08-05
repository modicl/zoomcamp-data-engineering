from airflow import DAG
from airflow.operators.python import PythonOperator
from operators.taxi_data_downloader import download_and_extract_taxi_data

dag = DAG(
    dag_id='taxi_backfill_dag',
    description='Descarga y descomprime datos de taxis verdes 2019-2021',
    schedule=None,
    tags=['backfill', 'data-ingestion', 'zoomcamp'],
)

with dag:
    download_task = PythonOperator(
        task_id='download_taxi_data',
        python_callable=download_and_extract_taxi_data,
        op_kwargs={
            'start_year': 2019,
            'start_month': 1,
            'end_year': 2021,
            'end_month': 7,
            'output_dir': 'data/green_taxi',
            'skip_on_error': True,
        },
    )
