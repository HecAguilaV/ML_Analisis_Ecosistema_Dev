# Guía: Ejecutar Clustering en Máquina Remota

## Escenario
Tienes el notebook en tu Mac, pero quieres ejecutarlo en otra máquina más potente (servidor, otra computadora, etc.).

## Flujo Completo

### Paso 1: Push del Notebook a Git (desde tu Mac actual)

```bash
# Asegúrate de estar en la rama correcta
git status

# Agregar el notebook
git add notebooks/04_clustering_analisis.ipynb

# Commit
git commit -m "feat: Agregar notebook de clustering optimizado"

# Push a GitHub
git push origin main
```

**Resultado:** El código del notebook queda en GitHub, listo para descargar en otra máquina.

---

### Paso 2: Clonar/Actualizar en la Máquina Potente

En la máquina más potente:

```bash
# Si es la primera vez, clonar el repo
git clone <tu-repo-url>
cd ML_Analisis_Ecosistema_Dev

# O si ya existe, actualizar
git pull origin main

# Activar entorno virtual
source .venv/bin/activate  # o el comando que uses

# Instalar dependencias si es necesario
pip install -r requirements.txt
```

---

### Paso 3: Configurar DVC en la Máquina Potente

```bash
# Verificar que DVC está configurado
cat .dvc/config

# Si necesitas configurar credenciales de GCS (solo primera vez)
# Copiar conf/bucket-dvc.json desde tu Mac o configurarlo

# Verificar conexión con DVC remote
dvc remote list

# Descargar datos necesarios (si no están localmente)
dvc pull data/01_raw/stackoverflow_2023/stack_overflow_survey_results_public.csv
```

---

### Paso 4: Ejecutar el Notebook en la Máquina Potente

```bash
# Opción 1: Jupyter Lab/Notebook
jupyter lab

# Opción 2: Ejecutar como script (más rápido, sin interfaz)
jupyter nbconvert --to notebook --execute notebooks/04_clustering_analisis.ipynb --inplace

# Opción 3: Usar papermill (si lo tienes instalado)
papermill notebooks/04_clustering_analisis.ipynb notebooks/04_clustering_analisis_executed.ipynb
```

**Tiempo estimado:** 30-45 minutos con las optimizaciones actuales.

---

### Paso 5: Verificar que se Generaron los Archivos

Después de ejecutar, verifica que se crearon:

```bash
# Modelos
ls -lh data/06_models/clustering_*.pkl

# Resultados
ls -lh data/07_model_output/datos_con_clusters.parquet

# Métricas
ls -lh data/08_reporting/metrics_clustering.json
```

---

### Paso 6: Versionar Modelos con DVC (en la Máquina Potente)

```bash
# Agregar modelos a DVC
dvc add data/06_models/clustering_kmeans_model.pkl
dvc add data/06_models/clustering_scaler.pkl
dvc add data/07_model_output/datos_con_clusters.parquet

# Agregar archivos .dvc a Git
git add data/06_models/*.dvc data/07_model_output/*.dvc

# Agregar métricas (archivos pequeños)
git add data/08_reporting/metrics_clustering.json
git add data/08_reporting/clustering_model_info.json

# Commit
git commit -m "feat: Modelos de clustering entrenados y resultados

- Modelo K-Means con k óptimo
- Scaler para normalización
- Dataset con clusters asignados
- Métricas de evaluación"

# Push a DVC remote (GCS)
dvc push

# Push a Git
git push origin main
```

---

### Paso 7: Descargar Resultados en tu Mac (Opcional)

Si quieres los modelos en tu Mac local:

```bash
# En tu Mac
cd ML_Analisis_Ecosistema_Dev
git pull origin main
dvc pull data/06_models/clustering_kmeans_model.pkl
dvc pull data/07_model_output/datos_con_clusters.parquet
```

---

## Ventajas de este Flujo

✅ **No necesitas ejecutar en tu Mac** - Ahorras recursos locales  
✅ **Modelos versionados en GCS** - Disponibles desde cualquier máquina  
✅ **Reproducible** - Cualquiera puede descargar y ejecutar  
✅ **Colaborativo** - Otros pueden usar los modelos entrenados  

---

## Preguntas Frecuentes

### ¿Puedo ejecutar solo partes del notebook?

Sí, puedes ejecutar celdas individuales en Jupyter. El notebook está diseñado para ejecutarse completo, pero puedes:

1. Ejecutar hasta la preparación de datos
2. Guardar el dataset preparado
3. Continuar con el clustering en otra sesión

### ¿Qué pasa si la máquina potente se apaga durante la ejecución?

- **Jupyter Notebook:** Guarda el estado de las variables en memoria. Si se apaga, pierdes el progreso.
- **Solución:** Usa `jupyter nbconvert --execute` o papermill, que guardan el output en cada celda.

### ¿Puedo ajustar el SAMPLE_SIZE en la máquina potente?

Sí, puedes modificar esta línea en la celda 8:

```python
SAMPLE_SIZE = 30000  # Aumentar si la máquina es muy potente
```

### ¿Necesito los datos raw en la máquina potente?

Sí, necesitas descargarlos con DVC:

```bash
dvc pull data/01_raw/stackoverflow_2023/stack_overflow_survey_results_public.csv
```

---

## Resumen del Flujo

```
Tu Mac (actual)
    ↓
1. git push (notebook)
    ↓
GitHub
    ↓
Máquina Potente
    ↓
2. git pull
3. Ejecutar notebook
4. dvc add (modelos)
5. dvc push (a GCS)
6. git push (archivos .dvc)
    ↓
GCS (modelos) + GitHub (código)
    ↓
Cualquier máquina puede descargar con dvc pull
```

---

**Última actualización:** 2025-01-XX
