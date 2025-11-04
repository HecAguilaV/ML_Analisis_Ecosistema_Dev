@echo off
REM ============================================================================
REM Script para detener Docker y Airflow
REM Proyecto: ML Analisis Ecosistema Dev
REM ============================================================================

REM Cambiar al directorio raiz del proyecto
cd /d "%~dp0\.."

echo.
echo ========================================
echo  Deteniendo Airflow
echo ========================================
echo.

echo Selecciona una opcion:
echo.
echo [1] Detener servicios (mantener datos)
echo [2] Detener servicios y eliminar volumenes (eliminar datos)
echo [3] Cancelar
echo.
set /p option="Ingresa tu opcion (1-3): "

if "%option%"=="1" goto STOP_ONLY
if "%option%"=="2" goto STOP_AND_CLEAN
if "%option%"=="3" goto CANCEL

:INVALID
echo [ERROR] Opcion invalida
pause
exit /b 1

:STOP_ONLY
echo.
echo [INFO] Deteniendo servicios...
docker-compose down
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Error al detener los servicios
    pause
    exit /b 1
)
echo [OK] Servicios detenidos correctamente
echo [INFO] Los datos se han preservado en los volumenes
goto END

:STOP_AND_CLEAN
echo.
echo [WARNING] Esto eliminara todos los datos, logs y configuraciones
set /p confirm="Estas seguro? (S/N): "
if /i not "%confirm%"=="S" goto CANCEL

echo.
echo [INFO] Deteniendo servicios y eliminando volumenes...
docker-compose down -v
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Error al detener los servicios
    pause
    exit /b 1
)
echo [OK] Servicios detenidos y volumenes eliminados
goto END

:CANCEL
echo.
echo [INFO] Operacion cancelada
goto END

:END
echo.
pause
