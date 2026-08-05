from datetime import datetime
from airflow.sdk import dag, task

@dag(
    dag_id="mi_primer_dag",
    start_date=datetime(2026, 8, 1),
    schedule="@daily",
    catchup=False,
    tags=["aprendizaje"],
)
def pipeline_demo():

    @task
    def extraer(**context):
        print(f"logical_date:        {context['logical_date']}")
        print(f"data_interval_start: {context['data_interval_start']}")
        print(f"data_interval_end:   {context['data_interval_end']}")
        print(f"ahora de verdad:     {datetime.now()}")
        return [1, 2, 3]

    @task
    def transformar(datos: list[int]) -> int:
        return sum(x * 10 for x in datos)

    @task
    def cargar(total: int) -> None:
        print(f"Total procesado: {total}")

    cargar(transformar(extraer()))

pipeline_demo()