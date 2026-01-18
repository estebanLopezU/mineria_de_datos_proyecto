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

## 🤖 Asistente IA OptiBot - Tu ChatGPT Personal
El dashboard incluye un asistente inteligente conversacional que:

### **Sobre tu PC:**
- **Análisis automático** del rendimiento del sistema en tiempo real
- **Recomendaciones personalizadas** basadas en estadísticas actuales
- **Diagnóstico inteligente** de problemas de rendimiento
- **Explicaciones detalladas** de componentes y funcionamiento
- **Planes de optimización** adaptados a tu situación

### **Conversación General:**
- **Cálculos matemáticos** (sumas, restas, multiplicaciones, divisiones)
- **Información técnica** sobre computación y tecnología
- **Explicaciones educativas** sobre conceptos complejos
- **Consejos prácticos** sobre diversos temas
- **Información general** (hora, fecha, consejos sobre clima)

### **Ejemplos de Preguntas:**
**Sobre optimización:**
• "¿Cómo está mi CPU?"
• "¿Qué optimizaciones recomiendas?"
• "¿Por qué mi PC está lenta?"
• "¿Cuánta memoria estoy usando?"

**Conversación general:**
• "¿Cuánto es 15 + 27?" (cálculos matemáticos)
• "¿Qué es la inteligencia artificial?" (explicaciones técnicas)
• "¿Qué hora es?" (información general)
• "¿Cómo funciona una computadora?" (explicaciones educativas)

**Preguntas abiertas:**
• "Hola" → Saludo personalizado con estado del sistema
• "¿Qué puedes hacer?" → Lista completa de capacidades
• "Gracias" → Respuesta amable y oferta de más ayuda

OptiBot combina el conocimiento especializado en optimización de PC con la capacidad de mantener conversaciones naturales sobre cualquier tema, ¡como un ChatGPT especializado en tu sistema!

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