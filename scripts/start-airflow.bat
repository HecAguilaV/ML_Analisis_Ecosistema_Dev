@echo off
setlocal enabledelayedexpansion
REM ============================================================================
REM Script de automatizacion para iniciar Docker y Airflow
REM Proyecto: ML Analisis Ecosistema Dev
REM ============================================================================

REM Cambiar al directorio raiz del proyecto
cd /d "%~dp0\.."

echo.
echo ========================================
echo  Iniciando Docker y Airflow
echo ========================================
echo.

REM Verificar si Docker esta instalado
where docker >nul 2>nul
if !ERRORLEVEL! NEQ 0 (
    echo [ERROR] Docker no esta instalado o no se encuentra en el PATH
    echo Por favor, instala Docker Desktop desde: https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)

echo [1/6] Verificando estado de Docker...
docker info >nul 2>nul
if !ERRORLEVEL! NEQ 0 (
    echo [INFO] Docker Desktop no esta corriendo. Iniciando Docker Desktop...
    start "" "C:\Program Files\Docker\Docker\Docker Desktop.exe"
    
    echo [INFO] Esperando a que Docker Desktop inicie (esto puede tomar 30-60 segundos^)...
    timeout /t 10 /nobreak >nul
    
    REM Esperar hasta que Docker este listo
    set RETRY_COUNT=0
    :WAIT_DOCKER
    docker info >nul 2>nul
    if !ERRORLEVEL! EQU 0 goto DOCKER_READY
    
    set /a RETRY_COUNT+=1
    if !RETRY_COUNT! GTR 30 (
        echo [ERROR] Docker no pudo iniciarse despues de 5 minutos
        pause
        exit /b 1
    )
    
    echo Esperando... Intento !RETRY_COUNT!/30
    timeout /t 10 /nobreak >nul
    goto WAIT_DOCKER
    
    :DOCKER_READY
    echo [OK] Docker esta corriendo correctamente
) else (
    echo [OK] Docker ya esta corriendo
)

echo.
echo [2/6] Verificando archivo .env...
if not exist ".env" (
    echo [WARNING] Archivo .env no encontrado. Creando uno basico...
    echo AIRFLOW_UID=50000 > .env
    echo _AIRFLOW_WWW_USER_USERNAME=airflow >> .env
    echo _AIRFLOW_WWW_USER_PASSWORD=airflow >> .env
    echo [OK] Archivo .env creado
) else (
    echo [OK] Archivo .env encontrado
)

echo.
echo [3/6] Verificando datos con DVC...
if exist "data\01_raw.dvc" (
    echo [INFO] Descargando datos con DVC si es necesario...
    dvc pull 2>nul
    if !ERRORLEVEL! EQU 0 (
        echo [OK] Datos sincronizados con DVC
    ) else (
        echo [WARNING] No se pudo ejecutar dvc pull. Continuando...
    )
) else (
    echo [WARNING] No se encontro archivo .dvc. Datos podrian no estar disponibles
)

echo.
echo [4/6] Creando directorios necesarios...
if not exist "logs" mkdir logs
if not exist "dags" mkdir dags
if not exist "plugins" mkdir plugins
if not exist "config" mkdir config

REM Limpiar archivos bloqueados en logs si existen
if exist "logs\dag_processor\latest" (
    echo [INFO] Limpiando archivos de log bloqueados...
    del /F /Q "logs\dag_processor\latest" 2>nul
)
echo [OK] Directorios verificados/creados

echo.
echo [5/7] Verificando imagen de Docker...
docker images custom-airflow:latest | findstr custom-airflow >nul 2>nul
if !ERRORLEVEL! EQU 0 (
    echo [OK] Imagen custom-airflow:latest ya existe
    echo [INFO] Si quieres reconstruir la imagen, ejecuta: docker-compose build
) else (
    echo [INFO] Construyendo imagen personalizada de Airflow...
    echo [INFO] Esto puede tomar varios minutos la primera vez...
    docker-compose build
    if !ERRORLEVEL! NEQ 0 (
        echo [ERROR] Error al construir la imagen de Docker
        pause
        exit /b 1
    )
    echo [OK] Imagen construida exitosamente
)

echo.
echo [6/7] Iniciando servicios de Airflow con Docker Compose...
docker-compose up -d
if !ERRORLEVEL! NEQ 0 (
    echo [ERROR] Error al iniciar los servicios
    pause
    exit /b 1
)
echo [OK] Servicios iniciados

echo.
echo [7/7] Esperando a que los servicios esten listos (30 segundos^)...
timeout /t 30 /nobreak >nul

echo.
echo ========================================
echo  Estado de los servicios
echo ========================================
docker-compose ps

echo.
echo ========================================
echo  AIRFLOW INICIADO CORRECTAMENTE
echo ========================================
echo.
echo Puedes acceder a Airflow en:
echo   URL: http://localhost:8080
echo   Usuario: airflow
echo   Contrasena: airflow
echo.
echo Flower (monitor de Celery^): http://localhost:5555
echo   (Si habilitaste el perfil flower^)
echo.
echo Para ver los logs en tiempo real:
echo   docker-compose logs -f
echo.
echo Para detener Airflow:
echo   docker-compose down
echo.
echo Para detener y eliminar volumenes:
echo   docker-compose down -v
echo.
pause
