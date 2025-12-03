"""Tests para el pipeline `data_analysis`.

Cobertura de tests para validar:
- Que el pipeline se construye sin errores
- Que los nodos principales funcionan correctamente con datos de ejemplo
- Validación de tipos de retorno
- Manejo de casos edge (datos vacíos, columnas faltantes, etc.)
"""

import pandas as pd
import pytest
from kedro.pipeline import Pipeline

from ml_analisis_ecosistema_dev.pipelines.data_analysis.nodes import (
    analyze_programming_languages,
    extract_salary_data,
    load_and_inspect_survey,
)
from ml_analisis_ecosistema_dev.pipelines.data_analysis.pipeline import (
    create_pipeline,
)


class TestPipelineStructure:
    """Tests para la estructura del pipeline."""

    def test_pipeline_builds(self):
        """El pipeline se construye correctamente."""
        pipeline = create_pipeline()
        assert isinstance(pipeline, Pipeline)
        assert len(pipeline.nodes) > 0

    def test_pipeline_has_expected_nodes(self):
        """El pipeline contiene los nodos esperados."""
        pipeline = create_pipeline()
        node_names = [node.name for node in pipeline.nodes]

        # Verificar que existen los nodos principales
        assert any(
            "load" in name.lower() or "inspect" in name.lower() for name in node_names
        )
        assert any(
            "language" in name.lower() or "programming" in name.lower()
            for name in node_names
        )
        assert any(
            "salary" in name.lower() or "extract" in name.lower() for name in node_names
        )


class TestLoadAndInspectSurvey:
    """Tests para la función load_and_inspect_survey."""

    def test_returns_dict(self):
        """La función retorna un diccionario."""
        df = pd.DataFrame({"col1": [1, 2, 3], "col2": [4, 5, 6]})
        result = load_and_inspect_survey(df)
        assert isinstance(result, dict)

    def test_contains_expected_keys(self):
        """El diccionario contiene las claves esperadas."""
        df = pd.DataFrame({"col1": [1, 2, 3], "col2": [4, 5, 6]})
        result = load_and_inspect_survey(df)

        expected_keys = {
            "total_filas",
            "total_columnas",
            "valores_nulos",
            "porcentaje_nulos",
            "mensaje",
        }
        assert expected_keys <= set(result.keys())

    def test_calculates_correct_statistics(self):
        """Calcula correctamente las estadísticas básicas."""
        df = pd.DataFrame({"col1": [1, 2, None], "col2": [4, None, 6]})
        result = load_and_inspect_survey(df)

        assert result["total_filas"] == 3
        assert result["total_columnas"] == 2
        assert result["valores_nulos"] == 2  # 2 valores None
        assert isinstance(result["porcentaje_nulos"], float)

    def test_handles_empty_dataframe(self):
        """Maneja correctamente un DataFrame vacío."""
        df = pd.DataFrame()
        result = load_and_inspect_survey(df)

        assert result["total_filas"] == 0
        assert result["total_columnas"] == 0
        assert result["valores_nulos"] == 0


class TestAnalyzeProgrammingLanguages:
    """Tests para la función analyze_programming_languages."""

    def test_returns_dataframe(self):
        """La función retorna un DataFrame."""
        df = pd.DataFrame(
            {
                "LanguageHaveWorkedWith": ["Python; SQL", "JavaScript", None],
                "OtherCol": [1, 2, 3],
            }
        )
        result = analyze_programming_languages(df)
        assert isinstance(result, pd.DataFrame)

    def test_contains_expected_columns(self):
        """El DataFrame contiene las columnas esperadas."""
        df = pd.DataFrame(
            {
                "LanguageHaveWorkedWith": ["Python; SQL", "JavaScript", None],
            }
        )
        result = analyze_programming_languages(df)

        expected_cols = {
            "columna",
            "respuestas_validas",
            "valores_unicos",
            "porcentaje_respuestas",
        }
        assert expected_cols <= set(result.columns)

    def test_finds_language_columns(self):
        """Encuentra correctamente las columnas relacionadas con lenguajes."""
        df = pd.DataFrame(
            {
                "LanguageHaveWorkedWith": ["Python", "JavaScript", "Java"],
                "LanguageWantToWorkWith": ["Rust", "Go", "Python"],
                "OtherCol": [1, 2, 3],
            }
        )
        result = analyze_programming_languages(df)

        # Debe encontrar al menos las columnas de lenguajes
        language_cols = result["columna"].tolist()
        assert "LanguageHaveWorkedWith" in language_cols
        assert "LanguageWantToWorkWith" in language_cols

    def test_handles_no_language_columns(self):
        """Maneja correctamente cuando no hay columnas de lenguajes."""
        df = pd.DataFrame(
            {
                "Col1": [1, 2, 3],
                "Col2": [4, 5, 6],
            }
        )
        result = analyze_programming_languages(df)

        # Debe usar las primeras 8 columnas como fallback
        assert len(result) > 0
        assert isinstance(result, pd.DataFrame)

    def test_calculates_percentages_correctly(self):
        """Calcula correctamente los porcentajes de respuestas."""
        df = pd.DataFrame(
            {
                "LanguageHaveWorkedWith": ["Python", "JavaScript", None],
            }
        )
        result = analyze_programming_languages(df)

        row = result[result["columna"] == "LanguageHaveWorkedWith"].iloc[0]
        assert row["respuestas_validas"] == 2  # 2 valores no nulos
        assert row["porcentaje_respuestas"] == pytest.approx(66.7, abs=0.1)


class TestExtractSalaryData:
    """Tests para la función extract_salary_data."""

    def test_returns_dataframe(self):
        """La función retorna un DataFrame."""
        df = pd.DataFrame(
            {
                "ConvertedComp": [50000, None, 30000],
                "Country": ["ES", "MX", "AR"],
            }
        )
        result = extract_salary_data(df)
        assert isinstance(result, pd.DataFrame)

    def test_finds_salary_columns(self):
        """Encuentra correctamente las columnas relacionadas con salarios."""
        df = pd.DataFrame(
            {
                "ConvertedComp": [50000, 60000, 70000],
                "ConvertedCompYearly": [50000, 60000, 70000],
                "OtherCol": [1, 2, 3],
            }
        )
        result = extract_salary_data(df)

        # Debe incluir las columnas de salario
        assert (
            "ConvertedComp" in result.columns or "ConvertedCompYearly" in result.columns
        )

    def test_includes_country_if_available(self):
        """Incluye la columna Country si está disponible."""
        df = pd.DataFrame(
            {
                "ConvertedComp": [50000, 60000, 70000],
                "Country": ["ES", "MX", "AR"],
            }
        )
        result = extract_salary_data(df)

        assert "Country" in result.columns

    def test_handles_no_salary_columns(self):
        """Maneja correctamente cuando no hay columnas de salario."""
        df = pd.DataFrame(
            {
                "Col1": [1, 2, 3],
                "Col2": [4, 5, 6],
            }
        )
        result = extract_salary_data(df)

        # Debe retornar un DataFrame con análisis básico
        assert isinstance(result, pd.DataFrame)
        assert len(result) > 0

    def test_extracts_correct_data(self):
        """Extrae correctamente los datos de salario."""
        df = pd.DataFrame(
            {
                "ConvertedComp": [50000, None, 30000],
                "Country": ["ES", "MX", "AR"],
            }
        )
        result = extract_salary_data(df)

        assert len(result) == 3  # Mismo número de filas
        assert "ConvertedComp" in result.columns
        assert "Country" in result.columns


class TestIntegration:
    """Tests de integración para el pipeline completo."""

    def test_pipeline_with_sample_data(self):
        """El pipeline funciona con datos de muestra."""
        sample_df = pd.DataFrame(
            {
                "LanguageHaveWorkedWith": ["Python; SQL", "JavaScript", "Java"],
                "ConvertedComp": [50000, None, 30000],
                "Country": ["ES", "MX", "AR"],
                "OtherCol": [1, 2, 3],
            }
        )

        # Ejecutar funciones individuales
        stats = load_and_inspect_survey(sample_df)
        assert isinstance(stats, dict)

        lang_df = analyze_programming_languages(sample_df)
        assert isinstance(lang_df, pd.DataFrame)

        sal_df = extract_salary_data(sample_df)
        assert isinstance(sal_df, pd.DataFrame)
