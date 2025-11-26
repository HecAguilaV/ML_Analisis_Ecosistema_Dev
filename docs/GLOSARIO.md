# Glosario de Términos Técnicos

Este documento define los conceptos y términos técnicos utilizados en el proyecto de análisis del ecosistema de desarrollo de software.

---

## Metodologías y Frameworks

### CRISP-DM
**Cross-Industry Standard Process for Data Mining**

Metodología estándar para proyectos de minería de datos y machine learning. Consta de 6 fases:
1. **Business Understanding**: Comprensión del problema y objetivos
2. **Data Understanding**: Exploración y análisis de datos
3. **Data Preparation**: Limpieza y transformación de datos
4. **Modeling**: Entrenamiento de modelos
5. **Evaluation**: Evaluación de resultados
6. **Deployment**: Implementación en producción

**Aplicación en el proyecto**: Todo el flujo de trabajo sigue esta metodología.

---

### MLOps
**Machine Learning Operations**

Conjunto de prácticas que combina desarrollo ML (Machine Learning) con operaciones IT (DevOps) para automatizar y mejorar el ciclo de vida de modelos ML.

**Componentes clave:**
- Versionado de datos y modelos (DVC)
- Pipelines automatizados (Kedro)
- Orquestación (Airflow)
- Contenedorización (Docker)
- Monitoreo continuo

**Nivel de madurez del proyecto**: 2-3 según modelo de Microsoft (automatización parcial con CI/CD básico)

---

## Herramientas y Tecnologías

### Kedro
Framework Python de código abierto para crear pipelines de datos reproducibles, mantenibles y modulares.

**Ventajas:**
- Separación clara entre código, configuración y datos
- Pipelines declarativos y reutilizables
- Integración con Jupyter Notebooks
- Visualización de flujos (Kedro Viz)

**En este proyecto**: 4 pipelines implementados (procesamiento_datos, regresion, clasificacion, regresion_polinomial)

---

### DVC
**Data Version Control**

Sistema de versionado diseñado específicamente para proyectos de ML/AI. Permite versionar datasets grandes, modelos y métricas.

**Funcionalidades:**
- Tracking de archivos grandes (Git LFS mejorado)
- Remote storage (Google Cloud Storage en este proyecto)
- Reproducibilidad de pipelines
- Gestión de experimentos

**Comandos clave:**
- `dvc add`: Agregar archivos al tracking
- `dvc push`: Subir artefactos al remote
- `dvc pull`: Descargar artefactos sin re-ejecutar
- `dvc repro`: Reproducir pipeline completo

---

### Airflow
**Apache Airflow**

Plataforma de orquestación de workflows. Permite programar, monitorear y gestionar pipelines de datos.

**Conceptos:**
- **DAG** (Directed Acyclic Graph): Grafo que define el flujo de tareas
- **Task**: Unidad mínima de trabajo
- **Operator**: Tipo de tarea (PythonOperator, BashOperator, etc.)
- **Schedule**: Programación de ejecución (cron expression)

**En este proyecto**: DAG que ejecuta pipelines Kedro y consolida resultados

---

### Docker
Plataforma de contenedorización que permite empaquetar aplicaciones con todas sus dependencias.

**Ventajas:**
- Reproducibilidad total del entorno
- Aislamiento de dependencias
- Portabilidad entre sistemas operativos
- Escalabilidad

**En este proyecto**: Docker Compose con 8 servicios (7 Airflow + 1 Kedro Viz)

---

## Conceptos de Machine Learning

### Pipeline
Secuencia de pasos automatizados que transforma datos en predicciones o insights.

**Ejemplo en este proyecto:**
```
datos_raw → limpieza → feature_engineering → entrenamiento → evaluación → modelo
```

---

### GridSearchCV
**Grid Search with Cross-Validation**

Técnica de búsqueda exhaustiva de hiperparámetros óptimos mediante validación cruzada.

**Proceso:**
1. Define una grilla de hiperparámetros
2. Entrena modelo con cada combinación
3. Evalúa con k-fold cross-validation
4. Selecciona la mejor combinación

**Parámetro k**: Número de particiones (folds) del dataset. En este proyecto: k≥5

---

### Cross-Validation (Validación Cruzada)
Técnica para evaluar la capacidad de generalización de un modelo.

**K-Fold CV:**
1. Divide dataset en K particiones (folds)
2. Entrena K veces usando K-1 folds para entrenamiento y 1 para validación
3. Promedia las métricas de las K iteraciones

**Ventaja**: Reduce overfitting y estima mejor el rendimiento real

---

### Imbalanced Data (Datos Desbalanceados)
Situación donde una clase tiene significativamente más muestras que otras.

**Soluciones:**
- **Oversampling**: SMOTE (Synthetic Minority Over-sampling Technique)
- **Undersampling**: Reducir clase mayoritaria
- **Class weights**: Penalizar más los errores en clase minoritaria

**En este proyecto**: SMOTE aplicado en pipeline de clasificación

---

## Métricas de Evaluación

### Regresión

#### R² (Coeficiente de Determinación)
Proporción de varianza explicada por el modelo. Rango: 0 a 1 (más cercano a 1 es mejor).

**Interpretación:**
- R² = 0.85 → El modelo explica el 85% de la variabilidad

---

#### MAE (Mean Absolute Error)
Error promedio absoluto entre predicciones y valores reales.

**Fórmula:** `MAE = Σ|y_real - y_pred| / n`

**Ventaja**: Fácil interpretación (en las mismas unidades que el target)

---

#### RMSE (Root Mean Squared Error)
Raíz cuadrada del error cuadrático medio. Penaliza más los errores grandes.

**Fórmula:** `RMSE = √(Σ(y_real - y_pred)² / n)`

**Uso**: Cuando los errores grandes son más costosos

---

### Clasificación

#### Accuracy (Exactitud)
Proporción de predicciones correctas sobre el total.

**Fórmula:** `Accuracy = (TP + TN) / (TP + TN + FP + FN)`

**Limitación**: No es confiable con datos desbalanceados

---

#### Precision (Precisión)
Proporción de positivos predichos que son realmente positivos.

**Fórmula:** `Precision = TP / (TP + FP)`

**Interpretación**: "De los que predije como positivos, ¿cuántos acerté?"

---

#### Recall (Sensibilidad)
Proporción de positivos reales que fueron correctamente identificados.

**Fórmula:** `Recall = TP / (TP + FN)`

**Interpretación**: "De todos los positivos reales, ¿cuántos detecté?"

---

#### F1-Score
Media armónica de Precision y Recall. Equilibra ambas métricas.

**Fórmula:** `F1 = 2 × (Precision × Recall) / (Precision + Recall)`

**Uso**: Métrica única cuando se necesita balance entre Precision y Recall

---

#### ROC-AUC
**Receiver Operating Characteristic - Area Under Curve**

Área bajo la curva ROC (gráfico de True Positive Rate vs False Positive Rate).

**Rango:** 0 a 1
- 0.5: Modelo aleatorio
- 0.7-0.8: Aceptable
- 0.8-0.9: Excelente
- >0.9: Excepcional

**Ventaja**: Independiente del umbral de decisión

---

#### Confusion Matrix (Matriz de Confusión)
Tabla que resume predicciones correctas e incorrectas por clase.

**Estructura (binaria):**
```
                 Predicho
                Pos    Neg
Real  Pos      TP     FN
      Neg      FP     TN
```

- **TP** (True Positive): Positivos correctamente identificados
- **TN** (True Negative): Negativos correctamente identificados
- **FP** (False Positive): Error Tipo I (falsa alarma)
- **FN** (False Negative): Error Tipo II (positivo no detectado)

---

## Principios de Ingeniería de Software

### Separation of Concerns
**Separación de Responsabilidades**

Principio de diseño donde cada componente tiene una responsabilidad única y bien definida.

**Beneficios:**
- Mayor mantenibilidad
- Facilita testing
- Permite desarrollo paralelo
- Reduce acoplamiento

**Aplicación en el proyecto:**
- Pipeline de procesamiento: Solo prepara datos
- Pipeline de clasificación: Solo entrena clasificadores
- Pipeline de regresión: Solo entrena regresores
- Notebooks: Solo analizan resultados

---

### Reproducibilidad
Capacidad de obtener los mismos resultados ejecutando el mismo código con los mismos datos.

**Elementos clave:**
- Versionado de código (Git)
- Versionado de datos (DVC)
- Versionado de dependencias (requirements.txt, conda env)
- Seeds aleatorias fijas (`random_state=42`)
- Documentación de entorno (Dockerfile)

**En este proyecto**: 100% reproducible con `git clone` + `dvc pull`

---

### CI/CD
**Continuous Integration / Continuous Deployment**

Prácticas de automatización del ciclo de desarrollo y despliegue.

**CI (Integración Continua):**
- Tests automáticos en cada commit
- Validación de código (linting)
- Build automático

**CD (Despliegue Continuo):**
- Deploy automático a producción
- Rollback automático si falla
- Monitoreo post-deploy

**En este proyecto**: CI/CD básico con GitHub Actions (pendiente implementación completa)

---

## Modelos Utilizados

### Regresión

#### Linear Regression
Modelo lineal que asume relación lineal entre features y target.

**Fórmula:** `y = β₀ + β₁x₁ + β₂x₂ + ... + βₙxₙ`

**Ventajas**: Simple, interpretable, rápido
**Limitaciones**: Asume linealidad, sensible a outliers

---

#### Ridge Regression (L2 Regularization)
Linear Regression con penalización L2 para evitar overfitting.

**Fórmula:** `Loss = MSE + α × Σβᵢ²`

**Parámetro α**: Controla la fuerza de regularización (mayor α → más regularización)

---

#### Lasso Regression (L1 Regularization)
Linear Regression con penalización L1. Puede eliminar features (β=0).

**Fórmula:** `Loss = MSE + α × Σ|βᵢ|`

**Ventaja**: Feature selection automática

---

#### Random Forest Regressor
Ensemble de árboles de decisión. Promedia predicciones de múltiples árboles.

**Hiperparámetros clave:**
- `n_estimators`: Número de árboles
- `max_depth`: Profundidad máxima de árboles
- `min_samples_split`: Mínimo de muestras para dividir nodo

**Ventajas**: Robusto, maneja no-linealidad, poco sensible a outliers

---

#### XGBoost Regressor
**Extreme Gradient Boosting**

Ensemble de árboles con gradient boosting. Construye árboles secuencialmente corrigiendo errores previos.

**Ventajas**: Alto rendimiento, maneja datos faltantes, regularización incorporada
**Desventaja**: Más lento, requiere tuning cuidadoso

---

### Clasificación

#### Logistic Regression
Modelo lineal para clasificación. Usa función sigmoide para probabilidades.

**Fórmula:** `P(y=1) = 1 / (1 + e^(-z))` donde `z = β₀ + β₁x₁ + ...`

**Ventajas**: Simple, rápido, probabilidades interpretables
**Limitaciones**: Asume relación lineal en espacio logit

---

#### Random Forest Classifier
Versión de clasificación de Random Forest.

**Ventajas**: Maneja no-linealidad, feature importance incorporado, poco overfitting

---

#### XGBoost Classifier
Versión de clasificación de XGBoost.

**Aplicación típica**: Competencias Kaggle, producción con datos estructurados

---

#### LightGBM
**Light Gradient Boosting Machine**

Implementación eficiente de gradient boosting desarrollada por Microsoft.

**Ventajas sobre XGBoost:**
- Más rápido en datasets grandes
- Menor uso de memoria
- Maneja mejor datos categóricos

**En este proyecto**: Mejor modelo de clasificación (98.49% accuracy)

---

#### Gradient Boosting Classifier
Implementación de scikit-learn de gradient boosting.

**Diferencias con XGBoost/LightGBM**: Más lento, menos optimizado, pero más simple de usar

---

## Conceptos de Feature Engineering

### One-Hot Encoding
Transforma variables categóricas en vectores binarios.

**Ejemplo:**
```
País: ['Chile', 'USA', 'Brasil']
→
Chile: [1, 0, 0]
USA:   [0, 1, 0]
Brasil:[0, 0, 1]
```

---

### Label Encoding
Asigna un número entero a cada categoría.

**Ejemplo:**
```
Ranking: ['Junior', 'Mid', 'Senior']
→ [0, 1, 2]
```

**Precaución**: Implica orden, solo usar con variables ordinales

---

### Feature Scaling
Normalización de features para que tengan rangos similares.

**StandardScaler**: `(x - μ) / σ` (media 0, desviación estándar 1)
**MinMaxScaler**: `(x - min) / (max - min)` (rango 0 a 1)

**Importancia**: Crítico para modelos basados en distancias (SVM, KNN, regresión lineal)

---

### Polynomial Features
Genera features polinómicas (interacciones entre variables).

**Ejemplo (grado 2):**
```
x₁, x₂ → x₁, x₂, x₁², x₁x₂, x₂²
```

**En este proyecto**: Ridge Polynomial en experimento de regresión

---

## Acrónimos Comunes

- **API**: Application Programming Interface
- **CLI**: Command Line Interface
- **CSV**: Comma-Separated Values
- **DAG**: Directed Acyclic Graph
- **EDA**: Exploratory Data Analysis
- **ETL**: Extract, Transform, Load
- **GCS**: Google Cloud Storage
- **JSON**: JavaScript Object Notation
- **ML**: Machine Learning
- **OOP**: Object-Oriented Programming
- **RAM**: Random Access Memory
- **REST**: Representational State Transfer
- **YAML**: YAML Ain't Markup Language

---

## Referencias

- [Kedro Documentation](https://docs.kedro.org/)
- [DVC Documentation](https://dvc.org/doc)
- [Apache Airflow Documentation](https://airflow.apache.org/docs/)
- [scikit-learn User Guide](https://scikit-learn.org/stable/user_guide.html)
- [XGBoost Documentation](https://xgboost.readthedocs.io/)
- [LightGBM Documentation](https://lightgbm.readthedocs.io/)
- [CRISP-DM Methodology](https://www.datascience-pm.com/crisp-dm-2/)
- [MLOps Maturity Model - Microsoft](https://learn.microsoft.com/en-us/azure/architecture/example-scenario/mlops/mlops-maturity-model)

---

**Última actualización:** Noviembre 2025  
**Versión del proyecto:** 1.0

>**© 2025 - Un Soñador con Poca RAM**