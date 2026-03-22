# PLAN TÉCNICO DETALLADO - SISTEMA DE INTEROPERABILIDAD

## 🏗️ Arquitectura del Sistema

### Diagrama de Componentes

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

## 🔧 Configuración Técnica

### Requisitos del Sistema

#### Hardware Mínimo
- **Procesador:** Intel Core i5 o equivalente
- **Memoria RAM:** 8 GB
- **Almacenamiento:** 50 GB disponibles
- **Conexión:** Red estable 100 Mbps

#### Software Requerido
- **Sistema Operativo:** Windows 10/11, Linux Ubuntu 20.04+, macOS 10.15+
- **Python:** Versión 3.10 o superior
- **Bases de Datos:** PostgreSQL 12+ o MySQL 8.0+
- **Contenedores:** Docker 20.10+ (opcional)

### Dependencias Técnicas

#### Python Packages
```python
# Core Analytics
pandas==2.0.0
numpy==1.24.0
scikit-learn==1.3.0
matplotlib==3.7.0
seaborn==0.12.0

# Web Framework
streamlit==1.22.0
plotly==5.14.0

# API Integration
requests==2.31.0
fastapi==0.100.0
uvicorn==0.22.0

# Database
sqlalchemy==2.0.0
psycopg2-binary==2.9.0

# Security
cryptography==41.0.0
pyjwt==2.8.0
```

#### Configuración de Entornos

##### Desarrollo
```yaml
# docker-compose.dev.yml
version: '3.8'
services:
  xroad-node:
    image: xroad/xroad-node:7.2.0
    ports:
      - "8080:8080"
    environment:
      - XROAD_NODE_ID=DEV-NODE
      - XROAD_CLIENT_ID=GOV/COLOMBIA/DASHBOARD
  
  scd-api:
    image: scd/api:latest
    ports:
      - "8081:8081"
    environment:
      - API_KEY=dashboard_api_key_2026
      - DB_HOST=scd-db
  
  dashboard:
    build: .
    ports:
      - "8511:8511"
    environment:
      - ENVIRONMENT=development
      - DEBUG=true
```

##### Producción
```yaml
# docker-compose.prod.yml
version: '3.8'
services:
  xroad-node:
    image: xroad/xroad-node:7.2.0
    ports:
      - "8080:8080"
    environment:
      - XROAD_NODE_ID=PROD-NODE
      - XROAD_CLIENT_ID=GOV/COLOMBIA/DASHBOARD
    deploy:
      replicas: 2
      restart_policy:
        condition: on-failure
  
  scd-api:
    image: scd/api:latest
    ports:
      - "8081:8081"
    environment:
      - API_KEY=dashboard_api_key_2026
      - DB_HOST=scd-db
    deploy:
      replicas: 2
      restart_policy:
        condition: on-failure
  
  dashboard:
    build: .
    ports:
      - "8511:8511"
    environment:
      - ENVIRONMENT=production
      - DEBUG=false
    deploy:
      replicas: 3
      restart_policy:
        condition: on-failure
```

## 📊 Estructura de Datos

### Modelo de Datos Principal

#### Entidades Públicas
```sql
CREATE TABLE entidades_publicas (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    sector VARCHAR(100) NOT NULL,
    nivel_madurez INTEGER CHECK (nivel_madurez BETWEEN 1 AND 5),
    conectado_xroad BOOLEAN DEFAULT FALSE,
    conectado_scd BOOLEAN DEFAULT FALSE,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fuente_datos VARCHAR(100)
);
```

#### Conectividad X-Road
```sql
CREATE TABLE conectividad_xroad (
    id SERIAL PRIMARY KEY,
    entidad_id INTEGER REFERENCES entidades_publicas(id),
    estado_conexion VARCHAR(50),
    servicios_disponibles INTEGER,
    volumen_transacciones INTEGER,
    tiempo_respuesta_promedio DECIMAL(10,2),
    fecha_monitoreo TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Servicios SCD
```sql
CREATE TABLE servicios_scd (
    id SERIAL PRIMARY KEY,
    entidad_id INTEGER REFERENCES entidades_publicas(id),
    servicios_activos INTEGER,
    transacciones_mensuales INTEGER,
    satisfaccion_ciudadana DECIMAL(3,2),
    disponibilidad_servicio DECIMAL(5,2),
    fecha_monitoreo TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Esquema de Archivos

#### CSV de Entidades Reales
```csv
ID,Entidad,Sector,Conectado_X_Road,Conectado_SCD,Nivel_Madurez,Fecha_Actualizacion
1,Ministerio de Salud,Salud,Si,No,3,2026-03-21
2,Ministerio de Educacion,Educacion,Si,Si,4,2026-03-21
3,DIAN,Hacienda,No,No,2,2026-03-21
...
```

#### JSON de Madurez
```json
{
  "entidad_id": "1",
  "entidad_nombre": "Ministerio de Salud",
  "nivel_actual": 3,
  "dimensiones": {
    "tecnologica": 3,
    "organizacional": 3,
    "legal": 2,
    "semantica": 3
  },
  "ultima_evaluacion": "2026-03-21",
  "recomendaciones": [
    "Implementar estandares de seguridad",
    "Capacitar personal en interoperabilidad"
  ]
}
```

## 🔌 Integración de APIs

### X-Road Integration Service

#### Endpoints Principales
```python
class XRoadIntegration:
    def get_service_list(self):
        """Obtiene lista de servicios disponibles"""
        url = f"{self.xroad_url}/services"
        return requests.get(url, headers=self.headers)
    
    def invoke_service(self, service_code, service_version, request_data):
        """Invoca un servicio específico"""
        payload = {
            "client": self.client_id,
            "service": {
                "serviceCode": service_code,
                "serviceVersion": service_version
            },
            "request": request_data
        }
        url = f"{self.xroad_url}/invoke"
        return requests.post(url, json=payload, headers=self.headers)
    
    def get_entity_status(self, entity_id):
        """Consulta estado de interoperabilidad de entidad"""
        service_data = {
            "entityId": entity_id,
            "statusType": "interoperability"
        }
        return self.invoke_service("interoperabilityStatusService", "v1", service_data)
```

#### Configuración de Seguridad
```python
# Certificados X-Road
XROAD_CERT_PATH = "/certs/xroad_client.crt"
XROAD_KEY_PATH = "/certs/xroad_client.key"
XROAD_CA_PATH = "/certs/xroad_ca.crt"

# Headers de autenticación
headers = {
    'Content-Type': 'application/json',
    'X-Road-Client': client_id,
    'X-Road-Port': '8080',
    'X-Road-Certificate': certificate_content
}
```

### SCD Integration Service

#### Endpoints Principales
```python
class SCDIntegration:
    def get_available_services(self):
        """Obtiene servicios disponibles en SCD"""
        url = f"{self.scd_url}/api/v1/services"
        return requests.get(url, headers=self.headers)
    
    def submit_transaction(self, service_id, transaction_data):
        """Envía transacción al SCD"""
        payload = {
            "serviceId": service_id,
            "transactionData": transaction_data,
            "timestamp": datetime.now().isoformat(),
            "sourceSystem": "dashboard_integration"
        }
        url = f"{self.scd_url}/api/v1/transactions"
        return requests.post(url, json=payload, headers=self.headers)
    
    def get_citizen_services(self, citizen_id):
        """Obtiene servicios disponibles para ciudadano"""
        url = f"{self.scd_url}/api/v1/citizens/{citizen_id}/services"
        return requests.get(url, headers=self.headers)
```

#### Configuración de Seguridad
```python
# API Key Authentication
headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json',
    'SCD-Port': '8081',
    'SCD-Client-ID': 'dashboard_client'
}

# Rate Limiting
RATE_LIMIT = 100  # requests per minute
```

## 📈 Métricas y Monitoreo

### KPIs Principales

#### Conectividad
- **Tasa de Conectividad X-Road:** Porcentaje de entidades conectadas
- **Tasa de Conectividad SCD:** Porcentaje de entidades con servicios digitales
- **Disponibilidad del Sistema:** Tiempo de operación efectiva

#### Madurez Digital
- **Nivel Promedio de Madurez:** Según modelo MinTIC
- **Progresión de Niveles:** Evolución temporal de madurez
- **Brechas de Madurez:** Diferencias entre sectores

#### Eficiencia Operativa
- **Tiempo de Respuesta:** Latencia en transacciones
- **Volumen de Transacciones:** Cantidad de operaciones procesadas
- **Satisfacción Ciudadana:** Métricas de calidad de servicio

### Dashboard de Monitoreo

#### Métricas en Tiempo Real
```python
# Streamlit Dashboard Components
st.metric("Conectividad X-Road", f"{xroad_percentage}%", delta=f"+{growth_rate}%")
st.metric("Nivel de Madurez", f"{avg_maturity}/5", delta=f"{maturity_trend}")
st.metric("Transacciones Hoy", transaction_count, delta=f"+{daily_growth}%")

# Gráficos de tendencias
fig = px.line(trend_data, x='fecha', y='valor', title='Evolución de Conectividad')
st.plotly_chart(fig)
```

#### Alertas y Notificaciones
```python
# Sistema de alertas
def check_connectivity_alerts():
    if xroad_percentage < 70:
        send_alert("Baja conectividad X-Road", "critical")
    elif scd_percentage < 50:
        send_alert("Baja adopción SCD", "warning")
    elif avg_maturity < 3:
        send_alert("Nivel de madurez bajo", "info")
```

## 🔒 Seguridad de la Información

### Arquitectura de Seguridad

#### Capas de Seguridad
1. **Seguridad Física:** Control de acceso a servidores
2. **Seguridad de Red:** Firewalls, VPN, segmentación
3. **Seguridad de Aplicación:** Validación de entradas, encriptación
4. **Seguridad de Datos:** Encriptación en reposo y tránsito
5. **Gestión de Identidades:** Autenticación y autorización

#### Controles de Seguridad

##### Autenticación
```python
# JWT Authentication
def authenticate_user(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

# OAuth2 Integration
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
```

##### Autorización
```python
# Role-Based Access Control
def check_permission(user_role, required_permission):
    permissions = {
        'admin': ['read', 'write', 'delete', 'admin'],
        'analyst': ['read', 'write'],
        'viewer': ['read']
    }
    return required_permission in permissions.get(user_role, [])
```

##### Encriptación
```python
# Data Encryption
from cryptography.fernet import Fernet

def encrypt_data(data):
    key = Fernet.generate_key()
    cipher_suite = Fernet(key)
    encrypted_data = cipher_suite.encrypt(data.encode())
    return encrypted_data, key

def decrypt_data(encrypted_data, key):
    cipher_suite = Fernet(key)
    decrypted_data = cipher_suite.decrypt(encrypted_data)
    return decrypted_data.decode()
```

### Cumplimiento Normativo

#### Normativas Aplicables
- **Ley 1581 de 2012:** Protección de datos personales
- **Decreto 1074 de 2015:** Marco de Gobierno Digital
- **ISO 27001:** Seguridad de la Información
- **NIST Cybersecurity Framework:** Ciberseguridad

#### Auditoría y Control
```python
# Logging de actividades
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('security.log'),
        logging.StreamHandler()
    ]
)

# Auditoría de accesos
def log_access(user_id, action, resource):
    logging.info(f"User {user_id} performed {action} on {resource}")
```

## 🚀 Despliegue y Operación

### Estrategia de Despliegue

#### Fases de Implementación
1. **Fase 1:** Entorno de desarrollo y pruebas
2. **Fase 2:** Entorno de staging y validación
3. **Fase 3:** Entorno de producción controlado
4. **Fase 4:** Expansión nacional

#### CI/CD Pipeline
```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Build Docker Image
        run: docker build -t dashboard:latest .
      - name: Deploy to Production
        run: |
          docker-compose -f docker-compose.prod.yml down
          docker-compose -f docker-compose.prod.yml up -d
```

### Monitoreo y Mantenimiento

#### Health Checks
```python
# Health check endpoints
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now(),
        "services": {
            "xroad": check_xroad_connection(),
            "scd": check_scd_connection(),
            "database": check_database_connection()
        }
    }
```

#### Backup y Recuperación
```python
# Backup strategy
def backup_database():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"backup_{timestamp}.sql"
    
    # PostgreSQL backup
    os.system(f"pg_dump -h {DB_HOST} -U {DB_USER} {DB_NAME} > {backup_file}")
    
    # Upload to cloud storage
    upload_to_cloud(backup_file)
    
    # Cleanup old backups
    cleanup_old_backups()
```

---

**Nota:** Este plan técnico detallado proporciona la base para la implementación completa del sistema de interoperabilidad. Cada sección puede ser expandida según las necesidades específicas del proyecto.