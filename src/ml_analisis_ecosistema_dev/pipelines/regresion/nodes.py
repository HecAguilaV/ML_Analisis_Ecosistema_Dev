import logging
from typing import Any

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.feature_selection import SelectKBest, f_regression  # Nuevas importaciones
from sklearn.linear_model import Lasso, LinearRegression, Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import GridSearchCV, KFold, train_test_split
from sklearn.preprocessing import PolynomialFeatures  # Importar
from xgboost import XGBRegressor

logger = logging.getLogger(__name__)


def split_data(data: pd.DataFrame, params: dict[str, Any]) -> dict[str, Any]:
    """Divide los datos en conjuntos de entrenamiento y prueba, asegurando que solo
    se usen columnas numéricas para las características.

    Args:
        data: DataFrame de entrada.
        params: Diccionario de parámetros con test_size y random_state.

    Returns:
        Un diccionario con X_train, X_test, y_train, y_test.
    """
    X = data.drop(columns=[params["target_col"]])

    # ELIMINAR ResponseId si existe (NO debe ser feature para modelo)
    if "ResponseId" in X.columns:
        X = X.drop(columns=["ResponseId"])
        logger.info("ResponseId excluido de features de entrenamiento")

    y = data[params["target_col"]]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=params["test_size"], random_state=params["random_state"]
    )

    logger.info(f"División de datos completada. Tamaño de X_train: {X_train.shape}")
    return {
        "X_train": X_train,
        "X_test": X_test,
        "y_train": y_train,
        "y_test": y_test,
    }


def _get_model_instance(model_name: str, params: dict[str, Any]):
    """Retorna una instancia del modelo basado en el nombre."""
    model_map = {
        "LinearRegression": LinearRegression(),
        "Ridge": Ridge(),
        "Lasso": Lasso(),
        "RandomForestRegressor": RandomForestRegressor(
            random_state=params.get("random_state")
        ),
        "XGBRegressor": XGBRegressor(random_state=params.get("random_state")),
    }
    if model_name not in model_map:
        raise ValueError(f"Modelo '{model_name}' no soportado.")
    return model_map[model_name]


def train_model_with_grid_search(
    X_train: pd.DataFrame, y_train: pd.Series, model_name: str, params: dict[str, Any]
) -> Any:
    """
    Entrena un modelo de regresión usando GridSearchCV para encontrar los mejores hiperperámetros.

    Args:
        X_train: DataFrame de características de entrenamiento.
        y_train: Serie del target de entrenamiento.
        model_name: Nombre del modelo a entrenar.
        params: Diccionario de parámetros que incluye la grilla para GridSearchCV.

    Returns:
        El mejor estimador encontrado por GridSearchCV.
    """
    model = _get_model_instance(model_name, params)
    param_grid = params["models"][model_name]["param_grid"]

    cv = KFold(
        n_splits=params.get("cv_folds", 5),
        shuffle=True,
        random_state=params.get("random_state"),
    )

    grid_search = GridSearchCV(
        estimator=model,
        param_grid=param_grid,
        cv=cv,
        scoring=params.get("scoring", "neg_root_mean_squared_error"),
        n_jobs=-1,
        verbose=1,
        error_score="raise",  # Añadido para depuración
    )

    logger.info(f"Iniciando GridSearchCV para el modelo {model_name}...")
    grid_search.fit(X_train, y_train)

    logger.info(f"Mejores parámetros para {model_name}: {grid_search.best_params_}")

    return grid_search.best_estimator_


def report_and_select_best_model(
    X_test: pd.DataFrame, y_test: pd.Series, **models
) -> dict[str, Any]:
    """
    Evalúa múltiples modelos, genera un informe de métricas, selecciona el mejor
    y lo guarda.

    Args:
        models: Un diccionario con los modelos entrenados.
        X_test: DataFrame de características de prueba.
        y_test: Serie del target de prueba.

    Returns:
        Un diccionario con el mejor modelo y las métricas de todos los modelos.
    """
    metrics_report = {}
    best_model = None
    best_r2 = -np.inf

    logger.info("--- Informe de Evaluación de Modelos de Regresión ---")

    for model_name, model in models.items():
        y_pred = model.predict(X_test)

        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        metrics_report[model_name] = {"rmse": rmse, "mae": mae, "r2": r2}

        logger.info(f"Modelo: {model_name}")
        logger.info(f"  - R^2: {r2:.4f}")
        logger.info(f"  - RMSE: {rmse:.4f}")
        logger.info(f"  - MAE: {mae:.4f}")

        if r2 > best_r2:
            best_r2 = r2
            best_model = model

    logger.info("--- Fin del Informe ---")
    logger.info(
        f"Mejor modelo seleccionado: {type(best_model).__name__} (R^2: {best_r2:.4f})"
    )

    return {
        "best_regression_model": best_model,
        "regression_metrics_report": metrics_report,
    }


def create_polynomial_features(
    X_train: pd.DataFrame, X_test: pd.DataFrame, parameters: dict[str, Any]
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Creates polynomial features for the training and testing data.

    Args:
        X_train: Training features.
        X_test: Testing features.
        parameters: Dictionary containing parameters, including the polynomial degree.

    Returns:
        A tuple containing the transformed training and testing dataframes.
    """
    degree = parameters.get("degree", 2)
    poly = PolynomialFeatures(degree=degree, include_bias=False)

    # Asegurarse de que los datos sean de tipo float para PolynomialFeatures
    X_train_numeric = X_train.astype(float)
    X_test_numeric = X_test.astype(float)

    X_train_poly = poly.fit_transform(X_train_numeric)
    X_test_poly = poly.transform(X_test_numeric)

    poly_feature_names = poly.get_feature_names_out(X_train.columns)

    X_train_poly_df = pd.DataFrame(
        X_train_poly, columns=poly_feature_names, index=X_train.index
    )
    X_test_poly_df = pd.DataFrame(
        X_test_poly, columns=poly_feature_names, index=X_test.index
    )

    logger.info(
        f"Created {len(poly_feature_names)} polynomial features with degree {degree}."
    )

    return X_train_poly_df, X_test_poly_df


def evaluate_poly_model(
    model: Any, X_test: pd.DataFrame, y_test: pd.Series
) -> dict[str, float]:
    """
    Evaluates a single regression model and returns its metrics.

    Args:
        model: Trained regression model.
        X_test: Test features.
        y_test: Test target.

    Returns:
        A dictionary containing the model\'s metrics (R^2, RMSE, MAE).
    """
    y_pred = model.predict(X_test)

    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    model_name = type(model).__name__
    logger.info(f"--- Evaluation for Polynomial Model: {model_name} ---")
    logger.info(f"  - R^2: {r2:.4f}")
    logger.info(f"  - RMSE: {rmse:.4f}")
    logger.info(f"  - MAE: {mae:.4f}")
    logger.info("--- End of Report ---")

    return {f"metrics_{model_name}_poly": {"r2": r2, "rmse": rmse, "mae": mae}}


def select_top_features(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    X_test: pd.DataFrame,
    params: dict[str, Any],
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Selects the top K features based on correlation with the target variable.

    Args:
        X_train: Training features.
        y_train: Training target.
        X_test: Testing features.
        params: Dictionary containing parameters, including 'num_features_to_select'.

    Returns:
        A tuple containing the selected training and testing dataframes.
    """
    num_features = params.get("num_features_to_select", 50)

    # Asegurarse de que X_train y y_train no tengan NaNs para SelectKBest
    # Aunque el preprocesamiento debería manejarlos, es una buena práctica defensiva
    X_train_clean = X_train.fillna(X_train.mean(numeric_only=True))
    y_train_clean = y_train.fillna(
        y_train.mean()
    )  # O eliminar filas, dependiendo de la estrategia

    selector = SelectKBest(f_regression, k=num_features)
    selector.fit(X_train_clean, y_train_clean)

    selected_features = X_train.columns[selector.get_support()]

    X_train_selected = X_train[selected_features]
    X_test_selected = X_test[selected_features]

    logger.info(f"Selected top {num_features} features for polynomial transformation.")

    return X_train_selected, X_test_selected
