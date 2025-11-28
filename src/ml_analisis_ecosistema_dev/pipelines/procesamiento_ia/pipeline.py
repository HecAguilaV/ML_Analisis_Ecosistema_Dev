"""
Pipeline de procesamiento de datos de IA.
Extrae, normaliza y consolida información sobre IA de los 3 datasets.
"""

from kedro.pipeline import Pipeline, node

from .nodes import (
    consolidar_datos_ia,
    extraer_datos_ia_jetbrains_2025,
    extraer_datos_ia_so_2023,
    extraer_datos_ia_so_2025,
)


def create_pipeline(**kwargs) -> Pipeline:
    """Crea el pipeline de procesamiento de datos de IA.

    Returns:
        El pipeline de procesamiento de datos de IA.
    """
    return Pipeline(
        [
            node(
                func=extraer_datos_ia_so_2023,
                inputs="datos_crudos_so_2023",
                outputs="datos_ia_so_2023",
                name="extraer_datos_ia_so_2023",
            ),
            node(
                func=extraer_datos_ia_so_2025,
                inputs="datos_crudos_so_2025",
                outputs="datos_ia_so_2025",
                name="extraer_datos_ia_so_2025",
            ),
            node(
                func=extraer_datos_ia_jetbrains_2025,
                inputs="datos_crudos_jb_2025_external",
                outputs="datos_ia_jetbrains_2025",
                name="extraer_datos_ia_jetbrains_2025",
            ),
            node(
                func=consolidar_datos_ia,
                inputs=[
                    "datos_ia_so_2023",
                    "datos_ia_so_2025",
                    "datos_ia_jetbrains_2025",
                ],
                outputs="datos_ia_consolidados",
                name="consolidar_datos_ia",
            ),
        ]
    )

