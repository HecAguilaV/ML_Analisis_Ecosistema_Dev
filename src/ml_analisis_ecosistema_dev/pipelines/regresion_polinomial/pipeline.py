"""
Pipeline de regresión polinomial separado del pipeline de regresión normal.

Esta separación sigue buenas prácticas de modularidad en Kedro:
- Permite comparar experimentos de regresión normal y polinomial de forma aislada.
- Facilita la trazabilidad, reproducibilidad y versionado de resultados.
- Evita dependencias cruzadas y sobreescritura de artefactos.

Si el experimento polinomial no aporta valor predictivo, puede eliminarse o dejarse como ejemplo de extensibilidad.
"""

from kedro.pipeline import Pipeline, node, pipeline

from ml_analisis_ecosistema_dev.pipelines.regresion.nodes import (
    select_top_features,
    train_model_with_grid_search,
)

from .nodes import create_polynomial_features, evaluate_poly_model


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=select_top_features,
                inputs=[
                    "X_train",
                    "y_train",
                    "X_test",
                    "params:regresion_polinomial",
                ],
                outputs=["X_train_selected", "X_test_selected"],
                name="select_top_features_node",
            ),
            node(
                func=create_polynomial_features,
                inputs=[
                    "X_train_selected",
                    "X_test_selected",
                    "params:regresion_polinomial",
                ],
                outputs=["X_train_poly", "X_test_poly"],
                name="create_polynomial_features_node",
            ),
            node(
                func=train_model_with_grid_search,
                inputs=[
                    "X_train_poly",
                    "y_train",
                    "params:regresion_polinomial.model_to_train_poly",
                    "params:regresion_polinomial",
                ],
                outputs="ridge_poly_model",
                name="train_ridge_poly_model_node",
            ),
            node(
                func=evaluate_poly_model,
                inputs=["ridge_poly_model", "X_test_poly", "y_test"],
                outputs="metrics_ridge_poly",
                name="evaluate_ridge_poly_model_node",
            ),
        ],
        inputs={"X_train", "X_test", "y_train", "y_test"},
        outputs={"metrics_ridge_poly"},
    )
