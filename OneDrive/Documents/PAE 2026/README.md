# Sistema de Interoperabilidad en Sector Público Colombiano

## 🏛️ PAE 2026 - Minería de Datos

Sistema científico para el análisis y monitoreo de interoperabilidad en el sector público colombiano, basado en el modelo MinTIC y plataformas X-Road/SCD.

## 📋 Tabla de Contenidos

- [Resumen Ejecutivo](#resumen-ejecutivo)
- [Arquitectura del Sistema](#arquitectura-del-sistema)
- [Estructura de Directorios](#estructura-de-directorios)
- [Instalación](#instalación)
- [Uso](#uso)
- [Documentación](#documentación)
- [Contribución](#contribución)
- [Licencia](#licencia)

## 📊 Resumen Ejecutivo

### 🎯 Objetivo
Desarrollar un **Sistema de Monitoreo y Análisis de Interoperabilidad** para el sector público colombiano que permita:

- **Diagnosticar** el estado actual de interoperabilidad entre entidades gubernamentales
- **Monitorear** en tiempo real la conectividad a plataformas X-Road y SCD
- **Generar** reportes científicos de madurez según el modelo MinTIC
- **Proponer** estrategias de mejora basadas en análisis estadístico avanzado

### 📈 Resultados Clave

#### **Entidades Analizadas:**
- **8 entidades gubernamentales** clave del sector público
- **7 sectores** diferentes (Salud, Educación, Hacienda, Transporte, Tecnología, Justicia, Social)

#### **Estado Actual de Conectividad:**
- **Conectividad X-Road:** 0% (0/8 entidades)
- **Conectividad SCD:** 0% (0/8 entidades)
- **Nivel de Madurez Promedio:** 2.00/5 (Nivel Básico)

#### **Impacto Potencial:**
- **Eficiencia Gubernamental:** 40-60% en trámites
- **Transparencia:** 100% de procesos trazables
- **Satisfacción Ciudadana:** >85% de satisfacción proyectada
- **Reducción Costos:** >30% en operaciones

## 🏗️ Arquitectura del Sistema

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   X-Road Node   │    │     SCD API     │    │  APIs Gov Data  │
│   (Puerto 8080) │    │   (Puerto 8081) │    │                 │
└─────────┬───────┘    └─────────┬───────┘    └─────────┬───────┘
          │                      │                      │
          └──────────────────────┼──────────────────────┘
                                 │
                    ┌─────────────▼─────────────┐
                    │   Integración Middleware  │
                    │                           │
                    │  - XRoadIntegration       │
                    │  - SCDIntegration         │
                    │  - APIConnection          │
                    └─────────────┬─────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │     Dashboard Streamlit   │
                    │                           │
                    │  - Visualizaciones        │
                    │  - Métricas en tiempo real│
                    │  - Reportes PDF           │
                    └─────────────┬─────────────┘
                                  │
                    ┌─────────────▼─────────────┐
                    │     Base de Datos         │
                    │                           │
                    │  - entidades_reales.csv   │
                    │  - xroad_reales.csv       │
                    │  - madurez_real.json      │
                    └───────────────────────────┘
```

## 📁 Estructura de Directorios

```
PAE 2026/
├── src/                          # Código fuente principal
│   ├── __init__.py              # Inicialización del paquete
│   ├── api/                     # Endpoints y APIs
│   │   └── __init__.py
│   ├── integration/             # Integración con APIs externas
│   │   └── __init__.py
│   ├── models/                  # Modelos de datos y análisis
│   │   └── __init__.py
│   ├── utils/                   # Utilidades y funciones auxiliares
│   │   └── __init__.py
│   └── config/                  # Configuración del sistema
│       └── __init__.py
├── data/                        # Datos del proyecto
│   ├── raw/                     # Datos crudos
│   ├── processed/               # Datos procesados
│   └── external/                # Datos externos
├── docs/                        # Documentación
│   ├── technical/               # Documentación técnica
│   └── reports/                 # Reportes generados
├── tests/                       # Pruebas del sistema
│   ├── unit/                    # Pruebas unitarias
│   └── integration/             # Pruebas de integración
├── scripts/                     # Scripts de utilidad
│   ├── setup/                   # Scripts de configuración
│   └── deployment/              # Scripts de despliegue
├── assets/                      # Recursos gráficos
│   ├── images/                  # Imágenes del proyecto
│   └── icons/                   # Iconos y recursos visuales
├── logs/                        # Registros de actividad
├── dashboard.py                 # Dashboard principal (Streamlit)
├── xroad_integration.py         # Integración con X-Road
├── api_connection.py            # Conexión a APIs externas
├── integration_config.json      # Configuración de integración
├── solicitud_acceso_xroad_scd.md # Solicitud de acceso a APIs
├── plan_tecnico_detallado.md    # Plan técnico de implementación
├── requirements.txt              # Dependencias del proyecto
└── README.md                    # Documentación del proyecto
```

## 🚀 Instalación

### Requisitos Previos

- **Python 3.10 o superior**
- **Git** (para clonar el repositorio)
- **Conexión a internet** (para descargar dependencias)

### Pasos de Instalación

1. **Clonar el repositorio:**
   ```bash
   git clone <url-del-repositorio>
   cd PAE-2026
   ```

2. **Crear entorno virtual:**
   ```bash
   python -m venv venv
   ```

3. **Activar entorno virtual:**
   - **Windows:**
     ```bash
     venv\Scripts\activate
     ```
   - **Linux/Mac:**
     ```bash
     source venv/bin/activate
     ```

4. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Verificar instalación:**
   ```bash
   python -c "import pandas, streamlit; print('Instalación exitosa')"
   ```

## 💻 Uso

### Iniciar el Dashboard

1. **Ejecutar el dashboard:**
   ```bash
   python -m streamlit run dashboard.py
   ```

2. **Acceder al dashboard:**
   - **Local:** http://localhost:8511
   - **Red:** http://[IP]:8511

### Configuración de Conexión

1. **Configurar integración:**
   Editar `integration_config.json` con las credenciales reales:
   ```json
   {
     "xroad_url": "https://xroad.example.gov",
     "xroad_client_id": "GOV/COLOMBIA/DASHBOARD",
     "scd_url": "https://scd.example.gov",
     "scd_api_key": "tu_api_key_real"
   }
   ```

2. **Conexión a APIs:**
   ```bash
   python api_connection.py
   ```

### Generar Reportes

1. **Reportes individuales por entidad:**
   ```bash
   python entity_reports.py
   ```

2. **Análisis estadístico:**
   ```bash
   python analysis.py
   ```

## 📚 Documentación

### Documentos Técnicos

- **[Solicitud de Acceso a X-Road y SCD](solicitud_acceso_xroad_scd.md)**
  - Formato formal para solicitar acceso a APIs reales
  - Requisitos de seguridad y cumplimiento
  - Beneficios del proyecto para el sector público

- **[Plan Técnico Detallado](plan_tecnico_detallado.md)**
  - Arquitectura completa del sistema
  - Configuración técnica detallada
  - Estrategia de despliegue y operación

### Documentos de Análisis

- **[Análisis de Interoperabilidad](Análisis de Interoperabilidad en Sector Público en Colombia.docx)**
  - Diagnóstico ejecutivo de conectividad
  - Plan de acción estratégico
  - KPIs de monitoreo

- **[Arquitectura de Interoperabilidad](arquitectura.md)**
  - Modelo de integración X-Road/SCD
  - Estándares de interoperabilidad
  - Mejores prácticas implementadas

## 🤝 Contribución

### Cómo Contribuir

1. **Fork del repositorio**
2. **Crear rama de característica:**
   ```bash
   git checkout -b feature/nueva-funcionalidad
   ```
3. **Realizar cambios y commits:**
   ```bash
   git add .
   git commit -m "Añadir nueva funcionalidad"
   ```
4. **Push a la rama:**
   ```bash
   git push origin feature/nueva-funcionalidad
   ```
5. **Crear Pull Request**

### Directrices de Contribución

- **Código limpio y bien documentado**
- **Pruebas unitarias para nuevas funcionalidades**
- **Cumplimiento de estándares de seguridad**
- **Documentación actualizada**

## 📄 Licencia

Este proyecto se encuentra bajo la Licencia [Nombre de la Licencia]. Ver el archivo [LICENSE](LICENSE) para más detalles.

## 📞 Contacto

**Coordinador del Proyecto:**
- **Nombre:** [Nombre del Coordinador Académico]
- **Correo:** [correo@universidad.edu.co]
- **Teléfono:** [Número de contacto]

**Asesor Técnico:**
- **Nombre:** [Nombre del Asesor Técnico]
- **Correo:** [correo_tecnico@universidad.edu.co]
- **Teléfono:** [Número de contacto técnico]

---

**Universidad [Nombre de la Universidad] - PAE 2026**
**Minería de Datos - Sistema de Interoperabilidad en Sector Público Colombiano**