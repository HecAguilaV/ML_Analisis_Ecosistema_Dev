"""
Nodos para el pipeline de procesamiento de datos de IA.
Extrae, normaliza y consolida información sobre IA de los 3 datasets.
"""

import logging
from typing import Dict, List

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


def extraer_datos_ia_so_2023(df_so_2023: pd.DataFrame) -> pd.DataFrame:
    """
    Extrae y procesa datos de IA del dataset Stack Overflow 2023.

    Columnas de IA en SO 2023:
    - AISearchHaveWorkedWith: Herramientas de búsqueda con IA
    - AISearchWantToWorkWith: Herramientas de búsqueda deseadas
    - AIDevHaveWorkedWith: Herramientas de desarrollo con IA
    - AIDevWantToWorkWith: Herramientas de desarrollo deseadas
    - SOAI: Uso de Stack Overflow con IA
    - AISelect: Selección de herramientas de IA
    - AISent: Sentimiento sobre IA
    - AIAcc: Precisión de IA
    - AIBen: Beneficios de IA
    - AIToolInterested in Using: Herramientas de interés
    - AIToolCurrently Using: Herramientas en uso
    - AIToolNot interested in Using: Herramientas no de interés

    Args:
        df_so_2023: DataFrame de Stack Overflow 2023

    Returns:
        DataFrame con datos de IA procesados de SO 2023
    """
    logger.info("--- Extrayendo datos de IA de Stack Overflow 2023 ---")

    # Identificar columnas relacionadas con IA
    ai_columns_2023 = [
        "AISearchHaveWorkedWith",
        "AISearchWantToWorkWith",
        "AIDevHaveWorkedWith",
        "AIDevWantToWorkWith",
        "SOAI",
        "AISelect",
        "AISent",
        "AIAcc",
        "AIBen",
        "AIToolInterested in Using",
        "AIToolCurrently Using",
        "AIToolNot interested in Using",
    ]

    # Filtrar columnas que existen en el dataset
    ai_cols_disponibles = [col for col in ai_columns_2023 if col in df_so_2023.columns]

    if not ai_cols_disponibles:
        logger.warning("No se encontraron columnas de IA en SO 2023")
        return pd.DataFrame()

    # Seleccionar columnas de IA + identificadores básicos
    cols_base = ["ResponseId"] if "ResponseId" in df_so_2023.columns else []
    if "Country" in df_so_2023.columns:
        cols_base.append("Country")
    if "YearsCodePro" in df_so_2023.columns:
        cols_base.append("YearsCodePro")

    df_ia_2023 = df_so_2023[cols_base + ai_cols_disponibles].copy()
    df_ia_2023["Dataset"] = "Stack Overflow 2023"
    df_ia_2023["Year"] = 2023

    logger.info(
        f"SO 2023 - Datos de IA extraídos: {len(df_ia_2023):,} registros, "
        f"{len(ai_cols_disponibles)} columnas de IA"
    )

    return df_ia_2023


def extraer_datos_ia_so_2025(df_so_2025: pd.DataFrame) -> pd.DataFrame:
    """
    Extrae y procesa datos de IA del dataset Stack Overflow 2025.

    Columnas de IA en SO 2025 (estructura diferente a 2023):
    - LearnCodeAI: Aprendizaje de código con IA
    - AILearnHow: Cómo aprenden con IA
    - AIThreat: Percepción de amenaza de IA
    - AIModelsChoice: Elección de modelos de IA
    - AIModelsHaveWorkedWith: Modelos de IA usados
    - AIModelsWantToWorkWith: Modelos de IA deseados
    - AIModelsAdmired: Modelos de IA admirados
    - AISelect: Selección de herramientas de IA
    - AISent: Sentimiento sobre IA
    - AIAcc: Precisión de IA
    - AIComplex: Complejidad de IA
    - AIToolCurrently partially AI: Herramientas parcialmente con IA
    - AIToolDon't plan to use AI for this task: Sin planes de usar IA
    - AIToolPlan to partially use AI: Planes de usar IA parcialmente
    - AIToolPlan to mostly use AI: Planes de usar IA mayormente
    - AIToolCurrently mostly AI: Actualmente usando IA mayormente
    - AIFrustration: Frustraciones con IA
    - AIExplain: Explicación de IA
    - AIAgents: Agentes de IA
    - AIAgentChange: Cambios en agentes de IA
    - AIAgent_Uses: Usos de agentes de IA
    - AIAgentImpact*: Impacto de agentes de IA
    - AIAgentChallenges*: Desafíos de agentes de IA
    - AIAgentKnowledge: Conocimiento de agentes de IA
    - AIAgentKnowWrite: Escribir conocimiento de agentes
    - AIAgentOrchestration: Orquestación de agentes
    - AIAgentOrchWrite: Escribir orquestación
    - AIAgentObserveSecure: Observar seguridad de agentes
    - AIAgentObsWrite: Escribir observación
    - AIAgentExternal: Agentes externos de IA
    - AIAgentExtWrite: Escribir agentes externos
    - AIHuman: IA humana
    - AIOpen: IA abierta

    Args:
        df_so_2025: DataFrame de Stack Overflow 2025

    Returns:
        DataFrame con datos de IA procesados de SO 2025
    """
    logger.info("--- Extrayendo datos de IA de Stack Overflow 2025 ---")

    # Identificar columnas relacionadas con IA (buscar todas las que empiezan con "AI")
    ai_columns_2025 = [col for col in df_so_2025.columns if col.startswith("AI")]

    if not ai_columns_2025:
        logger.warning("No se encontraron columnas de IA en SO 2025")
        return pd.DataFrame()

    # Seleccionar columnas de IA + identificadores básicos
    cols_base = ["ResponseId"] if "ResponseId" in df_so_2025.columns else []
    if "Country" in df_so_2025.columns:
        cols_base.append("Country")
    if "YearsCodePro" in df_so_2025.columns:
        cols_base.append("YearsCodePro")

    df_ia_2025 = df_so_2025[cols_base + ai_columns_2025].copy()
    df_ia_2025["Dataset"] = "Stack Overflow 2025"
    df_ia_2025["Year"] = 2025

    logger.info(
        f"SO 2025 - Datos de IA extraídos: {len(df_ia_2025):,} registros, "
        f"{len(ai_columns_2025)} columnas de IA"
    )

    return df_ia_2025


def extraer_datos_ia_jetbrains_2025(df_jb_2025: pd.DataFrame) -> pd.DataFrame:
    """
    Extrae y procesa datos de IA del dataset JetBrains 2025.

    Columnas de IA en JetBrains 2025 (prefijo 'usage_ai_coding::', 'ai_', etc.):
    - usage_ai_coding::*: Uso de herramientas de IA para codificación
    - ide_change_reasons::My new main IDE / editor has better AI features or plugins
    - devops_ai_purpose::*: Propósito de IA en DevOps
    - ds_ai_usage::*: Uso de IA en Data Science
    - nocode_ai_benefits::*: Beneficios de IA en NoCode
    - ai_models_copilot::*: Modelos de IA (Copilot)
    - best_ai_llm_for_coding: Mejor LLM para codificación
    - ai_types_tools::*: Tipos de herramientas de IA
    - devareas_ai_used_in_company::*: Áreas donde se usa IA en la empresa
    - ai_coding_aspects_imp::*: Aspectos importantes de IA en codificación
    - ai_coding_tasks_freq::*: Frecuencia de tareas de codificación con IA
    - ai_benefits::*: Beneficios de IA
    - ai_time_saving: Ahorro de tiempo con IA
    - ai_coding_delegate::*: Delegación de codificación a IA
    - concerns_ai_coding: Preocupaciones sobre IA en codificación
    - areas_want_ai_assist::*: Áreas donde quieren asistencia de IA
    - expect_coding_change_due_ai::*: Expectativas de cambio debido a IA
    - ai_coding_statements_future::*: Declaraciones sobre IA en el futuro
    - job_challenges::Implementing AI into my workflow
    - emotions_about_ai_society: Emociones sobre IA en la sociedad
    - ethical_concerns_ai::*: Preocupaciones éticas sobre IA
    - selfmon_problems::I feel overwhelmed by the need to keep up with the rapid advancements in AI
    - selfmon_problems::I feel anxious that AI advancements might eventually replace my role
    - media_ai_news::*: Noticias de IA en medios
    - answers_platform::ChatGPT or other AI chatbots

    Args:
        df_jb_2025: DataFrame de JetBrains 2025

    Returns:
        DataFrame con datos de IA procesados de JetBrains 2025
    """
    logger.info("--- Extrayendo datos de IA de JetBrains 2025 ---")

    # Identificar columnas relacionadas con IA
    ai_keywords = [
        "usage_ai_coding",
        "ai_",
        "ide_change_reasons::My new main IDE / editor has better AI",
        "devops_ai_purpose",
        "ds_ai_usage",
        "nocode_ai_benefits",
        "ai_models_copilot",
        "best_ai_llm_for_coding",
        "ai_types_tools",
        "devareas_ai_used_in_company",
        "ai_coding_aspects_imp",
        "ai_coding_tasks_freq",
        "ai_benefits",
        "ai_time_saving",
        "ai_coding_delegate",
        "concerns_ai_coding",
        "areas_want_ai_assist",
        "expect_coding_change_due_ai",
        "ai_coding_statements_future",
        "job_challenges::Implementing AI",
        "emotions_about_ai_society",
        "ethical_concerns_ai",
        "selfmon_problems::I feel overwhelmed by the need to keep up with the rapid advancements in AI",
        "selfmon_problems::I feel anxious that AI advancements might eventually replace my role",
        "media_ai_news",
        "answers_platform::ChatGPT",
    ]

    # Buscar columnas que contengan keywords de IA
    ai_columns_jb = []
    for col in df_jb_2025.columns:
        col_lower = col.lower()
        if any(keyword.lower() in col_lower for keyword in ai_keywords):
            ai_columns_jb.append(col)

    if not ai_columns_jb:
        logger.warning("No se encontraron columnas de IA en JetBrains 2025")
        return pd.DataFrame()

    # Seleccionar columnas de IA + identificadores básicos
    cols_base = []
    if "id" in df_jb_2025.columns:
        cols_base.append("id")
    if "country" in df_jb_2025.columns:
        cols_base.append("country")
    if "years_of_experience" in df_jb_2025.columns:
        cols_base.append("years_of_experience")

    df_ia_jb = df_jb_2025[cols_base + ai_columns_jb].copy()
    df_ia_jb["Dataset"] = "JetBrains 2025"
    df_ia_jb["Year"] = 2025

    logger.info(
        f"JetBrains 2025 - Datos de IA extraídos: {len(df_ia_jb):,} registros, "
        f"{len(ai_columns_jb)} columnas de IA"
    )

    return df_ia_jb


def consolidar_datos_ia(
    df_ia_so_2023: pd.DataFrame,
    df_ia_so_2025: pd.DataFrame,
    df_ia_jb_2025: pd.DataFrame,
) -> pd.DataFrame:
    """
    Consolida los datos de IA de los 3 datasets en un único DataFrame.

    Estrategia de consolidación:
    1. Mantener todas las columnas de cada dataset
    2. Agregar prefijos para evitar conflictos de nombres
    3. Crear columnas comunes normalizadas cuando sea posible
    4. Mantener metadatos de origen (Dataset, Year)

    Args:
        df_ia_so_2023: DataFrame de IA de SO 2023
        df_ia_so_2025: DataFrame de IA de SO 2025
        df_ia_jb_2025: DataFrame de IA de JetBrains 2025

    Returns:
        DataFrame consolidado con todos los datos de IA
    """
    logger.info("--- Consolidando datos de IA de los 3 datasets ---")

    dfs_consolidados = []

    # Procesar SO 2023
    if not df_ia_so_2023.empty:
        df_so_2023_consolidado = df_ia_so_2023.copy()
        # Agregar prefijo a columnas (excepto las de metadatos)
        cols_meta = ["Dataset", "Year", "ResponseId", "Country", "YearsCodePro"]
        cols_renombrar = {
            col: f"SO2023_{col}"
            for col in df_so_2023_consolidado.columns
            if col not in cols_meta
        }
        df_so_2023_consolidado = df_so_2023_consolidado.rename(columns=cols_renombrar)
        dfs_consolidados.append(df_so_2023_consolidado)

    # Procesar SO 2025
    if not df_ia_so_2025.empty:
        df_so_2025_consolidado = df_ia_so_2025.copy()
        # Agregar prefijo a columnas (excepto las de metadatos)
        cols_meta = ["Dataset", "Year", "ResponseId", "Country", "YearsCodePro"]
        cols_renombrar = {
            col: f"SO2025_{col}"
            for col in df_so_2025_consolidado.columns
            if col not in cols_meta
        }
        df_so_2025_consolidado = df_so_2025_consolidado.rename(columns=cols_renombrar)
        dfs_consolidados.append(df_so_2025_consolidado)

    # Procesar JetBrains 2025
    if not df_ia_jb_2025.empty:
        df_jb_consolidado = df_ia_jb_2025.copy()
        # Agregar prefijo a columnas (excepto las de metadatos)
        cols_meta = ["Dataset", "Year", "id", "country", "years_of_experience"]
        cols_renombrar = {
            col: f"JB2025_{col}"
            for col in df_jb_consolidado.columns
            if col not in cols_meta
        }
        df_jb_consolidado = df_jb_consolidado.rename(columns=cols_renombrar)
        # Normalizar nombres de columnas de metadatos
        if "id" in df_jb_consolidado.columns:
            df_jb_consolidado = df_jb_consolidado.rename(columns={"id": "ResponseId"})
        if "country" in df_jb_consolidado.columns:
            df_jb_consolidado = df_jb_consolidado.rename(columns={"country": "Country"})
        if "years_of_experience" in df_jb_consolidado.columns:
            df_jb_consolidado = df_jb_consolidado.rename(
                columns={"years_of_experience": "YearsCodePro"}
            )
        dfs_consolidados.append(df_jb_consolidado)

    if not dfs_consolidados:
        logger.warning("No hay datos de IA para consolidar")
        return pd.DataFrame()

    # Combinar todos los DataFrames
    # Usar outer join para mantener todas las columnas
    df_consolidado = pd.concat(dfs_consolidados, axis=0, ignore_index=True, sort=False)

    logger.info(
        f"Datos de IA consolidados: {len(df_consolidado):,} registros, "
        f"{len(df_consolidado.columns)} columnas"
    )
    logger.info(f"  - Registros por dataset:")
    if "Dataset" in df_consolidado.columns:
        for dataset in df_consolidado["Dataset"].unique():
            count = (df_consolidado["Dataset"] == dataset).sum()
            logger.info(f"    • {dataset}: {count:,} registros")

    return df_consolidado

