# Est Campus Unal - estaciones meteorologicas

Dashboard y API para las estaciones automaticas **La Nubia (24)** y
**Palogrande-Postgrados (29)**, Universidad Nacional de Colombia, sede Manizales.

Lo que hace:

- **Endpoint de recepcion** (`POST /api/v1/estaciones/datos/`): recibe lecturas
  JSON de las estaciones, las valida (rangos fisicos, valores centinela) y las
  guarda en una base de datos local (SQLite). Idempotente por
  `(estacion, timestamp)`: reenviar no duplica.
- **Dashboard web** (`/`): tarjetas de valor actual, brujula de viento, grafica
  de la ventana de 24 h, mapa de ubicacion de las estaciones, pronostico y
  visibilidad (Open-Meteo) e **historial estadistico** por ano/mes/dia/hora
  con exportacion CSV y datos crudos por dia.
- **API de consulta**: ultima lectura y serie agregada para las graficas.

## Requisitos

- Python 3.12 y el entorno virtual `C:\Users\esteb\entornos_venv\est_campus`
  (vive fuera de OneDrive a proposito).
- Windows PowerShell.

## Puesta en marcha

```powershell
. .\scripts\10_activar_entorno.ps1
python manage.py migrate
python manage.py runserver 0.0.0.0:5000
```

> Puerto unico `5000` en `0.0.0.0` (la consola Ambient solo reporta ahi).
> No usar `8000` ni `127.0.0.1`: dejan zombies y la consola no llega.
> Arranque rapido: `.\scripts\05_arrancar_servidor.ps1` (mata zombies y arranca).

Abrir http://127.0.0.1:5000/ en el navegador. La base ya viene con todo el
historico cargado; si se quiere recargar (o cargar solo un tramo):

```powershell
python manage.py cargar_historicos                 # todo (minutos)
python manage.py cargar_historicos --desde 2026-09-01   # tramo reciente
```

El comando es idempotente: se puede repetir sin duplicar.

### Estado actual de la base local

`db.sqlite3` contiene el **historial completo** de ambas estaciones
(4.800.409 lecturas, ~1,1 GB): La Nubia desde **2004-01-01** y Palogrande
desde **2002-01-01**, ambas hasta **2026-10-07**. El comando es idempotente:
se puede repetir sin duplicar (la restriccion unica estacion+timestamp y
`ignore_conflicts` deciden que insertar).

## Pruebas y verificaciones

```powershell
python manage.py test estaciones            # 20 pruebas del endpoint
python scripts\16_revisar_frontend.py       # sintaxis JS + estaticos + plantilla
python scripts\17_probar_servidor.py        # servidor en vivo de punta a punta
```

## Endpoint de recepcion

`POST /api/v1/estaciones/datos/` con un objeto o una lista:

```json
{
  "estacion": 24,
  "timestamp": "2026-10-07 22:30:00",
  "temperatura": 18.4,
  "humedad_relativa": 88,
  "precipitacion": 0.0,
  "presion_barometrica": 600.5,
  "velocidad_viento": 1.2,
  "direccion_viento": 110,
  "radiacion_solar": 0.0,
  "evapotranspiracion": 0.0
}
```

`GET` al mismo URL devuelve la documentacion. Respuestas: `201` creado,
`207` procesado con advertencias (valores fuera de rango descartados),
`400` peticion invalida, `401` sin token (solo si `INGEST_TOKEN` esta definido).

Con token (opcional, para el demo en red local):

```powershell
$env:INGEST_TOKEN = "clave-secreta"
```

y la estacion envia la cabecera `Authorization: Bearer clave-secreta`.

API de consulta:

- `GET /api/v1/estaciones/ultima/` - ultima lectura de cada estacion.
- `GET /api/v1/estaciones/serie/?estacion=24` - serie de 24 h hasta ahora.
- `GET /api/v1/estaciones/serie/?estacion=24&modo=reciente` - 24 h anteriores
  a la ultima lectura guardada (para historicos sin datos en vivo).
- `GET /api/v1/estaciones/pronostico/?estacion=24` - pronostico y visibilidad
  del modelo Open-Meteo para las coordenadas de la estacion (cache 10 min).
- `GET /api/v1/estaciones/historial/?estacion=24` - estadisticas por ano;
  `&anio=2026` por mes, `&anio=2026&mes=9` por dia,
  `&anio=2026&mes=9&dia=15` por hora y `&crudos=1` las lecturas de 5 min
  de ese dia (drill-down en cascada; el panel lo explora con selectores).

## Estructura

```text
est_campus/            configuracion Django (hora America/Bogota, SQLite local)
estaciones/
  models.py            Estacion + Lectura (restriccion unica estacion+timestamp)
  api/endpoints.py     endpoint POST con validacion de rangos y centinelas
  views.py             dashboard + API de consulta (serie agregada en Python)
  pronostico.py        cliente Open-Meteo: pronostico y visibilidad (cache 10 min)
  management/commands/cargar_historicos.py   carga los CSV de Est_Datos
  templates/dashboard.html
  static/css/dashboard.css  static/js/dashboard.js (canvas puro + Leaflet)
Est_Datos/             CSV originales (cada 5 min)
Excel_Organizado/      libros por anio + README de calidad de datos
scripts/               utilidades numeradas (explorar, validar, probar)
```

## Panel Ambient (estacion 99, aislada)

Consola estilo Ambient Weather en `GET /ambient/` (no mezcla con 24/29):

- Receptor Wunderground: `GET /weatherstation/updateweatherstation.php`
  (responde `success`, idempotente por estacion+timestamp).
- APIs propias: `GET /api/v1/ambient/ultima/` y `GET /api/v1/ambient/serie/`.
- Traduce imperial a metrico y guarda extras de la consola
  (racha, UV, indoor, lluvias dia/semana/mes/anio, presion abs/rel).

Configurar la consola (Custom Server):

- IP `192.168.137.1`, puerto `5000`,
  path `/weatherstation/updateweatherstation.php`, protocolo Wunderground.
- En `est_campus/settings.py` esa IP ya esta en `ALLOWED_HOSTS`;
  para otra red usar `$env:ALLOWED_HOSTS = "192.168.1.20"`.

Probar el receptor:

```powershell
Invoke-WebRequest "http://127.0.0.1:5000/weatherstation/updateweatherstation.php?ID=x&PASSWORD=x&dateutc=2026-10-14%2019:30:00&tempf=77&humidity=50&action=updateraw"
```

Pruebas del modulo: `python manage.py test estaciones.tests_ambient` (9 pruebas).

## Notas importantes

- Las estaciones emiten cada **5 minutos** (medido en los datos reales).
  El demo a **16 segundos** es un escenario acelerado: la base local lo aguanta
  (ver `scripts/12_prueba_carga_bd.py`), solo cambia el volumen.
- SQLite basta: con las **4,8 M** de lecturas la base ocupa ~1,1 GB y las
  consultas del dashboard tardan milisegundos. El historial agrega con
  `strftime` nativo (los `Trunc*` de Django en SQLite son una funcion
  Python por fila: 15 s por consulta; con `strftime` baja a ~3 s y las
  respuestas se cachean 10 min, segunda visita instantanea).
- Ojo con los totales de lluvia de 2005 en La Nubia: el CSV original trae
  valores altos dentro del rango valido (0-200 mm por lectura) que suman
  ~104.000 mm en el anio. Es un problema del dato fuente, no de la carga.
- Las coordenadas del mapa son **aproximadas**: verificar contra la ficha
  tecnica antes de publicarlas.
- Las estaciones **no miden** visibilidad ni emiten pronostico: esas tarjetas
  se llenan con el modelo **Open-Meteo** (`/api/v1/estaciones/pronostico/`) y
  se etiquetan como "(Open-Meteo)". El indice UV tampoco se mide: se estima
  de la radiacion solar y se etiqueta como estimado.
- Unidades inferidas de la nomenclatura de la red (ver `Excel_Organizado/README.md`):
  confirmar con la ficha tecnica.
