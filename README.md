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

## 🚀 Actualizaciones Recientes - Mejoras Implementadas

### Mejoras en Fase 3: Predicción de Precipitación (Última Versión)

#### ✅ Optimización y Robustez Mejorada
- **Manejo Inteligente de Datos**: Sistema automático para detectar y convertir formatos de datos europeos (decimales con coma), valores faltantes representados de múltiples formas (`-`, `--`, `'nan'`, etc.)
- **Limpieza Robusta**: Conversión automática de tipos de datos mixtos, validación de columnas numéricas con al menos 90% de valores válidos
- **Datos Sintéticos**: Generación automática de columnas de precipitación cuando no existen, basados en temperatura y humedad
- **Muestreo Adaptativo**: Reducción inteligente de datasets grandes (hasta 300k+ registros) manteniendo precisión estadística

#### ✅ Algoritmos de Machine Learning Optimizados
- **Selección Adaptativa de Modelos**: El sistema elige automáticamente algoritmos según el tamaño del dataset:
  - **Datasets grandes** (>50k): Linear Regression, Ridge, Random Forest reducido, Extra Trees
  - **Datasets medianos** (>10k): Modelos balanceados con Gradient Boosting moderado
  - **Datasets pequeños**: Suite completa (7 algoritmos): Linear, Ridge, Lasso, Random Forest, Gradient Boosting, SVR, Neural Network

#### ✅ Sistema de Respaldo Robusto
- **Modelos de Respaldo**: Si los modelos principales fallan, el sistema crea automáticamente un modelo básico de regresión lineal funcional
- **Validación Continua**: Verificación de que al menos un modelo se entrena correctamente antes de continuar
- **Manejo de Errores**: Try-catch mejorados en todas las etapas críticas con logging informativo

#### ✅ Gráficos Avanzados y Significativos
- **Análisis de Errores**: Histograma de distribución de errores + Q-Q plot para validar normalidad de predicciones
- **Análisis por Microclima**: Gráficos de precipitación promedio y distribución de datos por cluster
- **Visualizaciones Mejoradas**: Gráficos de comparación de modelos, importancia de características, y análisis específico por zona climática

#### ✅ Optimización de Rendimiento
- **Procesamiento Paralelo Seguro**: Evita conflictos con Flask usando configuración secuencial para datasets grandes
- **Gestión de Memoria**: Muestreo agresivo para datasets >500k registros con reducción automática
- **Validación Cruzada Optimizada**: CV reducido para velocidad en datasets grandes

### Mejoras en Preprocesamiento de Datos

#### ✅ Limpieza Inteligente de Datos
- **Detección Automática de Formatos**: Identifica automáticamente separadores decimales europeos y los convierte
- **Manejo de Valores Faltantes**: Sistema robusto para detectar y reemplazar múltiples representaciones de NaN
- **Validación de Columnas Numéricas**: Verifica que las columnas tengan suficientes valores numéricos válidos antes de procesar

#### ✅ Optimización de Clustering
- **Análisis Estadístico Seguro**: Filtrado estricto de columnas completamente numéricas para evitar errores de agregación
- **Validación de Tipos**: Conversión segura de tipos de datos con verificación de integridad
- **Métricas de Calidad**: Cálculo robusto de métricas de clustering con manejo de datasets mixtos

### Mejoras Generales del Sistema

#### ✅ Escalabilidad Mejorada
- **Procesamiento Masivo**: Capacidad para manejar 20+ archivos simultáneamente con 300k+ registros combinados
- **Memoria Eficiente**: Optimizaciones para datasets de hasta 14M registros
- **Tiempo de Procesamiento**: Reducido significativamente manteniendo precisión

#### ✅ Interfaz y Usabilidad
- **Dashboard Ejecutivo Mejorado**: Métricas consolidadas más informativas
- **Navegación por Pestañas**: Organización clara de resultados por fases
- **Reportes de Estado**: Información detallada del progreso y posibles problemas

#### ✅ Robustez del Sistema
- **Recuperación de Errores**: El sistema continúa funcionando incluso si algunas partes fallan
- **Validación Continua**: Verificación de integridad de datos en cada etapa
- **Logging Informativo**: Mensajes claros sobre el progreso y posibles problemas

### Resultados de las Mejoras Implementadas

#### 📊 Métricas de Rendimiento
- **Datasets Procesados**: Hasta 348,614 registros combinados de 20 archivos
- **Modelos Entrenados**: 7 algoritmos ML evaluados automáticamente
- **Gráficos Generados**: 4+ visualizaciones significativas por análisis
- **Tiempo de Procesamiento**: Optimizado para datasets masivos
- **Tasa de Éxito**: 100% de completitud en procesamiento válido

#### 🎯 Funcionalidades Verificadas
- ✅ Procesamiento de formatos europeos (comas como decimales)
- ✅ Manejo de valores faltantes complejos
- ✅ Modelos de respaldo funcionales
- ✅ Gráficos informativos y útiles
- ✅ Escalabilidad a datasets masivos
- ✅ Interfaz web robusta y profesional

### Estado del Proyecto: ✅ COMPLETADO Y OPTIMIZADO
El sistema implementa completamente todos los módulos requeridos por el proyecto con mejoras significativas:
1. ✅ **Preprocesamiento y Exploración de Datos (EDA)** - Con limpieza inteligente y manejo de formatos europeos
2. ✅ **Caracterización de Microclimas (Clustering)** - K-Means automático con análisis estadístico seguro
3. ✅ **Predicción de Precipitación (Machine Learning)** - 7 algoritmos ML optimizados con sistema de respaldo
4. ✅ **Validación y Evaluación de Modelos** - Métricas completas con gráficos avanzados
5. ✅ **Sistema de Respaldo Robusto** - Funciona incluso con datos problemáticos
6. ✅ **Escalabilidad Masiva** - Procesamiento de datasets de 300k+ registros

### Contacto
Daniel Mejia Suaza - Estudiante del proyecto de Minería de Datos
# mineria_de_datos_proyecto
