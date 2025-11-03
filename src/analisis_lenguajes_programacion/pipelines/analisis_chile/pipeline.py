"""
Pipeline de análisis del mercado chileno.

Este pipeline procesa los datos procesados y genera análisis comparativos
del mercado tecnológico en Chile.
"""

from kedro.pipeline import Pipeline, node
from kedro.pipeline.modular_pipeline import pipeline

from .nodes import (
    cargar_y_preparar_datos,
    analizar_distribucion_global,
    generar_reporte_preliminar,
    exportar_estadisticas_basicas,
)


def create_pipeline(**kwargs) -> Pipeline:
    """
    Crea el pipeline de análisis del mercado chileno.
    
    Returns:
        Pipeline de Kedro con todos los nodos de análisis
    """
    return pipeline(
        [
            node(
                func=cargar_y_preparar_datos,
                inputs="datos_para_modelado",
                outputs="datos_analisis_chile",
                name="cargar_datos_chile",
            ),
            node(
                func=analizar_distribucion_global,
                inputs="datos_analisis_chile",
                outputs="estadisticas_globales_chile",
                name="analizar_distribucion_global",
            ),
            node(
                func=generar_reporte_preliminar,
                inputs=["datos_analisis_chile", "estadisticas_globales_chile"],
                outputs="reporte_preliminar_chile",
                name="generar_reporte_preliminar",
            ),
            node(
                func=exportar_estadisticas_basicas,
                inputs=["datos_analisis_chile", "estadisticas_globales_chile"],
                outputs="tabla_estadisticas_chile",
                name="exportar_estadisticas_basicas",
            ),
        ],
        namespace="analisis_chile",
        inputs="datos_para_modelado",
        outputs={
            "estadisticas_globales_chile",
            "reporte_preliminar_chile",
            "tabla_estadisticas_chile",
        },
    )
