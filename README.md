# Proyecto Final - Minería de Datos

## Tema: Caracterización de Microclimas y Predicción de Precipitación en Zonas Urbanas Utilizando Algoritmos de Minería de Datos

### Integrante del Proyecto
- Daniel Mejia Suaza

### Descripción del Proyecto
Este proyecto se enfoca en la caracterización de microclimas urbanos en la ciudad de Manizales y la predicción de precipitación utilizando técnicas avanzadas de minería de datos. Los microclimas urbanos se caracterizan por variaciones climáticas significativas en distancias cortas debido a la topografía y desarrollo urbano de las ciudades.

El sistema implementa un **pipeline completo de minería de datos** que incluye:
1. **Preprocesamiento y Limpieza de Datos**
2. **Análisis Exploratorio de Datos (EDA)**
3. **Caracterización de Microclimas (Clustering)**
4. **Predicción de Precipitación (Machine Learning)**

### Estructura del Proyecto
```
mineriaDT/
├── app.py                           # Aplicación web Flask principal
├── excel_reader.py                  # Funciones para leer archivos Excel y CSV
├── data_preprocessing.py           # Módulo de preprocesamiento y EDA
├── microclimate_clustering.py      # Módulo de clustering para microclimas
├── precipitation_prediction.py     # Módulo de predicción de precipitación
├── templates/                      # Plantillas HTML para la interfaz web
│   ├── index.html                  # Página principal
│   ├── results.html               # Resultados de validación
│   └── mining_results.html       # Resultados completos de minería
├── uploads/                       # Directorio para archivos subidos
└── README.md                     # Este archivo
```

### Requisitos del Sistema
- Python 3.7+
- Librerías requeridas:
  - Flask
  - pandas
  - openpyxl
  - scikit-learn
  - matplotlib
  - seaborn
  - scipy

### Formatos de Archivo Soportados
- ✅ **Archivos Excel**: .xlsx y .xls
- ✅ **Archivos CSV**: .csv (con codificación UTF-8 o Latin1)
- ✅ **Carpetas completas**: Procesamiento automático de directorios

### Instalación y Configuración
1. Instalar las dependencias:
   ```bash
   pip install flask pandas openpyxl scikit-learn matplotlib seaborn scipy
   ```

2. Ejecutar la aplicación web:
   ```bash
   python app.py
   ```

3. Abrir el navegador web en `http://127.0.0.1:5000/`

### Configuración de Rendimiento
- **Límite de carga**: 20 GB para archivos/carpetas masivas (hasta 14M+ registros)
- **Memoria RAM**: Recomendado mínimo 32 GB para datasets de 14M registros
- **Procesamiento**: Optimizado para datasets de hasta 14,000,000 registros
- **Tiempo estimado**: 3-15 minutos dependiendo del tamaño del dataset

### Uso de la Aplicación Web

#### Análisis Completo de Minería de Datos
1. **Seleccionar método de entrada:**
   - **Archivos Individuales**: Seleccionar uno o múltiples archivos Excel (.xlsx, .xls) o CSV (.csv)
   - **Carpeta Completa**: Seleccionar una carpeta que contenga archivos Excel y CSV (procesa automáticamente todos los .xlsx, .xls y .csv)
2. Hacer clic en **"Iniciar Análisis Completo de Minería de Datos"**
3. El sistema ejecuta automáticamente todo el pipeline completo:

   **🔄 Fase 1: Preprocesamiento**
   - Análisis de datos faltantes
   - Limpieza y estandarización de nombres de columnas
   - Imputación de valores faltantes
   - Detección y manejo de outliers
   - Normalización de datos
   - Análisis Exploratorio de Datos (EDA)

   **🔄 Fase 2: Caracterización de Microclimas**
   - Determinación del número óptimo de clusters
   - Aplicación de algoritmos de clustering (K-Means)
   - Análisis de características de cada microclima
   - Visualización de clusters

   **🔄 Fase 3: Predicción de Precipitación**
   - Entrenamiento de múltiples modelos de ML
   - Evaluación comparativa de rendimiento
   - Optimización del mejor modelo
   - Predicciones diferenciadas por microclima

### Resultados Obtenidos

#### Dashboard Ejecutivo
- **Métricas consolidadas**: Archivos procesados, válidos, tasa de éxito
- **Resumen por fases**: Estadísticas de cada etapa del proceso
- **Insights clave**: Principales hallazgos del análisis

#### Reportes Detallados
- **Preprocesamiento**: Estadísticas de calidad de datos, distribuciones, correlaciones
- **Microclimas**: Número óptimo de clusters, características de cada zona climática
- **Predicción**: Comparación de modelos, importancia de variables, métricas de rendimiento

#### Visualizaciones
- Histogramas de distribución de variables
- Matrices de correlación
- Visualización de clusters en 2D (PCA)
- Gráficos de método del codo
- Comparación de rendimiento de modelos
- Importancia de características

### Características Especiales - Sistema Avanzado

#### 🏢 Interfaz Corporativa
- Diseño administrativo profesional con paleta empresarial
- Navegación por pestañas para diferentes fases del análisis
- Dashboard ejecutivo con métricas clave
- Funcionalidad de impresión de reportes

#### 🔄 Pipeline Automatizado
- **Preprocesamiento inteligente**: Detección automática de tipos de datos y estrategias de imputación
- **Clustering adaptativo**: Determinación automática del número óptimo de clusters
- **Modelado comparativo**: Evaluación automática de múltiples algoritmos de ML

#### 📊 Análisis Avanzado
- **EDA completo**: Estadísticas descriptivas, análisis de normalidad, correlaciones
- **Clustering robusto**: Múltiples algoritmos con validación de calidad
- **Predicción precisa**: Optimización de hiperparámetros y validación cruzada

#### 🎯 Caracterización de Microclimas
- Identificación automática de zonas climáticas homogéneas
- Análisis de características distintivas de cada microclima
- Predicciones específicas por zona climática

#### 📈 Predicción de Precipitación
- **7 algoritmos evaluados**: Regresión Lineal, Ridge, Lasso, Random Forest, Gradient Boosting, SVR, Red Neuronal
- **Métricas completas**: MAE, MSE, RMSE, R², validación cruzada
- **Importancia de variables**: Análisis de características más relevantes para la predicción

### Variables Esperadas en los Datos
**Variables meteorológicas:**
- estacion_sk: Identificador de la estación
- humedad: Nivel de humedad
- precipitacion: Cantidad de precipitación
- radiacion_solar: Radiación solar
- temperatura: Temperatura

**Variables de estado de estación:**
- estado
- alarma
- puerta_Abierta
- bateria_Baja
- solar_energia
- sensor_Activo
- observaciones

### Funcionalidades Implementadas
- ✅ Lectura de archivos Excel y CSV por nombre
- ✅ Validación inicial de datos meteorológicos
- ✅ **Validación masiva de múltiples archivos Excel/CSV** (selección múltiple)
- ✅ **Procesamiento de carpetas completas** (selección automática de archivos Excel/CSV)
- ✅ Interfaz web para carga y validación de archivos
- ✅ Información del proyecto y integrante
- ✅ Estadísticas básicas y detección de valores faltantes
- ✅ Verificación de columnas esperadas
- ✅ **Interfaz administrativa profesional** (diseño corporativo)
- ✅ Reporte consolidado con tasa de éxito de validación
- ✅ **Pipeline completo de minería de datos automatizado**
- ✅ **Preprocesamiento inteligente**: Limpieza, imputación, normalización
- ✅ **Análisis Exploratorio de Datos (EDA)**: Estadísticas, correlaciones, visualizaciones
- ✅ **Caracterización de microclimas**: Clustering automático con K-Means
- ✅ **Predicción de precipitación**: 7 algoritmos ML con optimización
- ✅ **Dashboard ejecutivo**: Métricas consolidadas y reportes detallados
- ✅ **Sistema de pestañas**: Navegación organizada por fases del análisis

### Estado del Proyecto: ✅ COMPLETADO
El sistema implementa completamente todos los módulos requeridos por el proyecto:
1. ✅ **Preprocesamiento y Exploración de Datos (EDA)** - Implementado con análisis completo
2. ✅ **Caracterización de Microclimas (Clustering)** - K-Means automático con evaluación
3. ✅ **Predicción de Precipitación (Machine Learning)** - Múltiples modelos optimizados
4. ✅ **Validación y Evaluación de Modelos** - Métricas completas y comparaciones

### Contacto
Daniel Mejia Suaza - Estudiante del proyecto de Minería de Datos
# mineria_de_datos_proyecto
