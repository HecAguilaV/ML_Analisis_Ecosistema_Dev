#!/bin/bash
# ============================================================================
# Script para detener Docker y Airflow (Mac/Linux)
# Proyecto: ML Analisis Ecosistema Dev
# ============================================================================

# Cambiar al directorio raiz del proyecto
cd "$(dirname "$0")/.." || exit 1

# Colores para mejor visualización
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}"
echo "========================================"
echo " Deteniendo Airflow"
echo "========================================"
echo -e "${NC}"

# Mostrar opciones
echo "Selecciona una opción:"
echo ""
echo "[1] Detener servicios (mantener datos)"
echo "[2] Detener servicios y eliminar volúmenes (eliminar datos)"
echo "[3] Cancelar"
echo ""
read -p "Ingresa tu opción (1-3): " option

case $option in
    1)
        echo ""
        echo -e "${CYAN}[INFO] Deteniendo servicios...${NC}"
        if ! docker-compose down; then
            echo -e "${RED}[ERROR] Error al detener los servicios${NC}"
            exit 1
        fi
        echo -e "${GREEN}[OK] Servicios detenidos correctamente${NC}"
        echo -e "${YELLOW}[INFO] Los datos se han preservado en los volúmenes${NC}"
        ;;
    2)
        echo ""
        echo -e "${YELLOW}[WARNING] Esto eliminará todos los datos, logs y configuraciones${NC}"
        read -p "¿Estás seguro? (s/N): " confirm
        if [[ $confirm == "s" || $confirm == "S" ]]; then
            echo ""
            echo -e "${CYAN}[INFO] Deteniendo servicios y eliminando volúmenes...${NC}"
            if ! docker-compose down -v; then
                echo -e "${RED}[ERROR] Error al detener los servicios${NC}"
                exit 1
            fi
            echo -e "${GREEN}[OK] Servicios detenidos y volúmenes eliminados${NC}"
        else
            echo -e "${YELLOW}[INFO] Operación cancelada${NC}"
        fi
        ;;
    3)
        echo ""
        echo -e "${YELLOW}[INFO] Operación cancelada${NC}"
        ;;
    *)
        echo ""
        echo -e "${RED}[ERROR] Opción inválida${NC}"
        exit 1
        ;;
esac

echo ""
