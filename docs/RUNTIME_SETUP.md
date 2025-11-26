# Runtime image and lightweight developer flow

Este documento explica cómo usar la imagen "runtime" y el compose overlay para evitar que cada desarrollador tenga que construir imágenes pesadas localmente.

1) Qué hicimos

- Se agregó `requirements-runtime.txt` (dependencias mínimas en tiempo de ejecución).
- Se agregó `requirements-dev.txt` (dependencias de desarrollo, Jupyter, xgboost, etc.).
- Se creó `docker/Dockerfile.runtime` que instala sólo `requirements-runtime.txt`.
- Se creó `docker/docker-compose.runtime.yml` — un overlay que construye una imagen más pequeña llamada `runtime-airflow:latest`.

2) Flujo recomendado para desarrolladores

- Clona el repositorio.
- Crea y activa un venv (recomendado):
  - `python3 -m venv venv`
  - `source venv/bin/activate`
- Instala dependencias de desarrollo locales (no necesarias para el contenedor runtime):
  - `pip install -r requirements-dev.txt`
- Si quieres construir y ejecutar los servicios con la imagen runtime (recomendado):
  - `docker compose -f docker-compose.yaml -f docker/docker-compose.runtime.yml up --build -d`

3) Flujo alternativo (pull de imagen publicada por CI)

Si en tu equipo existe una imagen publicada en un registro (por ejemplo GHCR), puedes evitar la construcción local y usar la imagen remota editando `.env` para apuntar a `AIRFLOW_IMAGE_NAME` o modificando `docker-compose.yaml` para usar `image: my-registry/myorg/runtime-airflow:tag`.

4) Notas importantes

- Mantén `requirements-runtime.txt` pequeña: sólo lo necesario para ejecutar los DAGs.
- Mantén `requirements-dev.txt` para herramientas de desarrollo (Jupyter, kedro-viz, pruebas, etc.).
- Si tu equipo quiere evitar builds locales, añade un workflow CI que construya `runtime-airflow` y lo publique en un registry — puedo añadir un ejemplo de GitHub Actions si lo deseas.

5) Ayuda rápida

- Ejecutar setup automático (instalar venv, deps dev y levantar con runtime overlay):
  - `./scripts/setup-and-run.sh`

Si algo falla, copia/pega el output y lo revisamos.
