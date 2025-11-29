"""
This is a boilerplate pipeline 'regresion_polinomial'
generated using Kedro 0.19.12
"""

import logging
from typing import Any

import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import PolynomialFeatures

logger = logging.getLogger(__name__)


def create_polynomial_features(
    X_train: pd.DataFrame, X_test: pd.DataFrame, parameters: dict
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

    # Fit on the training data and transform both train and test
    X_train_poly = poly.fit_transform(X_train)
    X_test_poly = poly.transform(X_test)

    # Get feature names for the new polynomial features
    # This is crucial for creating a DataFrame with meaningful column names
    poly_feature_names = poly.get_feature_names_out(X_train.columns)

    # Create new DataFrames with the polynomial features
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
        A dictionary containing the model's metrics (R^2, RMSE, MAE).
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

    # Para que la salida coincida con metrics_ridge_poly del catalog.yml
    return {"r2": r2, "rmse": rmse, "mae": mae}
