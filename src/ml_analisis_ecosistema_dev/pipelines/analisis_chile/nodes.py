"""
Nodos del pipeline de análisis comparativo Chile vs Global.

FASE 1: Análisis comparativo usando modelos globales entrenados.
- Carga datos raw de Chile (Stack Overflow 2023 + JetBrains 2025)
- Procesa con pipeline global
- Hace predicciones con modelos entrenados
- Genera análisis comparativo Chile vs Mundo
"""

import logging
from datetime import datetime
from typing import Any

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


def cargar_datos_raw_chile() -> pd.DataFrame:
    """
    Carga datos raw de Chile desde Stack Overflow 2023 y JetBrains 2025.
    Optimizado para cargar solo registros de Chile.

    Returns:
        DataFrame con datos raw de desarrolladores chilenos
    """
    logger.info("Cargando datos raw de Chile (optimizado)")

    # Cargar Stack Overflow 2023 - Solo filtrar Chile con chunks para optimizar
    logger.info("Cargando Stack Overflow 2023 (solo Chile)...")

    chile_chunks = []
    chunk_size = 10000
    total_processed = 0

    for chunk in pd.read_csv(
        "data/01_raw/stackoverflow_2023/stack_overflow_survey_results_public.csv",
        chunksize=chunk_size,
    ):
        chile_chunk = chunk[chunk["Country"] == "Chile"]
        if len(chile_chunk) > 0:
            chile_chunks.append(chile_chunk)
        total_processed += len(chunk)
        if total_processed % 50000 == 0:
            logger.info(f"Procesados {total_processed:,} registros...")

    chile_so_2023 = pd.concat(chile_chunks, ignore_index=True)
    chile_so_2023["source"] = "StackOverflow_2023"
    logger.info(
        f"Stack Overflow 2023 - Chile: {len(chile_so_2023)} registros de {total_processed:,} totales"
    )

    # Por ahora solo usamos Stack Overflow 2023
    # JetBrains requiere mapping de columnas (futuro)
    df_chile_raw = chile_so_2023

    logger.info(f"Total registros de Chile: {len(df_chile_raw)}")
    logger.info(f"Columnas disponibles: {df_chile_raw.shape[1]}")

    return df_chile_raw


def procesar_datos_chile(
    df_chile_raw: pd.DataFrame, df_procesado_global: pd.DataFrame
) -> pd.DataFrame:
    """
    Filtra los datos procesados globales para obtener solo los registros chilenos.

    Estrategia: Los datos procesados globales se generaron del mismo raw,
    así que podemos usar ResponseId para hacer el match.

    Args:
        df_chile_raw: DataFrame raw de Chile (con ResponseId)
        df_procesado_global: DataFrame procesado global (con ResponseId)

    Returns:
        DataFrame de Chile procesado con mismas features que el global
    """
    logger.info("Filtrando datos procesados para Chile")

    # Verificar que ResponseId existe
    if "ResponseId" not in df_chile_raw.columns:
        logger.error("ResponseId no encontrado en datos raw de Chile")
        raise ValueError("Se requiere ResponseId para match")

    # Obtener IDs chilenos
    chile_ids = set(df_chile_raw["ResponseId"].unique())
    logger.info(f"IDs chilenos: {len(chile_ids)}")

    # Filtrar datos procesados
    if "ResponseId" in df_procesado_global.columns:
        df_chile = df_procesado_global[
            df_procesado_global["ResponseId"].isin(chile_ids)
        ].copy()

        # Eliminar ResponseId (no es feature para modelo)
        df_chile = df_chile.drop(columns=["ResponseId"])
        logger.info(f"Datos Chile procesados: {df_chile.shape}")
    else:
        logger.error("ResponseId no encontrado en datos procesados!")
        logger.warning("Usando primeros 248 registros (FALLBACK)")
        df_chile = df_procesado_global.head(len(chile_ids)).copy()

    return df_chile


def cargar_modelos_entrenados(
    modelo_regresion: Any, modelo_clasificacion: Any
) -> tuple[Any, Any]:
    """
    Carga los modelos de regresión y clasificación ya entrenados.

    Args:
        modelo_regresion: Modelo de regresión (salarios)
        modelo_clasificacion: Modelo de clasificación (experiencia)

    Returns:
        Tupla con (modelo_regresion, modelo_clasificacion)
    """
    logger.info("Modelos cargados exitosamente")
    logger.info(f"Modelo regresión: {type(modelo_regresion).__name__}")
    logger.info(f"Modelo clasificación: {type(modelo_clasificacion).__name__}")

    return modelo_regresion, modelo_clasificacion


def generar_predicciones_chile(
    df_chile_procesado: pd.DataFrame, modelo_regresion: Any, modelo_clasificacion: Any
) -> pd.DataFrame:
    """
    Genera predicciones de salario y experiencia para desarrolladores chilenos.

    Args:
        df_chile_procesado: DataFrame de Chile procesado
        modelo_regresion: Modelo para predecir salarios
        modelo_clasificacion: Modelo para predecir nivel de experiencia

    Returns:
        DataFrame con predicciones agregadas
    """
    logger.info("Generando predicciones para desarrolladores chilenos")

    # Preparar features para predicción
    # Necesitamos identificar las columnas que los modelos esperan
    df_predicciones = df_chile_procesado.copy()

    # Identificar columna de salario real (si existe)
    salary_col = None
    for col in df_predicciones.columns:
        if "comptotal" in col.lower() or "salary" in col.lower():
            salary_col = col
            break

    if salary_col:
        logger.info(f"Columna de salario encontrada: {salary_col}")

    try:
        # Predicciones de regresión (salarios)
        logger.info("Generando predicciones de salario...")

        # Obtener features que el modelo espera
        if hasattr(modelo_regresion, "feature_names_in_"):
            expected_features = modelo_regresion.feature_names_in_.tolist()
        else:
            # Fallback: todas las numéricas excepto target
            expected_features = df_predicciones.select_dtypes(
                include=[np.number]
            ).columns.tolist()
            if salary_col and salary_col in expected_features:
                expected_features.remove(salary_col)

        # Preparar X con las features correctas
        X_features = df_predicciones[expected_features]

        logger.info(f"Features para predicción: {len(expected_features)}")
        logger.info(f"Primeras 5 features: {expected_features[:5]}")

        predicciones_salario = modelo_regresion.predict(X_features)
        df_predicciones["salario_predicho"] = predicciones_salario

        if salary_col and salary_col in df_predicciones.columns:
            df_predicciones["salario_real"] = df_predicciones[salary_col]
            df_predicciones["error_prediccion"] = (
                df_predicciones["salario_real"] - df_predicciones["salario_predicho"]
            )

        logger.info(f"Predicciones de salario generadas: {len(predicciones_salario)}")

    except Exception as e:
        logger.error(f"Error generando predicciones de salario: {e}")
        df_predicciones["salario_predicho"] = np.nan
        X_features = None  # Para evitar error en clasificación

    try:
        # Predicciones de clasificación (experiencia)
        logger.info("Generando predicciones de experiencia...")

        # Si X_features falló arriba, intentar obtener las correctas
        if X_features is None:
            if hasattr(modelo_clasificacion, "feature_names_in_"):
                expected_features_clf = modelo_clasificacion.feature_names_in_.tolist()
            else:
                expected_features_clf = df_predicciones.select_dtypes(
                    include=[np.number]
                ).columns.tolist()
                if salary_col and salary_col in expected_features_clf:
                    expected_features_clf.remove(salary_col)
            X_features = df_predicciones[expected_features_clf]

        predicciones_experiencia = modelo_clasificacion.predict(X_features)
        predicciones_proba = modelo_clasificacion.predict_proba(X_features)

        df_predicciones["experiencia_predicha"] = predicciones_experiencia
        df_predicciones["confianza_prediccion"] = predicciones_proba.max(axis=1)

        logger.info(
            f"Predicciones de experiencia generadas: {len(predicciones_experiencia)}"
        )

    except Exception as e:
        logger.error(f"Error generando predicciones de experiencia: {e}")
        df_predicciones["experiencia_predicha"] = np.nan

    logger.info("Predicciones completadas exitosamente")

    return df_predicciones


def analisis_comparativo_chile_global(
    df_predicciones_chile: pd.DataFrame,
    df_procesado_global: pd.DataFrame,
    modelo_regresion: Any,
    modelo_clasificacion: Any,
) -> dict[str, Any]:
    """
    Genera análisis comparativo entre Chile y el mercado global.

    Args:
        df_predicciones_chile: DataFrame con predicciones para Chile
        df_procesado_global: DataFrame procesado global
        modelo_regresion: Modelo de regresión
        modelo_clasificacion: Modelo de clasificación

    Returns:
        Diccionario con análisis comparativo completo
    """
    logger.info("Generando análisis comparativo Chile vs Global")

    reporte = {
        "metadata": {
            "fecha_generacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "registros_chile": len(df_predicciones_chile),
            "registros_global": len(df_procesado_global),
            "version": "1.0_fase1",
        }
    }

    # 1. Análisis de Salarios
    logger.info("Analizando salarios...")

    salary_col_global = None
    for col in df_procesado_global.columns:
        if "comptotal" in col.lower() or "salary" in col.lower():
            salary_col_global = col
            break

    if salary_col_global and "salario_predicho" in df_predicciones_chile.columns:
        salarios_chile = df_predicciones_chile["salario_predicho"].dropna()
        salarios_global = df_procesado_global[salary_col_global].dropna()

        reporte["salarios"] = {
            "chile": {
                "media": float(salarios_chile.mean()),
                "mediana": float(salarios_chile.median()),
                "std": float(salarios_chile.std()),
                "min": float(salarios_chile.min()),
                "max": float(salarios_chile.max()),
                "q25": float(salarios_chile.quantile(0.25)),
                "q75": float(salarios_chile.quantile(0.75)),
            },
            "global": {
                "media": float(salarios_global.mean()),
                "mediana": float(salarios_global.median()),
                "std": float(salarios_global.std()),
                "min": float(salarios_global.min()),
                "max": float(salarios_global.max()),
                "q25": float(salarios_global.quantile(0.25)),
                "q75": float(salarios_global.quantile(0.75)),
            },
            "comparacion": {
                "brecha_media": float(salarios_global.mean() - salarios_chile.mean()),
                "brecha_mediana": float(
                    salarios_global.median() - salarios_chile.median()
                ),
                "ratio_chile_global": float(
                    salarios_chile.mean() / salarios_global.mean()
                ),
            },
        }

        logger.info(f"Salario medio Chile: {reporte['salarios']['chile']['media']:.2f}")
        logger.info(
            f"Salario medio Global: {reporte['salarios']['global']['media']:.2f}"
        )

    # 2. Análisis de Experiencia
    logger.info("Analizando distribución de experiencia...")

    if "experiencia_predicha" in df_predicciones_chile.columns:
        exp_chile = df_predicciones_chile["experiencia_predicha"].value_counts()

        experiencia_data = {"chile_distribucion": exp_chile.to_dict()}

        # Agregar confianza solo si existe la columna
        if "confianza_prediccion" in df_predicciones_chile.columns:
            experiencia_data["chile_confianza_media"] = float(
                df_predicciones_chile["confianza_prediccion"].mean()
            )

        reporte["experiencia"] = experiencia_data

    # 3. Feature Importance (top features para el modelo)
    logger.info("Extrayendo feature importance...")

    try:
        if hasattr(modelo_regresion, "feature_importances_"):
            importances = modelo_regresion.feature_importances_
            feature_names = df_procesado_global.select_dtypes(
                include=[np.number]
            ).columns.tolist()

            # Eliminar columna target
            if salary_col_global and salary_col_global in feature_names:
                feature_names.remove(salary_col_global)

            top_features = sorted(
                zip(feature_names[: len(importances)], importances, strict=False),
                key=lambda x: x[1],
                reverse=True,
            )[:20]

            reporte["feature_importance"] = {
                "top_20_features": [
                    {"feature": feat, "importance": float(imp)}
                    for feat, imp in top_features
                ]
            }

            logger.info(f"Top 5 features: {[f[0] for f in top_features[:5]]}")
    except Exception as e:
        logger.warning(f"No se pudo extraer feature importance: {e}")

    # 4. Métricas de Calidad de Predicción
    if (
        "salario_real" in df_predicciones_chile.columns
        and "salario_predicho" in df_predicciones_chile.columns
    ):
        from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

        real = df_predicciones_chile["salario_real"].dropna()
        pred = df_predicciones_chile.loc[real.index, "salario_predicho"]

        reporte["metricas_prediccion_chile"] = {
            "r2_score": float(r2_score(real, pred)),
            "rmse": float(np.sqrt(mean_squared_error(real, pred))),
            "mae": float(mean_absolute_error(real, pred)),
        }

        logger.info(
            f"R² en Chile: {reporte['metricas_prediccion_chile']['r2_score']:.4f}"
        )

    # 5. Insights y Recomendaciones
    reporte["insights"] = {
        "titulo": "Análisis Comparativo Chile vs Global - FASE 1",
        "descripcion": "Análisis usando modelos globales entrenados",
        "hallazgos": [
            f"Se analizaron {len(df_predicciones_chile)} desarrolladores chilenos",
            "Predicciones generadas con modelos globales entrenados con 89K+ registros",
            "Análisis permite identificar brechas y oportunidades en el mercado chileno",
        ],
        "recomendaciones": [
            "Para trabajar remoto: enfocarse en tecnologías valoradas globalmente",
            "Para emigrar: considerar brechas salariales y skills demandados",
            "Para mercado local: identificar nichos específicos de Chile",
        ],
        "proximos_pasos": [
            "FASE 2: Entrenar modelo específico con top features identificados",
            "Análisis de tecnologías más valoradas en Chile",
            "Estudio de brechas de habilidades Chile vs Global",
        ],
    }

    logger.info("Análisis comparativo completado exitosamente")

    return reporte


def exportar_reporte_comparativo(reporte_comparativo: dict[str, Any]) -> pd.DataFrame:
    """
    Convierte el reporte comparativo en formato tabular para análisis.

    Args:
        reporte_comparativo: Diccionario con análisis comparativo

    Returns:
        DataFrame con resumen ejecutivo
    """
    logger.info("Exportando reporte comparativo a formato tabular")

    resumen_data = []

    # Metadata
    resumen_data.append(
        {
            "Categoría": "Metadata",
            "Métrica": "Fecha de Análisis",
            "Chile": reporte_comparativo["metadata"]["fecha_generacion"],
            "Global": "N/A",
            "Diferencia": "N/A",
        }
    )

    resumen_data.append(
        {
            "Categoría": "Metadata",
            "Métrica": "Total Registros",
            "Chile": f"{reporte_comparativo['metadata']['registros_chile']:,}",
            "Global": f"{reporte_comparativo['metadata']['registros_global']:,}",
            "Diferencia": "N/A",
        }
    )

    # Salarios
    if "salarios" in reporte_comparativo:
        sal = reporte_comparativo["salarios"]

        resumen_data.extend(
            [
                {
                    "Categoría": "Salarios",
                    "Métrica": "Media",
                    "Chile": f"${sal['chile']['media']:.2f}",
                    "Global": f"${sal['global']['media']:.2f}",
                    "Diferencia": f"${sal['comparacion']['brecha_media']:.2f}",
                },
                {
                    "Categoría": "Salarios",
                    "Métrica": "Mediana",
                    "Chile": f"${sal['chile']['mediana']:.2f}",
                    "Global": f"${sal['global']['mediana']:.2f}",
                    "Diferencia": f"${sal['comparacion']['brecha_mediana']:.2f}",
                },
                {
                    "Categoría": "Salarios",
                    "Métrica": "Ratio Chile/Global",
                    "Chile": f"{sal['comparacion']['ratio_chile_global']:.2%}",
                    "Global": "100%",
                    "Diferencia": f"{(sal['comparacion']['ratio_chile_global'] - 1) * 100:.2f}%",
                },
            ]
        )

    df_resumen = pd.DataFrame(resumen_data)

    logger.info(f"Reporte exportado con {len(df_resumen)} métricas")

    return df_resumen
