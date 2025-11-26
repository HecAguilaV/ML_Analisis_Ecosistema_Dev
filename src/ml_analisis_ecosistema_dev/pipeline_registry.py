"""Project pipelines."""

from typing import Dict
from kedro.pipeline import Pipeline

from ml_analisis_ecosistema_dev.pipelines.analisis_chile.pipeline import (
    create_pipeline as analisis_chile_pipeline,
)
from ml_analisis_ecosistema_dev.pipelines.clasificacion.pipeline import (
    create_pipeline as clasificacion_pipeline,
)
from ml_analisis_ecosistema_dev.pipelines.procesamiento_de_datos import (
    create_pipeline as dp_pipeline,
)
from ml_analisis_ecosistema_dev.pipelines.regresion.pipeline import (
    create_pipeline as regresion_pipeline,
)


def register_pipelines() -> Dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns:
        A mapping from pipeline names to ``Pipeline`` objects.
    """
    processing_pipeline = dp_pipeline()
    reg_pipeline = regresion_pipeline()
    clasif_pipeline = clasificacion_pipeline()
    # Importar aquí para evitar dependencias circulares
    from ml_analisis_ecosistema_dev.pipelines.regresion_polinomial.pipeline import (
        create_pipeline as reg_poli_pipeline,
    )

    reg_poli = reg_poli_pipeline()
    analisis_chile = analisis_chile_pipeline()

    # Pipeline completo: ejecuta todo en orden
    pipeline_completo = processing_pipeline + reg_pipeline + clasif_pipeline + reg_poli

    return {
        "__default__": pipeline_completo,  # Ahora ejecuta TODO
        "procesamiento_de_datos": processing_pipeline,
        "regresion": reg_pipeline,
        "clasificacion": clasif_pipeline,
        "regresion_polinomial": reg_poli,
        "analisis_chile": analisis_chile,
    }
