# Guía: Versionado de Modelos de Clustering con DVC

## Resumen

Después de ejecutar el notebook `04_clustering_analisis.ipynb`, se generan varios artefactos que deben ser versionados con DVC para mantener un historial de modelos y resultados.

## Artefactos Generados

El notebook genera los siguientes archivos que deben versionarse:

### 1. Modelos Entrenados
- `data/06_models/clustering_kmeans_model.pkl` - Modelo K-Means entrenado
- `data/06_models/clustering_scaler.pkl` - Scaler utilizado para normalización

### 2. Resultados y Predicciones
- `data/07_model_output/datos_con_clusters.parquet` - Dataset con etiquetas de clusters asignadas

### 3. Métricas y Reportes
- `data/08_reporting/metrics_clustering.json` - Métricas de evaluación de todos los modelos
- `data/08_reporting/clustering_model_info.json` - Información del modelo (parámetros, features, etc.)
- `data/08_reporting/kmeans_elbow_results.json` - Resultados del método Elbow
- `data/08_reporting/comparison_clustering_results.csv` - Comparación de modelos
- `data/08_reporting/cluster_profiles.json` - Perfiles de cada cluster
- Gráficos PNG (visualizaciones)

## Proceso de Versionado con DVC

### Paso 1: Agregar Modelos a DVC

```bash
# Agregar el modelo K-Means
dvc add data/06_models/clustering_kmeans_model.pkl

# Agregar el scaler
dvc add data/06_models/clustering_scaler.pkl

# Agregar el dataset con clusters
dvc add data/07_model_output/datos_con_clusters.parquet
```

**Nota:** Los archivos JSON y CSV de reportes generalmente NO se versionan con DVC (son pequeños y cambian frecuentemente). Se pueden commitear directamente a Git si es necesario.

### Paso 2: Verificar Archivos DVC Creados

Después de ejecutar `dvc add`, se crean archivos `.dvc` que son punteros a los archivos reales:

```bash
# Ver archivos .dvc creados
ls -la data/06_models/*.dvc
ls -la data/07_model_output/*.dvc
```

### Paso 3: Agregar Archivos DVC a Git

```bash
# Agregar los archivos .dvc (punteros) a Git
git add data/06_models/clustering_kmeans_model.pkl.dvc
git add data/06_models/clustering_scaler.pkl.dvc
git add data/07_model_output/datos_con_clusters.parquet.dvc

# Agregar métricas y reportes (opcional, son pequeños)
git add data/08_reporting/metrics_clustering.json
git add data/08_reporting/clustering_model_info.json
```

### Paso 4: Commit a Git

```bash
git commit -m "feat: Agregar modelos de clustering y resultados

- Modelo K-Means entrenado con k óptimo
- Scaler para normalización de datos
- Dataset con etiquetas de clusters asignadas
- Métricas de evaluación de todos los modelos"
```

### Paso 5: Push a DVC Remote (GCS)

```bash
# Subir los archivos grandes al bucket de GCS
dvc push
```

Esto sube los archivos `.pkl` y `.parquet` al bucket de Google Cloud Storage configurado en `.dvc/config`.

## Verificación

### Verificar que los archivos están en DVC

```bash
# Ver estado de DVC
dvc status

# Ver qué archivos están siendo rastreados por DVC
dvc list data/06_models/
dvc list data/07_model_output/
```

### Descargar archivos versionados (en otra máquina)

```bash
# Descargar todos los archivos versionados
dvc pull

# O descargar un archivo específico
dvc pull data/06_models/clustering_kmeans_model.pkl
```

## Estructura Final

Después del versionado, la estructura debería verse así:

```
data/
├── 06_models/
│   ├── clustering_kmeans_model.pkl      # Archivo grande (DVC)
│   ├── clustering_kmeans_model.pkl.dvc  # Puntero (Git)
│   ├── clustering_scaler.pkl             # Archivo grande (DVC)
│   └── clustering_scaler.pkl.dvc        # Puntero (Git)
│
├── 07_model_output/
│   ├── datos_con_clusters.parquet       # Archivo grande (DVC)
│   └── datos_con_clusters.parquet.dvc   # Puntero (Git)
│
└── 08_reporting/
    ├── metrics_clustering.json           # Archivo pequeño (Git)
    ├── clustering_model_info.json        # Archivo pequeño (Git)
    └── [otros archivos JSON/PNG]        # Archivos pequeños (Git)
```

## Uso de Modelos Versionados

Para usar un modelo versionado en otro notebook o script:

```python
import joblib
from pathlib import Path

# Cargar modelo
model_path = Path('data/06_models/clustering_kmeans_model.pkl')
kmeans_model = joblib.load(model_path)

# Cargar scaler
scaler_path = Path('data/06_models/clustering_scaler.pkl')
scaler = joblib.load(scaler_path)

# Preprocesar nuevos datos y predecir
X_new_scaled = scaler.transform(X_new)
clusters = kmeans_model.predict(X_new_scaled)
```

## Notas Importantes

1. **Los archivos `.pkl` y `.parquet` NO deben estar en Git** - DVC se encarga de ellos
2. **Los archivos `.dvc` SÍ deben estar en Git** - Son los punteros a los archivos reales
3. **Los archivos JSON pequeños pueden ir a Git** - Son métricas y reportes
4. **Siempre hacer `dvc push` después de `git push`** - Para sincronizar con el remote

## Troubleshooting

### Error: "file is missing"
```bash
# Descargar archivos faltantes del remote
dvc pull
```

### Error: "file is not tracked by DVC"
```bash
# Agregar el archivo a DVC
dvc add ruta/al/archivo.pkl
```

### Verificar configuración de DVC
```bash
# Ver configuración actual
cat .dvc/config

# Verificar que el remote está configurado
dvc remote list
```

---

**Última actualización:** 2025-01-XX
