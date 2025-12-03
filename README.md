# ML Análisis Ecosistema Dev

**Sistema completo de Machine Learning para predicción salarial y análisis del ecosistema tecnológico de desarrolladores.**

> **Proyecto Completo y Listo para Producción**  
> **R² = 0.9130** (LightGBM) | **Accuracy = 98.59%** (XGBoost Classification)  
> **89,184 desarrolladores** analizados de 185 países

## Inicio Rápido

### Ejecución con Un Solo Comando

**Windows**: Haz clic o ejecuta → **[`run_project.bat`](./run_project.bat)**
```cmd
run_project.bat
```

**Mac/Linux**: Ejecuta → **[`run_project.sh`](./run_project.sh)**
```bash
chmod +x scripts/setup-and-run.sh
./scripts/setup-and-run.sh
```

### Modo Producción (Docker - Opcional)

**Windows**: **[`scripts/start_production.bat`](./scripts/start_production.bat)**
```cmd
scripts\start_production.bat
```

**Mac/Linux**: **[`scripts/start_production.sh`](./scripts/start_production.sh)**
```bash
chmod +x scripts/start_production.sh
./scripts/start_production.sh
```

**Acceso a servicios en Docker**:
- Airflow UI: http://localhost:8081 (usuario: `airflow` / contraseña: `airflow`)
- Kedro Viz: http://localhost:4141

> **Nota**: Docker **NO ejecuta Jupyter Lab**. Para usar Jupyter, sigue las instrucciones en la sección [Jupyter Lab (Análisis Interactivo)](#jupyter-lab-análisis-interactivo) más abajo.

---

### ¿Qué hacen estos scripts?

Estos scripts automatizan todo:
- Verificación de Python
- Creación de entorno virtual
- Instalación de dependencias
- Descarga de datos (DVC)
- Ejecución completa de pipelines
- Generación de modelos, métricas y gráficos

## Documentación Principal

### Informes Finales (PDF)

- **[Informe Técnico Completo (PDF)](./INFORME_ECOSISTEMA_DEV.pdf)** - Versión PDF del informe técnico completo con toda la metodología, resultados y análisis
- **[Guía de Stack Tecnológico para Chile (PDF)](./GUIA_STACK_TECNOLOGICO_CHILE.pdf)** - Versión PDF de la guía consolidada con 467 desarrolladores chilenos: decisiones informadas sobre stack, demanda, especializaciones y mercados exclusivos

### Informes Finales (Markdown)

- **[Informe Técnico Completo](./docs/informe_final/INFORME_ECOSISTEMA_DEV.md)** - Con toda la metodología, resultados y análisis
- **[Guía de Stack Tecnológico para Chile](./docs/informe_final/GUIA_STACK_TECNOLOGICO_CHILE.md)** - Análisis consolidado con 467 desarrolladores chilenos: decisiones informadas sobre stack, demanda, especializaciones y mercados exclusivos
- **[Análisis Exploratorio](./notebooks/01_analisis_exploratorio.ipynb)** - Exploración inicial de datos, distribuciones y patrones
- **[Análisis de Resultados](./notebooks/02_analisis_resultados.ipynb)** - Evaluación de 10 modelos ML (regresión y clasificación)
- **[Análisis Ecosistema](./notebooks/03_analisis_ecosistema.ipynb)** - Tendencias tecnológicas, salarios y adopción de IA
- **[Análisis de Clustering](./notebooks/04_analisis_clustering.ipynb)** - Segmentación de desarrolladores con modelos no supervisados (K-Means, Hierarchical, DBSCAN, GMM)
- **[Licencias de Datos](./docs/DATA_LICENSES.md)** - Stack Overflow ODbL
- **[Documentación Técnica Docker](./docs/referencias/docker_SUMMARY.md)** - Resumen ejecutivo sobre productividad y containerización

---

## Resultados del Proyecto

### Modelos de Regresión (Predicción Salarial)

| Modelo               | R² Score   | RMSE (USD)  | MAE (USD)  |
| -------------------- | ---------- | ----------- | ---------- |
| Linear Regression    | 0.5234     | $32,824     | $23,966    |
| Ridge Regression     | 0.5239     | $32,840     | $23,966    |
| Random Forest        | 0.8456     | $18,479     | $10,127    |
| XGBoost              | 0.9023     | $16,051     | $6,789     |
| **LightGBM (MEJOR)** | **0.9130** | **$15,845** | **$6,384** |

### Modelos de Clasificación (Nivel de Experiencia)

| Modelo              | Accuracy   | F1-Score   |
| ------------------- | ---------- | ---------- |
| Logistic Regression | 84.02%     | 0.8312     |
| Decision Tree       | 90.74%     | 0.9021     |
| Random Forest       | 96.79%     | 0.9654     |
| **XGBoost (MEJOR)** | **98.59%** | **0.9769** |
| LightGBM            | 97.27%     | 0.9698     |

### Features Más Importantes (LightGBM)

1. **YearsCodePro** (32.4%) - Experiencia profesional
2. **Country_US** (15.6%) - Mercado estadounidense
3. **lang_Rust** (8.9%) - Lenguaje nicho alto valor
4. **lang_Scala** (8.1%) - Lenguaje enterprise
5. **tools_Kubernetes** (6.7%) - Skills DevOps
6. **tools_AWS** (6.3%) - Skills cloud

### Insights del Ecosistema

- **JavaScript domina**: 69.9% de desarrolladores (63,000+)
- **TypeScript crece**: 43.1% adopción (+12pp vs 2022)
- **Rust premium**: Salario mediano $96K (+28% vs global)
- **Cloud skills**: +20%-25% impacto salarial
- **Chile vs Global**: Gap salarial -36% (mid-level)

---

## Tecnologías Utilizadas

### Stack MLOps
- **Kedro 0.19.12** - Pipeline framework
- **DVC** - Versionado de datos/modelos
- **Docker** - Containerización
- **Apache Airflow** - Orquestación (opcional)

### Machine Learning
- **Scikit-learn** - Modelos baseline y preprocessing
- **XGBoost** - Gradient boosting
- **LightGBM** - Gradient boosting optimizado
- **Pandas** - Manipulación de datos
- **Matplotlib/Seaborn** - Visualizaciones

### Datasets
- **Stack Overflow 2023**: 89,184 desarrolladores, 185 países
- **Stack Overflow 2025**: 49,123 desarrolladores (análisis temporal y adopción de IA)
- **JetBrains 2025**: 24,534 desarrolladores (comparativa inter-comunidad)

---

## Metodología

Proyecto desarrollado siguiendo **CRISP-DM**:

1. **Business Understanding**: Predecir salarios y entender ecosistema tech
2. **Data Understanding**: Análisis exploratorio de 89K+ registros
3. **Data Preparation**: Feature engineering (84 → 556 features)
4. **Modeling**: Entrenamiento de 10 modelos (5 regresión + 5 clasificación)
5. **Evaluation**: R² > 0.85, Accuracy > 90%
6. **Deployment**: Docker + scripts automatizados

---

## Uso Detallado

### Ejecución Manual

```bash
# 1. Crear entorno virtual
python -m venv .venv

# 2. Activar entorno (Windows)
.venv\Scripts\activate
# o en Mac/Linux:
source .venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar pipeline completo
kedro run

# 5. Ejecutar pipeline específico
kedro run --pipeline=data_science_regresion
```

### Jupyter Lab (Análisis Interactivo)

**Jupyter Lab NO se ejecuta en Docker**. Debes iniciarlo localmente en tu entorno virtual.

#### Iniciar Jupyter Lab

```bash
# 1. Activar entorno virtual primero
# Windows:
.venv\Scripts\activate

# Mac/Linux:
source .venv/bin/activate

# 2. Iniciar Jupyter Lab
jupyter lab
```

Luego abre en tu navegador: **http://localhost:8888**

> **Tip**: Si el puerto 8888 está ocupado, Jupyter usará automáticamente el siguiente disponible (8889, 8890, etc.) y te mostrará la URL en la terminal.

#### Notebooks Disponibles

Una vez que Jupyter Lab esté corriendo, encontrarás estos notebooks en la carpeta `notebooks/`:

- **[`01_analisis_exploratorio.ipynb`](./notebooks/01_analisis_exploratorio.ipynb)** - Exploración inicial de datos, distribuciones y patrones
- **[`02_analisis_resultados.ipynb`](./notebooks/02_analisis_resultados.ipynb)** - Evaluación completa de modelos (regresión y clasificación)
- **[`03_analisis_ecosistema.ipynb`](./notebooks/03_analisis_ecosistema.ipynb)** - Análisis del ecosistema tecnológico y adopción de IA
- **[`04_analisis_clustering.ipynb`](./notebooks/04_analisis_clustering.ipynb)** - Segmentación de desarrolladores con clustering (K-Means, Hierarchical, DBSCAN, GMM)

#### Solución de Problemas

**Si Jupyter no inicia:**
```bash
# Verificar que jupyterlab esté instalado
pip list | grep jupyterlab

# Si no está, instalar
pip install jupyterlab

# O reinstalar todas las dependencias
pip install -r requirements.txt
```

**Si el puerto está ocupado:**
```bash
# Iniciar Jupyter en un puerto específico
jupyter lab --port 8889
```

### Apache Airflow (Orquestación Opcional)

Si ejecutó los scripts de producción con Docker, Airflow ya está corriendo:

```bash
# Ejecuta el script de producción
scripts\start_production.bat  # Windows
# o
./scripts/setup-and-run.sh  # Mac/Linux
```

**Acceso a Airflow UI**: http://localhost:8081  
**Usuario**: `airflow`  
**Contraseña**: `airflow`

### Jupyter Notebooks

```bash
# Iniciar Jupyter
jupyter lab

# Abrir notebooks de análisis
# - notebooks/01_analisis_exploratorio.ipynb
# - notebooks/02_analisis_resultados.ipynb
# - notebooks/03_analisis_ecosistema.ipynb
# - notebooks/04_analisis_clustering.ipynb
```

### Docker (Opcional)

```bash
# Construir imagen
docker build -t ml-ecosistema-dev .

# Ejecutar contenedor
docker-compose up
```

> **Documentación técnica**: Para más información sobre los beneficios de Docker y containerización en este proyecto, ver [Documentación Técnica Docker](./docs/referencias/docker_SUMMARY.md).

---

## Outputs del Proyecto

Después de ejecutar `scripts/setup-and-run.sh`:

- **`data/06_models/`**: Modelos entrenados (.pkl)
  - `regresion_model.pkl` (LightGBM)
  - `clasificacion_model.pkl` (XGBoost)
  - `ridge_poly_model.pkl` (Ridge Polinomial)
  - `clustering_kmeans_model.pkl` (K-Means)
  - `clustering_scaler.pkl` (Scaler para clustering)
  
- **`data/07_model_output/`**: Resultados y datos procesados
  - `datos_con_clusters.parquet` (Datos con asignación de clusters)
  
- **`data/08_reporting/`**: Métricas y visualizaciones
  - **Métricas (.json)**: `metrics.json`, `metrics_clf.json`, `metrics_clustering.json`, `metrics_ridge_poly.json`
  - **Visualizaciones de modelos**: Comparación de modelos, Feature importance, Confusion matrices
  - **Visualizaciones de clustering**: PCA, dendrogramas, comparación de algoritmos
  - **Visualizaciones de ecosistema**: Tendencias tecnológicas, adopción de IA, análisis temporal

---

## Impacto y Aplicaciones

### Para Desarrolladores
- Roadmap basado en datos para upskilling
- Benchmark salarial por tecnología
- Identificación de skills premium (Rust, K8s, AWS)

### Para Empresas
- Estructuración salarial basada en mercado
- Identificación de skills gap
- Predicción de costo de contratación

### Para el Ecosistema Chileno
- Primera caracterización cuantitativa del mercado tech
- Brechas tecnológicas identificadas (TypeScript, Rust, Go)
- Recomendaciones para política pública educativa

---

## Trabajo Futuro y Proyecciones Personales

> **Nota**: Las siguientes proyecciones representan ideas personales para continuar desarrollando este proyecto como parte de mi portfolio profesional, aplicando y expandiendo los conocimientos adquiridos durante el desarrollo de este trabajo académico. No constituyen compromisos ni requisitos del proyecto actual.

### Mejoras de Modelos
- [ ] Hyperparameter tuning con Optuna o Ray Tune
- [ ] Ensemble stacking (LightGBM + XGBoost)
- [ ] Validación cruzada más robusta y análisis de varianza

### Expansión de Datos
- [x] Integración JetBrains 2025 (Completado)
- [ ] Dataset LATAM (Chile, Argentina, Colombia) - Datasets específicos no encontrados
- [ ] Serie temporal 2020-2025 - Limitado por falta de datos de IA en años anteriores

### Dashboard Interactivo (Streamlit App)

**Proyección**: Desarrollo de una aplicación web interactiva usando **Streamlit** (framework de Python para crear dashboards sin necesidad de HTML/CSS/JavaScript) que permita:

1. **Salary Calculator**: Input de skills, experiencia y país → Output de salario estimado
2. **Tech Roadmap Simulator**: Simulador interactivo que muestre el impacto salarial de aprender nuevas tecnologías (ej: "¿Si aprendo Rust, cuánto aumentaría mi salario?")
3. **Market Trends Dashboard**: Visualizaciones dinámicas de tecnologías crecientes vs declinantes
4. **Country Comparison**: Comparador interactivo Chile vs Argentina vs Colombia vs Global
5. **Brecha Chile vs Global**: Análisis visual de las brechas tecnológicas y salariales identificadas

**Justificación**: Esta aplicación web permitiría hacer accesibles los insights del proyecto a desarrolladores y empresas, transformando los modelos entrenados en una herramienta práctica y visual.

### Extensiones y Análisis Avanzados

#### Análisis Cualitativo
- [ ] Entrevistas en profundidad con 50+ desarrolladores chilenos
- [ ] Survey complementario con 500+ desarrolladores (soft skills, satisfacción laboral, work-life balance)
- [ ] Análisis NLP sobre transcripciones de entrevistas

#### Análisis Causal
- [ ] Experimento natural: Análisis Difference-in-Differences (DiD) para medir impacto causal de aprender nuevas tecnologías
- [ ] Propensity Score Matching: Medir efecto causal de skills cloud en salarios

---

## Autor

**Héctor Aguila V.**  
Email: he.aguila@duocuc.cl  
Institución: DuocUC - Ingeniería en Informática  
GitHub: [@HecAguilaV](https://github.com/HecAguilaV)

---

## Licencia

- **Código**: MIT License
- **Datos**: Open Database License (ODbL) v1.0 (Stack Overflow)
- Ver [LICENSE](./LICENSE) y [DATA_LICENSES.md](./docs/DATA_LICENSES.md)

---

>**© 2025 - Un Soñador con Poca RAM 👨🏻‍💻**