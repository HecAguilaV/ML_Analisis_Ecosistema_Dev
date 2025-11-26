from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import json
import os

# Define la ruta base de tu proyecto Kedro
# Asegúrate de que esta ruta sea la correcta en tu entorno
KEDRO_PROJECT_PATH = "/opt/airflow/kedro_project"

# Configuración por defecto para todas las tareas
default_args = {
    "owner": "mlops_team",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}


def consolidate_results():
    """
    Consolida los resultados de todos los pipelines.
    Lee las métricas de regresión y clasificación y genera un resumen.
    """
    metrics_path = f"{KEDRO_PROJECT_PATH}/data/08_reporting"

    results = {"timestamp": datetime.now().isoformat(), "pipelines": {}}

    # Leer métricas de regresión
    try:
        with open(f"{metrics_path}/metrics.json", "r") as f:
            results["pipelines"]["regresion"] = json.load(f)
    except FileNotFoundError:
        results["pipelines"]["regresion"] = "No disponible"

    # Leer métricas de clasificación
    try:
        with open(f"{metrics_path}/metrics_clf.json", "r") as f:
            results["pipelines"]["clasificacion"] = json.load(f)
    except FileNotFoundError:
        results["pipelines"]["clasificacion"] = "No disponible"

    # Leer métricas polinomiales
    try:
        with open(f"{metrics_path}/metrics_ridge_poly.json", "r") as f:
            results["pipelines"]["regresion_polinomial"] = json.load(f)
    except FileNotFoundError:
        results["pipelines"]["regresion_polinomial"] = "No disponible"

    print("=" * 80)
    print("RESUMEN DE EJECUCIÓN DE PIPELINES")
    print("=" * 80)
    print(json.dumps(results, indent=2))
    print("=" * 80)

    return results


with DAG(
    dag_id="kedro_ml_pipeline",
    default_args=default_args,
    start_date=datetime(2025, 11, 1),
    schedule=None,  # Ejecución manual (para defensa académica)
    catchup=False,
    tags=["kedro", "mlops", "machine-learning", "defensa-academica"],
    description="Orquestación completa de pipelines ML: procesamiento → modelado → consolidación",
) as dag:
    # Tarea para ejecutar el pipeline de procesamiento de datos
    run_processing = BashOperator(
        task_id="run_processing_pipeline",
        bash_command=f"cd {KEDRO_PROJECT_PATH} && kedro run --pipeline=procesamiento_de_datos",
        dag=dag,
    )

    # Tarea para ejecutar el pipeline de regresión
    run_regression = BashOperator(
        task_id="run_regression_pipeline",
        bash_command=f"cd {KEDRO_PROJECT_PATH} && kedro run --pipeline=regresion",
        dag=dag,
    )

    # Tarea para ejecutar el pipeline de regresión polinomial
    run_regression_poly = BashOperator(
        task_id="run_regression_polinomial_pipeline",
        bash_command=f"cd {KEDRO_PROJECT_PATH} && kedro run --pipeline=regresion_polinomial",
        dag=dag,
    )

    # Tarea para ejecutar el pipeline de clasificación
    run_classification = BashOperator(
        task_id="run_classification_pipeline",
        bash_command=f"cd {KEDRO_PROJECT_PATH} && kedro run --pipeline=clasificacion",
        dag=dag,
    )

    # Tarea de consolidación de resultados
    consolidate_pipeline_results = PythonOperator(
        task_id="consolidate_pipeline_results",
        python_callable=consolidate_results,
        dag=dag,
    )

    # Definir las dependencias de las tareas:
    # El procesamiento debe terminar antes de que los modelos de regresión y clasificación puedan ejecutarse.
    run_processing >> [run_regression, run_regression_poly, run_classification]

    # Los tres pipelines de modelado deben completarse antes de la consolidación
    [
        run_regression,
        run_regression_poly,
        run_classification,
    ] >> consolidate_pipeline_results
