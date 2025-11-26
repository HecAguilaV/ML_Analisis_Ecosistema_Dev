"""
Pipeline de análisis comparativo Chile vs Global - FASE 1.

Este pipeline implementa análisis comparativo usando modelos globales entrenados:
1. Carga datos raw de Chile (Stack Overflow 2023)
2. Procesa con transformaciones del pipeline global
3. Hace predicciones con modelos entrenados (regresión + clasificación)
4. Genera análisis comparativo Chile vs Mundo
5. Exporta reportes y visualizaciones
"""

from kedro.pipeline import Pipeline, node, pipeline

from .nodes import (
    analisis_comparativo_chile_global,
    cargar_datos_raw_chile,
    cargar_modelos_entrenados,
    exportar_reporte_comparativo,
    generar_predicciones_chile,
    procesar_datos_chile,
)


def create_pipeline(**kwargs) -> Pipeline:
    """
    Crea el pipeline de análisis comparativo Chile vs Global - FASE 1.

    Returns:
        Pipeline de Kedro con todos los nodos de análisis comparativo
    """
    return pipeline(
        [
            # 1. Cargar datos raw de Chile
            node(
                func=cargar_datos_raw_chile,
                inputs=None,
                outputs="chile_datos_raw",
                name="cargar_datos_raw_chile",
            ),
            # 2. Procesar datos de Chile con pipeline global
            node(
                func=procesar_datos_chile,
                inputs=["chile_datos_raw", "datos_para_modelado"],
                outputs="chile_datos_procesados",
                name="procesar_datos_chile",
            ),
            # 3. Cargar modelos entrenados
            node(
                func=cargar_modelos_entrenados,
                inputs=["regresion_model", "clasificacion_model"],
                outputs="modelos_cargados",
                name="cargar_modelos",
            ),
            # 4. Generar predicciones para Chile
            node(
                func=generar_predicciones_chile,
                inputs=[
                    "chile_datos_procesados",
                    "regresion_model",  # modelo de regresión
                    "clasificacion_model",  # modelo de clasificación
                ],
                outputs="chile_predicciones",
                name="generar_predicciones_chile",
            ),
            # 5. Análisis comparativo Chile vs Global
            node(
                func=analisis_comparativo_chile_global,
                inputs=[
                    "chile_predicciones",
                    "datos_para_modelado",
                    "regresion_model",
                    "clasificacion_model",
                ],
                outputs="chile_reporte_comparativo",
                name="analisis_comparativo",
            ),
            # 6. Exportar reporte en formato tabular
            node(
                func=exportar_reporte_comparativo,
                inputs="chile_reporte_comparativo",
                outputs="chile_tabla_comparativa",
                name="exportar_tabla_comparativa",
            ),
        ],
        namespace="analisis_chile",
        inputs={"datos_para_modelado", "regresion_model", "clasificacion_model"},
        tags=["analisis", "chile", "comparativo", "fase1"],
    )
