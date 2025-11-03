@echo off
REM ===========================================
REM SCRIPT DE INICIO PARA PRODUCCIÓN (Windows)
REM ML Análisis Ecosistema Dev
REM ===========================================

echo.
echo ========================================
echo   ML Analisis Ecosistema - PRODUCCION
echo ========================================
echo.

REM Verificar que Docker esté corriendo
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Docker no esta corriendo.
    echo Por favor inicia Docker Desktop.
    pause
    exit /b 1
)

echo [1/4] Construyendo imagenes Docker...
docker-compose build

echo.
echo [2/4] Iniciando servicios de produccion...
docker-compose up -d

echo.
echo [3/4] Esperando a que los servicios esten listos...
timeout /t 20 /nobreak >nul

echo.
echo [4/4] Verificando estado de los servicios...
docker-compose ps

echo.
echo ========================================
echo   SERVICIOS INICIADOS
echo ========================================
echo.
echo   Airflow Webserver: http://localhost:8080
echo   Kedro Viz:         http://localhost:4141
echo   PostgreSQL:        Puerto 5432
echo   Redis:             Puerto 6379
echo.
echo ========================================
echo   CREDENCIALES AIRFLOW
echo ========================================
echo   Usuario:    airflow
echo   Contraseña: airflow
echo.
echo ========================================
echo   COMANDOS UTILES
echo ========================================
echo   Ver logs:          docker-compose logs -f
echo   Detener todo:      docker-compose down
echo   Ejecutar pipeline: docker-compose exec kedro-viz kedro run
echo.
echo Entorno de produccion listo!
echo.
pause
