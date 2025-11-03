# 🗺️ Roadmap: Plataforma Inteligente de Decisiones Tech Chile

## 🎯 Misión del Proyecto

Desarrollar una **plataforma web inteligente** que guíe a desarrolladores chilenos en la toma de decisiones estratégicas sobre tecnologías, lenguajes y herramientas del ecosistema de desarrollo, basándose en datos reales del mercado laboral nacional, regional y global.

---

## 🎓 Objetivo Final

Crear una **aplicación web predictiva** que permita a desarrolladores:

- 📊 **Predecir salarios** según perfil (país, experiencia, tecnologías)
- 🛠️ **Recomendar stacks tecnológicos** óptimos para maximizar empleabilidad
- 🗺️ **Generar roadmaps personalizados** de aprendizaje
- 🌎 **Comparar mercados**: Chile vs Latinoamérica vs Global
- 🤖 **Evaluar impacto de IA** y tecnologías emergentes en el mercado

---

## 🏗️ Arquitectura Objetivo

```
┌─────────────────────────────────────────────────────────────┐
│                    CAPA DE DATOS                            │
│  Stack Overflow 2023 + 2025  |  JetBrains 2025             │
│         DVC (Versionado)     |  GCS (Storage)              │
└──────────────────┬──────────────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────────────┐
│                 BACKEND ML (Kedro)                          │
│  Pipelines: procesamiento | regresión | clasificación       │
│  Modelos: RandomForest, XGBoost, Ridge, LGBM (10 total)    │
│  Métricas: R², RMSE, MAE, Accuracy, F1-Score               │
└──────────────────┬──────────────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────────────┐
│                  API REST (FastAPI)                         │
│  Endpoints:                                                  │
│    • POST /predict/salary      → Predicción salarial        │
│    • POST /predict/ranking     → Clasificación experiencia  │
│    • POST /recommend/stack     → Recomendación tecnológica  │
│    • GET  /stats/chile         → Estadísticas Chile         │
└──────────────────┬──────────────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────────────┐
│              FRONTEND WEB (Streamlit)                       │
│  Inputs del usuario:                                         │
│    • País (default: Chile)                                  │
│    • Años de experiencia                                    │
│    • Lenguajes actuales                                     │
│    • Sector de interés                                      │
│                                                              │
│  Outputs predictivos:                                        │
│    • Salario estimado (Chile vs Global)                     │
│    • Stack recomendado (% match)                            │
│    • Roadmap de aprendizaje priorizado                      │
│    • Comparativa regional                                   │
└──────────────────┬──────────────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────────────┐
│            DEPLOYMENT (Docker + Cloud)                      │
│  Docker Compose: backend + frontend + nginx                 │
│  CI/CD: GitHub Actions                                       │
│  Cloud: GCP Cloud Run / AWS ECS                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 📊 Fases de Desarrollo

### ✅ **Fase 1: Backend ML - Pipelines Kedro** (COMPLETADO - Oct 2025)

**Objetivo**: Implementar pipelines ML reproducibles con validación académica.

**Entregables completados:**
- ✅ Pipeline `procesamiento_de_datos`: Limpieza, encoding, feature engineering
- ✅ Pipeline `regresion`: 5 modelos (RandomForest, XGBoost, Ridge, Lasso, LinearRegression)
- ✅ Pipeline `clasificacion`: 5 modelos (LGBM, GradientBoosting, XGBoost, RandomForest, LogisticRegression)
- ✅ Pipeline `regresion_polinomial`: Modelo experimental con features polinómicas
- ✅ Validación cruzada k-fold (k≥5) en todos los modelos
- ✅ Métricas completas: R², RMSE, MAE (regresión) | Accuracy, F1, Precision, Recall, ROC-AUC (clasificación)
- ✅ Versionado de datos con DVC + Google Cloud Storage
- ✅ Notebooks de análisis: `01_exploratory_analysis.ipynb`, `02_analisis_de_resultados.ipynb`

**Mejor Modelo Regresión:** RandomForestRegressor (R²=0.9091, RMSE=$15,800, MAE=$6,181)  
**Mejor Modelo Clasificación:** LGBMClassifier (Accuracy=98.49%, F1=0.9751, ROC-AUC=0.9977)

**Stack Tecnológico:**
- Python 3.10+
- Kedro 0.19.15
- Scikit-learn, XGBoost, LightGBM
- DVC, Pandas, NumPy

---

### 🔄 **Fase 2: Análisis e Informes Técnicos** (EN PROGRESO - Nov 2025)

**Objetivo**: Documentar hallazgos científicos y generar informes profesionales.

**Tareas en progreso:**
- 🔄 Notebook `02_analisis_de_resultados.ipynb`: Visualizaciones avanzadas, comparativas
- 🔄 Sección "Data Understanding": Exploración de datasets (shape, describe, distribuciones)
- 🔄 Sección "Análisis Mercado Chile": Segmentación geográfica, comparativa regional
- 🔄 Integrar informe técnico Docker en documentación
- 🔄 Actualizar README.md con visión completa del proyecto

**Entregables pendientes:**
- ⏳ Estructura `docs/informe_final/`: README, TODO, templates
- ⏳ Disclaimer en `docs/informe_v1/INFORME_MERCADO_TECH_CHILE.md`
- ⏳ Exportar notebook a PDF profesional para entrega académica

**Duración estimada:** 1-2 semanas

---

### ⏳ **Fase 3: Análisis Comparativo 2023→2025 (Impacto IA)** (Q4 2025)

**Objetivo**: Identificar cambios en el mercado tech por la adopción masiva de IA.

**Tareas planificadas:**
- ⏳ Notebook `03_analisis_comparativo_2023_2025.ipynb`
- ⏳ Cargar Stack Overflow Survey 2025 (ya disponible en `data/01_raw/stackoverflow_2025/`)
- ⏳ Comparar adopción de herramientas:
  - GitHub Copilot (0% → 60% adopción)
  - ChatGPT para desarrollo
  - IA coding assistants
- ⏳ Analizar nuevas skills emergentes:
  - Prompt Engineering
  - LLM integration
  - Vector databases
- ⏳ Comparar salarios pre-IA (2023) vs post-IA (2025)
- ⏳ Identificar tecnologías emergentes (LangChain, Pinecone, etc.)

**Entregables:**
- Notebook comparativo ejecutable
- Informe `docs/informe_final/04_COMPARATIVA_2023_2025.md`
- Gráficos de evolución temporal

**Duración estimada:** 2-3 semanas

---

### ⏳ **Fase 4: Segmentación Mercado Chileno** (Q4 2025)

**Objetivo**: Análisis profundo del ecosistema tech en Chile vs LATAM vs Global.

**Tareas planificadas:**
- ⏳ Notebook `04_segmentacion_mercado_chile.ipynb`
- ⏳ Filtrar datos por país: Chile, Argentina, Colombia, Brasil, México
- ⏳ Análisis salarial por región chilena (RM vs regiones)
- ⏳ Identificar brechas de habilidades (skills gap)
- ⏳ Tecnologías más demandadas en Chile
- ⏳ Comparativa salarios Chile vs vecinos LATAM
- ⏳ Oportunidades laborales por sector (FinTech, HealthTech, etc.)

**Entregables:**
- Notebook de segmentación ejecutable
- Informe `docs/informe_final/03_MERCADO_CHILE.md`
- Mapas de calor y gráficos geográficos

**Duración estimada:** 2 semanas

---

### ⏳ **Fase 5: API Backend (FastAPI)** (Final Semestre - Dic 2025)

**Objetivo**: Exponer modelos ML como API REST para consumo web.

**Tareas planificadas:**
- ⏳ Estructura `webapp/backend/`:
  - `api.py`: Endpoints FastAPI
  - `models/`: Cargar modelos `.pkl` entrenados
  - `schemas.py`: Pydantic models para validación
  - `utils.py`: Funciones auxiliares
- ⏳ Endpoints a implementar:
  - `POST /predict/salary`: Predicción salarial
  - `POST /predict/ranking`: Clasificación de experiencia
  - `POST /recommend/stack`: Recomendación de stack tecnológico
  - `GET /stats/chile`: Estadísticas del mercado chileno
  - `GET /health`: Health check
- ⏳ Integración con modelos Kedro:
  - Cargar `RandomForestRegressor` (regresión)
  - Cargar `LGBMClassifier` (clasificación)
- ⏳ Documentación automática con Swagger UI
- ⏳ Tests unitarios con pytest

**Stack Tecnológico:**
- FastAPI
- Pydantic
- Uvicorn
- Joblib (carga de modelos)

**Duración estimada:** 2-3 semanas

---

### ⏳ **Fase 6: Frontend Web (Streamlit)** (Final Semestre - Dic 2025)

**Objetivo**: Interfaz de usuario interactiva para consumir predicciones.

**Tareas planificadas:**
- ⏳ Estructura `webapp/frontend/`:
  - `app.py`: Aplicación principal Streamlit
  - `components/`: Widgets personalizados
  - `pages/`: Múltiples páginas (predicción, análisis, about)
- ⏳ Features de la interfaz:
  - **Formulario de entrada**:
    - Selector de país (default: Chile)
    - Slider de años de experiencia
    - Multiselect de lenguajes actuales
    - Selector de sector de interés
  - **Outputs predictivos**:
    - Salario estimado con intervalo de confianza
    - Ranking de experiencia (Junior/Mid/Senior)
    - Stack tecnológico recomendado con % de match
    - Comparativa Chile vs LATAM vs Global
  - **Visualizaciones interactivas**:
    - Gráficos Plotly
    - Mapas geográficos
    - Tablas de rankings
- ⏳ Integración con API backend (requests HTTP)

**Stack Tecnológico:**
- Streamlit
- Plotly
- Requests
- Pandas

**Duración estimada:** 2-3 semanas

---

### ⏳ **Fase 7: Deployment & DevOps** (Final Semestre - Dic 2025)

**Objetivo**: Dockerizar, orquestar y desplegar la aplicación completa.

**Tareas planificadas:**
- ⏳ Dockerización:
  - `webapp/backend/Dockerfile`: FastAPI + Uvicorn
  - `webapp/frontend/Dockerfile`: Streamlit
  - `docker-compose.yml`: Orquestación completa
- ⏳ CI/CD con GitHub Actions:
  - Workflow: tests → build → push a registry → deploy
  - Linters: black, flake8, mypy
  - Security scans: Trivy
- ⏳ Deployment en Cloud:
  - Opción A: GCP Cloud Run (serverless)
  - Opción B: AWS ECS + Load Balancer
  - Opción C: DigitalOcean App Platform
- ⏳ Monitoreo y observabilidad:
  - Logging centralizado
  - Métricas de uso (requests/s)
  - Alertas por errores
- ⏳ Documentación de deployment:
  - README operacional
  - Runbooks para troubleshooting
  - Guía de contribución

**Stack Tecnológico:**
- Docker & Docker Compose
- GitHub Actions
- GCP Cloud Run / AWS ECS
- Nginx (reverse proxy)

**Duración estimada:** 2 semanas

---

## 🛠️ Stack Tecnológico Completo

### **Data & ML**
- **Lenguaje**: Python 3.10+
- **Datos**: Pandas, NumPy, Polars
- **ML**: Scikit-learn, XGBoost, LightGBM, CatBoost
- **Feature Engineering**: Category Encoders, Feature-engine
- **Visualización**: Matplotlib, Seaborn, Plotly

### **MLOps & Orquestación**
- **Pipelines**: Kedro 0.19.15
- **Versionado**: DVC + Google Cloud Storage
- **Orquestación**: Apache Airflow (futuro)
- **Experiment Tracking**: MLflow (futuro)

### **Backend & API**
- **Framework**: FastAPI
- **Server**: Uvicorn
- **Validación**: Pydantic
- **Testing**: Pytest, Hypothesis

### **Frontend**
- **Framework**: Streamlit
- **Visualización**: Plotly Express, Altair
- **HTTP Client**: Requests

### **DevOps & Infraestructura**
- **Contenedores**: Docker, Docker Compose
- **CI/CD**: GitHub Actions
- **Cloud**: GCP (Cloud Run, GCS), AWS (ECS, S3)
- **Reverse Proxy**: Nginx
- **Monitoreo**: Prometheus, Grafana (futuro)

### **Documentación**
- **Notebooks**: Jupyter Lab
- **Docs**: Markdown, Mermaid (diagramas)
- **API Docs**: Swagger UI (auto-generado por FastAPI)

---

## 🎯 Criterios de Éxito

### **Académicos (Requisitos de Tesis)**
1. ✅ Implementar ≥5 modelos por pipeline (regresión + clasificación)
2. ✅ Validación cruzada con k≥5 folds
3. ✅ Comparación cuantitativa con tablas de métricas
4. ✅ Reproducibilidad con DVC
5. 🔄 Informe técnico completo (en progreso)
6. ⏳ Defensa de resultados con visualizaciones

### **Técnicos (Calidad MLOps)**
1. ✅ Pipeline reproducible end-to-end
2. ✅ Versionado de datos y modelos
3. ⏳ API REST funcional con documentación
4. ⏳ Tests automatizados (cobertura >80%)
5. ⏳ Dockerización completa
6. ⏳ CI/CD con despliegue automatizado

### **Producto (Valor para Usuarios)**
1. ⏳ Predicciones de salario con error <15%
2. ⏳ Recomendaciones de stack personalizadas
3. ⏳ Interfaz intuitiva (<5 min para obtener predicción)
4. ⏳ Datos actualizados (Stack Overflow 2025)
5. ⏳ Análisis específico para mercado chileno
6. ⏳ Aplicación desplegada y accesible públicamente

---

## 📅 Estado del Proyecto

| Fase | Estado | Entregables |
|------|--------|-------------|
| **Fase 1**: Backend ML | ✅ COMPLETADO | 5 modelos regresión + 5 clasificación, pipelines Kedro, DVC + GCS |
| **Fase 2**: Informes Técnicos | 🔄 EN PROGRESO | Notebooks de análisis, documentación científica |
| **Fase 3**: Análisis Comparativo | ⏳ PLANIFICADO | Comparación SO 2023 vs 2025, impacto IA |
| **Fase 4**: Segmentación Mercado | ⏳ PLANIFICADO | Análisis geográfico Chile, oportunidades regionales |
| **Fase 5**: API con FastAPI | ⏳ PLANIFICADO | Endpoints REST, documentación Swagger |
| **Fase 6**: Frontend Streamlit | ⏳ PLANIFICADO | Interfaz web interactiva, dashboards |
| **Fase 7**: Despliegue Cloud | ⏳ PLANIFICADO | Docker + Kubernetes, CI/CD, monitoreo |

---

## 🚀 Próximos Pasos Inmediatos

### **Tareas Completadas:**
1. ✅ Actualizar notebook con Ridge Polinomial en visualizaciones
2. ✅ Agregar sección "Data Understanding" al notebook
3. ✅ Crear ROADMAP.md con arquitectura del proyecto
4. ✅ Actualizar README.md con visión completa
5. ✅ Crear estructura `docs/informe_final/`
6. 🔄 Ejecutar análisis preliminar mercado Chile

### **Próximas Tareas:**
1. ⏳ Cargar Stack Overflow 2025 en pipeline Kedro
2. ⏳ Crear notebook `03_analisis_comparativo_2023_2025.ipynb`
3. ⏳ Análisis de impacto IA en salarios y tecnologías
4. ⏳ Redactar `docs/informe_final/04_COMPARATIVA_2023_2025.md`
5. ⏳ Integrar análisis Docker en informe técnico

---

## 📖 Referencias y Recursos

### **Datasets**
- [Stack Overflow Developer Survey 2023](https://survey.stackoverflow.co/2023/)
- [Stack Overflow Developer Survey 2025](https://survey.stackoverflow.co/2025/) (disponible)
- [JetBrains Developer Ecosystem 2025](https://www.jetbrains.com/lp/devecosystem-2025/)

### **Metodología**
- [CRISP-DM Methodology](https://www.datascience-pm.com/crisp-dm-2/)
- [MLOps Maturity Model - Microsoft](https://learn.microsoft.com/en-us/azure/architecture/example-scenario/mlops/mlops-maturity-model)

### **Frameworks y Herramientas**
- [Kedro Documentation](https://docs.kedro.org/)
- [DVC Documentation](https://dvc.org/doc)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)

### **White Papers**
- Docker Productivity Whitepaper: `docs/referencias/docker_SUMMARY.md`

---

## 🤝 Contribución

Este proyecto es parte de una tesis académica. Para contribuciones o sugerencias:

1. Abrir un Issue en GitHub con propuesta
2. Fork del repositorio
3. Crear branch: `git checkout -b feature/nueva-funcionalidad`
4. Commit: `git commit -m "feat: descripción"`
5. Push: `git push origin feature/nueva-funcionalidad`
6. Abrir Pull Request

---

## 📝 Licencia

Consultar archivo [LICENSE](./LICENSE) en la raíz del proyecto.

---

## 👥 Autor

**Héctor Aguila V.**  
Ingeniería en Informática   
>Un Soñador con Poca RAM    

Machine Learning

---

**Última actualización**: 3 de noviembre de 2025  
**Versión del roadmap**: 1.0
