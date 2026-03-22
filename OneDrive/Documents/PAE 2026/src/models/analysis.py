import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Configuración de visualización
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

def load_data():
    """Carga datos reales o simulados según disponibilidad"""
    try:
        df = pd.read_csv('entidades_reales.csv')
        data_source = "Datos reales obtenidos de APIs oficiales"
        print("✓ Cargados datos reales de entidades")
    except FileNotFoundError:
        try:
            df = pd.read_csv('entidades_sample.csv')
            data_source = "Datos simulados basados en información pública"
            print("✓ Cargados datos simulados de entidades")
        except FileNotFoundError:
            print("✗ No se encontraron archivos de datos")
            return None, None
    
    return df, data_source

def descriptive_statistics(df):
    """Estadísticas descriptivas avanzadas"""
    print("\n" + "="*60)
    print("ANÁLISIS ESTADÍSTICO DESCRIPTIVO")
    print("="*60)
    
    # Estadísticas generales
    print(f"\nTotal de entidades analizadas: {len(df)}")
    print(f"Total de sectores: {df['Sector'].nunique()}")
    
    # Conectividad general
    xroad_connected = len(df[df['Conectado_X_Road'] == 'Sí'])
    scd_connected = len(df[df['Conectado_SCD'] == 'Sí'])
    
    print(f"\nConectividad General:")
    print(f"  - Conectadas a X-Road: {xroad_connected} ({xroad_connected/len(df)*100:.1f}%)")
    print(f"  - Conectadas a SCD: {scd_connected} ({scd_connected/len(df)*100:.1f}%)")
    
    # Estadísticas de madurez
    madurez_stats = df['Nivel_Madurez'].describe()
    print(f"\nEstadísticas de Nivel de Madurez:")
    print(f"  - Media: {madurez_stats['mean']:.2f}")
    print(f"  - Mediana: {madurez_stats['50%']:.2f}")
    print(f"  - Desviación estándar: {madurez_stats['std']:.2f}")
    print(f"  - Mínimo: {madurez_stats['min']:.0f}")
    print(f"  - Máximo: {madurez_stats['max']:.0f}")
    
    return madurez_stats

def sector_analysis(df):
    """Análisis detallado por sector"""
    print("\n" + "="*60)
    print("ANÁLISIS POR SECTOR")
    print("="*60)
    
    sector_analysis = df.groupby('Sector').agg({
        'Entidad': 'count',
        'Nivel_Madurez': ['mean', 'std', 'min', 'max'],
        'Conectado_X_Road': lambda x: (x == 'Sí').sum(),
        'Conectado_SCD': lambda x: (x == 'Sí').sum()
    }).round(2)
    
    sector_analysis.columns = ['Número_Entidades', 'Madurez_Media', 'Desv_Estándar', 'Mínimo', 'Máximo', 'X_Road_Conectadas', 'SCD_Conectadas']
    sector_analysis['Porcentaje_X_Road'] = (sector_analysis['X_Road_Conectadas'] / sector_analysis['Número_Entidades'] * 100).round(1)
    sector_analysis['Porcentaje_SCD'] = (sector_analysis['SCD_Conectadas'] / sector_analysis['Número_Entidades'] * 100).round(1)
    
    print("\nResumen por sector:")
    print(sector_analysis.to_string())
    
    # Identificar sectores líderes y rezagados
    sector_leaders = sector_analysis[sector_analysis['Madurez_Media'] >= sector_analysis['Madurez_Media'].quantile(0.75)]
    sector_laggards = sector_analysis[sector_analysis['Madurez_Media'] <= sector_analysis['Madurez_Media'].quantile(0.25)]
    
    print(f"\nSectores líderes (Top 25% en madurez):")
    for sector in sector_leaders.index:
        print(f"  - {sector}: {sector_leaders.loc[sector, 'Madurez_Media']:.2f}")
    
    print(f"\nSectores rezagados (Bottom 25% en madurez):")
    for sector in sector_laggards.index:
        print(f"  - {sector}: {sector_laggards.loc[sector, 'Madurez_Media']:.2f}")
    
    return sector_analysis

def connectivity_analysis(df):
    """Análisis de conectividad y correlaciones"""
    print("\n" + "="*60)
    print("ANÁLISIS DE CONECTIVIDAD Y CORRELACIONES")
    print("="*60)
    
    # Crear variables numéricas para análisis
    df_analysis = df.copy()
    df_analysis['X_Road_Num'] = (df_analysis['Conectado_X_Road'] == 'Sí').astype(int)
    df_analysis['SCD_Num'] = (df_analysis['Conectado_SCD'] == 'Sí').astype(int)
    
    # Correlación entre conectividad y madurez
    corr_xroad_madurez = stats.pearsonr(df_analysis['X_Road_Num'], df_analysis['Nivel_Madurez'])
    corr_scd_madurez = stats.pearsonr(df_analysis['SCD_Num'], df_analysis['Nivel_Madurez'])
    
    print(f"\nCorrelaciones:")
    print(f"  - X-Road vs Madurez: r = {corr_xroad_madurez[0]:.3f}, p = {corr_xroad_madurez[1]:.4f}")
    print(f"  - SCD vs Madurez: r = {corr_scd_madurez[0]:.3f}, p = {corr_scd_madurez[1]:.4f}")
    
    if corr_xroad_madurez[1] < 0.05:
        print(f"  ✓ Correlación significativa entre X-Road y madurez")
    else:
        print(f"  ✗ No hay correlación significativa entre X-Road y madurez")
    
    if corr_scd_madurez[1] < 0.05:
        print(f"  ✓ Correlación significativa entre SCD y madurez")
    else:
        print(f"  ✗ No hay correlación significativa entre SCD y madurez")
    
    # Distribución de conectividad cruzada
    print(f"\nDistribución cruzada de conectividad:")
    cross_table = pd.crosstab(df['Conectado_X_Road'], df['Conectado_SCD'])
    print(cross_table)
    
    return df_analysis

def bottleneck_analysis(df):
    """Análisis de cuellos de botella"""
    print("\n" + "="*60)
    print("ANÁLISIS DE CUELLOS DE BOTELLA")
    print("="*60)
    
    # Entidades con baja madurez
    low_maturity = df[df['Nivel_Madurez'] <= 2]
    print(f"\nEntidades con baja madurez (niveles 1-2): {len(low_maturity)}")
    if not low_maturity.empty:
        print(low_maturity[['Entidad', 'Sector', 'Nivel_Madurez']].to_string(index=False))
        print("  Recomendación: Capacitación intensiva en X-Road y estandarización semántica.")
    
    # Entidades completamente desconectadas
    disconnected = df[(df['Conectado_X_Road'] == 'No') & (df['Conectado_SCD'] == 'No')]
    print(f"\nEntidades completamente desconectadas: {len(disconnected)}")
    if not disconnected.empty:
        print(disconnected[['Entidad', 'Sector']].to_string(index=False))
        print("  Recomendación: Integración prioritaria a plataformas interoperables.")
    
    # Entidades con conectividad parcial
    partial_xroad = df[(df['Conectado_X_Road'] == 'Sí') & (df['Conectado_SCD'] == 'No')]
    partial_scd = df[(df['Conectado_X_Road'] == 'No') & (df['Conectado_SCD'] == 'Sí')]
    
    print(f"\nEntidades con conectividad parcial:")
    print(f"  - Solo X-Road: {len(partial_xroad)}")
    print(f"  - Solo SCD: {len(partial_scd)}")
    
    if not partial_xroad.empty:
        print("  Recomendación para entidades solo en X-Road: Integrar servicios ciudadanos digitales.")
    if not partial_scd.empty:
        print("  Recomendación para entidades solo en SCD: Conectar a X-Road para intercambio seguro.")

def advanced_visualizations(df):
    """Genera visualizaciones científicas avanzadas"""
    print("\n" + "="*60)
    print("GENERANDO VISUALIZACIONES CIENTÍFICAS")
    print("="*60)
    
    # Configurar subplots
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.suptitle('Análisis Científico de Interoperabilidad en Sector Público Colombiano', fontsize=16, fontweight='bold')
    
    # 1. Distribución de madurez con estadísticas
    ax1 = axes[0, 0]
    sns.histplot(df['Nivel_Madurez'], kde=True, ax=ax1, color='skyblue', alpha=0.7)
    ax1.axvline(df['Nivel_Madurez'].mean(), color='red', linestyle='--', label=f'Media: {df["Nivel_Madurez"].mean():.2f}')
    ax1.axvline(df['Nivel_Madurez'].median(), color='green', linestyle='--', label=f'Mediana: {df["Nivel_Madurez"].median():.2f}')
    ax1.set_title('Distribución de Niveles de Madurez', fontweight='bold')
    ax1.set_xlabel('Nivel de Madurez')
    ax1.set_ylabel('Frecuencia')
    ax1.legend()
    
    # 2. Box plot por sector
    ax2 = axes[0, 1]
    sns.boxplot(data=df, x='Sector', y='Nivel_Madurez', ax=ax2)
    ax2.set_title('Distribución de Madurez por Sector', fontweight='bold')
    ax2.set_xlabel('Sector')
    ax2.set_ylabel('Nivel de Madurez')
    ax2.tick_params(axis='x', rotation=45)
    
    # 3. Heatmap de correlación
    ax3 = axes[0, 2]
    df_corr = df.copy()
    df_corr['X_Road_Num'] = (df_corr['Conectado_X_Road'] == 'Sí').astype(int)
    df_corr['SCD_Num'] = (df_corr['Conectado_SCD'] == 'Sí').astype(int)
    correlation_matrix = df_corr[['Nivel_Madurez', 'X_Road_Num', 'SCD_Num']].corr()
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0, ax=ax3)
    ax3.set_title('Mapa de Correlación', fontweight='bold')
    
    # 4. Sunburst de conectividad (simulado con pie charts)
    ax4 = axes[1, 0]
    connectivity_data = pd.crosstab(df['Conectado_X_Road'], df['Conectado_SCD'])
    connectivity_data.plot(kind='bar', stacked=True, ax=ax4, color=['lightblue', 'lightcoral'])
    ax4.set_title('Conectividad Cruzada X-Road vs SCD', fontweight='bold')
    ax4.set_xlabel('Conectado a X-Road')
    ax4.set_ylabel('Número de Entidades')
    ax4.legend(['No SCD', 'Sí SCD'])
    
    # 5. Violin plot por sector
    ax5 = axes[1, 1]
    sns.violinplot(data=df, x='Sector', y='Nivel_Madurez', ax=ax5)
    ax5.set_title('Distribución Detallada por Sector', fontweight='bold')
    ax5.set_xlabel('Sector')
    ax5.set_ylabel('Nivel de Madurez')
    ax5.tick_params(axis='x', rotation=45)
    
    # 6. Radar chart de sectores
    ax6 = axes[1, 2]
    sector_means = df.groupby('Sector')['Nivel_Madurez'].mean()
    sectors = sector_means.index.tolist()
    values = sector_means.values.tolist()
    
    # Crear radar chart
    angles = np.linspace(0, 2 * np.pi, len(sectors), endpoint=False).tolist()
    values += values[:1]  # Cerrar el gráfico
    angles += angles[:1]
    
    ax6 = plt.subplot(2, 3, 6, projection='polar')
    ax6.plot(angles, values, 'o-', linewidth=2)
    ax6.fill(angles, values, alpha=0.25)
    ax6.set_thetagrids(np.degrees(angles[:-1]), sectors)
    ax6.set_title('Radar de Madurez por Sector', fontweight='bold', pad=20)
    ax6.grid(True)
    
    plt.tight_layout()
    plt.savefig('analisis_cientifico.png', dpi=300, bbox_inches='tight')
    print("✓ Gráfico científico guardado en 'analisis_cientifico.png'")
    
    # Gráfico individual de madurez
    plt.figure(figsize=(10, 6))
    madurez_counts = df['Nivel_Madurez'].value_counts().sort_index()
    plt.bar(madurez_counts.index, madurez_counts.values, color='steelblue', alpha=0.7)
    plt.title('Distribución de Niveles de Madurez en Interoperabilidad', fontsize=14, fontweight='bold')
    plt.xlabel('Nivel de Madurez (Modelo MinTIC)')
    plt.ylabel('Número de Entidades')
    plt.xticks(range(1, 6))
    plt.grid(axis='y', alpha=0.3)
    plt.savefig('madurez_plot_cientifico.png', dpi=300, bbox_inches='tight')
    print("✓ Gráfico de madurez guardado en 'madurez_plot_cientifico.png'")
    
    # Gráfico por sector
    plt.figure(figsize=(12, 6))
    sector_summary = df.groupby('Sector')['Nivel_Madurez'].mean().sort_values(ascending=False)
    bars = plt.bar(sector_summary.index, sector_summary.values, color='lightseagreen', alpha=0.8)
    plt.title('Madurez Promedio por Sector', fontsize=14, fontweight='bold')
    plt.xlabel('Sector')
    plt.ylabel('Madurez Promedio')
    plt.xticks(rotation=45, ha='right')
    
    # Añadir valores encima de las barras
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.05,
                f'{height:.2f}', ha='center', va='bottom')
    
    plt.tight_layout()
    plt.savefig('sector_plot_cientifico.png', dpi=300, bbox_inches='tight')
    print("✓ Gráfico por sector guardado en 'sector_plot_cientifico.png'")

def generate_report(df, madurez_stats, sector_analysis_df, df_analysis):
    """Genera un reporte científico detallado"""
    print("\n" + "="*60)
    print("GENERANDO REPORTES CIENTÍFICOS")
    print("="*60)
    
    # Reporte estadístico
    report = {
        'fecha_analisis': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S'),
        'total_entidades': len(df),
        'total_sectores': df['Sector'].nunique(),
        'estadisticas_madurez': {
            'media': float(madurez_stats['mean']),
            'mediana': float(madurez_stats['50%']),
            'desviacion_estandar': float(madurez_stats['std']),
            'minimo': int(madurez_stats['min']),
            'maximo': int(madurez_stats['max'])
        },
        'conectividad': {
            'xroad_conectadas': int((df['Conectado_X_Road'] == 'Sí').sum()),
            'scd_conectadas': int((df['Conectado_SCD'] == 'Sí').sum()),
            'porcentaje_xroad': float((df['Conectado_X_Road'] == 'Sí').sum() / len(df) * 100),
            'porcentaje_scd': float((df['Conectado_SCD'] == 'Sí').sum() / len(df) * 100)
        },
        'sectores': sector_analysis_df.to_dict('index'),
        'correlaciones': {
            'xroad_madurez_r': float(stats.pearsonr(df_analysis['X_Road_Num'], df_analysis['Nivel_Madurez'])[0]),
            'xroad_madurez_p': float(stats.pearsonr(df_analysis['X_Road_Num'], df_analysis['Nivel_Madurez'])[1]),
            'scd_madurez_r': float(stats.pearsonr(df_analysis['SCD_Num'], df_analysis['Nivel_Madurez'])[0]),
            'scd_madurez_p': float(stats.pearsonr(df_analysis['SCD_Num'], df_analysis['Nivel_Madurez'])[1])
        }
    }
    
    # Guardar reporte JSON
    with open('reporte_estadistico.json', 'w', encoding='utf-8') as f:
        import json
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    # Generar reporte en Markdown
    markdown_report = f"""# Reporte Científico de Interoperabilidad en Sector Público Colombiano

**Fecha de análisis:** {report['fecha_analisis']}

## Resumen Ejecutivo

Se analizaron **{report['total_entidades']} entidades** pertenecientes a **{report['total_sectores']} sectores** diferentes.

### Principales Hallazgos

- **Nivel de madurez promedio:** {report['estadisticas_madurez']['media']:.2f} (escala 1-5)
- **Mediana de madurez:** {report['estadisticas_madurez']['mediana']:.2f}
- **Desviación estándar:** {report['estadisticas_madurez']['desviacion_estandar']:.2f}
- **Conectividad a X-Road:** {report['conectividad']['porcentaje_xroad']:.1f}% de las entidades
- **Conectividad a SCD:** {report['conectividad']['porcentaje_scd']:.1f}% de las entidades

## Análisis Estadístico Detallado

### Distribución de Niveles de Madurez

| Nivel | Frecuencia | Porcentaje |
|-------|------------|------------|
"""
    
    for nivel in range(1, 6):
        frecuencia = len(df[df['Nivel_Madurez'] == nivel])
        porcentaje = (frecuencia / len(df)) * 100
        markdown_report += f"| {nivel} | {frecuencia} | {porcentaje:.1f}% |\n"
    
    markdown_report += f"""

### Sectores Analizados

"""
    
    for sector, data in report['sectores'].items():
        markdown_report += f"""
#### {sector}
- **Número de entidades:** {data['Número_Entidades']}
- **Madurez promedio:** {data['Madurez_Media']:.2f}
- **Desviación estándar:** {data['Desv_Estándar']:.2f}
- **Conectividad X-Road:** {data['Porcentaje_X_Road']:.1f}%
- **Conectividad SCD:** {data['Porcentaje_SCD']:.1f}%
"""
    
    markdown_report += f"""

## Correlaciones Estadísticas

- **X-Road vs Madurez:** r = {report['correlaciones']['xroad_madurez_r']:.3f}, p = {report['correlaciones']['xroad_madurez_p']:.4f}
- **SCD vs Madurez:** r = {report['correlaciones']['scd_madurez_r']:.3f}, p = {report['correlaciones']['scd_madurez_p']:.4f}

"""
    
    if report['correlaciones']['xroad_madurez_p'] < 0.05:
        markdown_report += "✓ **Correlación significativa** entre conectividad X-Road y nivel de madurez.\n"
    else:
        markdown_report += "✗ **No hay correlación significativa** entre conectividad X-Road y nivel de madurez.\n"
    
    if report['correlaciones']['scd_madurez_p'] < 0.05:
        markdown_report += "✓ **Correlación significativa** entre conectividad SCD y nivel de madurez.\n"
    else:
        markdown_report += "✗ **No hay correlación significativa** entre conectividad SCD y nivel de madurez.\n"
    
    markdown_report += """

## Recomendaciones Estratégicas

1. **Fortalecer la conectividad:** Incrementar la adopción de X-Road y SCD en sectores con baja penetración.
2. **Capacitación sectorial:** Enfocar esfuerzos en sectores con niveles de madurez bajos (1-2).
3. **Estandarización semántica:** Implementar ontologías comunes para mejorar la interoperabilidad.
4. **Monitoreo continuo:** Establecer métricas de seguimiento para evaluar el progreso.

## Metodología

Este análisis utiliza técnicas estadísticas descriptivas e inferenciales, incluyendo:
- Estadísticas descriptivas (media, mediana, desviación estándar)
- Análisis de correlación de Pearson
- Distribuciones por sector
- Visualizaciones científicas (histogramas, box plots, heatmaps)

"""
    
    with open('reporte_cientifico.md', 'w', encoding='utf-8') as f:
        f.write(markdown_report)
    
    print("✓ Reporte estadístico JSON guardado en 'reporte_estadistico.json'")
    print("✓ Reporte científico en Markdown guardado en 'reporte_cientifico.md'")

def main():
    """Función principal del análisis estadístico avanzado"""
    print("INICIANDO ANÁLISIS ESTADÍSTICO CIENTÍFICO DE INTEROPERABILIDAD")
    print("="*60)
    
    # Cargar datos
    df, data_source = load_data()
    if df is None:
        return
    
    print(f"Fuente de datos: {data_source}")
    
    # Realizar análisis
    madurez_stats = descriptive_statistics(df)
    sector_analysis_df = sector_analysis(df)
    df_analysis = connectivity_analysis(df)
    bottleneck_analysis(df)
    
    # Generar visualizaciones
    advanced_visualizations(df)
    
    # Generar reportes
    generate_report(df, madurez_stats, sector_analysis_df, df_analysis)
    
    print("\n" + "="*60)
    print("ANÁLISIS ESTADÍSTICO COMPLETADO EXITOSAMENTE")
    print("="*60)
    print("Archivos generados:")
    print("  - analisis_cientifico.png (visualizaciones avanzadas)")
    print("  - madurez_plot_cientifico.png (distribución de madurez)")
    print("  - sector_plot_cientifico.png (madurez por sector)")
    print("  - reporte_estadistico.json (datos numéricos)")
    print("  - reporte_cientifico.md (reporte detallado)")

if __name__ == "__main__":
    main()
