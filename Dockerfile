FROM apache/airflow:2.7.3

# Small runtime image for local development / CI distribution
# Installs only runtime requirements and copies dags/src. Keep image lean so devs can pull

# Install system dependencies for LightGBM
USER root
RUN apt-get update && apt-get install -y libgomp1 && apt-get clean && rm -rf /var/lib/apt/lists/*

USER airflow
COPY --chown=airflow:root requirements.txt /tmp/requirements.txt
COPY --chown=airflow:root requirements-runtime.txt /tmp/requirements-runtime.txt
RUN pip install --no-cache-dir -r /tmp/requirements-runtime.txt \
    && rm -f /tmp/requirements-runtime.txt

# Copy dags and source code used by the scheduler and tasks
COPY --chown=airflow:root dags/ /opt/airflow/dags/
COPY --chown=airflow:root src/ /opt/airflow/src/

# Ensure default workdir
WORKDIR /opt/airflow

CMD ["/usr/bin/dumb-init", "--", "/entrypoint"]
