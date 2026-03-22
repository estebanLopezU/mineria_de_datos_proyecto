import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime
import os

# Configuración de la página
st.set_page_config(
    page_title="Dashboard Científico de Interoperabilidad",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Cargar datos: intentar reales, sino error
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('entidades_reales.csv')
        data_source = "Datos reales obtenidos de APIs oficiales"
        st.sidebar.success("✓ Datos reales cargados")
        return df, data_source
    except FileNotFoundError:
        st.error("✗ No se encontraron archivos de datos reales. Se requiere entidades_reales.csv para funcionamiento en producción.")
        st.info("Para pruebas, se necesita implementar conexión a APIs reales de X-Road y SCD.")
        return None, None

# Cargar datos
df, data_source = load_data()

if df is None:
    st.stop()

# Sidebar con filtros y controles
st.sidebar.header("Controles del Dashboard")
st.sidebar.subheader("Filtros")

# Filtros por sector
sectores_disponibles = df['Sector'].unique().tolist()
sectores_seleccionados = st.sidebar.multiselect(
    "Seleccionar Sectores",
    sectores_disponibles,
    default=sectores_disponibles
)

# Filtros por nivel de madurez
nivel_min, nivel_max = st.sidebar.slider(
    "Rango de Nivel de Madurez",
    min_value=1,
    max_value=5,
    value=(1, 5)
)

# Filtros por conectividad
conectado_xroad = st.sidebar.checkbox("Conectado a X-Road", value=True)
conectado_scd = st.sidebar.checkbox("Conectado a SCD", value=True)

# Aplicar filtros
df_filtrado = df[
    (df['Sector'].isin(sectores_seleccionados)) &
    (df['Nivel_Madurez'] >= nivel_min) &
    (df['Nivel_Madurez'] <= nivel_max)
]

if not conectado_xroad:
    df_filtrado = df_filtrado[df_filtrado['Conectado_X_Road'] == 'No']
if not conectado_scd:
    df_filtrado = df_filtrado[df_filtrado['Conectado_SCD'] == 'No']

# Título principal
st.title("🏛️ Dashboard Científico de Interoperabilidad en Sector Público Colombiano")
st.markdown("**Análisis estadístico avanzado basado en el Marco MinTIC y plataforma X-Road**")
st.caption(f"Fuente de datos: {data_source} | Última actualización: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Explicación de interoperabilidad
with st.expander("📚 ¿Qué es la Interoperabilidad en el Sector Público?", expanded=False):
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔍 Definición")
        st.write("""
        **Interoperabilidad** es la capacidad de los sistemas, organizaciones y personas para intercambiar 
        información y conocimientos de manera efectiva para lograr metas comunes.
        """)
        
        st.subheader("📊 Modelo MinTIC de Madurez")
        st.write("""
        **Nivel 1 (Inicial):** Procesos manuales, sin estandarización
        **Nivel 2 (Básico):** Procesos parcialmente automatizados
        **Nivel 3 (Intermedio):** Procesos estandarizados y documentados
        **Nivel 4 (Avanzado):** Interoperabilidad parcial entre sistemas
        **Nivel 5 (Optimizado):** Interoperabilidad total y continua mejora
        """)
    
    with col2:
        st.subheader("🔗 Plataformas Clave")
        st.write("**X-Road:** Sistema de intercambio seguro de datos entre entidades")
        st.write("**SCD:** Servicios Ciudadanos Digitales para trámites en línea")
        st.write("**Beneficios:** Eficiencia, transparencia, reducción de trámites")
        
        st.subheader("🎯 Indicadores de Éxito")
        st.write("- Conectividad a plataformas interoperables")
        st.write("- Nivel de madurez de procesos")
        st.write("- Calidad de datos intercambiados")
        st.write("- Satisfacción ciudadana")

# Métricas generales
st.header("📊 Métricas Generales del Sistema")

# Crear métricas con mejor visualización
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        label="🏛️ Entidades Analizadas",
        value=len(df_filtrado),
        delta=f"{len(df_filtrado) - len(df)}" if len(df_filtrado) != len(df) else "Total",
        help="Número total de entidades públicas analizadas"
    )

with col2:
    xroad_conectadas = len(df_filtrado[df_filtrado['Conectado_X_Road'] == 'Sí'])
    xroad_porcentaje = f"{xroad_conectadas/len(df_filtrado)*100:.1f}%" if len(df_filtrado) > 0 else "0%"
    st.metric(
        label="🔗 Conectadas a X-Road",
        value=xroad_conectadas,
        delta=xroad_porcentaje,
        help="Entidades con intercambio seguro de datos"
    )

with col3:
    scd_conectadas = len(df_filtrado[df_filtrado['Conectado_SCD'] == 'Sí'])
    scd_porcentaje = f"{scd_conectadas/len(df_filtrado)*100:.1f}%" if len(df_filtrado) > 0 else "0%"
    st.metric(
        label="💻 Conectadas a SCD",
        value=scd_conectadas,
        delta=scd_porcentaje,
        help="Entidades con servicios ciudadanos digitales"
    )

with col4:
    madurez_promedio = df_filtrado['Nivel_Madurez'].mean()
    madurez_delta = f"{madurez_promedio - df['Nivel_Madurez'].mean():.2f}" if len(df_filtrado) != len(df) else "General"
    st.metric(
        label="📈 Madurez Promedio",
        value=f"{madurez_promedio:.2f}/5",
        delta=madurez_delta,
        help="Nivel promedio según modelo MinTIC (1=Inicial, 5=Optimizado)"
    )

with col5:
    sectores_activos = df_filtrado['Sector'].nunique()
    st.metric(
        label="🏛️ Sectores Activos",
        value=sectores_activos,
        delta=f"{sectores_activos - df['Sector'].nunique()}" if len(df_filtrado) != len(df) else "Total",
        help="Número de sectores del gobierno analizados"
    )

# Indicadores de progreso
st.subheader("🎯 Indicadores de Progreso")
col1, col2, col3 = st.columns(3)

with col1:
    # Progreso de X-Road
    progreso_xroad = xroad_conectadas / len(df_filtrado) if len(df_filtrado) > 0 else 0
    st.progress(progreso_xroad)
    st.caption(f"X-Road: {progreso_xroad*100:.1f}% de adopción")

with col2:
    # Progreso de SCD
    progreso_scd = scd_conectadas / len(df_filtrado) if len(df_filtrado) > 0 else 0
    st.progress(progreso_scd)
    st.caption(f"SCD: {progreso_scd*100:.1f}% de adopción")

with col3:
    # Progreso de Madurez
    progreso_madurez = madurez_promedio / 5 if len(df_filtrado) > 0 else 0
    st.progress(progreso_madurez)
    st.caption(f"Madurez: {progreso_madurez*100:.1f}% del nivel óptimo")

# Análisis por entidad específica
st.header("🔍 Análisis Detallado por Entidad")
entidad_seleccionada = st.selectbox(
    "Seleccionar Entidad para Análisis Detallado:",
    df_filtrado['Entidad'].tolist(),
    key="entidad_select"
)

if entidad_seleccionada:
    entidad_data = df_filtrado[df_filtrado['Entidad'] == entidad_seleccionada].iloc[0]
    
    # Métricas de la entidad seleccionada
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Nivel de Madurez", entidad_data['Nivel_Madurez'])
    
    with col2:
        sector_avg = df_filtrado[df_filtrado['Sector'] == entidad_data['Sector']]['Nivel_Madurez'].mean()
        st.metric("Promedio Sectorial", f"{sector_avg:.2f}")
    
    with col3:
        st.metric("Conectividad X-Road", "✅" if entidad_data['Conectado_X_Road'] == 'Sí' else "❌")
    
    with col4:
        st.metric("Conectividad SCD", "✅" if entidad_data['Conectado_SCD'] == 'Sí' else "❌")
    
    # Gráficos comparativos para la entidad
    col1, col2 = st.columns(2)
    
    with col1:
        # Posición relativa en el sector
        sector_data = df_filtrado[df_filtrado['Sector'] == entidad_data['Sector']]['Nivel_Madurez']
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.histplot(sector_data, kde=True, ax=ax, color='lightblue', alpha=0.7, label='Sector')
        ax.axvline(entidad_data['Nivel_Madurez'], color='red', linestyle='--', linewidth=3, 
                  label=f'{entidad_seleccionada}: {entidad_data["Nivel_Madurez"]}')
        ax.axvline(sector_avg, color='green', linestyle='-', linewidth=2,
                  label=f'Promedio sector: {sector_avg:.2f}')
        ax.set_title(f'Posición de {entidad_seleccionada} en el Sector {entidad_data["Sector"]}', fontweight='bold')
        ax.set_xlabel('Nivel de Madurez')
        ax.set_ylabel('Frecuencia')
        ax.legend()
        st.pyplot(fig)
    
    with col2:
        # Radar de interoperabilidad
        categories = ['Madurez', 'X-Road', 'SCD', 'Sector\nPromedio']
        values = [
            entidad_data['Nivel_Madurez'] / 5,
            1 if entidad_data['Conectado_X_Road'] == 'Sí' else 0,
            1 if entidad_data['Conectado_SCD'] == 'Sí' else 0,
            sector_avg / 5
        ]
        
        angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
        values += values[:1]
        angles += angles[:1]
        
        fig, ax = plt.subplots(figsize=(8, 6), subplot_kw=dict(projection='polar'))
        ax.plot(angles, values, 'o-', linewidth=2, label=entidad_seleccionada)
        ax.fill(angles, values, alpha=0.25)
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories)
        ax.set_ylim(0, 1)
        ax.set_title('Perfil de Interoperabilidad', fontweight='bold', pad=20)
        ax.legend()
        st.pyplot(fig)

# Visualizaciones científicas avanzadas
st.header("🔬 Visualizaciones Científicas Avanzadas")

# Configurar subplots para visualizaciones
col1, col2 = st.columns(2)

with col1:
    # Distribución de madurez con estadísticas
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(df_filtrado['Nivel_Madurez'], kde=True, ax=ax, color='steelblue', alpha=0.7)
    ax.axvline(df_filtrado['Nivel_Madurez'].mean(), color='red', linestyle='--', 
              label=f'Media: {df_filtrado["Nivel_Madurez"].mean():.2f}')
    ax.axvline(df_filtrado['Nivel_Madurez'].median(), color='green', linestyle='--',
              label=f'Mediana: {df_filtrado["Nivel_Madurez"].median():.2f}')
    ax.set_title('Distribución de Niveles de Madurez', fontweight='bold', fontsize=14)
    ax.set_xlabel('Nivel de Madurez (Modelo MinTIC)')
    ax.set_ylabel('Frecuencia')
    ax.legend()
    ax.grid(True, alpha=0.3)
    st.pyplot(fig)

with col2:
    # Box plot por sector
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(data=df_filtrado, x='Sector', y='Nivel_Madurez', ax=ax)
    ax.set_title('Distribución de Madurez por Sector', fontweight='bold', fontsize=14)
    ax.set_xlabel('Sector')
    ax.set_ylabel('Nivel de Madurez')
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)

# Heatmap de correlación
st.subheader("🌡️ Mapa de Correlación")
if len(df_filtrado) > 1:  # Verificar que haya suficientes datos para correlación
    df_corr = df_filtrado.copy()
    # Convertir valores de texto a numéricos para correlación
    df_corr['X_Road_Num'] = df_corr['Conectado_X_Road'].map({'Si': 1, 'No': 0})
    df_corr['SCD_Num'] = df_corr['Conectado_SCD'].map({'Si': 1, 'No': 0})
    
    # Seleccionar solo columnas numéricas para correlación
    numeric_cols = ['Nivel_Madurez', 'X_Road_Num', 'SCD_Num']
    correlation_matrix = df_corr[numeric_cols].corr()
    
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0, ax=ax, 
               square=True, fmt='.3f', cbar_kws={'label': 'Coeficiente de Correlación'})
    ax.set_title('Correlación entre Variables de Interoperabilidad', fontweight='bold', fontsize=14)
    ax.set_xlabel('Variables')
    ax.set_ylabel('Variables')
    st.pyplot(fig)
    
    # Interpretación de correlaciones
    st.write("**Interpretación de correlaciones:**")
    st.write("- **X-Road vs Madurez:**", f"{correlation_matrix.loc['X_Road_Num', 'Nivel_Madurez']:.3f}")
    st.write("- **SCD vs Madurez:**", f"{correlation_matrix.loc['SCD_Num', 'Nivel_Madurez']:.3f}")
    st.write("- **X-Road vs SCD:**", f"{correlation_matrix.loc['X_Road_Num', 'SCD_Num']:.3f}")
else:
    st.warning("No hay suficientes datos para generar el mapa de correlación. Se requieren al menos 2 entidades con datos completos.")

# Análisis por sector detallado
st.header("📈 Análisis Detallado por Sector")

sector_analysis = df_filtrado.groupby('Sector').agg({
    'Entidad': 'count',
    'Nivel_Madurez': ['mean', 'std', 'min', 'max'],
    'Conectado_X_Road': lambda x: (x == 'Sí').sum(),
    'Conectado_SCD': lambda x: (x == 'Sí').sum()
}).round(2)

sector_analysis.columns = ['Número_Entidades', 'Madurez_Media', 'Desv_Estándar', 'Mínimo', 'Máximo', 'X_Road_Conectadas', 'SCD_Conectadas']
sector_analysis['Porcentaje_X_Road'] = (sector_analysis['X_Road_Conectadas'] / sector_analysis['Número_Entidades'] * 100).round(1)
sector_analysis['Porcentaje_SCD'] = (sector_analysis['SCD_Conectadas'] / sector_analysis['Número_Entidades'] * 100).round(1)

st.dataframe(sector_analysis, use_container_width=True)

# Gráfico de madurez por sector
fig, ax = plt.subplots(figsize=(12, 6))
sector_means = sector_analysis['Madurez_Media'].sort_values(ascending=False)
bars = ax.bar(sector_means.index, sector_means.values, color='lightseagreen', alpha=0.8)
ax.set_title('Madurez Promedio por Sector (Ordenado)', fontweight='bold', fontsize=14)
ax.set_xlabel('Sector')
ax.set_ylabel('Madurez Promedio')
ax.tick_params(axis='x', rotation=45)

# Añadir valores encima de las barras
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height + 0.05,
            f'{height:.2f}', ha='center', va='bottom', fontweight='bold')

plt.tight_layout()
st.pyplot(fig)

# Identificación de cuellos de botella
st.header("⚠️ Identificación de Cuellos de Botella")

col1, col2 = st.columns(2)

with col1:
    # Entidades con baja madurez
    low_maturity = df_filtrado[df_filtrado['Nivel_Madurez'] <= 2]
    st.subheader("Entidades con Baja Madurez (Niveles 1-2)")
    if not low_maturity.empty:
        st.dataframe(low_maturity[['Entidad', 'Sector', 'Nivel_Madurez']], use_container_width=True)
        st.warning(f"Se identificaron {len(low_maturity)} entidades con niveles críticos de madurez")
    else:
        st.success("No se identificaron entidades con baja madurez")

with col2:
    # Entidades completamente desconectadas
    disconnected = df_filtrado[(df_filtrado['Conectado_X_Road'] == 'No') & (df_filtrado['Conectado_SCD'] == 'No')]
    st.subheader("Entidades Completamente Desconectadas")
    if not disconnected.empty:
        st.dataframe(disconnected[['Entidad', 'Sector']], use_container_width=True)
        st.error(f"Se identificaron {len(disconnected)} entidades sin conectividad")
    else:
        st.success("Todas las entidades tienen al menos una conexión activa")

# Distribución cruzada de conectividad
st.subheader("🔄 Distribución Cruzada de Conectividad")
if len(df_filtrado) > 0:
    cross_table = pd.crosstab(df_filtrado['Conectado_X_Road'], df_filtrado['Conectado_SCD'])
    st.dataframe(cross_table, use_container_width=True)
    
    # Gráfico de conectividad cruzada
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Crear gráfico de barras apiladas
    cross_table.plot(kind='bar', stacked=True, ax=ax, color=['lightcoral', 'lightblue'])
    ax.set_title('Conectividad Cruzada X-Road vs SCD', fontweight='bold', fontsize=14)
    ax.set_xlabel('Conectado a X-Road')
    ax.set_ylabel('Número de Entidades')
    ax.legend(['No SCD', 'Sí SCD'], title='Conectado a SCD')
    ax.tick_params(axis='x', rotation=0)
    
    # Añadir valores encima de las barras
    for container in ax.containers:
        ax.bar_label(container, label_type='center')
    
    st.pyplot(fig)
    
    # Análisis de conectividad cruzada
    st.write("**Análisis de Conectividad Cruzada:**")
    total_entidades = len(df_filtrado)
    
    # Contar combinaciones específicas
    ambos_conectados = len(df_filtrado[(df_filtrado['Conectado_X_Road'] == 'Si') & (df_filtrado['Conectado_SCD'] == 'Si')])
    solo_xroad = len(df_filtrado[(df_filtrado['Conectado_X_Road'] == 'Si') & (df_filtrado['Conectado_SCD'] == 'No')])
    solo_scd = len(df_filtrado[(df_filtrado['Conectado_X_Road'] == 'No') & (df_filtrado['Conectado_SCD'] == 'Si')])
    ninguno = len(df_filtrado[(df_filtrado['Conectado_X_Road'] == 'No') & (df_filtrado['Conectado_SCD'] == 'No')])
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("✅ Ambas Plataformas", f"{ambos_conectados}/{total_entidades}", f"{ambos_conectados/total_entidades*100:.1f}%")
        st.metric("🔗 Solo X-Road", f"{solo_xroad}/{total_entidades}", f"{solo_xroad/total_entidades*100:.1f}%")
    
    with col2:
        st.metric("💻 Solo SCD", f"{solo_scd}/{total_entidades}", f"{solo_scd/total_entidades*100:.1f}%")
        st.metric("❌ Ninguna", f"{ninguno}/{total_entidades}", f"{ninguno/total_entidades*100:.1f}%")
else:
    st.warning("No hay datos suficientes para generar la distribución cruzada de conectividad.")

# Recomendaciones estratégicas
st.header("💡 Recomendaciones Estratégicas")

recomendaciones = []

# Análisis para recomendaciones
if len(low_maturity) > 0:
    recomendaciones.append("🔴 **Prioridad Alta:** Implementar programas de capacitación intensiva para entidades con niveles 1-2 de madurez")

if len(disconnected) > 0:
    recomendaciones.append("🔴 **Prioridad Alta:** Conectar urgentemente las entidades completamente desconectadas a plataformas interoperables")

if len(df_filtrado) > 0:
    if xroad_conectadas/len(df_filtrado) < 0.7:
        recomendaciones.append("🟡 **Prioridad Media:** Fortalecer la adopción de X-Road en sectores con baja penetración")

    if scd_conectadas/len(df_filtrado) < 0.7:
        recomendaciones.append("🟡 **Prioridad Media:** Incrementar la implementación de Servicios Ciudadanos Digitales")

    if madurez_promedio < 3.0:
        recomendaciones.append("🟡 **Prioridad Media:** Establecer metas claras de mejora de madurez con seguimiento mensual")

if len(recomendaciones) == 0:
    recomendaciones.append("🟢 **Estado Óptimo:** El sistema de interoperabilidad se encuentra en buen estado")

for i, rec in enumerate(recomendaciones, 1):
    st.markdown(f"{i}. {rec}")

# Exportación de datos
st.header("📤 Exportación de Datos")

col1, col2, col3 = st.columns(3)

with col1:
        if st.button("📊 Exportar Datos Filtrados (CSV)"):
            # Configurar codificación UTF-8 para manejar caracteres especiales
            csv = df_filtrado.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label="Descargar CSV",
                data=csv,
                file_name=f"datos_interoperabilidad_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                help="Archivo CSV con codificación UTF-8 para manejar caracteres especiales"
            )

with col2:
    if st.button("📈 Exportar Gráficos (PNG)"):
        st.info("Los gráficos se pueden descargar individualmente haciendo clic derecho sobre ellos")

with col3:
    if st.button("📋 Generar Reporte PDF"):
        st.info("Para generar reportes PDF completos, ejecute el script 'entity_reports.py'")

# Información del sistema
st.sidebar.header("Información del Sistema")
st.sidebar.info(f"""
**Estadísticas del Filtro Actual:**
- Entidades: {len(df_filtrado)}
- Sectores: {df_filtrado['Sector'].nunique()}
- Madurez Promedio: {df_filtrado['Nivel_Madurez'].mean():.2f}
- X-Road: {xroad_conectadas}/{len(df_filtrado)} ({xroad_conectadas/len(df_filtrado)*100:.1f}%)
- SCD: {scd_conectadas}/{len(df_filtrado)} ({scd_conectadas/len(df_filtrado)*100:.1f}%)
""")

st.sidebar.markdown("---")
st.sidebar.caption("Dashboard desarrollado con Streamlit | Análisis científico de interoperabilidad")
