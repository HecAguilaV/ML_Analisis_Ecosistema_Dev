# 📊 Evaluación de Algoritmos No Supervisados (Clustering)

## 1. Técnicas de Evaluación

### Métricas Internas (Sin Etiquetas Verdaderas) ✅ PRINCIPALES

Estas son las métricas que usaremos porque **NO tenemos etiquetas verdaderas** de clusters:

#### **Silhouette Score** ⭐ MÁS IMPORTANTE
- **Rango**: -1 a 1
- **Interpretación**:
  - > 0.7: Clusters muy bien definidos
  - 0.5 - 0.7: Clusters razonables
  - < 0.5: Clusters poco definidos
- **Ventaja**: Funciona con cualquier algoritmo
- **Fórmula**: `(b - a) / max(a, b)` donde:
  - `a` = distancia promedio intra-cluster
  - `b` = distancia promedio al cluster más cercano

#### **Davies-Bouldin Index**
- **Rango**: 0 a ∞ (menor es mejor)
- **Interpretación**: Ratio de distancia intra-cluster vs inter-cluster
- **Ventaja**: No requiere especificar número de clusters a priori

#### **Calinski-Harabasz Index** (Variance Ratio)
- **Rango**: 0 a ∞ (mayor es mejor)
- **Interpretación**: Ratio de varianza entre clusters vs dentro de clusters
- **Ventaja**: Bueno para comparar diferentes k

#### **Inertia (WCSS - Within-Cluster Sum of Squares)**
- **Solo para K-Means**
- **Rango**: 0 a ∞ (menor es mejor)
- **Uso**: Elbow Method para seleccionar k
- **Limitación**: Solo funciona con métodos de partición

#### **AIC/BIC** (Solo para GMM)
- **Rango**: -∞ a ∞ (menor es mejor)
- **Uso**: Seleccionar número de componentes en GMM
- **Ventaja**: Penaliza complejidad del modelo

### Métricas Externas (Con Etiquetas Verdaderas) ⚠️ OPCIONALES

Solo si tenemos alguna referencia externa (ej: nivel de experiencia, país, etc.):

#### **Adjusted Rand Index (ARI)**
- **Rango**: -1 a 1 (1 = perfecto match)
- **Uso**: Comparar clusters con etiquetas conocidas
- **Ejemplo**: ¿Los clusters coinciden con niveles de experiencia?

#### **Normalized Mutual Information (NMI)**
- **Rango**: 0 a 1 (1 = perfecto match)
- **Uso**: Similar a ARI pero basado en información mutua

#### **Homogeneity, Completeness, V-Measure**
- **Rango**: 0 a 1
- **Uso**: Evaluar calidad de clusters vs etiquetas verdaderas

---

## 2. Compatibilidad entre Métricas Internas y Externas

### ✅ SÍ, son compatibles entre sí

**Puedes usar ambas simultáneamente** si tienes:
- Métricas internas: Para evaluar calidad de clusters sin referencia
- Métricas externas: Para validar si los clusters tienen sentido con variables conocidas

### Ejemplo Práctico en tu Proyecto:

```python
# Métricas internas (sin etiquetas)
silhouette = silhouette_score(X, labels)
davies_bouldin = davies_bouldin_score(X, labels)

# Métricas externas (con etiquetas de referencia)
# Ejemplo: ¿Los clusters coinciden con niveles de experiencia?
ari = adjusted_rand_score(y_experience, labels)
nmi = normalized_mutual_info_score(y_experience, labels)
```

### Recomendación para tu Proyecto:

1. **Usar métricas internas como principales** (Silhouette, Davies-Bouldin, Calinski-Harabasz)
2. **Usar métricas externas como validación** (si tienes variables como `EdLevel`, `DevType`, `Country`)
3. **Comparar ambas** para entender si los clusters tienen sentido de negocio

---

## 3. Algoritmos de Clustering Implementados

### Algoritmos Evaluados en el Proyecto:

#### **K-Means** ⭐ Principal
- ✅ Requiere especificar `k` (número de clusters)
- ✅ Usa métricas: Silhouette Score, Inertia (WCSS), Davies-Bouldin, Calinski-Harabasz
- ✅ Puede usar **Elbow Method** para seleccionar k
- ✅ Rápido y eficiente: O(n)
- ✅ Centroide: Media (puede no existir en espacios no euclidianos)
- ✅ Sensible a outliers
- ✅ Distancia: Euclidiana

#### **DBSCAN** (Detección de Outliers)
- ✅ No requiere especificar número de clusters
- ✅ Identifica outliers automáticamente
- ✅ Flexible para formas irregulares
- ✅ Basado en densidad

### Estrategia Recomendada:

1. **Empezar con K-Means** (más rápido y interpretable)
2. **Si hay outliers**: DBSCAN puede identificarlos automáticamente
3. **Para datos con forma irregular**: DBSCAN es más flexible que K-Means
4. **Si no hay outliers**: K-Means es suficiente y más rápido

---

## 4. ¿Usar TODAS las Técnicas o Solo las que se Adapten?

### 🎯 Respuesta: **Usar las que se adapten al proyecto, pero demostrar conocimiento de todas**

### Estrategia Recomendada:

#### **Fase 1: Exploración (Demostrar Conocimiento)**
Implementar y comparar brevemente:
- ✅ K-Means
- ✅ Clustering Jerárquico
- ✅ DBSCAN
- ✅ GMM

**Objetivo**: Demostrar que conoces todas las técnicas del temario

#### **Fase 2: Selección (Adaptación al Proyecto)**
Elegir 2-3 algoritmos que mejor se adapten:
- **K-Means**: Para segmentación por perfil tecnológico
- **Clustering Jerárquico**: Para entender estructura jerárquica
- **GMM**: Si quieres soft clustering (probabilidades)

**Objetivo**: Profundizar en los que tienen más sentido para tu objetivo

#### **Fase 3: Evaluación Final**
Usar el mejor algoritmo para:
- Interpretación de clusters
- Insights de negocio
- Recomendaciones

### Criterios de Selección:

1. **Tipo de datos**:
   - Datos numéricos normalizados → K-Means, GMM
   - Datos con outliers → DBSCAN
   - Necesitas jerarquía → Clustering Jerárquico

2. **Objetivo del negocio**:
   - Segmentación clara → K-Means
   - Perfiles con probabilidades → GMM
   - Detectar outliers → DBSCAN

3. **Interpretabilidad**:
   - K-Means: Fácil de interpretar
   - GMM: Más complejo pero más rico
   - DBSCAN: Útil para detección de anomalías

### Recomendación Específica para tu Proyecto:

**Para segmentación de desarrolladores por perfil tecnológico:**

1. **K-Means** (principal): Rápido, interpretable, bueno para perfiles tecnológicos
2. **DBSCAN** (comparación): Si hay outliers en salarios o tecnologías
3. **GMM** (opcional): Si quieres probabilidades de pertenencia
4. **Clustering Jerárquico** (opcional): Para entender jerarquía de perfiles

**Estrategia**: Implementar todos, comparar métricas, elegir el mejor para análisis final.

---

## 5. ¿Necesitas Crear un Nuevo Pipeline de Kedro?

### ❌ NO es necesario

### Opciones Disponibles:

#### **Opción 1: Usar Datos del Catálogo (Recomendado)** ✅

```python
# En el notebook
from kedro.framework.session import KedroSession
from kedro.framework.startup import bootstrap_project

# Cargar datos ya procesados
df = catalog.load("datos_procesados_finales")  # O el que tengas disponible
```

**Ventajas**:
- Reutiliza el trabajo previo
- Datos ya limpios y procesados
- Consistente con el resto del proyecto

#### **Opción 2: Preprocesamiento Específico en el Notebook** ✅

```python
# En el notebook
# Cargar datos raw o procesados
df = catalog.load("datos_crudos_so_2023")

# Preprocesamiento específico para clustering
# (puede ser diferente al de regresión/clasificación)
X_clustering = prepare_for_clustering(df)
```

**Ventajas**:
- Flexibilidad para preparar datos específicos para clustering
- Puede incluir/excluir variables diferentes
- Control total sobre el preprocesamiento

#### **Opción 3: Pipeline de Kedro (Opcional, Solo si Quieres)** ⚠️

Solo si quieres que el clustering sea parte del pipeline automatizado:

```python
# src/ml_analisis_ecosistema_dev/pipelines/clustering/pipeline.py
def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=apply_kmeans,
            inputs=["datos_procesados_finales", "params:clustering"],
            outputs="clusters_kmeans",
            name="kmeans_clustering"
        ),
        # ...
    ])
```

**Cuándo usar**:
- Si quieres automatizar el clustering
- Si quieres guardar los clusters en el catálogo
- Si quieres que sea parte del pipeline completo

**Cuándo NO usar**:
- Si el clustering es exploratorio
- Si necesitas iterar rápidamente
- Si es solo para análisis en notebook

### Recomendación para tu Proyecto:

**Usar Opción 1 o 2** (cargar del catálogo o preprocesar en notebook):

1. **Cargar datos procesados** del catálogo (si ya tienes datos limpios)
2. **Hacer preprocesamiento específico** en el notebook para clustering:
   - Seleccionar features relevantes para clustering
   - Normalizar/estandarizar
   - Aplicar PCA si es necesario
3. **NO crear pipeline nuevo** a menos que quieras automatizar

**Razón**: El clustering es más exploratorio y necesita iteración rápida, mejor en notebook.

---

## 📋 Resumen de Recomendaciones

### Métricas de Evaluación:
- ✅ **Principal**: Silhouette Score (para todos los algoritmos)
- ✅ **Secundarias**: Davies-Bouldin, Calinski-Harabasz
- ✅ **Específicas**: Inertia (K-Means), AIC/BIC (GMM)
- ✅ **Opcionales**: ARI, NMI (si tienes etiquetas de referencia)

### Algoritmos:
- ✅ **Implementar todos** para demostrar conocimiento
- ✅ **Profundizar en 2-3** que mejor se adapten
- ✅ **K-Means como principal** (rápido, interpretable)
- ✅ **DBSCAN para detección de outliers** (robusto a anomalías)

### Pipeline:
- ❌ **NO crear pipeline nuevo**
- ✅ **Usar datos del catálogo** o preprocesar en notebook
- ✅ **Mantener flexibilidad** para iteración rápida

---

> **Última actualización**: Enero 2025  
> **Estado**: Guía de evaluación para clustering

