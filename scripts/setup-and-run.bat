@echo off
REM ============================================================================
REM Script de instalación y ejecución automática - Windows
REM Proyecto: ML Analisis Ecosistema Dev
REM Descripción: Instala todas las dependencias y ejecuta el proyecto completo
REM ============================================================================

setlocal enabledelayedexpansion

echo ============================================
echo   SETUP AUTOMATICO - ML ECOSISTEMA DEV
echo   Instalacion completa desde cero
echo ============================================
echo.

REM Cambiar al directorio raíz del proyecto
cd /d "%~dp0.."
set PROJECT_ROOT=%CD%

echo [1/10] Verificando sistema operativo...
echo [OK] Sistema operativo: Windows
echo.

REM ============================================================================
REM PASO 2: Verificar/Instalar Chocolatey
REM ============================================================================
echo [2/10] Verificando Chocolatey (gestor de paquetes)...
where choco >nul 2>nul
if %errorlevel% neq 0 (
    echo [INFO] Chocolatey no esta instalado. Instalando...
    echo [INFO] Se requieren permisos de administrador.
    echo.
    powershell -NoProfile -ExecutionPolicy Bypass -Command "Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))"
    
    if !errorlevel! neq 0 (
        echo [ERROR] No se pudo instalar Chocolatey
        echo [INFO] Por favor, instala Chocolatey manualmente desde: https://chocolatey.org/install
        echo [INFO] O instala Docker Desktop y Python manualmente
        pause
        exit /b 1
    )
    
    echo [OK] Chocolatey instalado
    echo [INFO] Por favor, cierra esta ventana y abre una nueva ventana de PowerShell como Administrador
    echo [INFO] Luego ejecuta este script nuevamente
    pause
    exit /b 0
) else (
    echo [OK] Chocolatey ya esta instalado
)
echo.

REM ============================================================================
REM PASO 3: Verificar/Instalar Docker Desktop
REM ============================================================================
echo [3/10] Verificando Docker Desktop...
where docker >nul 2>nul
if %errorlevel% neq 0 (
    echo [INFO] Docker no esta instalado. Instalando...
    echo [INFO] Esto puede tomar varios minutos...
    choco install docker-desktop -y
    
    if !errorlevel! neq 0 (
        echo [ERROR] No se pudo instalar Docker Desktop
        echo [INFO] Por favor, instala Docker Desktop manualmente desde: https://www.docker.com/products/docker-desktop
        pause
        exit /b 1
    )
    
    echo [OK] Docker Desktop instalado
    echo [WARNING] Por favor, reinicia tu computadora y ejecuta este script nuevamente
    pause
    exit /b 0
) else (
    echo [OK] Docker ya esta instalado
)
echo.

REM ============================================================================
REM PASO 4: Verificar Docker Desktop corriendo
REM ============================================================================
echo [4/10] Verificando que Docker Desktop este corriendo...
docker info >nul 2>nul
if %errorlevel% neq 0 (
    echo [INFO] Docker Desktop no esta corriendo. Intentando iniciar...
    start "" "C:\Program Files\Docker\Docker\Docker Desktop.exe"
    
    echo [INFO] Esperando a que Docker Desktop inicie (maximo 3 minutos)...
    set RETRY_COUNT=0
    set MAX_RETRIES=36
    
    :DOCKER_WAIT_LOOP
    set /a RETRY_COUNT+=1
    echo   Intento !RETRY_COUNT!/%MAX_RETRIES%...
    
    docker info >nul 2>nul
    if %errorlevel% equ 0 (
        echo [OK] Docker Desktop esta corriendo
        goto DOCKER_READY
    )
    
    if !RETRY_COUNT! geq %MAX_RETRIES% (
        echo [ERROR] Docker Desktop no pudo iniciarse despues de 3 minutos
        echo [INFO] Por favor, abre Docker Desktop manualmente y ejecuta este script nuevamente
        pause
        exit /b 1
    )
    
    timeout /t 5 /nobreak >nul
    goto DOCKER_WAIT_LOOP
    
    :DOCKER_READY
) else (
    echo [OK] Docker Desktop ya esta corriendo
)
echo.

REM ============================================================================
REM PASO 5: Verificar/Instalar Python
REM ============================================================================
echo [5/10] Verificando Python...
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [INFO] Python no esta instalado. Instalando Python 3.11...
    choco install python311 -y
    
    if !errorlevel! neq 0 (
        echo [ERROR] No se pudo instalar Python
        echo [INFO] Por favor, instala Python manualmente desde: https://www.python.org/downloads/
        pause
        exit /b 1
    )
    
    echo [OK] Python instalado
    echo [INFO] Por favor, cierra esta ventana y abre una nueva
    echo [INFO] Luego ejecuta este script nuevamente
    pause
    exit /b 0
) else (
    for /f "tokens=*" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
    echo [OK] Python ya esta instalado: !PYTHON_VERSION!
)
echo.

REM ============================================================================
REM PASO 6: Verificar/Instalar Git
REM ============================================================================
echo [6/10] Verificando Git...
where git >nul 2>nul
if %errorlevel% neq 0 (
    echo [INFO] Git no esta instalado. Instalando...
    choco install git -y
    
    if !errorlevel! neq 0 (
        echo [ERROR] No se pudo instalar Git
        echo [INFO] Por favor, instala Git manualmente desde: https://git-scm.com/download/win
        pause
        exit /b 1
    )
    
    echo [OK] Git instalado
    echo [INFO] Por favor, cierra esta ventana y abre una nueva
    echo [INFO] Luego ejecuta este script nuevamente
    pause
    exit /b 0
) else (
    for /f "tokens=*" %%i in ('git --version 2^>^&1') do set GIT_VERSION=%%i
    echo [OK] Git ya esta instalado: !GIT_VERSION!
)
echo.

REM ============================================================================
REM PASO 7: Detectar o crear entorno virtual Python
REM - Verifica si ya hay un entorno virtual activo (variable VIRTUAL_ENV)
REM - Busca entornos virtuales existentes: .venv, venv, env, .env
REM - Si no existe ninguno, crea uno nuevo llamado 'venv'
REM - Activa el entorno virtual para instalar dependencias localmente
REM ============================================================================
echo [7/10] Configurando entorno virtual Python...

REM Verificar si ya hay un entorno virtual activo
if defined VIRTUAL_ENV (
    echo [OK] Entorno virtual ya esta activo: %VIRTUAL_ENV%
    set VENV_ACTIVE=true
) else (
    set VENV_ACTIVE=false
    set VENV_PATH=
    
    REM Buscar entornos virtuales existentes en orden de preferencia
    if exist ".venv\Scripts\activate.bat" (
        set VENV_PATH=.venv
        echo [OK] Entorno virtual encontrado: %PROJECT_ROOT%\.venv
    ) else if exist "venv\Scripts\activate.bat" (
        set VENV_PATH=venv
        echo [OK] Entorno virtual encontrado: %PROJECT_ROOT%\venv
    ) else if exist "env\Scripts\activate.bat" (
        set VENV_PATH=env
        echo [OK] Entorno virtual encontrado: %PROJECT_ROOT%\env
    ) else if exist ".env\Scripts\activate.bat" (
        set VENV_PATH=.env
        echo [OK] Entorno virtual encontrado: %PROJECT_ROOT%\.env
    )
    
    REM Si no se encontró ningún entorno virtual, crear uno nuevo
    if "!VENV_PATH!"=="" (
        echo [INFO] No se encontro entorno virtual. Creando 'venv'...
        python -m venv venv
        if !errorlevel! neq 0 (
            echo [ERROR] No se pudo crear el entorno virtual
            pause
            exit /b 1
        )
        set VENV_PATH=venv
        echo [OK] Entorno virtual creado en: %PROJECT_ROOT%\venv
    )
    
    REM Activar el entorno virtual encontrado o recién creado
    echo [INFO] Activando entorno virtual: !VENV_PATH!
    call !VENV_PATH!\Scripts\activate.bat
    if !errorlevel! neq 0 (
        echo [ERROR] No se pudo activar el entorno virtual
        pause
        exit /b 1
    )
    echo [OK] Entorno virtual activado
)
echo.

REM ============================================================================
REM PASO 8: Instalar/actualizar dependencias Python desde requirements.txt
REM - Actualiza pip, setuptools y wheel a las últimas versiones
REM - Instala todas las dependencias listadas en requirements.txt
REM - Las dependencias incluyen: kedro, kedro-viz, pandas, scikit-learn, dvc[gcs], etc.
REM - Si un paquete ya está instalado, pip lo verificará y lo actualizará solo si es necesario
REM ============================================================================
echo [8/10] Instalando/verificando dependencias Python...

REM Actualizar herramientas base de pip
echo [INFO] Actualizando pip, setuptools y wheel...
python -m pip install --upgrade pip setuptools wheel --quiet
echo [OK] Herramientas base actualizadas

REM Verificar si requirements.txt existe
if not exist "requirements.txt" (
    echo [ERROR] No se encontro el archivo requirements.txt
    pause
    exit /b 1
)

REM Instalar dependencias desde requirements.txt
REM pip install -r verificará automáticamente qué paquetes ya están instalados
echo [INFO] Instalando dependencias desde requirements.txt...
echo [INFO] Esto puede tomar varios minutos si es la primera vez...
pip install -r requirements.txt
if %errorlevel% equ 0 (
    echo [OK] Todas las dependencias instaladas/verificadas correctamente
    echo     - kedro y kedro-viz instalados
    echo     - pandas, scikit-learn, xgboost, lightgbm instalados
    echo     - dvc[gcs] instalado para control de versiones de datos
) else (
    echo [WARNING] Algunas dependencias pueden haber fallado
    echo [INFO] Continuando con la instalacion...
)
echo.

REM ============================================================================
REM PASO 9: Configurar DVC y descargar datos
REM ============================================================================
REM DVC (Data Version Control) maneja versionado de datos grandes
REM Similar a Git pero optimizado para datasets
echo [9/10] Configurando DVC y descargando datos...

REM Verificar si DVC está instalado
where dvc >nul 2>nul
if %errorlevel% neq 0 (
    echo [INFO] DVC no esta instalado. Instalando...
    
    REM Instalar DVC con soporte para Google Cloud Storage
    pip install "dvc[gs]" dvc-gs gcsfs
    
    if !errorlevel! equ 0 (
        echo [OK] DVC instalado correctamente
    ) else (
        echo [ERROR] No se pudo instalar DVC
        echo [WARNING] Continuando sin DVC...
    )
) else (
    echo [OK] DVC ya esta instalado
    REM Mostrar versión instalada para verificación
    for /f "tokens=*" %%i in ('dvc version 2^>^&1 ^| findstr /R "^[0-9]"') do (
        echo     Version: %%i
    )
)

REM Verificar si existe configuración de DVC en el proyecto
if exist ".dvc\config" goto DVC_CONFIG_FOUND
if exist "data\01_raw.dvc" goto DVC_CONFIG_FOUND
goto NO_DVC_CONFIG

:DVC_CONFIG_FOUND
echo [INFO] Configuracion DVC encontrada. Inicializando datos...

REM Verificar si el repositorio DVC está inicializado
if not exist ".dvc" (
    echo [INFO] Inicializando repositorio DVC...
    dvc init --no-scm 2>nul
)

REM Intentar descargar los datos desde el storage remoto
echo [INFO] Descargando datos con DVC desde almacenamiento remoto...
echo [INFO] Esto puede tomar varios minutos dependiendo del tamano de los datos...

REM Ejecutar dvc pull con manejo de errores
dvc pull -v > "%TEMP%\dvc_pull.log" 2>&1
if %errorlevel% equ 0 (
    echo [OK] Datos sincronizados exitosamente con DVC
    
    REM Mostrar resumen de datos descargados
    if exist "data\01_raw" (
        for /f %%a in ('dir /b /a-d "data\01_raw" 2^>nul ^| find /c /v ""') do (
            echo     Archivos en data\01_raw: %%a
        )
    )
) else (
    REM Capturar el código de error
    set DVC_EXIT_CODE=%errorlevel%
    echo [WARNING] No se pudieron descargar todos los datos con DVC (codigo: !DVC_EXIT_CODE!)
    
    REM Verificar razones comunes de fallo
    findstr /i "authentication" "%TEMP%\dvc_pull.log" >nul 2>nul
    if !errorlevel! equ 0 (
        echo [INFO] Posible problema de autenticacion con el storage remoto
        echo [INFO] Verifica tus credenciales de Google Cloud Storage
    )
    
    findstr /i "not found" "%TEMP%\dvc_pull.log" >nul 2>nul
    if !errorlevel! equ 0 (
        echo [INFO] Algunos archivos no se encontraron en el storage remoto
    )
    
    echo [INFO] El proyecto continuara sin los datos remotos
    echo [INFO] Puedes ejecutar 'dvc pull' manualmente mas tarde
    
    REM Limpiar archivo temporal de log
    del "%TEMP%\dvc_pull.log" 2>nul
)

REM Verificar si hay datos locales disponibles
if exist "data\01_raw" (
    dir /b /a-d "data\01_raw" 2>nul | findstr "^" >nul
    if !errorlevel! equ 0 (
        echo [OK] Datos disponibles localmente en data\01_raw
    ) else (
        echo [WARNING] No hay datos en data\01_raw
        echo [INFO] El proyecto funcionara pero los pipelines de datos pueden fallar
    )
) else (
    echo [WARNING] Directorio data\01_raw no existe
)

goto DVC_END

:NO_DVC_CONFIG
echo [INFO] No se encontro configuracion DVC en el proyecto
echo [INFO] Si necesitas DVC, ejecuta: dvc init

:DVC_END
echo.

REM ============================================================================
REM PASO 10: Ejecutar Airflow con Docker
REM ============================================================================
echo [10/10] Iniciando servicios con Docker...

REM Verificar docker-compose
where docker-compose >nul 2>nul
if %errorlevel% equ 0 (
    set DOCKER_COMPOSE_CMD=docker-compose
) else (
    docker compose version >nul 2>nul
    if !errorlevel! equ 0 (
        set DOCKER_COMPOSE_CMD=docker compose
    ) else (
        echo [ERROR] docker-compose no esta disponible
        pause
        exit /b 1
    )
)

REM Crear archivo .env si no existe
if not exist ".env" (
    echo [INFO] Creando archivo .env...
    (
        echo AIRFLOW_UID=50000
        echo _AIRFLOW_WWW_USER_USERNAME=airflow
        echo _AIRFLOW_WWW_USER_PASSWORD=airflow
    ) > .env
    echo [OK] Archivo .env creado
)

REM Crear directorios necesarios
if not exist "logs" mkdir logs
if not exist "dags" mkdir dags
if not exist "plugins" mkdir plugins
if not exist "config" mkdir config
if not exist "data\01_raw" mkdir data\01_raw
if not exist "data\02_intermediate" mkdir data\02_intermediate
if not exist "data\03_primary" mkdir data\03_primary
if not exist "data\04_feature" mkdir data\04_feature
if not exist "data\05_model_input" mkdir data\05_model_input

REM Construir e iniciar servicios
echo [INFO] Construyendo e iniciando servicios Docker...
echo [INFO] Esto puede tomar 5-10 minutos la primera vez...
echo.

%DOCKER_COMPOSE_CMD% build
if %errorlevel% neq 0 (
    echo [ERROR] Error al construir la imagen de Docker
    pause
    exit /b 1
)

%DOCKER_COMPOSE_CMD% up -d
if %errorlevel% neq 0 (
    echo [ERROR] Error al iniciar los servicios
    pause
    exit /b 1
)

REM Esperar a que los servicios estén listos
echo [INFO] Esperando a que los servicios esten completamente listos...
timeout /t 30 /nobreak >nul

REM ============================================================================
REM RESUMEN FINAL
REM ============================================================================
echo.
echo ============================================
echo   INSTALACION COMPLETADA CON EXITO
echo ============================================
echo.
echo.
echo Servicios disponibles:
echo.
echo  Airflow UI:
echo    URL: http://localhost:8081
echo    Usuario: airflow
echo    Contraseña: airflow
echo.
echo  Kedro-Viz:
echo    URL: http://localhost:4141
echo.
echo  Jupyter Notebook:
echo    URL: http://localhost:8888
echo.
echo Comandos utiles:
echo.
echo   Ver estado de servicios:
echo     %DOCKER_COMPOSE_CMD% ps
echo.
echo   Ver logs en tiempo real:
echo     %DOCKER_COMPOSE_CMD% logs -f
echo.
echo   Detener servicios:
echo     %DOCKER_COMPOSE_CMD% down
echo.
echo   Reiniciar servicios:
echo     %DOCKER_COMPOSE_CMD% restart
echo.
echo   Activar entorno virtual Python:
echo     venv\Scripts\activate.bat
echo.
echo Disfruta desarrollando!
echo.
pause
