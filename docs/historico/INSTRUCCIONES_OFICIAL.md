# 📋 Evaluación Parcial 2 - Machine Learning
## Pipelines de Clasificación y Regresión + MLOps + Defensa Técnica

**DOCUMENTO INTEGRADO - Combinación de ambas instrucciones oficiales del docente**

---

## 📌 Información General

| Campo | Detalle |
|-------|---------|
| **Asignatura** | MLY0100 - Machine Learning |
| **Institución** | Duoc UC |
| **Modalidad** | Parejas |
| **Duración** | 4 semanas |
| **Ponderación** | 40% (Técnico) + 30% (Académico) = **Complementarios** |
| **Entorno** | Laboratorio / Remoto |

---

## 🎯 Objetivo General

Implementar y documentar un flujo completo de Machine Learning siguiendo la metodología **CRISP-DM**, con pipelines modulares de clasificación y regresión, versionado de datos y modelos, orquestación, reproducibilidad y defensa técnica, usando las mejores prácticas de **MLOps**.

---

## 📊 PARTE 1: Requisitos Técnicos MLOps (40%)

### 1️⃣ Pipelines Kedro
- ✅ Dos pipelines **independientes** y **modulares**: clasificación y regresión
- ✅ Ejecutables sin errores
- ✅ Al menos **5 modelos por pipeline** (≥5 para clasificación y ≥5 para regresión)

### 2️⃣ Búsqueda de Hiperparámetros
- ✅ **GridSearchCV** en todos los modelos
- ✅ **CrossValidation** con k≥5 (mínimo 5 folds)
- ✅ Tabla comparativa con **mean±std** de métricas

### 3️⃣ Métricas y Visualizaciones
- ✅ Métricas apropiadas por tipo de tarea
- ✅ Tabla comparativa con gráficos
- ✅ Análisis visual de resultados

### 4️⃣ DVC (Versionado)
- ✅ Datasets versionados
- ✅ Features versionadas
- ✅ Modelos versionados con métricas
- ✅ Stages definidos en `dvc.yaml`
- ✅ Artefactos rastreables

### 5️⃣ Airflow (Orquestación)
- ✅ DAG funcional
- ✅ Ejecuta ambos pipelines
- ✅ Consolida resultados
- ✅ Operativo y documentado

### 6️⃣ Docker (Portabilidad)
- ✅ Imagen funcional y reproducible
- ✅ Instrucciones claras de ejecución
- ✅ Entorno completo containerizado

### 7️⃣ Reproducibilidad
- ✅ Git + DVC + Docker integrados
- ✅ Ejecución determinística
- ✅ Documentación completa

### 8️⃣ Documentación
- ✅ README con instrucciones paso a paso
- ✅ Arquitectura del proyecto explicada
- ✅ Cómo ejecutar local, Docker, Airflow
- ✅ Enlaces a datos y reportes

### 9️⃣ Reporte de Experimentos
- ✅ Comparación final de modelos
- ✅ Discusión de resultados
- ✅ Conclusiones fundamentadas

### 🔟 Defensa Técnica
- ✅ Presentación oral: **10 min + 5 min preguntas**
- ✅ Explicación del flujo Kedro→Airflow→DVC→Docker
- ✅ Justificación de decisiones técnicas

---

## 📚 PARTE 2: Requisitos Académicos y Rúbrica (30%)

### A. Metodología CRISP-DM Completa

#### **Formato: Jupyter Notebook con estructura de informe**

El notebook debe incluir:
- ✅ Markdown explicativo en cada sección
- ✅ Justificación de decisiones técnicas
- ✅ Contexto de negocio integrado
- ✅ Componentes estadísticos y matemáticos
- ✅ Visualizaciones profesionales

#### **Fase 1: Business Understanding**
- ✅ Contexto del problema claramente definido
- ✅ Objetivos del proyecto establecidos
- ✅ Criterios de éxito definidos

#### **Fase 2: Data Understanding**
- ✅ Análisis exploratorio completo (EDA)
- ✅ Estadísticas descriptivas (mean, median, std, etc.)
- ✅ Visualizaciones de distribuciones (histogramas, boxplots)
- ✅ Análisis de correlación entre features (heatmap)
- ✅ Detección de valores faltantes y outliers
- ✅ Análisis de balance de clases (para clasificación)

#### **Fase 3: Data Preparation**
- ✅ Transformación de atributos justificada
- ✅ Feature engineering documentado
- ✅ Selección de características explicada
- ✅ Tratamiento de valores nulos
- ✅ Encoding de variables categóricas
- ✅ Normalización/Estandarización (si aplica)

#### **Fase 4: Modeling**
- ✅ Implementación de modelos supervisados
- ✅ Justificación de algoritmos seleccionados
- ✅ Hiperparámetros optimizados con GridSearchCV
- ✅ División train/test documentada
- ✅ Validación cruzada implementada

#### **Fase 5: Evaluation**
- ✅ Métricas de evaluación apropiadas
- ✅ Comparación de modelos (tabla + gráficos)
- ✅ Selección del mejor modelo fundamentada
- ✅ Análisis de overfitting/underfitting
- ✅ Interpretación de resultados

#### **Fase 6: Deployment**
- ✅ Plan de despliegue (pipeline, API, Docker)
- ✅ Reproducibilidad garantizada
- ✅ Documentación de uso

---

### B. Modelos de Regresión (Mínimo requerido)

#### Requisitos Mínimos:
- ✅ Target **continuo** (columna numérica justificada según caso)
- ✅ **Mínimo 5 algoritmos** diferentes implementados:
  - Ejemplo: LinearRegression, Ridge, Lasso, RandomForest, XGBoost, etc.
- ✅ **GridSearchCV** + **CrossValidation** (k≥5)
- ✅ Split train/test apropiado (ej: 80/20 o 70/30)

#### Métricas Requeridas:
- ✅ **R²** (Coeficiente de Determinación) - Qué tan bien explica el modelo
- ✅ **RMSE** (Root Mean Squared Error) - Error cuadrático medio
- ✅ **MAE** (Mean Absolute Error) - Error absoluto medio

#### Análisis Obligatorio:
- ✅ Comparación de métricas entre modelos (tabla)
- ✅ Tabla con **mean±std** de cross-validation
- ✅ Selección del mejor modelo **justificada** (no solo por R²)
- ✅ Gráficos de predicciones vs valores reales
- ✅ Análisis de residuos (si aplica)

#### Justificaciones Requeridas:
- ✅ Por qué eligieron esa columna como target
- ✅ Por qué usaron esos 5+ algoritmos
- ✅ Qué hiperparámetros optimizaron y por qué
- ✅ Cuál modelo es mejor para el caso de negocio

---

### C. Modelos de Clasificación (Mínimo requerido)

#### Requisitos Mínimos:
- ✅ Target **discreto** (columna "target" o equivalente con clases)
- ✅ **Mínimo 5 algoritmos** diferentes implementados:
  - Ejemplo: LogisticRegression, RandomForest, XGBoost, LGBM, KNN, SVM, etc.
- ✅ **GridSearchCV** + **CrossValidation** (k≥5)
- ✅ **Stratified K-Fold** (mantener proporción de clases en cada fold)
- ✅ Split train/test apropiado

#### Métricas Requeridas:
- ✅ **Accuracy** (Precisión general)
- ✅ **Precision** (Precisión por clase)
- ✅ **Recall** (Exhaustividad / Sensibilidad)
- ✅ **F1-Score** (Media armónica Precision/Recall)
- ✅ **ROC-AUC** (Área bajo la curva ROC)
- ✅ **Matriz de Confusión** con visualización clara

#### Técnicas Avanzadas Obligatorias:
- ✅ **Balance de clases** implementado:
  - SMOTE (Synthetic Minority Over-sampling Technique)
  - ADASYN
  - O técnica equivalente justificada
- ✅ Análisis de ventajas/desventajas de cada métrica
- ✅ Selección del mejor modelo según el contexto del caso
- ✅ Explicación de cuándo usar Accuracy vs F1 vs ROC-AUC

#### Análisis Obligatorio:
- ✅ Tabla comparativa con **mean±std** de CV
- ✅ Matrices de confusión por modelo (mínimo top 3)
- ✅ Curvas ROC comparativas (si aplica)
- ✅ Análisis de errores: FP (Falsos Positivos) y FN (Falsos Negativos)
- ✅ Justificación de qué tipo de error es más crítico para el negocio

#### Conceptos Clave a Demostrar:
- ✅ Diferencia clara entre Precision y Recall
- ✅ Por qué F1 es mejor que Accuracy en clases desbalanceadas
- ✅ Qué son TP, TN, FP, FN y cómo calcularlos
- ✅ Trade-off entre métricas

---

### D. Conceptos y Justificaciones Requeridas

#### 1. Diferenciación Clara:
- ✅ Explicar diferencia entre **regresión** (target continuo) y **clasificación** (target discreto)
- ✅ Dar ejemplos concretos del caso
- ✅ Justificar por qué cada columna target fue seleccionada

#### 2. Análisis de Correlaciones:
- ✅ Matriz de correlación entre features (Pearson)
- ✅ Heatmap de correlaciones visualizado
- ✅ Selección de features basada en correlación
- ✅ Análisis de multicolinealidad (si aplica)

#### 3. Overfitting/Underfitting:
- ✅ Reconocer cuándo un modelo tiene **overfitting**:
  - Train score alto, Test score bajo
  - Gran diferencia entre métricas de entrenamiento y validación
- ✅ Técnicas para mitigarlo:
  - Regularización (Ridge, Lasso, ElasticNet)
  - Cross-validation
  - Early stopping
  - Reducción de complejidad del modelo
- ✅ Análisis de curvas de aprendizaje (opcional pero recomendado)

#### 4. Feature Engineering:
- ✅ Justificar **cada transformación** aplicada
- ✅ Explicar por qué se crearon nuevas features
- ✅ Documentar features eliminadas y por qué

---

## 📈 Rúbrica de Evaluación Integrada

| Criterio | % | Evidencias de Logro | Documento Origen |
|----------|---|---------------------|------------------|
| **1. Integración de Pipelines** | 8% | Pipelines Kedro modulares, independientes y ejecutables sin errores | Doc 1 (MLOps) |
| **2. DVC (Versionado Completo)** | 7% | Datasets, features, modelos y métricas versionados. Stages en dvc.yaml | Doc 1 (MLOps) |
| **3. Airflow (Orquestación)** | 7% | DAG funcional que ejecuta ambos pipelines y consolida resultados | Doc 1 (MLOps) |
| **4. Docker (Portabilidad)** | 7% | Imagen funcional, reproducible, con instrucciones claras de ejecución | Doc 1 (MLOps) |
| **5. Métricas y Visualizaciones** | 10% | Métricas correctas por tipo de tarea, gráficos comparativos | Doc 1 + Doc 2 |
| **6. Cobertura de Modelos + Tuning + CV** | 24% | ≥5 modelos por tipo, GridSearch + CV (k≥5), tabla mean±std | Doc 1 + Doc 2 |
| **7. Reproducibilidad (Git+DVC+Docker)** | 7% | Ejecución determinística, versionado completo, documentación | Doc 1 (MLOps) |
| **8. Documentación Técnica** | 5% | README con instrucciones, arquitectura, cómo ejecutar todo | Doc 1 + Doc 2 |
| **9. Reporte de Experimentos** | 5% | Comparación final, discusión de resultados, conclusiones | Doc 1 + Doc 2 |
| **10. Defensa Técnica (Oral)** | 20% | 10 min presentación + 5 min preguntas. Flujo Kedro–Airflow–DVC–Docker | Doc 1 (MLOps) |
| **TOTAL** | **100%** | | |

---

## 📊 Desglose Detallado por Indicadores (Documento 2)

### **A. Indicadores de Regresión (35 puntos)**

| Indicador | Peso | Descripción | Nivel Logro |
|-----------|------|-------------|-------------|
| Target continuo apropiado | 5% | Target numérico continuo justificado según el caso | 100% / 80% / 60% / 40% / 20% |
| Algoritmos de regresión | 10% | ≥5 algoritmos supervisados implementados correctamente | 100% / 80% / 60% / 40% / 20% |
| Métricas de evaluación | 5% | R², RMSE, MAE calculadas según estándares | 100% / 80% / 60% / 40% / 20% |
| Selección mejor modelo | 5% | Selección fundamentada en métricas y generalización | 100% / 80% / 60% / 40% / 20% |
| Transformación atributos | 10% | Feature engineering documentado y justificado | 100% / 80% / 60% / 40% / 20% |

### **B. Indicadores de Clasificación (65 puntos)**

| Indicador | Peso | Descripción | Nivel Logro |
|-----------|------|-------------|-------------|
| Diferencia Regresión vs Clasificación | 5% | Explicación clara de target continuo vs discreto | 100% / 80% / 60% / 40% / 20% |
| Análisis de correlación | 5% | Matriz de correlación, heatmap, análisis de features | 100% / 80% / 60% / 40% / 20% |
| Transformación atributos clasificación | 10% | Feature engineering específico para clasificación | 100% / 80% / 60% / 40% / 20% |
| Justificación selección features | 5% | Argumentación basada en correlación y relevancia | 100% / 80% / 60% / 40% / 20% |
| Algoritmos de clasificación | 10% | ≥5 algoritmos supervisados correctamente implementados | 100% / 80% / 60% / 40% / 20% |
| Reconoce overfitting/underfitting | 5% | Análisis de curvas de aprendizaje y validación | 100% / 80% / 60% / 40% / 20% |
| Métricas de clasificación | 10% | Accuracy, Precision, Recall, F1, ROC-AUC calculadas | 100% / 80% / 60% / 40% / 20% |
| Matriz de confusión | 5% | Visualización y análisis de TP, TN, FP, FN | 100% / 80% / 60% / 40% / 20% |
| Balance de clases (SMOTE) | 10% | SMOTE, ADASYN, o técnica equivalente implementada | 100% / 80% / 60% / 40% / 20% |
| Análisis y selección modelo | 5% | Selección fundamentada según caso de negocio | 100% / 80% / 60% / 40% / 20% |
| Ventajas/desventajas métricas | 5% | Discusión de cuándo usar cada métrica | 100% / 80% / 60% / 40% / 20% |

---

## ✅ Checklist de Entrega Final

### **Código y Pipelines:**
- [ ] Pipeline de clasificación ejecuta sin errores
- [ ] Pipeline de regresión ejecuta sin errores
- [ ] Al menos 5 modelos por pipeline implementados
- [ ] GridSearchCV configurado en todos los modelos
- [ ] Cross-validation k≥5 en todos los modelos

### **Versionado y Orquestación:**
- [ ] DVC versiona datasets
- [ ] DVC versiona features procesadas
- [ ] DVC versiona modelos entrenados
- [ ] DVC versiona métricas de modelos
- [ ] Archivo dvc.yaml con stages definidos
- [ ] DAG de Airflow funcional
- [ ] DAG ejecuta ambos pipelines
- [ ] DAG consolida resultados

### **Docker y Reproducibilidad:**
- [ ] Dockerfile funcional y testeado
- [ ] Imagen Docker construye sin errores
- [ ] Instrucciones de ejecución en README
- [ ] Todo el código versionado en Git
- [ ] Ejecución determinística (mismos resultados siempre)

### **Documentación:**
- [ ] README con instrucciones paso a paso
- [ ] Arquitectura del proyecto explicada (diagrama)
- [ ] Cómo ejecutar localmente
- [ ] Cómo ejecutar en Docker
- [ ] Cómo ejecutar con Airflow
- [ ] Enlaces a datos y reportes

### **Notebook de Informe:**
- [ ] Formato profesional con markdown
- [ ] Todas las fases de CRISP-DM cubiertas
- [ ] Justificación de decisiones técnicas
- [ ] Análisis exploratorio completo (EDA)
- [ ] Visualizaciones claras y etiquetadas
- [ ] Tabla comparativa de modelos con mean±std
- [ ] Gráficos de comparación de métricas
- [ ] Conclusiones y recomendaciones

### **Métricas de Regresión:**
- [ ] R² calculado para todos los modelos
- [ ] RMSE calculado para todos los modelos
- [ ] MAE calculado para todos los modelos
- [ ] Tabla comparativa con mean±std de CV
- [ ] Gráfico de predicciones vs valores reales
- [ ] Justificación del mejor modelo

### **Métricas de Clasificación:**
- [ ] Accuracy calculado
- [ ] Precision calculado
- [ ] Recall calculado
- [ ] F1-Score calculado
- [ ] ROC-AUC calculado (si aplica)
- [ ] Matriz de confusión visualizada
- [ ] Análisis de FP y FN
- [ ] Balance de clases con SMOTE implementado
- [ ] Justificación del mejor modelo según contexto

### **Conceptos Demostrados:**
- [ ] Diferencia entre regresión y clasificación explicada
- [ ] Análisis de correlaciones con heatmap
- [ ] Overfitting/Underfitting identificado y mitigado
- [ ] Feature engineering documentado
- [ ] Ventajas/desventajas de métricas discutidas

### **Defensa Técnica:**
- [ ] Presentación de 10 minutos preparada
- [ ] Explicación del flujo Kedro→Airflow→DVC→Docker
- [ ] Respuestas a preguntas técnicas preparadas
- [ ] Justificación de decisiones técnicas clara
- [ ] Ensayo de presentación realizado

---

## 🎯 Criterios de Niveles de Logro

### **Muy Buen Desempeño (100%)**
Demuestra un desempeño destacado, evidenciando el logro de **todos** los aspectos evaluados en el indicador.

### **Buen Desempeño (80%)**
Demuestra un alto desempeño del indicador, presentando **pequeñas omisiones**, dificultades y/o errores menores.

### **Desempeño Aceptable (60%)**
Demuestra un desempeño competente, evidenciando el logro de los **elementos básicos** del indicador, pero con omisiones, dificultades o errores.

### **Desempeño Incipiente (40%)**
Presenta importantes omisiones, dificultades o errores en el desempeño, que no permiten evidenciar los elementos básicos del logro del indicador.

### **Desempeño Insuficiente (20%)**
Presenta desempeño incorrecto o no presenta evidencia del indicador.

---

## 📅 Recomendaciones de Planificación

### **Semana 1: Setup y Data Understanding**
- Configurar pipelines Kedro
- EDA completo
- Análisis de correlaciones
- Feature engineering inicial

### **Semana 2: Modelado**
- Implementar 5+ modelos de regresión
- Implementar 5+ modelos de clasificación
- GridSearchCV en todos
- Balance de clases (SMOTE)

### **Semana 3: Evaluación y Optimización**
- Comparación de métricas
- Tablas con mean±std
- Visualizaciones
- Selección de mejores modelos

### **Semana 4: MLOps y Defensa**
- Integrar DVC completo
- Configurar DAG de Airflow
- Dockerizar proyecto
- Preparar defensa técnica
- Documentación final

---

## 📞 Contacto y Entrega

**Entrega:**
- Repositorio Git con todo el código
- README con instrucciones claras
- Notebook de informe exportado a PDF
- Presentación para defensa técnica (PPT/PDF)

**Defensa:**
- Duración: 10 minutos presentación + 5 minutos preguntas
- Ambos integrantes deben participar
- Explicar flujo técnico completo
- Justificar decisiones tomadas

---

**Este documento integra ambas instrucciones oficiales del docente y debe ser la guía definitiva para el desarrollo y entrega del proyecto.**
