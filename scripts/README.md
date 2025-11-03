# 🚀 Scripts de Producción - ML Análisis Ecosistema Dev

Scripts automatizados para iniciar y detener el entorno de producción dockerizado.

## 📁 Archivos Disponibles

| Archivo | Plataforma | Descripción |
|---------|-----------|-------------|
| `start_production.bat` | Windows | Inicia todos los servicios |
| `stop_production.bat` | Windows | Detiene todos los servicios |
| `start_production.sh` | Linux/Mac | Inicia todos los servicios |
| `run_project.sh` | Linux/Mac | Script original del proyecto |

---

## 🪟 Uso en Windows

### Iniciar Servicios

```cmd
# Opción 1: Doble clic en el archivo
start_production.bat

# Opción 2: Desde CMD
cd scripts
start_production.bat
```

### Detener Servicios

```cmd
stop_production.bat
```

---

## 🐧 Uso en Linux/Mac

### Dar permisos de ejecución (solo la primera vez)

```bash
chmod +x start_production.sh
chmod +x stop_production.bat
```

### Iniciar Servicios

```bash
./scripts/start_production.sh
```

### Detener Servicios

```bash
docker-compose down
```

---

## 🎯 Servicios Incluidos

El script inicia los siguientes servicios:

| Servicio | Puerto | Descripción |
|----------|--------|-------------|
| **Airflow Webserver** | 8080 | Interfaz web de Airflow |
| **Airflow Scheduler** | - | Programador de tareas |
| **Airflow Worker** | - | Ejecutor de tareas |
| **Kedro Viz** | 4141 | Visualización de pipelines |
| **PostgreSQL** | 5432 | Base de datos |
| **Redis** | 6379 | Message broker |
| **Flower** | 5555 | Monitor de Celery |

---

## 🔐 Credenciales por Defecto

### Airflow Web UI
- **URL:** http://localhost:8080
- **Usuario:** `airflow`
- **Contraseña:** `airflow`

### PostgreSQL
- **Host:** `localhost`
- **Puerto:** `5432`
- **Usuario:** `airflow`
- **Contraseña:** `airflow`
- **Base de datos:** `airflow`

---

## 📊 Acceso a Servicios

Después de iniciar los servicios, accede a:

- 🌐 **Airflow UI:** http://localhost:8080
- 📈 **Kedro Viz:** http://localhost:4141
- 🌺 **Flower (Monitor):** http://localhost:5555

---

## 💡 Comandos Útiles

### Ver logs en tiempo real

```bash
# Todos los servicios
docker-compose logs -f

# Solo Kedro Viz
docker-compose logs -f kedro-viz

# Solo Airflow Webserver
docker-compose logs -f airflow-webserver
```

### Ejecutar pipeline Kedro manualmente

```bash
# Desde Docker
docker-compose exec kedro-viz kedro run

# Pipeline específico
docker-compose exec kedro-viz kedro run --pipeline=regresion
```

### Verificar estado de servicios

```bash
docker-compose ps
```

### Reiniciar un servicio específico

```bash
docker-compose restart kedro-viz
```

---

## 🛠️ Solución de Problemas

### Docker no está corriendo

```
❌ Error: Docker no está corriendo
```

**Solución:** Inicia Docker Desktop antes de ejecutar el script.

---

### Puerto ya en uso

```
Error: port is already allocated
```

**Solución:** Detén otros servicios que usen los mismos puertos:

```bash
# Detener todo
docker-compose down

# Verificar puertos en uso (Windows)
netstat -ano | findstr "8080"
netstat -ano | findstr "4141"

# Verificar puertos en uso (Linux/Mac)
lsof -i :8080
lsof -i :4141
```

---

### Servicios no inician correctamente

**Solución:** Reconstruir imágenes desde cero:

```bash
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

---

## 📝 Notas Importantes

1. **Primera ejecución:** La primera vez puede tardar 5-10 minutos en construir las imágenes.

2. **Reinicio de servicios:** Si modificas el código, reinicia los servicios:
   ```bash
   docker-compose restart kedro-viz
   ```

3. **Persistencia de datos:** Los datos se guardan en volúmenes Docker y persisten entre reinicios.

4. **Limpieza completa:** Para eliminar TODO (incluyendo datos):
   ```bash
   docker-compose down -v
   ```

---

## 🎓 Para la Defensa Académica

Estos scripts demuestran:

- ✅ **Automatización completa** del despliegue
- ✅ **Reproducibilidad** en cualquier máquina con Docker
- ✅ **Buenas prácticas DevOps**
- ✅ **Documentación clara** para replicabilidad científica
- ✅ **Portabilidad** entre Windows, Linux y Mac

---

## 📞 Soporte

Si encuentras problemas, revisa:

1. Los logs: `docker-compose logs -f`
2. El estado: `docker-compose ps`
3. La documentación de Docker Compose: https://docs.docker.com/compose/
