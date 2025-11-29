# 🚀 Scripts de Instalación y Ejecución Automática

Esta carpeta contiene scripts para instalar y ejecutar el proyecto completo de forma automática en diferentes sistemas operativos.

---

## 📋 Índice

- [Scripts Disponibles](#scripts-disponibles)
- [Uso Rápido](#uso-rápido)
- [Características](#características)
- [Requisitos Previos](#requisitos-previos)
- [Solución de Problemas](#solución-de-problemas)

---

## 📦 Scripts Disponibles

### 1. `setup-and-run.sh` (Mac/Linux)
**Script de instalación completa para macOS y Linux**

Instala automáticamente:
- ✅ Homebrew (solo macOS)
- ✅ Docker Desktop
- ✅ Python 3.11+
- ✅ Git
- ✅ Entorno virtual Python
- ✅ Todas las dependencias del proyecto
- ✅ DVC (Data Version Control)
- ✅ Descarga datos con DVC automáticamente
- ✅ Construye e inicia todos los servicios Docker

### 2. `setup-and-run.bat` (Windows)
**Script de instalación completa para Windows**

Instala automáticamente:
- ✅ Chocolatey (gestor de paquetes)
- ✅ Docker Desktop
- ✅ Python 3.11+
- ✅ Git
- ✅ Entorno virtual Python
- ✅ Todas las dependencias del proyecto
- ✅ DVC (Data Version Control)
- ✅ Descarga datos con DVC automáticamente
- ✅ Construye e inicia todos los servicios Docker

### 3. `run-airflow-auto.sh` (Mac/Linux)
**Script rápido para ejecutar Airflow (asume que ya tienes Docker instalado)**

- Detecta Docker automáticamente
- Corrige problemas de PATH
- Crea alias para docker-compose si es necesario
- Ejecuta el script start-airflow.sh

### 4. `start-airflow.sh` (Mac/Linux)
**Script original de inicio de Airflow**

### 5. `stop-airflow.sh` (Mac/Linux)
**Detiene todos los servicios de Airflow**

---

## ⚡ Uso Rápido

### En Mac/Linux

#### Primera vez (instalación completa):
```bash
# Dar permisos de ejecución
chmod +x scripts/setup-and-run.sh

# Ejecutar instalación completa
./scripts/setup-and-run.sh
```

#### Ejecuciones posteriores:
```bash
# Opción 1: Script automático (detecta Docker)
./scripts/run-airflow-auto.sh

# Opción 2: Script directo
./scripts/start-airflow.sh
```

### En Windows

#### Primera vez (instalación completa):
```batch
REM Abrir PowerShell como Administrador
REM Navegar a la carpeta del proyecto
cd C:\ruta\al\proyecto

REM Ejecutar instalación completa
scripts\setup-and-run.bat
```

#### Ejecuciones posteriores:
```batch
REM Opción 1: Script completo
scripts\setup-and-run.bat

REM Opción 2: Script directo de Airflow
scripts\start-airflow.bat
```

---

## ✨ Características

### 🔧 Instalación Automática
- **Detecta** qué software falta en tu sistema
- **Instala** automáticamente todas las dependencias
- **Configura** entornos virtuales Python
- **Valida** cada paso antes de continuar

### 📊 Gestión de Datos con DVC
- **Instala DVC** automáticamente si no está disponible
- **Descarga datos** desde Google Cloud Storage
- **Maneja errores** de autenticación y conexión
- **Continúa** sin datos si no están disponibles (no bloquea)
- **Reporta** el estado de los datos descargados

### 🐳 Docker Inteligente
- **Detecta** si Docker está instalado
- **Inicia** Docker Desktop automáticamente
- **Espera** a que Docker esté listo (hasta 3 minutos)
- **Construye** imágenes solo si es necesario
- **Maneja** tanto `docker-compose` como `docker compose`

### 📝 Logging y Feedback
- **Colores** para distinguir mensajes (INFO, OK, ERROR, WARNING)
- **Progreso** detallado de cada paso
- **Errores claros** con sugerencias de solución
- **Resumen final** con URLs y comandos útiles

---

## 📋 Requisitos Previos

### Mínimos (se instalan automáticamente)
- **Sistema Operativo**: macOS 10.15+, Windows 10/11, o Linux (Ubuntu 20.04+)
- **Permisos**: Administrador (para instalar software)
- **Internet**: Conexión estable para descargar paquetes
- **Espacio en disco**: ~10 GB libres (para Docker e imágenes)

### Recomendados
- **RAM**: 8 GB mínimo, 16 GB recomendado
- **CPU**: 4 cores mínimo
- **Ancho de banda**: Bueno para descargar datos con DVC

---

## 🔍 Qué hace cada paso

### Setup Completo (`setup-and-run.sh` / `setup-and-run.bat`)

1. **[1/10] Detectar sistema operativo**
   - Identifica si es macOS, Linux o Windows
   - Ajusta comandos según el sistema

2. **[2/10] Instalar gestor de paquetes**
   - macOS: Homebrew
   - Windows: Chocolatey
   - Linux: apt-get (ya incluido)

3. **[3/10] Instalar Docker Desktop**
   - Descarga e instala Docker
   - Requiere reinicio si es primera instalación

4. **[4/10] Verificar Docker corriendo**
   - Inicia Docker Desktop si no está activo
   - Espera hasta que Docker responda
   - Timeout de 3 minutos máximo

5. **[5/10] Instalar Python 3.11+**
   - Verifica versión instalada
   - Instala si es necesario

6. **[6/10] Instalar Git**
   - Necesario para clonar repos y DVC
   - Verifica versión instalada

7. **[7/10] Crear entorno virtual Python**
   - Aísla dependencias del proyecto
   - Crea carpeta `venv/`

8. **[8/10] Instalar dependencias Python**
   - Lee `requirements.txt`
   - Instala todos los paquetes necesarios
   - Actualiza pip, setuptools, wheel

9. **[9/10] Configurar DVC y descargar datos**
   - ✨ **NUEVO**: Instala DVC automáticamente
   - ✨ **NUEVO**: Verifica credenciales de Google Cloud
   - ✨ **NUEVO**: Descarga datos desde storage remoto
   - ✨ **NUEVO**: Maneja errores sin bloquear el proyecto
   - ✨ **NUEVO**: Reporta cantidad de archivos descargados

10. **[10/10] Iniciar servicios Docker**
    - Crea archivo `.env` con configuración
    - Construye imagen custom de Airflow
    - Inicia todos los contenedores
    - Espera 30 segundos a que estén listos

---

## 🌐 Servicios Disponibles

Después de ejecutar el script, tendrás acceso a:

| Servicio | URL | Credenciales |
|----------|-----|--------------|
| **Airflow UI** | http://localhost:8081 | user: `airflow`, pass: `airflow` |
| **Kedro-Viz** | http://localhost:4141 | - |
| **Jupyter Notebook** | http://localhost:8888 | - |

---

## 🛠️ Solución de Problemas

### ❌ "Docker no está instalado"
**Solución:**
```bash
# Mac
brew install --cask docker

# Windows (PowerShell como Admin)
choco install docker-desktop

# Linux
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

### ❌ "DVC pull failed" o "Authentication error"
**Causas comunes:**
- No tienes credenciales de Google Cloud configuradas
- Los datos no existen en el storage remoto
- No tienes permisos para acceder al bucket

**Solución:**
```bash
# Configurar credenciales de Google Cloud
gcloud auth login
gcloud auth application-default login

# Verificar configuración DVC
dvc remote list
dvc remote default

# Intentar pull manual
dvc pull -v
```

**Nota:** El script continuará aunque DVC falle. Puedes ejecutar `dvc pull` manualmente más tarde.

### ❌ "Permission denied" (Mac/Linux)
**Solución:**
```bash
chmod +x scripts/setup-and-run.sh
chmod +x scripts/run-airflow-auto.sh
chmod +x scripts/start-airflow.sh
```

### ❌ "Docker Desktop no inicia"
**Solución:**
1. Abre Docker Desktop manualmente
2. Espera a que el icono muestre "Running"
3. Ejecuta el script nuevamente

### ❌ "Port already in use" (8080, 8081, etc.)
**Solución:**
```bash
# Ver qué está usando el puerto
lsof -i :8081  # Mac/Linux
netstat -ano | findstr :8081  # Windows

# Detener servicios existentes
docker compose down

# O cambiar puertos en docker-compose.yaml
```

### ❌ "Build failed" durante docker compose
**Solución:**
```bash
# Limpiar imágenes antiguas
docker system prune -a

# Reconstruir desde cero
docker compose build --no-cache

# Ver logs detallados
docker compose up --build
```

### ❌ "No space left on device"
**Solución:**
```bash
# Limpiar Docker
docker system prune -a --volumes

# Liberar espacio en disco
# Mac/Linux: verificar con `df -h`
# Windows: verificar con `Get-PSDrive C`
```

---

## 📚 Comandos Útiles

### Docker
```bash
# Ver servicios corriendo
docker ps

# Ver todos los contenedores
docker ps -a

# Ver logs en tiempo real
docker compose logs -f

# Reiniciar un servicio específico
docker compose restart airflow-scheduler

# Detener todos los servicios
docker compose down

# Detener y eliminar volúmenes
docker compose down -v
```

### DVC
```bash
# Ver estado de archivos
dvc status

# Descargar datos
dvc pull

# Ver configuración de remote
dvc remote list

# Ver logs detallados
dvc pull -v
```

### Python
```bash
# Activar entorno virtual
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate.bat  # Windows

# Instalar paquetes adicionales
pip install nombre-paquete

# Ver paquetes instalados
pip list

# Actualizar requirements.txt
pip freeze > requirements.txt
```

---

## 🤝 Contribuir

Si encuentras problemas o mejoras para estos scripts:

1. Reporta issues en el repositorio
2. Sugiere mejoras en los scripts
3. Comparte tu experiencia de instalación

---

## 📝 Notas Adicionales

### Sobre DVC
- **Primera vez**: Si es tu primera vez usando el proyecto, DVC intentará descargar ~X GB de datos
- **Sin credenciales**: El script NO fallará si no tienes acceso a GCS, simplemente continuará sin datos
- **Configuración manual**: Puedes configurar DVC después con `dvc remote add` y `dvc pull`

### Sobre Docker
- **Recursos**: Docker Desktop necesita al menos 4 GB de RAM asignados
- **Primera construcción**: Puede tomar 10-15 minutos
- **Caché**: Construcciones posteriores son mucho más rápidas

### Sobre los puertos
- Si ya tienes servicios en los puertos 8080, 8081, 4141, o 8888, ajusta `docker-compose.yaml`

---

## 📞 Soporte

Si tienes problemas:

1. Revisa la sección [Solución de Problemas](#solución-de-problemas)
2. Busca en los logs: `docker compose logs -f`
3. Verifica el estado: `docker ps -a`
4. Consulta la documentación del proyecto

---

**¡Listo para desarrollar! 🚀**
