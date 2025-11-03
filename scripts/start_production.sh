#!/bin/bash

# ===========================================
# SCRIPT DE INICIO PARA PRODUCCIÓN
# ML Análisis Ecosistema Dev
# ===========================================

echo "🚀 Iniciando ML Análisis Ecosistema - Entorno de PRODUCCIÓN"
echo "============================================================"

# Verificar que Docker esté corriendo
if ! docker info > /dev/null 2>&1; then
    echo "❌ Error: Docker no está corriendo. Por favor inicia Docker Desktop."
    exit 1
fi

# Construir imágenes si es necesario
echo "🔨 Construyendo imágenes Docker..."
docker-compose build

# Iniciar servicios de producción
echo "🛠️  Iniciando servicios de producción..."
docker-compose up -d

# Esperar a que los servicios estén listos
echo "⏳ Esperando a que los servicios estén listos..."
sleep 20

# Verificar estado de los servicios
echo "📊 Estado de los servicios:"
docker-compose ps

echo ""
echo "✅ Servicios de producción iniciados:"
echo "   🎯 Airflow Webserver: http://localhost:8080"
echo "   📊 Airflow Scheduler: Ejecutando en background"
echo "   📈 Kedro Viz: http://localhost:4141"
echo "   🗄️  PostgreSQL: Puerto 5432"
echo "   🔴 Redis: Puerto 6379"
echo ""
echo "💡 Comandos útiles:"
echo "   Ver logs: docker-compose logs -f"
echo "   Ver logs de Kedro Viz: docker-compose logs -f kedro-viz"
echo "   Detener todo: docker-compose down"
echo "   Ejecutar pipeline Kedro: docker-compose exec kedro-viz kedro run"
echo ""
echo "🔐 Credenciales Airflow:"
echo "   Usuario: airflow"
echo "   Contraseña: airflow"
echo ""
echo "🎉 ¡Entorno de producción listo!"
