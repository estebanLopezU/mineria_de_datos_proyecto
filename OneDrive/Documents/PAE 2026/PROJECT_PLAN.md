# Plan del Proyecto: Mapeo de Interoperabilidad X-Road Colombia

## 🎯 Visión General
Sistema de diagnóstico y visualización de entidades públicas colombianas conectadas bajo el estándar X-Road, evaluando su nivel de madurez según el Marco de Interoperabilidad del MinTIC.

---

## 🏗️ Arquitectura del Sistema

### Backend - Python + FastAPI
```
backend/
├── app/
│   ├── main.py              # Aplicación principal
│   ├── config.py            # Configuración
│   ├── database.py          # Conexión DB
│   ├── models/              # Modelos SQLAlchemy
│   │   ├── entity.py
│   │   ├── sector.py
│   │   ├── service.py
│   │   ├── maturity.py
│   │   └── interoperability.py
│   ├── schemas/             # Schemas Pydantic
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/
│   │       │   ├── entities.py
│   │       │   ├── sectors.py
│   │       │   ├── services.py
│   │       │   ├── maturity.py
│   │       │   ├── dashboard.py
│   │       │   └── reports.py
│   │       └── router.py
│   ├── services/            # Lógica de negocio
│   │   ├── entity_service.py
│   │   ├── maturity_service.py
│   │   └── analytics_service.py
│   └── utils/
└── requirements.txt
```

### Frontend - React + Vite + Tailwind
```
frontend/
├── src/
│   ├── main.jsx
│   ├── App.jsx
│   ├── pages/
│   │   ├── Dashboard.jsx        # Vista principal con KPIs
│   │   ├── Entidades.jsx        # CRUD entidades
│   │   ├── MatrizServicios.jsx  # Matriz de interconexión
│   │   ├── MapaInteractivo.jsx  # Mapa geográfico
│   │   ├── EvaluacionMadurez.jsx # Evaluación de madurez
│   │   └── Reportes.jsx         # Generación de reportes
│   ├── components/
│   │   ├── layout/
│   │   ├── dashboard/
│   │   ├── entities/
│   │   ├── matrix/
│   │   ├── map/
│   │   └── common/
│   ├── hooks/
│   ├── services/
│   └── utils/
└── package.json
```

---

## 📊 Modelo de Datos

### Tablas Principales:
1. **sectors** - Sectores (Salud, Educación, Hacienda, etc.)
2. **entities** - Entidades públicas
3. **services** - Servicios de interoperabilidad
4. **maturity_assessments** - Evaluaciones de madurez
5. **interoperability_links** - Enlaces entre entidades

### Niveles de Madurez (Marco MinTIC):
- **Nivel 1 - Inicial**: Sin estándares definidos
- **Nivel 2 - Básico**: APIs básicas, datos no estandarizados
- **Nivel 3 - Intermedio**: APIs REST, datos semiestructurados
- **Nivel 4 - Avanzado**: X-Road completo, estándares semánticos

---

## 🎨 Componentes del Frontend

### Dashboard Principal:
- KPIs: Total entidades, % conectadas X-Road, nivel promedio madurez
- Gráfico de sectores
- Mapa de Colombia con entidades
- Top 10 entidades más maduras

### Matriz de Servicios:
- Tabla cruzada sectores vs sectores
- Heatmap de interconexiones
- Filtros por tipo de servicio

### Mapa Interactivo:
- Visualización geográfica
- Nodos = Entidades
- Aristas = Conexiones de interoperabilidad
- Filtros por sector y nivel de madurez

### Evaluación de Madurez:
- Formulario de evaluación
- Radar chart por dominio (Legal, Organizacional, Semántico, Técnico)
- Comparativa entre entidades

---

## 🔧 Stack Tecnológico

### Backend:
- **Framework**: FastAPI 0.100+
- **ORM**: SQLAlchemy 2.0
- **Database**: PostgreSQL 15
- **Migrations**: Alembic
- **Validation**: Pydantic v2
- **Documentation**: Swagger/OpenAPI

### Frontend:
- **Framework**: React 18
- **Build**: Vite 5
- **Styling**: Tailwind CSS 3
- **Charts**: Recharts
- **Maps**: Leaflet + React-Leaflet
- **HTTP**: Axios
- **State**: React Context + Hooks
- **Icons**: Lucide React

### DevOps:
- **Containerization**: Docker + Docker Compose
- **Database**: PostgreSQL en contenedor