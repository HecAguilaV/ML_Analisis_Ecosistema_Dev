#!/bin/bash
# ============================================================================
# Script de automatización para iniciar Docker y Airflow (Mac/Linux)
# Proyecto: ML Analisis Ecosistema Dev
# ============================================================================

# Cambiar al directorio raiz del proyecto
cd "$(dirname "$0")/.." || exit 1

# Colores para mejor visualización
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}"
echo "========================================"
echo " Iniciando Docker y Airflow"
echo "========================================"
echo -e "${NC}"

# Paso 1: Verificar Docker instalado
echo -e "${CYAN}[1/6] Verificando instalación de Docker...${NC}"
if ! command -v docker &> /dev/null; then
    echo -e "${RED}[ERROR] Docker no está instalado${NC}"
    echo "Por favor, instala Docker desde: https://www.docker.com/products/docker-desktop"
    exit 1
fi
echo -e "${GREEN}[OK] Docker está instalado${NC}"

# Paso 2: Verificar y iniciar Docker
echo -e "${CYAN}[2/6] Verificando estado de Docker...${NC}"
if ! docker info &> /dev/null; then
    echo -e "${YELLOW}[INFO] Docker no está corriendo. Intentando iniciar...${NC}"
    
    # Para Mac
    if [[ "$OSTYPE" == "darwin"* ]]; then
        open -a Docker
        echo -e "${YELLOW}[INFO] Esperando a que Docker Desktop inicie...${NC}"
        
        # Esperar hasta que Docker esté listo (máximo 5 minutos)
        RETRY_COUNT=0
        MAX_RETRIES=30
        while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
            RETRY_COUNT=$((RETRY_COUNT + 1))
            echo "Verificando Docker... Intento $RETRY_COUNT/$MAX_RETRIES"
            
            if docker info &> /dev/null; then
                break
            fi
            
            sleep 10
        done
        
        if ! docker info &> /dev/null; then
            echo -e "${RED}[ERROR] Docker no pudo iniciarse después de 5 minutos${NC}"
            exit 1
        fi
        
        echo -e "${GREEN}[OK] Docker Desktop está corriendo correctamente${NC}"
    else
        # Para Linux
        echo -e "${YELLOW}[INFO] Por favor, inicia Docker manualmente${NC}"
        echo "Ejecuta: sudo systemctl start docker"
        exit 1
    fi
else
    echo -e "${GREEN}[OK] Docker ya está corriendo${NC}"
fi

# Paso 3: Verificar archivo .env
echo -e "${CYAN}[3/6] Verificando archivo .env...${NC}"
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}[WARNING] Archivo .env no encontrado. Creando uno básico...${NC}"
    cat > .env << EOF
AIRFLOW_UID=50000
_AIRFLOW_WWW_USER_USERNAME=airflow
_AIRFLOW_WWW_USER_PASSWORD=airflow
EOF
    echo -e "${GREEN}[OK] Archivo .env creado${NC}"
else
    echo -e "${GREEN}[OK] Archivo .env encontrado${NC}"
fi

# Paso 3: Verificar datos con DVC
echo -e "${CYAN}[3/7] Verificando datos con DVC...${NC}"
if [ -f "data/01_raw.dvc" ]; then
    echo -e "${YELLOW}[INFO] Descargando datos con DVC si es necesario...${NC}"
    if dvc pull 2>/dev/null; then
        echo -e "${GREEN}[OK] Datos sincronizados con DVC${NC}"
    else
        echo -e "${YELLOW}[WARNING] No se pudo ejecutar dvc pull. Continuando...${NC}"
    fi
else
    echo -e "${YELLOW}[WARNING] No se encontró archivo .dvc. Datos podrían no estar disponibles${NC}"
fi

# Paso 4: Crear directorios necesarios
echo -e "${CYAN}[4/7] Verificando/creando directorios necesarios...${NC}"
mkdir -p logs dags plugins config

# Limpiar archivos bloqueados en logs si existen
if [ -f "logs/dag_processor/latest" ]; then
    echo -e "${YELLOW}[INFO] Limpiando archivos de log bloqueados...${NC}"
    rm -f "logs/dag_processor/latest" 2>/dev/null || true
fi
echo -e "${GREEN}[OK] Directorios verificados/creados${NC}"

# Paso 5: Verificar imagen de Docker
echo -e "${CYAN}[5/7] Verificando imagen de Docker...${NC}"
if docker images custom-airflow:latest | grep -q custom-airflow; then
    echo -e "${GREEN}[OK] Imagen custom-airflow:latest ya existe${NC}"
    echo -e "${YELLOW}[INFO] Si quieres reconstruir la imagen, ejecuta: docker-compose build${NC}"
else
    echo -e "${YELLOW}[INFO] Construyendo imagen personalizada de Airflow...${NC}"
    echo -e "${YELLOW}[INFO] Esto puede tomar varios minutos la primera vez...${NC}"
    if ! docker-compose build; then
        echo -e "${RED}[ERROR] Error al construir la imagen de Docker${NC}"
        exit 1
    fi
    echo -e "${GREEN}[OK] Imagen construida exitosamente${NC}"
fi

# Paso 6: Iniciar servicios
echo -e "${CYAN}[6/7] Iniciando servicios de Airflow con Docker Compose...${NC}"
if ! docker-compose up -d; then
    echo -e "${RED}[ERROR] Error al iniciar los servicios${NC}"
    exit 1
fi
echo -e "${GREEN}[OK] Servicios iniciados${NC}"

# Esperar a que los servicios estén listos
echo -e "${YELLOW}[7/7] Esperando a que los servicios estén completamente listos (30 segundos)...${NC}"
sleep 30

# Mostrar estado de los servicios
echo -e "${CYAN}"
echo "========================================"
echo " Estado de los servicios"
echo "========================================"
echo -e "${NC}"
docker-compose ps

# Mensaje final
echo -e "${GREEN}"
echo "========================================"
echo " AIRFLOW INICIADO CORRECTAMENTE"
echo "========================================"
echo -e "${NC}"
echo ""
echo -e "${YELLOW}Puedes acceder a Airflow en:${NC}"
echo -e "  URL: ${CYAN}http://localhost:8080${NC}"
echo -e "  Usuario: ${CYAN}airflow${NC}"
echo -e "  Contraseña: ${CYAN}airflow${NC}"
echo ""
echo -e "${YELLOW}Flower (monitor de Celery):${NC} ${CYAN}http://localhost:5555${NC}"
echo -e "  (Si habilitaste el perfil flower)"
echo ""
echo -e "${YELLOW}Comandos útiles:${NC}"
echo -e "  Ver logs en tiempo real:"
echo -e "    ${CYAN}docker-compose logs -f${NC}"
echo -e "  Detener Airflow:"
echo -e "    ${CYAN}docker-compose down${NC}"
echo -e "  Detener y eliminar volúmenes:"
echo -e "    ${CYAN}docker-compose down -v${NC}"
echo ""
