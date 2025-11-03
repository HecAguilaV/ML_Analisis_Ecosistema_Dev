@echo off
REM ===========================================
REM SCRIPT DE DETENCIÓN PARA PRODUCCIÓN (Windows)
REM ML Análisis Ecosistema Dev
REM ===========================================

echo.
echo ========================================
echo   DETENIENDO SERVICIOS
echo ========================================
echo.

docker-compose down

echo.
echo Servicios detenidos correctamente.
echo.
pause
