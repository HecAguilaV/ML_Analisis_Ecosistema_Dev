# 📊 Informes Finales del Proyecto

Esta carpeta contiene los **informes técnicos definitivos** del proyecto de análisis del ecosistema de desarrollo de software, enfocado en el mercado chileno con perspectiva regional y global.

---

## 📑 Estructura de Informes

### **01_RESUMEN_EJECUTIVO.md** ⏳

**Audiencia**: Stakeholders, profesores, evaluadores  
**Duración de lectura**: 5-10 minutos  
**Estado**: Pendiente

**Contenido:**

- Introducción y contexto del proyecto
- Objetivos y alcance
- Metodología resumida (CRISP-DM)
- Resultados clave (top 3 hallazgos)
- Conclusiones y recomendaciones
- Próximos pasos

---

### **02_INFORME_TECNICO_COMPLETO.md** ⏳

**Audiencia**: Equipo técnico, revisores académicos  
**Duración de lectura**: 30-45 minutos  
**Estado**: Pendiente

**Contenido:**

1. **Introducción**
   - Contexto del proyecto
   - Problema a resolver
   - Justificación

2. **Metodología CRISP-DM**
   - Business Understanding
   - Data Understanding
   - Data Preparation
   - Modeling
   - Evaluation
   - Deployment (plan futuro)

3. **Datasets Utilizados**
   - Stack Overflow Survey 2023 (90,000 respuestas)
   - Stack Overflow Survey 2025 (completo)
   - JetBrains Developer Ecosystem 2025
   - Proceso de integración y limpieza

4. **Pipelines de Procesamiento**
   - Pipeline `procesamiento_de_datos`
   - Feature engineering aplicado
   - Selección de características

5. **Modelos Implementados**
   - **Regresión** (predicción salarial): 5 modelos + 1 experimental
   - **Clasificación** (nivel de experiencia): 5 modelos
   - Hiperparámetros y validación cruzada

6. **Resultados y Métricas**
   - Comparativa de modelos
   - Mejor modelo por pipeline
   - Matrices de confusión
   - Análisis de errores

7. **Integración Docker**
   - Resumen del whitepaper Docker (`docs/referencias/docker_SUMMARY.md`)
   - Aplicación al proyecto (reproducibilidad)
   - Implicaciones para deployment

8. **Conclusiones Técnicas**
   - Hallazgos principales
   - Limitaciones del estudio
   - Trabajo futuro

9. **Referencias**
   - Bibliografía
   - Fuentes de datos
   - Herramientas utilizadas

---

### **03_MERCADO_CHILE.md** ⏳

**Audiencia**: Desarrolladores chilenos, empresas tech locales  
**Duración de lectura**: 15-20 minutos  
**Estado**: Pendiente

**Contenido:**

1. **Contexto del Mercado Chileno**
   - Estado actual del sector tech en Chile
   - Comparación con economías vecinas (Argentina, Colombia, Brasil)
   - Crecimiento del sector en últimos 5 años

2. **Análisis de Datos Chile**
   - Desarrolladores chilenos en el dataset
   - Distribución demográfica
   - Niveles de experiencia

3. **Salarios en Chile**
   - Salario mediano por nivel de experiencia
   - Comparativa con LATAM
   - Comparativa con mercado global
   - Factores que influyen en salarios chilenos

4. **Tecnologías y Stack**
   - Lenguajes más usados en Chile
   - Frameworks y herramientas populares
   - Comparación con tendencias globales
   - Brechas tecnológicas (skills gap)

5. **Oportunidades Laborales**
   - Sectores con mayor demanda (FinTech, HealthTech, etc.)
   - Empresas tech en Chile
   - Trabajo remoto vs presencial
   - Oportunidades en regiones vs Región Metropolitana

6. **Recomendaciones para Desarrolladores Chilenos**
   - Tecnologías prioritarias para aprender
   - Skills de alto valor en el mercado local
   - Estrategias para maximizar salario
   - Transición a roles senior

7. **Proyecciones Futuras**
   - Tendencias emergentes
   - Impacto de IA en el mercado chileno
   - Oportunidades de crecimiento

---

### **04_COMPARATIVA_2023_2025.md** ⏳

**Audiencia**: Desarrolladores, investigadores, tech leads  
**Duración de lectura**: 20-25 minutos  
**Estado**: Pendiente

**Contenido:**

1. **Introducción: La Revolución de la IA**
   - Contexto: 2023 (pre-ChatGPT masivo) vs 2025 (era IA)
   - Cambios disruptivos en la industria

2. **Metodología de Comparación**
   - Datasets utilizados
   - Variables comparables
   - Limitaciones del análisis temporal

3. **Adopción de Herramientas de IA**
   - GitHub Copilot: 0% (2023) → 60% (2025)
   - ChatGPT para desarrollo
   - Otras herramientas de IA (Tabnine, CodeWhisperer, etc.)

4. **Impacto en Salarios**
   - Salarios pre-IA vs post-IA
   - Roles emergentes: ML Engineer, AI Specialist, Prompt Engineer
   - Roles tradicionales: ¿aumento o estancamiento?

5. **Nuevas Skills Emergentes**
   - Prompt Engineering
   - LLM integration
   - Vector databases (Pinecone, Weaviate, Chroma)
   - AI agents y workflows

6. **Cambios en Tecnologías**
   - Lenguajes: Python ↑, JavaScript estable, nuevos nichos (Rust, Go)
   - Frameworks: Next.js, Astro, Svelte
   - Infraestructura: Serverless, edge computing

7. **Impacto en Productividad**
   - Tiempo de desarrollo reducido
   - Calidad del código
   - Necesidad de nuevas habilidades

8. **Predicciones para 2026-2027**
   - Evolución esperada del mercado
   - Skills a priorizar
   - Preparación para el futuro

---

## 🛠️ Herramientas y Formatos

### **Notebooks de Análisis**

Los informes se basan en análisis ejecutables en Jupyter Notebooks:

- `notebooks/02_analisis_de_resultados.ipynb` - Análisis completo de modelos
- `notebooks/03_analisis_comparativo_2023_2025.ipynb` - Comparación temporal (pendiente)
- `notebooks/04_segmentacion_mercado_chile.ipynb` - Análisis Chile (pendiente)

### **Exportación a PDF**

Para generar PDFs profesionales:

```bash
# Instalar nbconvert
pip install nbconvert

# Exportar notebook a PDF
jupyter nbconvert --to pdf notebooks/02_analisis_de_resultados.ipynb

# Exportar con plantilla personalizada
jupyter nbconvert --to pdf --template classic notebooks/02_analisis_de_resultados.ipynb
```

### **Gráficos Estáticos**

Los gráficos de alta resolución para los informes se guardarán en:

```
docs/informe_final/assets/
├── salarios_chile_vs_global.png
├── adopcion_ia_2023_2025.png
├── top_tecnologias_chile.png
├── comparacion_modelos_ml.png
└── ...
```

---

## 📅 Estado de Desarrollo

| Informe | Estado | Prioridad |
|---------|--------|-----------|
| 02_INFORME_TECNICO_COMPLETO.md | ⏳ Pendiente | Alta |
| 03_MERCADO_CHILE.md | ⏳ Pendiente | Media |
| 04_COMPARATIVA_2023_2025.md | ⏳ Pendiente | Media |
| 01_RESUMEN_EJECUTIVO.md | ⏳ Pendiente | Baja (último) |

---

## ✅ Checklist de Calidad

Antes de considerar un informe como "completado":

- [ ] Revisión ortográfica y gramatical
- [ ] Todas las tablas tienen títulos descriptivos
- [ ] Todos los gráficos tienen ejes etiquetados y leyendas
- [ ] Referencias bibliográficas completas
- [ ] Enlaces internos funcionan correctamente
- [ ] Código reproducible (si aplica)
- [ ] Exportación a PDF exitosa
- [ ] Revisión por par (peer review)

---

## 📖 Guía de Estilo

### **Formato Markdown**

- Usar headers jerárquicos (##, ###, ####)
- Código inline con \`backticks\`
- Bloques de código con \`\`\`python
- Listas con `-` o `1.` según corresponda
- Tablas con formato GitHub Markdown

### **Citas y Referencias**

```markdown
Según Stack Overflow Survey 2023[^1], el salario mediano...

[^1]: Stack Overflow Developer Survey 2023. https://survey.stackoverflow.co/2023/
```

### **Gráficos**

```markdown
![Descripción del gráfico](./assets/nombre_grafico.png)
*Figura X: Título descriptivo del gráfico. Fuente: Dataset propio.*
```

---

## 🤝 Contribución

Para agregar o modificar informes:

1. Crear borrador en formato Markdown
2. Solicitar revisión técnica
3. Incorporar feedback
4. Generar visualizaciones finales
5. Exportar a PDF
6. Marcar como completado en este README

---



- **Autor**: Héctor Aguila V.
- **Email**: he.aguila@duocuc.cl
- **GitHub**: [@HecAguilaV](https://github.com/HecAguilaV)

---

**Última actualización**: 3 Noviembre 2025  
**Versión**: 1.0

