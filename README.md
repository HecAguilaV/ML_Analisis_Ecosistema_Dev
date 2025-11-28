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
./scripts/setup-and-run.sh
```

**Acceso a servicios en Docker**:
- Airflow UI: http://localhost:8081 (usuario: `airflow` / contraseña: `airflow`)
- Kedro Viz: http://localhost:4141

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

- **[Informe Técnico Completo](./docs/informe_final/02_INFORME_TECNICO_COMPLETO.md)** - ~100 páginas con toda la metodología, resultados y análisis
- **[Análisis de Resultados](./notebooks/02_analisis_de_resultados.ipynb)** - Evaluación de 10 modelos ML
- **[Análisis Ecosistema](./notebooks/03_ecosystem_analysis.ipynb)** - Tendencias tecnológicas y salarios
- **[Licencias de Datos](./docs/DATA_LICENSES.md)** - Stack Overflow ODbL

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
- **JetBrains 2025**: Pendiente integración

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

Para explorar los notebooks interactivamente:

```bash
# Activar entorno virtual primero
.venv\Scripts\activate  # Windows
# o
source .venv/bin/activate  # Mac/Linux

# Iniciar Jupyter Lab
jupyter lab
```

Luego abre en tu navegador: **http://localhost:8888**

**Notebooks disponibles**:
- [`notebooks/02_analisis_de_resultados.ipynb`](./notebooks/02_analisis_de_resultados.ipynb) - Evaluación completa de modelos
- [`notebooks/03_ecosystem_analysis.ipynb`](./notebooks/03_ecosystem_analysis.ipynb) - Análisis del ecosistema tecnológico

### Apache Airflow (Orquestación Opcional)

Si ejecutaste los scripts de producción con Docker, Airflow ya está corriendo:

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
# - notebooks/02_analisis_de_resultados.ipynb
# - notebooks/03_ecosystem_analysis.ipynb
```

### Docker (Opcional)

```bash
# Construir imagen
docker build -t ml-ecosistema-dev .

# Ejecutar contenedor
docker-compose up
```

---

## Outputs del Proyecto

Después de ejecutar `scripts/setup-and-run.sh`:

- **`data/06_models/`**: Modelos entrenados (.pkl)
  - `regresion_model.pkl` (LightGBM)
  - `clasificacion_model.pkl` (XGBoost)
  
- **`data/07_model_output/`**: Métricas (.json)
  - `regresion_metrics.json`
  - `clasificacion_metrics.json`
  
- **`data/08_reporting/`**: Visualizaciones (.png)
  - Comparación de modelos
  - Feature importance
  - Confusion matrices
  - Distribuciones salariales

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

## Trabajo Futuro

### Mejoras de Modelos
- [ ] Hyperparameter tuning con Optuna
- [ ] Ensemble stacking (LightGBM + XGBoost)
- [ ] Deep learning (TabNet, FT-Transformer)

### Expansión de Datos
- [ ] Integración JetBrains 2025
- [ ] Dataset LATAM (Chile, Argentina, Colombia)
- [ ] Serie temporal 2020-2025

### Dashboard Interactivo
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