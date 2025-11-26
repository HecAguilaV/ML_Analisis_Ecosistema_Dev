"""
Nodos para el pipeline de procesamiento de datos, con un enfoque robusto y controlado por una "allowlist".
"""

import logging
from typing import Any, Dict, Tuple

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

logger = logging.getLogger(__name__)


def cargar_datos(
    so_2023: pd.DataFrame,
    jb_external: pd.DataFrame,
    jb_narrow: pd.DataFrame,
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Carga los datos crudos desde el catálogo."""
    return so_2023, jb_external, jb_narrow


def combinar_stack_overflow_2023_2025(
    so_2023: pd.DataFrame,
    so_2025: pd.DataFrame,
) -> pd.DataFrame:
    """
    Combina Stack Overflow 2023 y 2025 en un solo dataset.

    - Identifica columnas comunes entre ambos datasets
    - Agrega columna 'Year' para identificar origen
    - Maneja columnas que solo existen en uno de los datasets
    - Prioriza ToolsTechHaveWorkedWith de SO2023 (no existe en SO2025)

    Args:
        so_2023: DataFrame de Stack Overflow 2023
        so_2025: DataFrame de Stack Overflow 2025

    Returns:
        DataFrame combinado con columnas comunes + Year
    """
    logger.info("--- Combinando Stack Overflow 2023 y 2025 ---")

    # Agregar columna Year para identificar origen
    so_2023_copy = so_2023.copy()
    so_2025_copy = so_2025.copy()

    so_2023_copy["Year"] = 2023
    so_2025_copy["Year"] = 2025

    logger.info(
        f"SO2023: {len(so_2023_copy):,} registros, {len(so_2023_copy.columns)} columnas"
    )
    logger.info(
        f"SO2025: {len(so_2025_copy):,} registros, {len(so_2025_copy.columns)} columnas"
    )

    # Identificar columnas comunes
    cols_2023 = set(so_2023_copy.columns)
    cols_2025 = set(so_2025_copy.columns)
    cols_comunes = cols_2023.intersection(cols_2025)

    # Columnas que solo están en 2023 (las importantes para nosotros)
    cols_solo_2023 = cols_2023 - cols_2025
    cols_importantes_solo_2023 = {"ToolsTechHaveWorkedWith", "YearsCodePro"}
    cols_importantes_disponibles = cols_importantes_solo_2023.intersection(
        cols_solo_2023
    )

    if cols_importantes_disponibles:
        logger.warning(
            f"Columnas importantes solo en SO2023: {cols_importantes_disponibles}. "
            f"SO2025 tendrá NaN en estas columnas."
        )

    # Seleccionar columnas para combinar: comunes + importantes de 2023
    columnas_finales = list(cols_comunes.union(cols_importantes_disponibles))

    # Asegurar que SO2025 tenga las columnas de SO2023 (rellenar con NaN)
    for col in columnas_finales:
        if col not in so_2025_copy.columns:
            so_2025_copy[col] = np.nan
            logger.info(f"Agregada columna '{col}' a SO2025 con valores NaN")

    # Seleccionar solo columnas finales en ambos datasets
    so_2023_final = so_2023_copy[columnas_finales]
    so_2025_final = so_2025_copy[columnas_finales]

    # Combinar datasets
    df_combinado = pd.concat([so_2023_final, so_2025_final], axis=0, ignore_index=True)

    logger.info(
        f"✅ Dataset combinado: {len(df_combinado):,} registros, {len(df_combinado.columns)} columnas"
    )
    logger.info(f"   - Registros de 2023: {(df_combinado['Year'] == 2023).sum():,}")
    logger.info(f"   - Registros de 2025: {(df_combinado['Year'] == 2025).sum():,}")

    return df_combinado


def analizar_y_limpiar_nulos(
    so_2023: pd.DataFrame,
    jb_external: pd.DataFrame,
    jb_narrow: pd.DataFrame,
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Analiza y elimina columnas con un alto porcentaje de valores nulos."""
    logger.info("--- Análisis y Limpieza de Nulos por Columna ---")

    def _limpiar_df(df: pd.DataFrame, nombre: str) -> pd.DataFrame:
        nan_percentages = df.isnull().sum() / len(df)
        cols_to_drop = nan_percentages[nan_percentages > 0.5].index
        if len(cols_to_drop) > 0:
            logger.info(
                f"En '{nombre}', eliminando {len(cols_to_drop)} columnas con >50% de nulos."
            )
            df = df.drop(columns=cols_to_drop)
        return df

    so_2023_clean = _limpiar_df(so_2023, "Stack Overflow 2023")
    jb_external_clean = _limpiar_df(jb_external, "JetBrains External")
    jb_narrow_clean = _limpiar_df(jb_narrow, "JetBrains Narrow")
    return so_2023_clean, jb_external_clean, jb_narrow_clean


def eliminar_filas_sin_salario(df_so: pd.DataFrame, target_col: str) -> pd.DataFrame:
    """Elimina las filas del dataset de Stack Overflow donde el salario es nulo."""
    logger.info(f"--- Eliminando filas sin datos de '{target_col}' ---")
    df_cleaned = df_so.dropna(subset=[target_col])
    logger.info(
        f"Se eliminaron {len(df_so) - len(df_cleaned)} filas donde '{target_col}' era nulo."
    )
    return df_cleaned


def filtrar_outliers_salario(df_so: pd.DataFrame, target_col: str) -> pd.DataFrame:
    """Filtra outliers de la columna de salarios usando el método IQR."""
    logger.info(f"--- Filtrando outliers de '{target_col}' ---")
    Q1 = df_so[target_col].quantile(0.25)
    Q3 = df_so[target_col].quantile(0.75)
    IQR = Q3 - Q1
    limite_inferior = Q1 - 1.5 * IQR
    limite_superior = Q3 + 1.5 * IQR
    df_filtered = df_so[
        (df_so[target_col] >= limite_inferior) & (df_so[target_col] <= limite_superior)
    ]
    logger.info(
        f"Se eliminaron {len(df_so) - len(df_filtered)} filas consideradas outliers."
    )
    return df_filtered


def preprocesamiento_final_con_allowlist(
    df: pd.DataFrame, params: Dict[str, Any]
) -> pd.DataFrame:
    """
    Realiza el preprocesamiento final basándose en una "allowlist" de columnas para evitar errores de memoria y tipo.
    """
    logger.info("--- Iniciando Preprocesamiento Final con Allowlist --- ")

    target_col = params["target_col"]
    if target_col not in df.columns:
        raise ValueError(f"La columna objetivo '{target_col}' no se encuentra.")

    y = df[target_col]
    features_df = df.drop(columns=[target_col])

    # PRESERVAR ResponseId para análisis posterior (Chile, segmentación, etc.)
    response_id = None
    if "ResponseId" in features_df.columns:
        response_id = features_df["ResponseId"].copy()
        features_df = features_df.drop(columns=["ResponseId"])
        logger.info("ResponseId preservado para restauración posterior")

    # 1. Definir la "Allowlist" de columnas categóricas que queremos procesar
    multi_answer_cols = params.get("multi_answer_cols", [])
    standard_categorical_cols = params.get("standard_categorical_cols", [])
    allowlist = set(multi_answer_cols + standard_categorical_cols)

    # 2. Identificar y eliminar todas las columnas de texto que NO están en la allowlist
    all_object_cols = features_df.select_dtypes(
        include=["object", "category"]
    ).columns.tolist()
    cols_to_drop = [col for col in all_object_cols if col not in allowlist]
    if cols_to_drop:
        logger.warning(
            f"Eliminando {len(cols_to_drop)} columnas de texto no incluidas en la allowlist: {cols_to_drop}"
        )
        features_df = features_df.drop(columns=cols_to_drop)

    # 3. Procesar columnas de respuesta múltiple de la allowlist
    for col in multi_answer_cols:
        if col in features_df.columns:
            dummies = features_df[col].fillna("").str.get_dummies(sep=";")
            dummies = dummies.add_prefix(f"{col}_")
            features_df = pd.concat([features_df.drop(columns=[col]), dummies], axis=1)

    # 4. Procesar columnas categóricas estándar de la allowlist
    cols_to_encode = [
        col for col in standard_categorical_cols if col in features_df.columns
    ]
    if cols_to_encode:
        features_df = pd.get_dummies(
            features_df, columns=cols_to_encode, dummy_na=False
        )

    # 4.5 RELLENAR NaN EN COLUMNAS NUMÉRICAS
    # Esto maneja casos donde columnas como WorkExp tienen valores faltantes
    # o columnas de tecnologías de un solo dataset (ToolsTechHaveWorkedWith solo en SO2023)
    numeric_features = features_df.select_dtypes(include=np.number).columns.tolist()
    if numeric_features:
        nan_counts = features_df[numeric_features].isna().sum()
        cols_with_nan = nan_counts[nan_counts > 0]
        if len(cols_with_nan) > 0:
            logger.warning(
                f"Rellenando NaN en {len(cols_with_nan)} columnas numéricas con 0"
            )
            logger.info(f"Columnas afectadas: {cols_with_nan.index.tolist()[:10]}...")
            features_df[numeric_features] = features_df[numeric_features].fillna(0)

    # 5. Escalar todas las características numéricas resultantes
    numeric_features = features_df.select_dtypes(include=np.number).columns.tolist()
    if numeric_features:
        scaler = StandardScaler()
        features_df[numeric_features] = scaler.fit_transform(
            features_df[numeric_features]
        )

    final_df = pd.concat([features_df, y], axis=1)

    # 6. RESTAURAR ResponseId (NO será usado para modelado pero sí para análisis)
    if response_id is not None:
        final_df.insert(0, "ResponseId", response_id)
        logger.info("ResponseId restaurado en posición 0")

    # 7. Sanitizar nombres de columnas para compatibilidad con LightGBM/XGBoost
    logger.info("Sanitizando nombres de columnas...")
    final_df.columns = final_df.columns.str.replace(r"[^A-Za-z0-9_]+", "_", regex=True)

    # 8. ELIMINAR COLUMNAS DUPLICADAS (causadas por sanitización de C++, C#, etc.)
    duplicate_cols = final_df.columns[final_df.columns.duplicated()].tolist()
    if duplicate_cols:
        logger.warning(
            f"Encontradas {len(duplicate_cols)} columnas duplicadas después de sanitización:"
        )
        logger.warning(
            f"Columnas duplicadas: {duplicate_cols[:10]}..."
        )  # Mostrar primeras 10

        # Eliminar duplicados manteniendo la primera ocurrencia
        final_df = final_df.loc[:, ~final_df.columns.duplicated()]
        logger.info(
            f"Columnas duplicadas eliminadas. Nueva dimensión: {final_df.shape}"
        )

    logger.info(
        f"--- Preprocesamiento Final Completado. Dimensiones: {final_df.shape} ---"
    )

    return final_df
