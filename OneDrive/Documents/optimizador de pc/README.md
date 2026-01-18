# Optimizador de PC

Este proyecto es una herramienta de optimización para PC desarrollada en Python. Utiliza técnicas de análisis de datos para mejorar el rendimiento del sistema.

## Características

### Optimizaciones Básicas
- Obtención de información del sistema (CPU, memoria, disco)
- Limpieza de archivos temporales
- Vaciado de la papelera de reciclaje
- Lista de programas de inicio

### Optimizaciones Avanzadas
- Desfragmentación de disco duro
- Limpieza de archivos prefetch
- Limpieza de cache de navegadores (Chrome, Firefox)
- Limpieza de archivos temporales de Windows Update
- Cálculo estimado de espacio liberado

## Requisitos

- Python 3.x
- Bibliotecas: psutil, shutil (incluida en Python)

Instalar dependencias:
```
pip install -r requirements.txt
```

## Uso

Ejecuta el proyecto:
```
python main.py
```
Esto iniciará automáticamente la interfaz web y abrirá tu navegador en http://127.0.0.1:5000/

## Dashboard de Monitoreo en Tiempo Real
Accede al dashboard para ver estadísticas en tiempo real del sistema:
- **CPU**: Uso porcentual y frecuencia
- **Memoria RAM**: Uso y capacidad total
- **Disco Duro**: Espacio usado y disponible
- **Red**: Datos enviados y recibidos
- **Procesos**: Número de procesos activos
- **Información del sistema**: Uptime, versión del SO, etc.

## 🤖 Asistente IA OptiBot
El dashboard incluye un asistente inteligente que:
- **Analiza automáticamente** el rendimiento de tu sistema
- **Genera recomendaciones** personalizadas basadas en estadísticas
- **Responde preguntas** sobre optimización y componentes de PC
- **Explica estadísticas** en tiempo real
- **Proporciona consejos** preventivos de mantenimiento

Pregúntale sobre CPU, memoria, disco, red, procesos, o cualquier aspecto de tu PC.

Si prefieres ejecutar solo la versión web sin auto-abrir navegador:
```
python app.py
```

Para la versión de consola (sin interfaz gráfica):
Crea un script separado o modifica el código según necesites.

## Contribución

Este proyecto está relacionado con minería de datos para analizar el impacto de las optimizaciones en el rendimiento del sistema.

## Autor

Esteban López