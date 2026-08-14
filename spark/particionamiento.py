"""
Lee el CSV de Yellow Taxi (31M filas, ~3.8GB) y lo reparticiona en 64 partes
para observar como PySpark maneja el particionamiento de archivos grandes.
"""

import os
import time
from pathlib import Path

# En Windows, Spark necesita winutils.exe/hadoop.dll (via HADOOP_HOME) para
# poder escribir archivos localmente. Debe configurarse ANTES de crear la
# SparkSession / importar pyspark.sql.
HADOOP_HOME = Path(__file__).parent / "hadoop-winutils"
os.environ["HADOOP_HOME"] = str(HADOOP_HOME)
os.environ["PATH"] = str(HADOOP_HOME / "bin") + os.pathsep + os.environ.get("PATH", "")

from pyspark.sql import SparkSession

NUM_PARTICIONES = 64
ARCHIVO_ENTRADA = Path(__file__).parent / "2021_Yellow_Taxi_Trip_Data_20260814.csv"
CARPETA_SALIDA = Path(__file__).parent / "output" / "yellow_taxi_64_particiones_parquet"

# Link descarga dataset : https://data.cityofnewyork.us/Transportation/2021-Yellow-Taxi-Trip-Data/m6nq-qud6/about_data

def main():
    spark = (
        SparkSession.builder
        .master("local[*]")
        .appName("particionamiento-csv-64")
        .config("spark.driver.memory", "16g")
        .config("spark.sql.shuffle.partitions", NUM_PARTICIONES)
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("WARN")

    inicio = time.time()

    print(f"Leyendo {ARCHIVO_ENTRADA.name} ...")
    df = (
        spark.read
        .option("header", "true")
        .option("inferSchema", "true")
        .csv(str(ARCHIVO_ENTRADA))
    )

    print(f"Particiones al leer (Spark las infiere segun el tamaño del archivo/bloques): {df.rdd.getNumPartitions()}")

    total_filas = df.count()
    print(f"Filas totales: {total_filas:,}")

    df_particionado = df.repartition(NUM_PARTICIONES)
    print(f"Particiones tras repartition({NUM_PARTICIONES}): {df_particionado.rdd.getNumPartitions()}")

    print(f"Escribiendo {NUM_PARTICIONES} archivos en {CARPETA_SALIDA} ...")
    (
        df_particionado.write
        .mode("overwrite")
        .parquet(str(CARPETA_SALIDA))
    )

    archivos_parquet = list(CARPETA_SALIDA.glob("part-*.parquet"))
    print(f"Archivos part-*.parquet generados: {len(archivos_parquet)}")

    print(f"Listo en {time.time() - inicio:.1f} segundos")

    spark.stop()


if __name__ == "__main__":
    main()
