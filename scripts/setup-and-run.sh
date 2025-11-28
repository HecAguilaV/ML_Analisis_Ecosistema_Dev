#!/bin/bash
# ============================================================================
# Script de instalación y ejecución automática - Mac/Linux
# Proyecto: ML Analisis Ecosistema Dev
# Descripción: Instala todas las dependencias y ejecuta el proyecto completo
# ============================================================================

set -e  # Salir si hay algún error

# Colores para mejor visualización
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m' # No Color

# Cambiar al directorio raíz del proyecto
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$PROJECT_ROOT" || exit 1

echo -e "${MAGENTA}"
echo "============================================"
echo "  SETUP AUTOMÁTICO - ML ECOSISTEMA DEV"
echo "  Instalación completa desde cero"
echo "============================================"
echo -e "${NC}"

# ============================================================================
# PASO 1: Detectar sistema operativo
# ============================================================================
echo -e "${CYAN}[1/10] Detectando sistema operativo...${NC}"
OS_TYPE="unknown"
if [[ "$OSTYPE" == "darwin"* ]]; then
    OS_TYPE="mac"
    echo -e "${GREEN}[OK] Sistema operativo: macOS${NC}"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS_TYPE="linux"
    echo -e "${GREEN}[OK] Sistema operativo: Linux${NC}"
else
    echo -e "${RED}[ERROR] Sistema operativo no soportado: $OSTYPE${NC}"
    exit 1
fi

# ============================================================================
# PASO 2: Verificar/Instalar Homebrew (solo macOS)
# ============================================================================
if [ "$OS_TYPE" = "mac" ]; then
    echo -e "${CYAN}[2/10] Verificando Homebrew...${NC}"
    if ! command -v brew &> /dev/null; then
        echo -e "${YELLOW}[INFO] Homebrew no está instalado. Instalando...${NC}"
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        
        # Agregar Homebrew al PATH
        if [ -f "/opt/homebrew/bin/brew" ]; then
            echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
            eval "$(/opt/homebrew/bin/brew shellenv)"
        fi
        
        echo -e "${GREEN}[OK] Homebrew instalado${NC}"
    else
        echo -e "${GREEN}[OK] Homebrew ya está instalado${NC}"
    fi
else
    echo -e "${CYAN}[2/10] Saltando instalación de Homebrew (Linux)${NC}"
fi

# ============================================================================
# PASO 3: Verificar/Instalar Docker
# ============================================================================
echo -e "${CYAN}[3/10] Verificando Docker...${NC}"
if ! command -v docker &> /dev/null; then
    echo -e "${YELLOW}[INFO] Docker no está instalado. Instalando...${NC}"
    
    if [ "$OS_TYPE" = "mac" ]; then
        brew install --cask docker
        echo -e "${GREEN}[OK] Docker instalado${NC}"
        echo -e "${YELLOW}[INFO] Por favor, abre Docker Desktop y vuelve a ejecutar este script${NC}"
        open -a Docker
        exit 0
    else
        echo -e "${YELLOW}[INFO] Instalando Docker en Linux...${NC}"
        curl -fsSL https://get.docker.com -o get-docker.sh
        sudo sh get-docker.sh
        sudo usermod -aG docker $USER
        rm get-docker.sh
        echo -e "${GREEN}[OK] Docker instalado${NC}"
        echo -e "${YELLOW}[WARNING] Por favor, cierra sesión y vuelve a iniciar para aplicar los permisos de Docker${NC}"
        exit 0
    fi
else
    echo -e "${GREEN}[OK] Docker ya está instalado${NC}"
fi

# ============================================================================
# PASO 4: Verificar Docker Desktop corriendo
# ============================================================================
echo -e "${CYAN}[4/10] Verificando Docker Desktop...${NC}"

# Buscar Docker en ubicaciones comunes si no está en PATH
DOCKER_PATHS=(
    "/usr/local/bin"
    "/opt/homebrew/bin"
    "/Applications/Docker.app/Contents/Resources/bin"
    "$HOME/.docker/bin"
)

DOCKER_CMD="docker"
if ! command -v docker &> /dev/null; then
    for docker_path in "${DOCKER_PATHS[@]}"; do
        if [ -f "$docker_path/docker" ]; then
            export PATH="$docker_path:$PATH"
            DOCKER_CMD="$docker_path/docker"
            echo -e "${GREEN}[OK] Docker encontrado en: $docker_path${NC}"
            break
        fi
    done
fi

if ! $DOCKER_CMD info &> /dev/null; then
    echo -e "${YELLOW}[INFO] Docker Desktop no está corriendo. Iniciando...${NC}"
    
    if [ "$OS_TYPE" = "mac" ]; then
        open -a Docker
        echo -e "${YELLOW}[INFO] Esperando a que Docker Desktop inicie (máximo 3 minutos)...${NC}"
        
        RETRY_COUNT=0
        MAX_RETRIES=36  # 36 * 5 seg = 3 minutos
        while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
            RETRY_COUNT=$((RETRY_COUNT + 1))
            echo "  Intento $RETRY_COUNT/$MAX_RETRIES..."
            
            if $DOCKER_CMD info &> /dev/null; then
                echo -e "${GREEN}[OK] Docker Desktop está corriendo${NC}"
                break
            fi
            sleep 5
        done
        
        if ! $DOCKER_CMD info &> /dev/null; then
            echo -e "${RED}[ERROR] Docker Desktop no pudo iniciarse${NC}"
            echo "Por favor, abre Docker Desktop manualmente y vuelve a ejecutar este script"
            exit 1
        fi
    else
        echo -e "${YELLOW}[INFO] Iniciando Docker daemon en Linux...${NC}"
        sudo systemctl start docker
        sleep 5
        
        if ! $DOCKER_CMD info &> /dev/null; then
            echo -e "${RED}[ERROR] No se pudo iniciar Docker${NC}"
            exit 1
        fi
        echo -e "${GREEN}[OK] Docker iniciado${NC}"
    fi
else
    echo -e "${GREEN}[OK] Docker Desktop ya está corriendo${NC}"
fi

# ============================================================================
# PASO 5: Verificar/Instalar Python
# ============================================================================
echo -e "${CYAN}[5/10] Verificando Python...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${YELLOW}[INFO] Python3 no está instalado. Instalando...${NC}"
    
    if [ "$OS_TYPE" = "mac" ]; then
        brew install python@3.11
    else
        sudo apt-get update
        sudo apt-get install -y python3 python3-pip python3-venv
    fi
    echo -e "${GREEN}[OK] Python3 instalado${NC}"
else
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}[OK] Python ya está instalado: $PYTHON_VERSION${NC}"
fi

# ============================================================================
# PASO 6: Verificar/Instalar Git
# ============================================================================
echo -e "${CYAN}[6/10] Verificando Git...${NC}"
if ! command -v git &> /dev/null; then
    echo -e "${YELLOW}[INFO] Git no está instalado. Instalando...${NC}"
    
    if [ "$OS_TYPE" = "mac" ]; then
        brew install git
    else
        sudo apt-get install -y git
    fi
    echo -e "${GREEN}[OK] Git instalado${NC}"
else
    GIT_VERSION=$(git --version)
    echo -e "${GREEN}[OK] Git ya está instalado: $GIT_VERSION${NC}"
fi

# ============================================================================
# PASO 7: Crear/activar entorno virtual Python (requerido)
# - Detecta si ya hay un entorno virtual activo en la sesión actual
# - Busca entornos virtuales existentes: .venv, venv, env, .env
# - Si no existe ninguno, crea uno nuevo llamado 'venv'
# - Activa el entorno virtual para instalar dependencias localmente
# ============================================================================
echo -e "${CYAN}[7/10] Configurando entorno virtual Python...${NC}"

# Verificar si ya hay un entorno virtual activo
if [ -n "$VIRTUAL_ENV" ]; then
    echo -e "${GREEN}[OK] Entorno virtual ya está activo: $VIRTUAL_ENV${NC}"
else
    # Buscar entornos virtuales existentes en orden de preferencia
    VENV_PATH=""
    for venv_candidate in ".venv" "venv" "env" ".env"; do
        if [ -d "$venv_candidate" ] && [ -f "$venv_candidate/bin/activate" ]; then
            VENV_PATH="$venv_candidate"
            echo -e "${GREEN}[OK] Entorno virtual encontrado: $PROJECT_ROOT/$VENV_PATH${NC}"
            break
        fi
    done
    
    # Si no se encontró ningún entorno virtual, crear uno nuevo
    if [ -z "$VENV_PATH" ]; then
        echo -e "${YELLOW}[INFO] No se encontró entorno virtual. Creando 'venv'...${NC}"
        python3 -m venv venv
        if [ $? -ne 0 ]; then
            echo -e "${RED}[ERROR] No se pudo crear el entorno virtual${NC}"
            exit 1
        fi
        VENV_PATH="venv"
        echo -e "${GREEN}[OK] Entorno virtual creado en: $PROJECT_ROOT/$VENV_PATH${NC}"
    fi
    
    # Activar el entorno virtual encontrado o recién creado
    echo -e "${CYAN}[INFO] Activando entorno virtual: $VENV_PATH${NC}"
    if [ -f "$VENV_PATH/bin/activate" ]; then
        # shellcheck disable=SC1090,SC1091
        source "$VENV_PATH/bin/activate"
        echo -e "${GREEN}[OK] Entorno virtual activado${NC}"
    else
        echo -e "${RED}[ERROR] No se encontró el script de activación en $VENV_PATH/bin/activate${NC}"
        exit 1
    fi
fi

# ============================================================================
# PASO 8: Instalar/actualizar dependencias Python desde requirements.txt
# - Actualiza pip, setuptools y wheel a las últimas versiones
# - Instala todas las dependencias listadas en requirements.txt
# - Las dependencias incluyen: kedro, kedro-viz, pandas, scikit-learn, dvc[gcs], etc.
# - Si un paquete ya está instalado, pip lo verificará y lo actualizará solo si es necesario
# ============================================================================
echo -e "${CYAN}[8/10] Instalando/verificando dependencias Python...${NC}"

# Actualizar herramientas base de pip
echo -e "${CYAN}[INFO] Actualizando pip, setuptools y wheel...${NC}"
pip install --upgrade pip setuptools wheel --quiet
echo -e "${GREEN}[OK] Herramientas base actualizadas${NC}"

# Preferimos instalar dependencias de desarrollo localmente desde
# requirements-dev.txt (ligero para runtime). El contenedor Docker se
# construirá usando docker/Dockerfile.runtime que instala sólo
# requirements-runtime.txt.
DEV_REQ_FILE="requirements-dev.txt"
RUNTIME_REQ_FILE="requirements-runtime.txt"

if [ -f "$DEV_REQ_FILE" ]; then
    echo -e "${CYAN}[INFO] Instalando dependencias de desarrollo desde $DEV_REQ_FILE en el venv...${NC}"
    echo -e "${YELLOW}[INFO] Esto puede tomar varios minutos la primera vez...${NC}"
    if pip install -r "$DEV_REQ_FILE"; then
        echo -e "${GREEN}[OK] Dependencias de desarrollo instaladas correctamente${NC}"
    else
        echo -e "${YELLOW}[WARNING] Algunas dependencias de desarrollo fallaron al instalarse.${NC}"
        echo -e "${YELLOW}[INFO] Puedes intentar 'pip install -r $DEV_REQ_FILE' manualmente o revisar los errores.${NC}"
    fi
else
    # Fallback: try requirements.txt for backwards compatibility
    if [ -f "requirements.txt" ]; then
        echo -e "${YELLOW}[INFO] No se encontró $DEV_REQ_FILE — usando requirements.txt como fallback${NC}"
        if pip install -r requirements.txt; then
            echo -e "${GREEN}[OK] Dependencias instaladas desde requirements.txt${NC}"
        else
            echo -e "${YELLOW}[WARNING] Instalación desde requirements.txt falló.${NC}"
        fi
    else
        echo -e "${YELLOW}[WARNING] No se encontró ningún archivo de requirements. Saltando instalación de dependencias.${NC}"
    fi
fi

# ============================================================================
# PASO 9: Verificar DVC y descargar datos si están configurados
# - DVC (Data Version Control) maneja versionado de datos grandes
# - Similar a Git pero optimizado para datasets
# - Si existe data/01_raw.dvc, intenta hacer pull de los datos
# ============================================================================
echo -e "${CYAN}[9/10] Configurando DVC y descargando datos...${NC}"

# Verificar que DVC esté disponible (ya debería estar desde requirements.txt)
if ! command -v dvc &> /dev/null; then
    echo -e "${YELLOW}[WARNING] DVC no está disponible después de instalar requirements.txt${NC}"
    echo -e "${YELLOW}[INFO] Intentando instalar DVC manualmente...${NC}"
    
    if pip install 'dvc[gcs]' gcsfs; then
        echo -e "${GREEN}[OK] DVC instalado correctamente${NC}"
    else
        echo -e "${RED}[ERROR] No se pudo instalar DVC. Continuando sin datos de DVC...${NC}"
        echo -e "${YELLOW}[WARNING] Continuando sin DVC...${NC}"
    fi
else
    echo -e "${GREEN}[OK] DVC ya está instalado${NC}"
    # Mostrar versión instalada para verificación
    DVC_VERSION=$(dvc version | head -n 1)
    echo -e "${GREEN}    Versión: $DVC_VERSION${NC}"
fi

# Verificar si existe configuración de DVC en el proyecto
if [ -f ".dvc/config" ] || [ -f "data/01_raw.dvc" ]; then
    echo -e "${YELLOW}[INFO] Configuración DVC encontrada. Inicializando datos...${NC}"
    
    # Verificar si el repositorio DVC está inicializado
    if [ ! -d ".dvc" ]; then
        echo -e "${YELLOW}[INFO] Inicializando repositorio DVC...${NC}"
        dvc init --no-scm 2>/dev/null || true
    fi
    
    # Intentar descargar los datos desde el storage remoto
    echo -e "${YELLOW}[INFO] Descargando datos con DVC desde almacenamiento remoto...${NC}"
    echo -e "${YELLOW}[INFO] Esto puede tomar varios minutos dependiendo del tamaño de los datos...${NC}"
    
    # Ejecutar dvc pull con manejo de errores
    if dvc pull -v 2>&1 | tee /tmp/dvc_pull.log; then
        echo -e "${GREEN}[OK] Datos sincronizados exitosamente con DVC${NC}"
        
        # Mostrar resumen de datos descargados
        if [ -d "data/01_raw" ]; then
            FILE_COUNT=$(find data/01_raw -type f | wc -l)
            echo -e "${GREEN}    Archivos en data/01_raw: $FILE_COUNT${NC}"
        fi
    else
        # Capturar el código de error
        DVC_EXIT_CODE=$?
        echo -e "${YELLOW}[WARNING] No se pudieron descargar todos los datos con DVC (código: $DVC_EXIT_CODE)${NC}"
        
        # Verificar razones comunes de fallo
        if grep -q "authentication" /tmp/dvc_pull.log 2>/dev/null; then
            echo -e "${YELLOW}[INFO] Posible problema de autenticación con el storage remoto${NC}"
            echo -e "${YELLOW}[INFO] Verifica tus credenciales de Google Cloud Storage${NC}"
        elif grep -q "not found" /tmp/dvc_pull.log 2>/dev/null; then
            echo -e "${YELLOW}[INFO] Algunos archivos no se encontraron en el storage remoto${NC}"
        fi
        
        echo -e "${YELLOW}[INFO] El proyecto continuará sin los datos remotos${NC}"
        echo -e "${YELLOW}[INFO] Puedes ejecutar 'dvc pull' manualmente más tarde${NC}"
        
        # Limpiar archivo temporal de log
        rm -f /tmp/dvc_pull.log
    fi
    
    # Verificar si hay datos locales disponibles
    if [ -d "data/01_raw" ] && [ "$(ls -A data/01_raw 2>/dev/null)" ]; then
        echo -e "${GREEN}[OK] Datos disponibles localmente en data/01_raw${NC}"
    else
        echo -e "${YELLOW}[WARNING] No hay datos en data/01_raw${NC}"
        echo -e "${YELLOW}[INFO] El proyecto funcionará pero los pipelines de datos pueden fallar${NC}"
    fi
else
    echo -e "${YELLOW}[INFO] No se encontró configuración DVC en el proyecto${NC}"
    echo -e "${YELLOW}[INFO] Si necesitas DVC, ejecuta: dvc init${NC}"
fi

echo ""

# ============================================================================
# PASO 10: Ejecutar Airflow con Docker
# ============================================================================
echo -e "${CYAN}[10/10] Iniciando servicios con Docker...${NC}"

# Verificar docker-compose
if command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
elif $DOCKER_CMD compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
else
    echo -e "${RED}[ERROR] docker-compose no está disponible${NC}"
    exit 1
fi

# Crear archivo .env si no existe
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}[INFO] Creando archivo .env...${NC}"
    cat > .env << EOF
AIRFLOW_UID=50000
_AIRFLOW_WWW_USER_USERNAME=airflow
_AIRFLOW_WWW_USER_PASSWORD=airflow
EOF
    echo -e "${GREEN}[OK] Archivo .env creado${NC}"
fi

# Crear directorios necesarios
mkdir -p logs dags plugins config data/{01_raw,02_intermediate,03_primary,04_feature,05_model_input}

# Construir e iniciar servicios
echo -e "${YELLOW}[INFO] Construyendo e iniciando servicios Docker...${NC}"
echo -e "${YELLOW}[INFO] Esto puede tomar 5-10 minutos la primera vez...${NC}"

if [ "$DOCKER_COMPOSE_CMD" = "docker-compose" ]; then
    docker-compose build
    docker-compose up -d
else
    $DOCKER_CMD compose build
    $DOCKER_CMD compose up -d
fi

# Esperar a que los servicios estén listos
echo -e "${YELLOW}[INFO] Esperando a que los servicios estén completamente listos...${NC}"
sleep 30

# ============================================================================
# PULL DE DATOS CON DVC (si aplica)
# - Si existe un archivo .dvc (ej. data/01_raw.dvc) y DVC está instalado, intentamos
#   sincronizar los datos remotos con `dvc pull`.
# - Si falla, mostramos una advertencia y continuamos (para no romper el flujo).
# ============================================================================
echo -e "${CYAN}[11/11] Sincronizando datos con DVC (si aplica)...${NC}"
if [ -f "data/01_raw.dvc" ]; then
    if command -v dvc &> /dev/null; then
        echo -e "${YELLOW}[INFO] Ejecutando: dvc pull${NC}"
        if dvc pull; then
            echo -e "${GREEN}[OK] Datos sincronizados con DVC${NC}"
        else
            echo -e "${YELLOW}[WARNING] dvc pull falló. Asegúrate de tener credenciales remotas configuradas.${NC}"
        fi
    else
        echo -e "${YELLOW}[WARNING] Se detectó DVC config (data/01_raw.dvc) pero DVC no está instalado en el entorno virtual.${NC}"
        echo -e "${YELLOW}Instala DVC manualmente o revisa el entorno virtual (venv)${NC}"
    fi
else
    echo -e "${YELLOW}[INFO] No se encontró configuración DVC. Saltando dvc pull...${NC}"
fi

# ============================================================================
# RESUMEN FINAL
# ============================================================================

# ============================================================================
# PASO EXTRA: Ejecutar pipeline de Kedro automáticamente
# ============================================================================
echo -e "${CYAN}[12/12] Ejecutando pipeline de Kedro...${NC}"
source venv/bin/activate
kedro run

echo ""
echo -e "${GREEN}"
echo "============================================"
echo "  ✅ INSTALACIÓN COMPLETADA CON ÉXITO"
echo "============================================"
echo -e "${NC}"
echo ""
echo -e "${CYAN}📊 Servicios disponibles:${NC}"
echo ""
echo -e "${YELLOW}🌐 Airflow UI:${NC}"
echo -e "   URL: ${GREEN}http://localhost:8081${NC}"
echo -e "   Usuario: ${CYAN}airflow${NC}"
echo -e "   Contraseña: ${CYAN}airflow${NC}"
echo ""
echo -e "${YELLOW}📊 Kedro-Viz:${NC}"
echo -e "   URL: ${GREEN}http://localhost:4141${NC}"
echo ""
echo -e "${YELLOW}📓 Jupyter Notebook:${NC}"
echo -e "   URL: ${GREEN}http://localhost:8888${NC}"
echo ""
echo -e "${CYAN}🔧 Comandos útiles:${NC}"
echo -e "  Ver estado de servicios:"
echo -e "    ${GREEN}$DOCKER_COMPOSE_CMD ps${NC}"
echo ""
echo -e "  Ver logs en tiempo real:"
echo -e "    ${GREEN}$DOCKER_COMPOSE_CMD logs -f${NC}"
echo ""
echo -e "  Detener servicios:"
echo -e "    ${GREEN}$DOCKER_COMPOSE_CMD down${NC}"
echo ""
echo -e "  Reiniciar servicios:"
echo -e "    ${GREEN}$DOCKER_COMPOSE_CMD restart${NC}"
echo ""
echo -e "  Activar entorno virtual Python:"
echo -e "    ${GREEN}source venv/bin/activate${NC}"
echo ""
echo -e "${YELLOW}💡 Tip:${NC} Guarda estos comandos para uso futuro"
echo ""
echo -e "${GREEN}¡Disfruta desarrollando! 🚀${NC}"
echo ""
