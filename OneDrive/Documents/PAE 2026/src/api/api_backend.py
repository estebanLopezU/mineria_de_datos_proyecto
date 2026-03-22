from fastapi import FastAPI, HTTPException
import pandas as pd

app = FastAPI(
    title="API de Interoperabilidad en Sector Público Colombiano",
    description="API para consultar datos de interoperabilidad, entidades, madurez y estadísticas.",
    version="1.0.0"
)

# Cargar datos
try:
    df = pd.read_csv('entidades_reales.csv')
    data_source = "Datos reales"
except FileNotFoundError:
    df = pd.read_csv('entidades_sample.csv')
    data_source = "Datos simulados"

@app.get("/")
def root():
    return {"message": "API de Interoperabilidad", "data_source": data_source}

@app.get("/entidades")
def get_entidades():
    """Obtener lista de todas las entidades con sus datos."""
    return df.to_dict(orient='records')

@app.get("/entidades/{entidad_id}")
def get_entidad(entidad_id: int):
    """Obtener detalles de una entidad específica por ID."""
    entidad = df[df['ID'] == entidad_id]
    if entidad.empty:
        raise HTTPException(status_code=404, detail="Entidad no encontrada")
    data = entidad.to_dict(orient='records')[0]
    # Agregar estadísticas comparativas
    sector = data['Sector']
    sector_avg = df[df['Sector'] == sector]['Nivel_Madurez'].mean()
    data['madurez_sector_promedio'] = round(sector_avg, 1)
    data['posicion_sectorial'] = "Por encima" if data['Nivel_Madurez'] > sector_avg else ("Por debajo" if data['Nivel_Madurez'] < sector_avg else "En promedio")
    return data

@app.get("/estadisticas")
def get_estadisticas():
    """Obtener estadísticas generales del sistema de interoperabilidad."""
    stats = {
        "total_entidades": int(len(df)),
        "conectadas_xroad": int(len(df[df['Conectado_X_Road'] == 'Sí'])),
        "conectadas_scd": int(len(df[df['Conectado_SCD'] == 'Sí'])),
        "madurez_promedio": round(df['Nivel_Madurez'].mean(), 1),
        "distribucion_madurez": df['Nivel_Madurez'].value_counts().sort_index().to_dict(),
        "sectores": df['Sector'].nunique(),
        "entidades_desconectadas": int(len(df[(df['Conectado_X_Road'] == 'No') & (df['Conectado_SCD'] == 'No')])),
        "entidades_baja_madurez": int(len(df[df['Nivel_Madurez'] <= 2]))
    }
    return stats

@app.get("/sectores")
def get_sectores():
    """Obtener resumen por sectores."""
    sector_summary = df.groupby('Sector').agg({
        'Entidad': 'count',
        'Nivel_Madurez': 'mean'
    }).rename(columns={'Entidad': 'numero_entidades', 'Nivel_Madurez': 'madurez_promedio'}).round(1).to_dict()
    return sector_summary

@app.get("/buscar")
def buscar_entidad(q: str = None):
    """Buscar entidades por nombre (parcial)."""
    if not q:
        return {"error": "Proporcione un parámetro 'q' para buscar"}
    resultados = df[df['Entidad'].str.contains(q, case=False, na=False)]
    return resultados.to_dict(orient='records')