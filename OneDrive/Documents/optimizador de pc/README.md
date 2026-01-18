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

## 🎨 Dashboard Moderno con Bootstrap

### **Interfaz Profesional y Responsiva**
El dashboard cuenta con un diseño moderno construido con **Bootstrap 5**, ofreciendo:

#### **Navegación Lateral**
- **Sidebar colapsable** con menú intuitivo
- **Indicadores en tiempo real** del estado del sistema
- **Navegación fluida** entre secciones

#### **Layout de Tarjetas**
- **4 tarjetas principales** para métricas clave (CPU, RAM, Disco, Procesos)
- **Colores temáticos** (Azul, Verde, Amarillo, Rojo)
- **Iconos Bootstrap** para mejor visualización
- **Animaciones de carga** y transiciones suaves

#### **Gráficos Interactivos**
- **Gráfico principal de CPU** con historial de 20 puntos
- **Gráficos circulares** para memoria y disco
- **Gráfico de red** con datos enviados/recibidos
- **Actualización automática** cada 2 segundos

#### **Información del Sistema**
- **Panel completo** con uptime, versiones y estado
- **Indicadores visuales** con badges de colores
- **Información contextual** del sistema operativo

### **📱 Diseño Responsivo**
- **Desktop**: Layout completo con sidebar expandido
- **Tablet**: Sidebar colapsable, grid adaptativo
- **Móvil**: Sidebar oculto, navegación móvil, tarjetas apiladas
- **Puntos de quiebre** inteligentes para diferentes tamaños

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

## 🎨 Características Avanzadas del Chat

### **📱 Interfaz Móvil y Arrastrable**
- **Arrastrar como WhatsApp:** Mueve el chat arrastrando desde el título
- **Responsive:** Se adapta perfectamente a móviles y tablets
- **Posicionamiento flotante:** Se mantiene fijo en la pantalla

### **😊 Barra de Emojis Interactiva**
- **8 emojis principales:** 😊 👍 ❤️ 😂 😮 🙏 🔧 💻
- **Inserción automática:** Haz clic para agregar al mensaje
- **Expresividad:** Mejora la comunicación natural

### **⚡ Experiencia de Chat Fluida**
- **Indicadores de escritura:** "OptiBot está escribiendo..." con animación
- **Timestamps en tiempo real:** Cada mensaje con hora exacta
- **Historial inteligente:** Mantiene los últimos 15 mensajes
- **Auto-scroll:** Se desplaza automáticamente a mensajes nuevos
- **Estados visuales:** Feedback visual durante envío y recepción

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