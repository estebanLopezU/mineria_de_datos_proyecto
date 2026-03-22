#!/usr/bin/env python3
"""
Generador de Documentos de Nivel de Madurez
Análisis de Interoperabilidad en Sector Público Colombiano
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime
import os
import json

class MaturityDocumentGenerator:
    def __init__(self, data_source='entidades_sample.csv'):
        """
        Inicializa el generador de documentos de madurez
        """
        self.data_source = data_source
        self.df = self.load_data()
        self.sector_benchmarks = self.calculate_sector_benchmarks()
        
    def load_data(self):
        """Carga los datos de entidades"""
        try:
            df = pd.read_csv(self.data_source)
            print(f"✓ Datos cargados desde {self.data_source}")
            return df
        except FileNotFoundError:
            print(f"✗ No se encontró el archivo {self.data_source}")
            return None
    
    def calculate_sector_benchmarks(self):
        """Calcula benchmarks por sector"""
        if self.df is None:
            return {}
        
        sector_stats = self.df.groupby('Sector').agg({
            'Nivel_Madurez': ['mean', 'std', 'min', 'max', 'count'],
            'Conectado_X_Road': lambda x: (x == 'Sí').sum(),
            'Conectado_SCD': lambda x: (x == 'Sí').sum()
        })
        
        sector_stats.columns = ['madurez_media', 'desv_estandar', 'minimo', 'maximo', 'total_entidades', 'xroad_conectadas', 'scd_conectadas']
        sector_stats['porcentaje_xroad'] = (sector_stats['xroad_conectadas'] / sector_stats['total_entidades'] * 100).round(1)
        sector_stats['porcentaje_scd'] = (sector_stats['scd_conectadas'] / sector_stats['total_entidades'] * 100).round(1)
        
        return sector_stats.to_dict('index')
    
    def generate_sector_maturity_document(self, sector_name):
        """Genera documento de madurez para un sector específico"""
        if sector_name not in self.sector_benchmarks:
            print(f"✗ Sector '{sector_name}' no encontrado")
            return None
        
        sector_data = self.df[self.df['Sector'] == sector_name]
        benchmark = self.sector_benchmarks[sector_name]
        
        # Análisis estadístico del sector
        stats_analysis = self.analyze_sector_statistics(sector_data, benchmark)
        
        # Generar visualizaciones
        viz_files = self.generate_sector_visualizations(sector_name, sector_data, benchmark)
        
        # Generar documento
        doc_content = self.create_sector_document(sector_name, sector_data, benchmark, stats_analysis, viz_files)
        
        return doc_content
    
    def analyze_sector_statistics(self, sector_data, benchmark):
        """Realiza análisis estadístico detallado del sector"""
        stats = {
            'total_entidades': len(sector_data),
            'madurez_media': sector_data['Nivel_Madurez'].mean(),
            'madurez_mediana': sector_data['Nivel_Madurez'].median(),
            'madurez_moda': sector_data['Nivel_Madurez'].mode().iloc[0] if not sector_data['Nivel_Madurez'].mode().empty else None,
            'desviacion_estandar': sector_data['Nivel_Madurez'].std(),
            'varianza': sector_data['Nivel_Madurez'].var(),
            'coeficiente_variacion': sector_data['Nivel_Madurez'].std() / sector_data['Nivel_Madurez'].mean() if sector_data['Nivel_Madurez'].mean() > 0 else 0,
            'rango': sector_data['Nivel_Madurez'].max() - sector_data['Nivel_Madurez'].min(),
            'cuartiles': {
                'Q1': sector_data['Nivel_Madurez'].quantile(0.25),
                'Q2': sector_data['Nivel_Madurez'].quantile(0.5),
                'Q3': sector_data['Nivel_Madurez'].quantile(0.75)
            },
            'asimetria': sector_data['Nivel_Madurez'].skew(),
            'kurtosis': sector_data['Nivel_Madurez'].kurtosis()
        }
        
        # Análisis de conectividad
        stats['conectividad'] = {
            'xroad_conectadas': len(sector_data[sector_data['Conectado_X_Road'] == 'Sí']),
            'scd_conectadas': len(sector_data[sector_data['Conectado_SCD'] == 'Sí']),
            'xroad_porcentaje': (len(sector_data[sector_data['Conectado_X_Road'] == 'Sí']) / len(sector_data) * 100),
            'scd_porcentaje': (len(sector_data[sector_data['Conectado_SCD'] == 'Sí']) / len(sector_data) * 100),
            'conectividad_total': len(sector_data[(sector_data['Conectado_X_Road'] == 'Sí') | (sector_data['Conectado_SCD'] == 'Sí')])
        }
        
        # Clasificación de entidades por nivel de madurez
        stats['distribucion_madurez'] = {
            'nivel_1': len(sector_data[sector_data['Nivel_Madurez'] == 1]),
            'nivel_2': len(sector_data[sector_data['Nivel_Madurez'] == 2]),
            'nivel_3': len(sector_data[sector_data['Nivel_Madurez'] == 3]),
            'nivel_4': len(sector_data[sector_data['Nivel_Madurez'] == 4]),
            'nivel_5': len(sector_data[sector_data['Nivel_Madurez'] == 5])
        }
        
        return stats
    
    def generate_sector_visualizations(self, sector_name, sector_data, benchmark):
        """Genera visualizaciones científicas para el sector"""
        viz_files = {}
        
        # 1. Distribución de madurez con estadísticas
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle(f'Análisis Científico de Madurez - Sector {sector_name}', fontsize=16, fontweight='bold')
        
        # Histograma con estadísticas
        ax1 = axes[0, 0]
        sns.histplot(sector_data['Nivel_Madurez'], kde=True, ax=ax1, color='steelblue', alpha=0.7)
        ax1.axvline(sector_data['Nivel_Madurez'].mean(), color='red', linestyle='--', linewidth=2, 
                  label=f'Media: {sector_data["Nivel_Madurez"].mean():.2f}')
        ax1.axvline(sector_data['Nivel_Madurez'].median(), color='green', linestyle='-', linewidth=2,
                  label=f'Mediana: {sector_data["Nivel_Madurez"].median():.2f}')
        ax1.axvline(benchmark['madurez_media'], color='orange', linestyle='-.', linewidth=2,
                  label=f'Benchmark: {benchmark["madurez_media"]:.2f}')
        ax1.set_title('Distribución de Niveles de Madurez', fontweight='bold')
        ax1.set_xlabel('Nivel de Madurez')
        ax1.set_ylabel('Frecuencia')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Box plot
        ax2 = axes[0, 1]
        sns.boxplot(data=sector_data, y='Nivel_Madurez', ax=ax2, color='lightseagreen')
        ax2.set_title('Distribución por Cuartiles', fontweight='bold')
        ax2.set_ylabel('Nivel de Madurez')
        
        # Distribución por niveles
        ax3 = axes[1, 0]
        madurez_counts = sector_data['Nivel_Madurez'].value_counts().sort_index()
        bars = ax3.bar(madurez_counts.index, madurez_counts.values, color='skyblue', alpha=0.8)
        ax3.set_title('Frecuencia por Nivel de Madurez', fontweight='bold')
        ax3.set_xlabel('Nivel de Madurez')
        ax3.set_ylabel('Número de Entidades')
        ax3.set_xticks(range(1, 6))
        
        # Añadir valores encima de las barras
        for bar in bars:
            height = bar.get_height()
            ax3.text(bar.get_x() + bar.get_width()/2., height + 0.05,
                    f'{int(height)}', ha='center', va='bottom', fontweight='bold')
        
        # Radar de conectividad
        ax4 = axes[1, 1]
        categories = ['X-Road\nConectado', 'SCD\nConectado', 'Madurez\nMedia', 'Benchmark\nSectorial']
        values = [
            benchmark['porcentaje_xroad'] / 100,
            benchmark['porcentaje_scd'] / 100,
            benchmark['madurez_media'] / 5,
            benchmark['madurez_media'] / 5  # Mismo valor para comparación
        ]
        
        angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
        values += values[:1]
        angles += angles[:1]
        
        ax4 = plt.subplot(2, 2, 4, projection='polar')
        ax4.plot(angles, values, 'o-', linewidth=2, color='purple')
        ax4.fill(angles, values, alpha=0.25, color='purple')
        ax4.set_xticks(angles[:-1])
        ax4.set_xticklabels(categories)
        ax4.set_ylim(0, 1)
        ax4.set_title('Indicadores Clave del Sector', fontweight='bold', pad=20)
        
        plt.tight_layout()
        
        # Guardar visualización
        output_dir = 'documentos_madurez'
        os.makedirs(output_dir, exist_ok=True)
        filename = f"{output_dir}/sector_{sector_name.replace(' ', '_')}_analisis.png"
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        
        viz_files['analisis_completo'] = filename
        
        # Gráfico individual de distribución
        plt.figure(figsize=(10, 6))
        madurez_counts = sector_data['Nivel_Madurez'].value_counts().sort_index()
        plt.bar(madurez_counts.index, madurez_counts.values, color='lightcoral', alpha=0.8)
        plt.title(f'Distribución de Niveles de Madurez - Sector {sector_name}', fontsize=14, fontweight='bold')
        plt.xlabel('Nivel de Madurez (Modelo MinTIC)')
        plt.ylabel('Número de Entidades')
        plt.xticks(range(1, 6))
        plt.grid(axis='y', alpha=0.3)
        
        # Añadir porcentajes
        total = len(sector_data)
        for i, count in madurez_counts.items():
            percentage = (count / total) * 100
            plt.text(i, count + 0.1, f'{count} ({percentage:.1f}%)', 
                    ha='center', va='bottom', fontweight='bold')
        
        filename2 = f"{output_dir}/sector_{sector_name.replace(' ', '_')}_distribucion.png"
        plt.savefig(filename2, dpi=300, bbox_inches='tight')
        plt.close()
        
        viz_files['distribucion'] = filename2
        
        return viz_files
    
    def create_sector_document(self, sector_name, sector_data, benchmark, stats, viz_files):
        """Crea documento de madurez para el sector"""
        
        # Calcular percentiles y posición relativa
        percentil_25 = stats['cuartiles']['Q1']
        percentil_50 = stats['cuartiles']['Q2']
        percentil_75 = stats['cuartiles']['Q3']
        
        # Clasificación del sector
        if stats['madurez_media'] >= 4.0:
            clasificacion = "Excelente (Nivel Avanzado-Optimizado)"
            color_clasificacion = "🟢"
        elif stats['madurez_media'] >= 3.0:
            clasificacion = "Bueno (Nivel Intermedio-Avanzado)"
            color_clasificacion = "🟡"
        elif stats['madurez_media'] >= 2.0:
            clasificacion = "Regular (Nivel Básico-Intermedio)"
            color_clasificacion = "🟠"
        else:
            clasificacion = "Crítico (Nivel Inicial-Básico)"
            color_clasificacion = "🔴"
        
        # Análisis de distribución
        distribucion_text = ""
        if stats['asimetria'] > 0.5:
            distribucion_text = "Asimétrica hacia la derecha (mayor concentración en niveles bajos)"
        elif stats['asimetria'] < -0.5:
            distribucion_text = "Asimétrica hacia la izquierda (mayor concentración en niveles altos)"
        else:
            distribucion_text = "Distribución relativamente simétrica"
        
        # Contenido del documento
        document = f"""# Documento de Nivel de Madurez - Sector {sector_name}

**Fecha de generación:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Metodología:** Modelo de Madurez MinTIC para Gobierno Digital
**Alcance:** {len(sector_data)} entidades del sector {sector_name}

## Resumen Ejecutivo

{color_clasificacion} **Clasificación del Sector:** {clasificacion}

- **Madurez Promedio:** {stats['madurez_media']:.2f}/5
- **Desviación Estándar:** {stats['desviacion_estandar']:.2f}
- **Coeficiente de Variación:** {stats['coeficiente_variacion']:.2f}
- **Entidades con X-Road:** {stats['conectividad']['xroad_porcentaje']:.1f}%
- **Entidades con SCD:** {stats['conectividad']['scd_porcentaje']:.1f}%

## Análisis Estadístico Detallado

### Estadísticas Descriptivas

| Estadística | Valor | Interpretación |
|-------------|-------|----------------|
| Media | {stats['madurez_media']:.2f} | Nivel promedio de madurez |
| Mediana | {stats['madurez_mediana']:.2f} | Valor central de la distribución |
| Moda | {stats['madurez_moda']:.0f} | Nivel más frecuente |
| Desviación Estándar | {stats['desviacion_estandar']:.2f} | Dispersión de los datos |
| Varianza | {stats['varianza']:.2f} | Variabilidad de los niveles |
| Rango | {stats['rango']:.0f} | Diferencia entre máximo y mínimo |

### Cuartiles y Percentiles

| Cuartil | Valor | Significado |
|---------|-------|-------------|
| Q1 (25%) | {percentil_25:.2f} | 25% de entidades están por debajo |
| Q2 (50%) | {percentil_50:.2f} | Mediana del sector |
| Q3 (75%) | {percentil_75:.2f} | 75% de entidades están por debajo |

### Distribución de Niveles de Madurez

| Nivel | Entidades | Porcentaje | Interpretación |
|-------|-----------|------------|----------------|
| 1 (Inicial) | {stats['distribucion_madurez']['nivel_1']} | {stats['distribucion_madurez']['nivel_1']/len(sector_data)*100:.1f}% | Entidades con madurez crítica |
| 2 (Básico) | {stats['distribucion_madurez']['nivel_2']} | {stats['distribucion_madurez']['nivel_2']/len(sector_data)*100:.1f}% | Entidades en desarrollo |
| 3 (Intermedio) | {stats['distribucion_madurez']['nivel_3']} | {stats['distribucion_madurez']['nivel_3']/len(sector_data)*100:.1f}% | Entidades con procesos estandarizados |
| 4 (Avanzado) | {stats['distribucion_madurez']['nivel_4']} | {stats['distribucion_madurez']['nivel_4']/len(sector_data)*100:.1f}% | Entidades con interoperabilidad avanzada |
| 5 (Optimizado) | {stats['distribucion_madurez']['nivel_5']} | {stats['distribucion_madurez']['nivel_5']/len(sector_data)*100:.1f}% | Entidades líderes en interoperabilidad |

## Análisis de Conectividad

### Plataforma X-Road

- **Entidades conectadas:** {stats['conectividad']['xroad_conectadas']}/{len(sector_data)} ({stats['conectividad']['xroad_porcentaje']:.1f}%)
- **Benchmark sectorial:** {benchmark['porcentaje_xroad']:.1f}%
- **Estado:** {"✅ Excelente" if stats['conectividad']['xroad_porcentaje'] >= 80 else "🟡 Regular" if stats['conectividad']['xroad_porcentaje'] >= 50 else "🔴 Crítico"}

### Servicios Ciudadanos Digitales (SCD)

- **Entidades conectadas:** {stats['conectividad']['scd_conectadas']}/{len(sector_data)} ({stats['conectividad']['scd_porcentaje']:.1f}%)
- **Benchmark sectorial:** {benchmark['porcentaje_scd']:.1f}%
- **Estado:** {"✅ Excelente" if stats['conectividad']['scd_porcentaje'] >= 80 else "🟡 Regular" if stats['conectividad']['scd_porcentaje'] >= 50 else "🔴 Crítico"}

## Diagnóstico del Sector

### Fortalezas

"""
        
        # Identificar fortalezas
        if stats['madurez_media'] >= 4.0:
            document += "- **Alto nivel de madurez** en la mayoría de entidades\n"
        if stats['conectividad']['xroad_porcentaje'] >= 80:
            document += "- **Excelente conectividad X-Road** para intercambio seguro de datos\n"
        if stats['conectividad']['scd_porcentaje'] >= 80:
            document += "- **Alta adopción de SCD** para servicios ciudadanos\n"
        if stats['coeficiente_variacion'] < 0.3:
            document += "- **Baja variabilidad** en los niveles de madurez (homogeneidad)\n"
        
        document += """
### Áreas de Mejora

"""
        
        # Identificar áreas de mejora
        if stats['madurez_media'] < 3.0:
            document += "- **Nivel de madurez bajo** que requiere atención prioritaria\n"
        if stats['conectividad']['xroad_porcentaje'] < 70:
            document += "- **Baja conectividad X-Road** que limita el intercambio de datos\n"
        if stats['conectividad']['scd_porcentaje'] < 70:
            document += "- **Implementación insuficiente de SCD** para servicios digitales\n"
        if stats['coeficiente_variacion'] > 0.5:
            document += "- **Alta variabilidad** en niveles de madurez (desigualdad)\n"
        if stats['distribucion_madurez']['nivel_1'] > 0:
            document += f"- **{stats['distribucion_madurez']['nivel_1']} entidades** en nivel crítico de madurez\n"
        
        document += f"""
## Recomendaciones Estratégicas

### Prioridad Alta

"""
        
        # Recomendaciones basadas en análisis
        if stats['madurez_media'] < 3.0:
            document += """1. **Implementar programa de capacitación intensiva** para entidades con niveles 1-2
2. **Establecer metas claras de mejora** con seguimiento mensual
3. **Asignar recursos específicos** para mejorar la interoperabilidad
"""
        
        if stats['conectividad']['xroad_porcentaje'] < 70:
            document += """4. **Priorizar conexión a X-Road** para entidades no conectadas
5. **Evaluar requisitos técnicos** para integración segura
"""
        
        if stats['conectividad']['scd_porcentaje'] < 70:
            document += """6. **Implementar Servicios Ciudadanos Digitales** en entidades faltantes
7. **Mejorar experiencia de usuario** en trámites digitales
"""
        
        document += """
### Prioridad Media

"""
        
        if stats['coeficiente_variacion'] > 0.4:
            document += """8. **Establecer políticas de estandarización** para reducir variabilidad
9. **Fomentar buenas prácticas** entre entidades del sector
"""
        
        if stats['distribucion_madurez']['nivel_5'] == 0:
            document += """10. **Identificar entidades líderes** para que sirvan de modelo a seguir
11. **Crear redes de conocimiento** entre entidades del sector
"""
        
        document += """
### Prioridad Baja

"""
        
        if stats['madurez_media'] >= 3.5:
            document += """12. **Explorar oportunidades de innovación** en interoperabilidad
13. **Compartir experiencias exitosas** con otros sectores
"""
        
        document += f"""
## Metodología y Limitaciones

### Metodología

Este análisis se basa en el **Modelo de Madurez del MinTIC** para Gobierno Digital, que considera:

- **Indicadores de conectividad:** X-Road y Servicios Ciudadanos Digitales
- **Niveles de madurez:** Escala del 1 al 5 según capacidades de interoperabilidad
- **Benchmarking sectorial:** Comparación con entidades del mismo sector
- **Análisis estadístico:** Media, mediana, desviación estándar, cuartiles

### Limitaciones

- **Muestra limitada:** Basado en {len(sector_data)} entidades del sector
- **Datos estáticos:** Representa un corte temporal específico
- **Autoevaluación:** Los niveles de madurez pueden estar basados en autoevaluaciones
- **Contexto cambiante:** La interoperabilidad es un proceso continuo de mejora

## Entidades del Sector

"""
        
        # Listar entidades del sector
        for _, entidad in sector_data.iterrows():
            document += f"""
### {entidad['Entidad']}

- **ID:** {entidad['ID']}
- **Nivel de Madurez:** {entidad['Nivel_Madurez']}/5
- **Conectividad X-Road:** {entidad['Conectado_X_Road']}
- **Conectividad SCD:** {entidad['Conectado_SCD']}
- **Posición relativa:** {"Por encima" if entidad['Nivel_Madurez'] > benchmark['madurez_media'] else "Por debajo" if entidad['Nivel_Madurez'] < benchmark['madurez_media'] else "En promedio"} del promedio sectorial ({benchmark['madurez_media']:.2f})

"""
        
        document += f"""
## Visualizaciones

![Análisis Científico del Sector {sector_name}]({viz_files['analisis_completo']})

![Distribución de Niveles de Madurez]({viz_files['distribucion']})

## Conclusiones

El sector {sector_name} presenta un nivel de madurez de interoperabilidad de **{stats['madurez_media']:.2f}/5**, lo que lo sitúa en el rango **{"excelente" if stats['madurez_media'] >= 4.0 else "bueno" if stats['madurez_media'] >= 3.0 else "regular" if stats['madurez_media'] >= 2.0 else "crítico"}**.

**Principales hallazgos:**
- {len(sector_data)} entidades analizadas
- {stats['conectividad']['xroad_porcentaje']:.1f}% de conectividad a X-Road
- {stats['conectividad']['scd_porcentaje']:.1f}% de implementación de SCD
- {distribucion_text}

**Próximos pasos recomendados:**
1. Implementar el plan de mejoras priorizadas
2. Establecer métricas de seguimiento continuo
3. Fomentar la colaboración entre entidades del sector
4. Actualizar este análisis periódicamente

---
*Documento generado automáticamente por el Sistema de Análisis de Interoperabilidad*
*Para consultas o actualizaciones, contactar al equipo de transformación digital*
"""
        
        # Guardar documento
        output_dir = 'documentos_madurez'
        os.makedirs(output_dir, exist_ok=True)
        filename = f"{output_dir}/sector_{sector_name.replace(' ', '_')}_documento_madurez.md"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(document)
        
        return filename
    
    def generate_all_sectors_documents(self):
        """Genera documentos de madurez para todos los sectores"""
        print("Generando documentos de madurez para todos los sectores...")
        
        all_documents = {}
        
        for sector in self.df['Sector'].unique():
            print(f"Generando documento para sector: {sector}")
            doc_file = self.generate_sector_maturity_document(sector)
            if doc_file:
                all_documents[sector] = doc_file
        
        # Generar índice de documentos
        self.generate_documents_index(all_documents)
        
        print(f"✓ Se generaron {len(all_documents)} documentos de madurez")
        return all_documents
    
    def generate_documents_index(self, all_documents):
        """Genera un índice con todos los documentos generados"""
        index_content = """# Índice de Documentos de Nivel de Madurez

Este documento contiene el índice de todos los documentos de madurez generados para los sectores analizados.

## Sectores Analizados

"""
        
        for sector, file_path in all_documents.items():
            index_content += f"""
### Sector {sector}

- **Documento completo:** [Documento de Madurez - {sector}]({file_path})

"""
        
        index_content += """
## Metodología

Todos los documentos se generaron utilizando:

- **Modelo de Madurez MinTIC:** Evaluación estandarizada de nivel de interoperabilidad
- **Análisis estadístico avanzado:** Media, mediana, desviación estándar, cuartiles, distribución
- **Benchmarking sectorial:** Comparación interna entre entidades del mismo sector
- **Visualizaciones científicas:** Gráficos estadísticos avanzados
- **Recomendaciones basadas en datos:** Estrategias específicas para cada sector

## Estructura de los Documentos

Cada documento de madurez contiene:

1. **Resumen Ejecutivo:** Clasificación y métricas clave
2. **Análisis Estadístico:** Estadísticas descriptivas y distribuciones
3. **Diagnóstico del Sector:** Fortalezas y áreas de mejora
4. **Recomendaciones Estratégicas:** Plan de acción priorizado
5. **Entidades del Sector:** Detalle individual de cada entidad
6. **Visualizaciones:** Gráficos científicos del análisis
7. **Conclusiones:** Síntesis y próximos pasos

## Contacto

Para consultas sobre los documentos o el análisis de interoperabilidad:

- **Sistema de Análisis de Interoperabilidad**
- **Fecha de generación:** """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + """
"""
        
        # Guardar índice
        output_dir = 'documentos_madurez'
        os.makedirs(output_dir, exist_ok=True)
        index_file = f"{output_dir}/indice_documentos_madurez.md"
        
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(index_content)
        
        print(f"✓ Índice de documentos guardado en {index_file}")

def main():
    """Función principal"""
    print("GENERADOR DE DOCUMENTOS DE NIVEL DE MADUREZ")
    print("=" * 60)
    
    # Inicializar generador
    generator = MaturityDocumentGenerator()
    
    if generator.df is None:
        print("✗ No se pudieron cargar los datos")
        return
    
    print(f"✓ Base de datos cargada: {len(generator.df)} entidades")
    print(f"✓ Sectores analizados: {generator.df['Sector'].nunique()}")
    
    # Generar todos los documentos
    all_documents = generator.generate_all_sectors_documents()
    
    print("\n" + "=" * 60)
    print("GENERACIÓN DE DOCUMENTOS COMPLETADA")
    print("=" * 60)
    print(f"Archivos generados en: documentos_madurez/")
    print(f"Total de documentos: {len(all_documents)}")
    print("Archivos por sector:")
    print("  - sector_[Nombre]_documento_madurez.md (Documento completo)")
    print("  - sector_[Nombre]_analisis.png (Visualizaciones científicas)")
    print("  - sector_[Nombre]_distribucion.png (Distribución de niveles)")
    print("  - indice_documentos_madurez.md (Índice general)")

if __name__ == "__main__":
    main()