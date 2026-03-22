#!/usr/bin/env python3
"""
Generador de Reportes Individuales por Entidad
Análisis de Interoperabilidad en Sector Público Colombiano
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime
import os
import json

class EntityReportGenerator:
    def __init__(self, data_source='entidades_sample.csv'):
        """
        Inicializa el generador de reportes
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
            'Nivel_Madurez': ['mean', 'std', 'min', 'max'],
            'Conectado_X_Road': lambda x: (x == 'Sí').sum(),
            'Conectado_SCD': lambda x: (x == 'Sí').sum()
        })
        
        sector_stats.columns = ['madurez_media', 'desv_estandar', 'minimo', 'maximo', 'xroad_conectadas', 'scd_conectadas']
        sector_stats['total_entidades'] = self.df.groupby('Sector').size()
        sector_stats['porcentaje_xroad'] = (sector_stats['xroad_conectadas'] / sector_stats['total_entidades'] * 100).round(1)
        sector_stats['porcentaje_scd'] = (sector_stats['scd_conectadas'] / sector_stats['total_entidades'] * 100).round(1)
        
        return sector_stats.to_dict('index')
    
    def analyze_entity(self, entity_name):
        """Analiza una entidad específica"""
        entity_data = self.df[self.df['Entidad'] == entity_name]
        
        if entity_data.empty:
            return None
        
        entity = entity_data.iloc[0]
        sector = entity['Sector']
        sector_benchmark = self.sector_benchmarks.get(sector, {})
        
        # Análisis comparativo
        comparison = {
            'entidad': entity_name,
            'sector': sector,
            'nivel_madurez': entity['Nivel_Madurez'],
            'sector_media': sector_benchmark.get('madurez_media', 0),
            'sector_desv': sector_benchmark.get('desv_estandar', 0),
            'posicion_relativa': self.calculate_relative_position(entity['Nivel_Madurez'], sector_benchmark),
            'conectividad': {
                'xroad': entity['Conectado_X_Road'],
                'scd': entity['Conectado_SCD'],
                'sector_xroad_pct': sector_benchmark.get('porcentaje_xroad', 0),
                'sector_scd_pct': sector_benchmark.get('porcentaje_scd', 0)
            }
        }
        
        return comparison
    
    def calculate_relative_position(self, entity_maturity, sector_benchmark):
        """Calcula la posición relativa de la entidad en su sector"""
        if not sector_benchmark:
            return "Sin datos de comparación"
        
        media = sector_benchmark.get('madurez_media', 0)
        desv = sector_benchmark.get('desv_estandar', 0)
        
        if entity_maturity >= media + desv:
            return "Excelente (Por encima del promedio)"
        elif entity_maturity >= media:
            return "Bueno (Por encima del promedio)"
        elif entity_maturity >= media - desv:
            return "Regular (Cercano al promedio)"
        else:
            return "Necesita mejora (Por debajo del promedio)"
    
    def generate_entity_visualization(self, entity_name, comparison):
        """Genera visualización específica para una entidad"""
        if comparison is None:
            return
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle(f'Análisis Detallado: {entity_name}', fontsize=16, fontweight='bold')
        
        # 1. Posición relativa en el sector
        ax1 = axes[0, 0]
        sector_data = self.df[self.df['Sector'] == comparison['sector']]['Nivel_Madurez']
        sns.histplot(sector_data, kde=True, ax=ax1, color='lightblue', alpha=0.7, label='Sector')
        ax1.axvline(comparison['nivel_madurez'], color='red', linestyle='--', linewidth=3, 
                   label=f'{entity_name}: {comparison["nivel_madurez"]}')
        ax1.axvline(comparison['sector_media'], color='green', linestyle='-', linewidth=2,
                   label=f'Promedio sector: {comparison["sector_media"]:.2f}')
        ax1.set_title(f'Posición en el Sector {comparison["sector"]}', fontweight='bold')
        ax1.set_xlabel('Nivel de Madurez')
        ax1.set_ylabel('Frecuencia')
        ax1.legend()
        
        # 2. Comparación de conectividad
        ax2 = axes[0, 1]
        categories = ['X-Road', 'SCD']
        entity_values = [1 if comparison['conectividad']['xroad'] == 'Sí' else 0,
                        1 if comparison['conectividad']['scd'] == 'Sí' else 0]
        sector_values = [comparison['conectividad']['sector_xroad_pct']/100,
                        comparison['conectividad']['sector_scd_pct']/100]
        
        x = np.arange(len(categories))
        width = 0.35
        
        ax2.bar(x - width/2, entity_values, width, label=entity_name, alpha=0.8)
        ax2.bar(x + width/2, sector_values, width, label=f'Promedio {comparison["sector"]}', alpha=0.8)
        ax2.set_title('Conectividad vs Promedio Sectorial', fontweight='bold')
        ax2.set_ylabel('Conectividad')
        ax2.set_xticks(x)
        ax2.set_xticklabels(categories)
        ax2.set_ylim(0, 1.1)
        ax2.legend()
        ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{y:.0%}'))
        
        # 3. Radar de fortalezas
        ax3 = axes[1, 0]
        categories_radar = ['Madurez', 'X-Road', 'SCD', 'Sector\nPromedio']
        values_radar = [
            comparison['nivel_madurez'] / 5,  # Normalizar a 0-1
            1 if comparison['conectividad']['xroad'] == 'Sí' else 0,
            1 if comparison['conectividad']['scd'] == 'Sí' else 0,
            comparison['sector_media'] / 5
        ]
        
        angles = np.linspace(0, 2 * np.pi, len(categories_radar), endpoint=False).tolist()
        values_radar += values_radar[:1]  # Cerrar el gráfico
        angles += angles[:1]
        
        ax3 = plt.subplot(2, 2, 3, projection='polar')
        ax3.plot(angles, values_radar, 'o-', linewidth=2, label=entity_name)
        ax3.fill(angles, values_radar, alpha=0.25)
        ax3.set_xticks(angles[:-1])
        ax3.set_xticklabels(categories_radar)
        ax3.set_ylim(0, 1)
        ax3.set_title('Perfil de Interoperabilidad', fontweight='bold', pad=20)
        ax3.legend()
        
        # 4. Recomendaciones visualizadas
        ax4 = axes[1, 1]
        recommendations = self.get_recommendations(comparison)
        ax4.text(0.1, 0.9, f'Análisis de {entity_name}', fontsize=14, fontweight='bold', transform=ax4.transAxes)
        ax4.text(0.1, 0.8, f'Sector: {comparison["sector"]}', fontsize=12, transform=ax4.transAxes)
        ax4.text(0.1, 0.7, f'Nivel de Madurez: {comparison["nivel_madurez"]}/5', fontsize=12, transform=ax4.transAxes)
        ax4.text(0.1, 0.6, f'Posición: {comparison["posicion_relativa"]}', fontsize=12, transform=ax4.transAxes)
        
        ax4.text(0.1, 0.45, 'Recomendaciones Clave:', fontsize=12, fontweight='bold', transform=ax4.transAxes)
        for i, rec in enumerate(recommendations[:4]):  # Mostrar máximo 4 recomendaciones
            ax4.text(0.1, 0.4 - i*0.08, f'• {rec}', fontsize=11, transform=ax4.transAxes)
        
        ax4.set_xlim(0, 1)
        ax4.set_ylim(0, 1)
        ax4.axis('off')
        
        plt.tight_layout()
        
        # Crear directorio si no existe
        output_dir = 'reportes_entidades'
        os.makedirs(output_dir, exist_ok=True)
        
        filename = f"{output_dir}/{entity_name.replace(' ', '_').replace('/', '_')}_analisis.png"
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        
        return filename
    
    def get_recommendations(self, comparison):
        """Genera recomendaciones basadas en el análisis"""
        recommendations = []
        
        # Recomendaciones basadas en nivel de madurez
        if comparison['nivel_madurez'] <= 2:
            recommendations.append("Priorizar capacitación en X-Road y estandarización semántica")
            recommendations.append("Implementar plan de mejora continua de interoperabilidad")
            recommendations.append("Establecer metas claras de madurez a corto y mediano plazo")
        elif comparison['nivel_madurez'] <= 3:
            recommendations.append("Fortalecer procesos de estandarización de datos")
            recommendations.append("Mejorar integración con otras entidades del sector")
            recommendations.append("Implementar métricas de seguimiento de interoperabilidad")
        else:
            recommendations.append("Mantener y mejorar los procesos de interoperabilidad existentes")
            recommendations.append("Compartir mejores prácticas con otras entidades del sector")
            recommendations.append("Explorar oportunidades de innovación en interoperabilidad")
        
        # Recomendaciones basadas en conectividad
        if comparison['conectividad']['xroad'] == 'No':
            recommendations.append("Conectar prioritariamente a la plataforma X-Road")
            recommendations.append("Evaluar requisitos técnicos para integración segura")
        
        if comparison['conectividad']['scd'] == 'No':
            recommendations.append("Integrar servicios ciudadanos digitales")
            recommendations.append("Mejorar experiencia de usuario en trámites digitales")
        
        # Recomendaciones basadas en posición relativa
        if "Necesita mejora" in comparison['posicion_relativa']:
            recommendations.append("Realizar auditoría completa de procesos de interoperabilidad")
            recommendations.append("Establecer plan de acción con metas mensuales")
        
        return recommendations
    
    def generate_entity_report(self, entity_name):
        """Genera reporte completo para una entidad"""
        comparison = self.analyze_entity(entity_name)
        
        if comparison is None:
            print(f"✗ Entidad '{entity_name}' no encontrada")
            return None
        
        # Generar visualización
        viz_file = self.generate_entity_visualization(entity_name, comparison)
        
        # Generar reporte en Markdown
        report_md = self.generate_markdown_report(entity_name, comparison, viz_file)
        
        # Generar reporte JSON
        report_json = self.generate_json_report(entity_name, comparison)
        
        return {
            'markdown': report_md,
            'json': report_json,
            'visualization': viz_file
        }
    
    def generate_markdown_report(self, entity_name, comparison, viz_file):
        """Genera reporte en formato Markdown"""
        recommendations = self.get_recommendations(comparison)
        
        report = f"""# Reporte de Interoperabilidad: {entity_name}

**Fecha de generación:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Sector:** {comparison['sector']}

## Análisis General

### Nivel de Madurez
- **Nivel actual:** {comparison['nivel_madurez']}/5
- **Promedio sectorial:** {comparison['sector_media']:.2f}/5
- **Desviación estándar sectorial:** {comparison['sector_desv']:.2f}
- **Posición relativa:** {comparison['posicion_relativa']}

### Conectividad

| Plataforma | Estado | Promedio Sectorial |
|------------|--------|-------------------|
| X-Road | {comparison['conectividad']['xroad']} | {comparison['conectividad']['sector_xroad_pct']:.1f}% |
| SCD | {comparison['conectividad']['scd']} | {comparison['conectividad']['sector_scd_pct']:.1f}% |

## Diagnóstico Detallado

### Fortalezas
"""
        
        if comparison['nivel_madurez'] > comparison['sector_media']:
            report += f"- **Nivel de madurez superior** al promedio sectorial ({comparison['nivel_madurez']} vs {comparison['sector_media']:.2f})\n"
        
        if comparison['conectividad']['xroad'] == 'Sí':
            report += "- **Conectividad X-Road activa** para intercambio seguro de datos\n"
        
        if comparison['conectividad']['scd'] == 'Sí':
            report += "- **Servicios ciudadanos digitales** implementados\n"
        
        report += """
### Áreas de Mejora
"""
        
        if comparison['nivel_madurez'] <= 2:
            report += "- **Nivel de madurez bajo** (niveles 1-2), requiere atención prioritaria\n"
        
        if comparison['conectividad']['xroad'] == 'No':
            report += "- **Falta conexión a X-Road**, impide intercambio seguro de datos\n"
        
        if comparison['conectividad']['scd'] == 'No':
            report += "- **No implementa SCD**, limita servicios digitales al ciudadano\n"
        
        if comparison['nivel_madurez'] < comparison['sector_media']:
            report += f"- **Por debajo del promedio sectorial** ({comparison['nivel_madurez']} vs {comparison['sector_media']:.2f})\n"
        
        report += f"""
## Recomendaciones Estratégicas

"""
        
        for i, rec in enumerate(recommendations, 1):
            report += f"{i}. {rec}\n"
        
        report += f"""
## Metodología

Este análisis se basa en el **Modelo de Madurez del MinTIC** para Gobierno Digital y considera:

- **Indicadores de conectividad:** X-Road y Servicios Ciudadanos Digitales
- **Comparación sectorial:** Benchmarking con entidades del mismo sector
- **Análisis estadístico:** Posición relativa basada en media y desviación estándar

## Visualización

![Análisis de {entity_name}]({viz_file})

---
*Este reporte fue generado automáticamente por el Sistema de Análisis de Interoperabilidad*
"""
        
        # Guardar reporte
        output_dir = 'reportes_entidades'
        os.makedirs(output_dir, exist_ok=True)
        filename = f"{output_dir}/{entity_name.replace(' ', '_').replace('/', '_')}_reporte.md"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report)
        
        return filename
    
    def generate_json_report(self, entity_name, comparison):
        """Genera reporte en formato JSON"""
        recommendations = self.get_recommendations(comparison)
        
        report = {
            'entidad': entity_name,
            'fecha_generacion': datetime.now().isoformat(),
            'sector': comparison['sector'],
            'analisis': {
                'nivel_madurez': comparison['nivel_madurez'],
                'promedio_sectorial': comparison['sector_media'],
                'desviacion_estandar_sectorial': comparison['sector_desv'],
                'posicion_relativa': comparison['posicion_relativa']
            },
            'conectividad': comparison['conectividad'],
            'diagnostico': {
                'fortalezas': self.get_strengths(comparison),
                'areas_mejora': self.get_improvement_areas(comparison)
            },
            'recomendaciones': recommendations
        }
        
        # Guardar reporte JSON
        output_dir = 'reportes_entidades'
        os.makedirs(output_dir, exist_ok=True)
        filename = f"{output_dir}/{entity_name.replace(' ', '_').replace('/', '_')}_reporte.json"
        
        # Convertir tipos numpy a tipos Python nativos para JSON
        def convert_numpy_types(obj):
            if isinstance(obj, np.integer):
                return int(obj)
            elif isinstance(obj, np.floating):
                return float(obj)
            elif isinstance(obj, np.ndarray):
                return obj.tolist()
            return obj
        
        # Convertir el reporte
        report_serializable = json.loads(json.dumps(report, default=convert_numpy_types))
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report_serializable, f, indent=2, ensure_ascii=False)
        
        return filename
    
    def get_strengths(self, comparison):
        """Identifica fortalezas de la entidad"""
        strengths = []
        
        if comparison['nivel_madurez'] > comparison['sector_media']:
            strengths.append(f"Nivel de madurez superior al promedio sectorial")
        
        if comparison['conectividad']['xroad'] == 'Sí':
            strengths.append("Conectividad X-Road activa")
        
        if comparison['conectividad']['scd'] == 'Sí':
            strengths.append("Servicios ciudadanos digitales implementados")
        
        return strengths
    
    def get_improvement_areas(self, comparison):
        """Identifica áreas de mejora"""
        areas = []
        
        if comparison['nivel_madurez'] <= 2:
            areas.append("Nivel de madurez bajo (requiere atención prioritaria)")
        
        if comparison['conectividad']['xroad'] == 'No':
            areas.append("Falta conexión a X-Road")
        
        if comparison['conectividad']['scd'] == 'No':
            areas.append("No implementa Servicios Ciudadanos Digitales")
        
        if comparison['nivel_madurez'] < comparison['sector_media']:
            areas.append("Por debajo del promedio sectorial")
        
        return areas
    
    def generate_all_reports(self):
        """Genera reportes para todas las entidades"""
        print("Generando reportes para todas las entidades...")
        
        all_reports = {}
        
        for entity in self.df['Entidad'].unique():
            print(f"Generando reporte para: {entity}")
            report = self.generate_entity_report(entity)
            if report:
                all_reports[entity] = {
                    'markdown': report['markdown'],
                    'json': report['json'],
                    'visualization': report['visualization']
                }
        
        # Generar índice de reportes
        self.generate_reports_index(all_reports)
        
        print(f"✓ Se generaron {len(all_reports)} reportes individuales")
        return all_reports
    
    def generate_reports_index(self, all_reports):
        """Genera un índice con todos los reportes generados"""
        index_content = """# Índice de Reportes de Interoperabilidad

Este documento contiene el índice de todos los reportes generados para las entidades analizadas.

## Entidades Analizadas

"""
        
        for entity, files in all_reports.items():
            index_content += f"""
### {entity}

- **Reporte completo:** [{entity}_reporte.md]({files['markdown']})
- **Datos JSON:** [{entity}_reporte.json]({files['json']})
- **Visualización:** [{entity}_analisis.png]({files['visualization']})

"""
        
        index_content += """
## Metodología

Todos los reportes se generaron utilizando:

- **Modelo de Madurez MinTIC:** Evaluación estandarizada de nivel de interoperabilidad
- **Benchmarking sectorial:** Comparación con entidades del mismo sector
- **Análisis estadístico:** Media, desviación estándar y posición relativa
- **Recomendaciones personalizadas:** Basadas en el diagnóstico específico de cada entidad

## Contacto

Para consultas sobre los reportes o el análisis de interoperabilidad:

- **Sistema de Análisis de Interoperabilidad**
- **Fecha de generación:** """ + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + """
"""
        
        # Guardar índice
        output_dir = 'reportes_entidades'
        os.makedirs(output_dir, exist_ok=True)
        index_file = f"{output_dir}/indice_reportes.md"
        
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(index_content)
        
        print(f"✓ Índice de reportes guardado en {index_file}")

def main():
    """Función principal"""
    print("GENERADOR DE REPORTES INDIVIDUALES POR ENTIDAD")
    print("=" * 60)
    
    # Inicializar generador
    generator = EntityReportGenerator()
    
    if generator.df is None:
        print("✗ No se pudieron cargar los datos")
        return
    
    print(f"✓ Base de datos cargada: {len(generator.df)} entidades")
    print(f"✓ Sectores analizados: {generator.df['Sector'].nunique()}")
    
    # Generar todos los reportes
    all_reports = generator.generate_all_reports()
    
    print("\n" + "=" * 60)
    print("GENERACIÓN DE REPORTES COMPLETADA")
    print("=" * 60)
    print(f"Archivos generados en: reportes_entidades/")
    print(f"Total de reportes: {len(all_reports)}")
    print("Archivos por entidad:")
    print("  - [Entidad]_reporte.md (Reporte detallado)")
    print("  - [Entidad]_reporte.json (Datos estructurados)")
    print("  - [Entidad]_analisis.png (Visualización científica)")
    print("  - indice_reportes.md (Índice general)")

if __name__ == "__main__":
    main()