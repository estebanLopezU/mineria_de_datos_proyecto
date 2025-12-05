"""
Módulo de Caracterización de Microclimas
Proyecto Final - Minería de Datos
Caracterización de Microclimas y Predicción de Precipitación
"""

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering, MiniBatchKMeans
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# Configurar matplotlib para entorno web (sin GUI)
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.spatial.distance import pdist, squareform
import io
import base64
from typing import Dict, List, Tuple, Any

class MicroclimateClustering:
    def __init__(self):
        self.data = None
        self.scaled_data = None
        self.cluster_labels = None
        self.cluster_centers = None
        self.n_clusters = None
        self.cluster_metrics = {}
        self.pca_components = None

    def load_processed_data(self, dataframe: pd.DataFrame) -> None:
        """Cargar datos procesados para clustering"""
        self.data = dataframe.copy()

        # Seleccionar solo variables meteorológicas relevantes para clustering
        meteorological_vars = ['humedad', 'precipitacion', 'radiacion_solar', 'temperatura']
        available_vars = [col for col in meteorological_vars if col in self.data.columns]

        if len(available_vars) == 0:
            raise ValueError("No se encontraron variables meteorológicas para clustering")

        self.data = self.data[available_vars + (['estacion_sk'] if 'estacion_sk' in self.data.columns else [])]

    def preprocess_for_clustering(self) -> None:
        """Preprocesar datos para clustering"""
        # Separar identificadores si existen
        self.station_ids = None
        if 'estacion_sk' in self.data.columns:
            self.station_ids = self.data['estacion_sk']
            clustering_data = self.data.drop('estacion_sk', axis=1)
        else:
            clustering_data = self.data

        # Seleccionar SOLO columnas numéricas válidas para clustering
        numeric_columns = []
        for col in clustering_data.columns:
            # Skip columnas claramente no numéricas
            if col in ['_source_file'] or 'fecha' in col.lower() or 'hora' in col.lower():
                continue

            try:
                # Intentar convertir la columna a numérico
                pd.to_numeric(clustering_data[col], errors='coerce')
                # Si no hay muchos NaN después de la conversión, incluirla
                if clustering_data[col].notna().sum() > len(clustering_data) * 0.5:  # Al menos 50% de datos válidos
                    numeric_columns.append(col)
            except:
                continue

        if len(numeric_columns) == 0:
            raise ValueError("No se encontraron columnas numéricas válidas para clustering")

        # Usar solo las columnas numéricas válidas
        clustering_data = clustering_data[numeric_columns].copy()

        # Convertir a numérico y manejar valores no numéricos
        for col in clustering_data.columns:
            clustering_data[col] = pd.to_numeric(clustering_data[col], errors='coerce')

        # Rellenar NaN con medianas
        clustering_data = clustering_data.fillna(clustering_data.median())

        # Guardar las columnas de clustering para referencia posterior
        self.clustering_columns = clustering_data.columns.tolist()

        print(f"Clustering con {len(self.clustering_columns)} columnas numéricas: {self.clustering_columns}")

        # Normalizar datos
        self.scaler = StandardScaler()
        self.scaled_data = self.scaler.fit_transform(clustering_data)

    def determine_optimal_clusters(self, max_clusters: int = 8, fast_mode: bool = True) -> Dict[str, Any]:
        """Determinar el número óptimo de clusters usando métodos optimizados"""
        if self.scaled_data is None:
            raise ValueError("Datos no preprocesados. Ejecutar preprocess_for_clustering() primero.")

        optimal_clusters = {}
        n_samples = len(self.scaled_data)

        if fast_mode and n_samples > 5000:
            # Modo rápido: usar submuestreo para determinar clusters óptimos
            print("Usando modo rápido para determinación de clusters...")
            sample_size = min(5000, max(1000, n_samples // 10))  # Máximo 5000 muestras
            sample_indices = np.random.choice(n_samples, size=sample_size, replace=False)
            sample_data = self.scaled_data[sample_indices]
            print(f"Usando muestra de {sample_size} puntos para determinar clusters óptimos")
        else:
            sample_data = self.scaled_data

        # Método simplificado y más rápido
        if fast_mode:
            # Estrategia rápida: probar menos valores y usar heurísticas
            test_clusters = [3, 4, 5, 6]  # Solo probar 4 valores en lugar de 2-10
            print(f"Probando {len(test_clusters)} configuraciones de clusters...")
        else:
            test_clusters = list(range(2, min(max_clusters + 1, 8)))

        wcss = []
        silhouette_scores = []

        for k in test_clusters:
            kmeans = KMeans(n_clusters=k, random_state=42, n_init=5, max_iter=100)  # Reducir iteraciones
            kmeans.fit(sample_data)
            wcss.append(kmeans.inertia_)

            # Calcular silhouette score en muestra más pequeña para velocidad
            if len(sample_data) > 1000:
                sil_sample = sample_data[np.random.choice(len(sample_data), size=min(1000, len(sample_data)), replace=False)]
                sil_labels = kmeans.predict(sil_sample)
            else:
                sil_labels = kmeans.labels_
                sil_sample = sample_data

            try:
                silhouette_avg = silhouette_score(sil_sample, sil_labels)
                silhouette_scores.append(silhouette_avg)
            except:
                silhouette_scores.append(0)  # En caso de error, usar 0

        # Método del codo simplificado
        if len(wcss) > 2:
            # Calcular cambios porcentuales
            wcss_changes = np.abs(np.diff(wcss) / wcss[:-1])
            # Encontrar el punto donde el cambio es significativo pero no extremo
            optimal_k = test_clusters[np.argmax(wcss_changes) + 1] if len(wcss_changes) > 0 else test_clusters[1]
        else:
            optimal_k = test_clusters[1] if len(test_clusters) > 1 else test_clusters[0]

        optimal_clusters['elbow_method'] = optimal_k
        optimal_clusters['silhouette_scores'] = dict(zip(test_clusters, silhouette_scores))
        optimal_clusters['wcss_values'] = dict(zip(test_clusters, wcss))

        # Método de silhouette máximo
        if silhouette_scores:
            best_silhouette_k = test_clusters[np.argmax(silhouette_scores)]
            optimal_clusters['silhouette_method'] = best_silhouette_k
        else:
            optimal_clusters['silhouette_method'] = optimal_k

        # Usar un valor conservador si el óptimo es muy alto
        final_k = min(optimal_clusters['silhouette_method'], 6)  # Máximo 6 clusters para velocidad
        optimal_clusters['recommended_clusters'] = final_k

        print(f"Clusters óptimos determinados: Elbow={optimal_k}, Silhouette={optimal_clusters['silhouette_method']}, Recomendado={final_k}")
        return optimal_clusters

    def perform_kmeans_clustering(self, n_clusters: int) -> Dict[str, Any]:
        """Realizar clustering con K-Means o MiniBatchKMeans según el tamaño del dataset"""
        if self.scaled_data is None:
            raise ValueError("Datos no preprocesados. Ejecutar preprocess_for_clustering() primero.")

        n_samples = len(self.scaled_data)

        # Elegir algoritmo según tamaño del dataset
        if n_samples > 10000:  # Usar MiniBatchKMeans para datasets grandes
            print(f"Usando MiniBatchKMeans para {n_samples} muestras (más rápido para datasets grandes)")
            kmeans = MiniBatchKMeans(
                n_clusters=n_clusters,
                random_state=42,
                batch_size=min(1000, n_samples // 10),  # Tamaño de batch adaptativo
                max_iter=200,  # Más iteraciones para MiniBatch
                n_init=5
            )
        else:  # Usar KMeans estándar para datasets pequeños
            print(f"Usando KMeans estándar para {n_samples} muestras")
            kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10, max_iter=100)

        self.cluster_labels = kmeans.fit_predict(self.scaled_data)
        self.cluster_centers = kmeans.cluster_centers_
        self.n_clusters = n_clusters

        # Calcular métricas de evaluación (en muestra para velocidad si es muy grande)
        if n_samples > 5000:
            # Calcular métricas en una muestra representativa para velocidad
            sample_size = min(5000, n_samples)
            sample_indices = np.random.choice(n_samples, size=sample_size, replace=False)
            sample_data = self.scaled_data[sample_indices]
            sample_labels = self.cluster_labels[sample_indices]

            print(f"Calculando métricas en muestra de {sample_size} puntos para velocidad")
            self.cluster_metrics = {
                'silhouette_score': silhouette_score(sample_data, sample_labels),
                'calinski_harabasz_score': calinski_harabasz_score(sample_data, sample_labels),
                'davies_bouldin_score': davies_bouldin_score(sample_data, sample_labels)
            }
        else:
            # Calcular métricas en todos los datos para precisión
            self.cluster_metrics = {
                'silhouette_score': silhouette_score(self.scaled_data, self.cluster_labels),
                'calinski_harabasz_score': calinski_harabasz_score(self.scaled_data, self.cluster_labels),
                'davies_bouldin_score': davies_bouldin_score(self.scaled_data, self.cluster_labels)
            }

        # Crear DataFrame con resultados
        results_df = self.data.copy()
        results_df['cluster'] = self.cluster_labels

        return {
            'cluster_labels': self.cluster_labels,
            'cluster_centers': self.cluster_centers,
            'metrics': self.cluster_metrics,
            'results_df': results_df,
            'algorithm_used': 'MiniBatchKMeans' if n_samples > 10000 else 'KMeans'
        }

    def perform_dbscan_clustering(self, eps: float = 0.5, min_samples: int = 5) -> Dict[str, Any]:
        """Realizar clustering con DBSCAN"""
        if self.scaled_data is None:
            raise ValueError("Datos no preprocesados. Ejecutar preprocess_for_clustering() primero.")

        dbscan = DBSCAN(eps=eps, min_samples=min_samples)
        labels = dbscan.fit_predict(self.scaled_data)

        # Contar clusters (excluyendo ruido marcado como -1)
        n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
        n_noise = list(labels).count(-1)

        # Calcular métricas solo si hay clusters válidos
        metrics = {}
        if n_clusters > 1:
            # Filtrar ruido para calcular métricas
            valid_labels = labels[labels != -1]
            valid_data = self.scaled_data[labels != -1]
            if len(valid_labels) > 1:
                metrics = {
                    'silhouette_score': silhouette_score(valid_data, valid_labels),
                    'calinski_harabasz_score': calinski_harabasz_score(valid_data, valid_labels),
                    'davies_bouldin_score': davies_bouldin_score(valid_data, valid_labels)
                }

        results_df = self.data.copy()
        results_df['cluster'] = labels

        return {
            'cluster_labels': labels,
            'n_clusters': n_clusters,
            'n_noise_points': n_noise,
            'metrics': metrics,
            'results_df': results_df,
            'eps': eps,
            'min_samples': min_samples
        }

    def perform_hierarchical_clustering(self, n_clusters: int, linkage: str = 'ward') -> Dict[str, Any]:
        """Realizar clustering jerárquico"""
        if self.scaled_data is None:
            raise ValueError("Datos no preprocesados. Ejecutar preprocess_for_clustering() primero.")

        hierarchical = AgglomerativeClustering(n_clusters=n_clusters, linkage=linkage)
        labels = hierarchical.fit_predict(self.scaled_data)

        # Calcular métricas
        metrics = {
            'silhouette_score': silhouette_score(self.scaled_data, labels),
            'calinski_harabasz_score': calinski_harabasz_score(self.scaled_data, labels),
            'davies_bouldin_score': davies_bouldin_score(self.scaled_data, labels)
        }

        results_df = self.data.copy()
        results_df['cluster'] = labels

        return {
            'cluster_labels': labels,
            'n_clusters': n_clusters,
            'linkage': linkage,
            'metrics': metrics,
            'results_df': results_df
        }

    def analyze_clusters(self, results_df: pd.DataFrame) -> Dict[str, Any]:
        """Analizar características de los clusters encontrados con manejo robusto de errores"""
        cluster_analysis = {}

        try:
            # Verificar que existe la columna cluster
            if 'cluster' not in results_df.columns:
                print("⚠️  Columna 'cluster' no encontrada en results_df")
                return cluster_analysis

            # Verificar que hay clusters válidos
            unique_clusters = results_df['cluster'].unique()
            if len(unique_clusters) == 0:
                print("⚠️  No se encontraron clusters válidos")
                return cluster_analysis

            print(f"📊 Analizando {len(unique_clusters)} clusters con {len(results_df)} muestras")

            # Identificar columnas numéricas disponibles para análisis
            all_columns = results_df.columns.tolist()
            numeric_columns = []

            for col in all_columns:
                if col == 'cluster':
                    continue

                # Verificar si la columna es numérica y tiene datos válidos
                try:
                    if results_df[col].dtype in ['int64', 'float64', 'int32', 'float32']:
                        # Verificar que no sea toda NaN
                        if not results_df[col].isna().all():
                            numeric_columns.append(col)
                    else:
                        # Intentar convertir strings numéricos
                        sample_values = results_df[col].dropna().head(10)
                        if len(sample_values) > 0:
                            try:
                                pd.to_numeric(sample_values, errors='coerce')
                                # Si la conversión funciona parcialmente, incluir
                                if not pd.to_numeric(results_df[col], errors='coerce').isna().all():
                                    numeric_columns.append(col)
                            except:
                                pass
                except Exception as e:
                    print(f"⚠️  Error evaluando columna {col}: {e}")
                    continue

            if len(numeric_columns) == 0:
                print("⚠️  No se encontraron columnas numéricas para análisis de clusters")
                # Crear análisis básico con solo tamaños de cluster
                cluster_sizes = results_df['cluster'].value_counts().sort_index()
                cluster_analysis['cluster_sizes'] = cluster_sizes.to_dict()
                cluster_analysis['warning'] = 'No numeric columns available for detailed cluster analysis'
                return cluster_analysis

            print(f"📈 Analizando {len(numeric_columns)} variables numéricas: {numeric_columns[:5]}{'...' if len(numeric_columns) > 5 else ''}")

            # Filtrar columnas que realmente sean numéricas y no contengan strings
            valid_numeric_columns = []
            for col in numeric_columns:
                try:
                    # Verificar que la columna no contenga valores no numéricos
                    sample_values = results_df[col].dropna().head(10)
                    if len(sample_values) > 0:
                        # Intentar convertir a numérico
                        pd.to_numeric(sample_values, errors='coerce')
                        # Si después de la conversión no hay muchos NaN, es válida
                        converted = pd.to_numeric(results_df[col], errors='coerce')
                        if converted.notna().sum() > len(results_df) * 0.8:  # Al menos 80% de valores válidos
                            valid_numeric_columns.append(col)
                except:
                    continue

            if len(valid_numeric_columns) == 0:
                print("⚠️  No hay columnas numéricas válidas para análisis estadístico detallado")
                cluster_analysis['cluster_statistics'] = {'warning': 'No numeric columns available for detailed statistics'}
            else:
                print(f"✅ Usando {len(valid_numeric_columns)} columnas numéricas válidas para estadísticas")

            # Estadísticas por cluster con manejo robusto de tipos de datos
            try:
                # Filtrar aún más las columnas para asegurar que sean completamente numéricas
                truly_numeric_columns = []
                for col in valid_numeric_columns:
                    try:
                        # Verificar que la columna sea completamente numérica sin valores mixtos
                        col_data = results_df[col]
                        # Convertir a numérico y verificar que no se pierdan muchos valores
                        numeric_col = pd.to_numeric(col_data, errors='coerce')
                        if numeric_col.notna().sum() > len(col_data) * 0.9:  # Al menos 90% numérico
                            truly_numeric_columns.append(col)
                        else:
                            print(f"⚠️  Columna {col} descartada: solo {numeric_col.notna().sum()}/{len(col_data)} valores numéricos")
                    except Exception as col_check_error:
                        print(f"⚠️  Error verificando columna {col}: {col_check_error}")
                        continue

                if len(truly_numeric_columns) == 0:
                    cluster_analysis['cluster_statistics'] = {'warning': 'No truly numeric columns found for detailed statistics'}
                else:
                    print(f"✅ Calculando estadísticas para {len(truly_numeric_columns)} columnas numéricas válidas")

                    # Calcular estadísticas por cluster de forma segura
                    cluster_stats_dict = {}
                    for col in truly_numeric_columns:
                        try:
                            col_stats = results_df.groupby('cluster')[col].agg(['mean', 'std', 'min', 'max', 'count'])
                            # Convertir a tipos nativos de Python para evitar problemas de serialización
                            col_stats_clean = {}
                            for stat_name in ['mean', 'std', 'min', 'max', 'count']:
                                if stat_name in col_stats.columns:
                                    stat_values = col_stats[stat_name].to_dict()
                                    # Convertir valores numpy a tipos Python
                                    col_stats_clean[stat_name] = {k: float(v) if pd.notna(v) else None for k, v in stat_values.items()}
                            cluster_stats_dict[col] = col_stats_clean
                        except Exception as col_error:
                            print(f"⚠️  Error calculando estadísticas para columna {col}: {col_error}")
                            continue

                    cluster_analysis['cluster_statistics'] = cluster_stats_dict if cluster_stats_dict else {'warning': 'Could not calculate detailed statistics'}

            except Exception as e:
                print(f"⚠️  Error general calculando estadísticas de cluster: {e}")
                cluster_analysis['cluster_statistics'] = {'error': str(e)}

            # Tamaño de clusters
            cluster_sizes = results_df['cluster'].value_counts().sort_index()
            cluster_analysis['cluster_sizes'] = cluster_sizes.to_dict()

            # Centroides en espacio original
            if self.cluster_centers is not None and hasattr(self, 'scaler') and hasattr(self, 'clustering_columns'):
                try:
                    original_centers = self.scaler.inverse_transform(self.cluster_centers)
                    cluster_analysis['cluster_centers_original'] = {
                        f'cluster_{i}': dict(zip(self.clustering_columns, center))
                        for i, center in enumerate(original_centers)
                    }
                except Exception as e:
                    print(f"⚠️  Error desescalando centroides: {e}")
                    # Fallback: usar centroides escalados si disponibles
                    try:
                        cluster_analysis['cluster_centers_scaled'] = {
                            f'cluster_{i}': dict(zip(self.clustering_columns, center))
                            for i, center in enumerate(self.cluster_centers)
                        }
                    except:
                        pass

            print("✅ Análisis de clusters completado exitosamente")
            return cluster_analysis

        except Exception as e:
            print(f"❌ Error general en análisis de clusters: {e}")
            # Retornar análisis básico si hay error
            try:
                cluster_sizes = results_df['cluster'].value_counts().sort_index()
                cluster_analysis['cluster_sizes'] = cluster_sizes.to_dict()
                cluster_analysis['error'] = str(e)
            except:
                cluster_analysis['error'] = f'Complete analysis failure: {str(e)}'

            return cluster_analysis

    def generate_clustering_plots(self, results_df: pd.DataFrame) -> Dict[str, str]:
        """Generar gráficos de visualización de clusters"""
        plots = {}

        if self.scaled_data.shape[1] < 2:
            return plots

        # Aplicar PCA para visualización 2D
        pca = PCA(n_components=2)
        pca_data = pca.fit_transform(self.scaled_data)
        self.pca_components = pca.components_

        # Gráfico de clusters en 2D
        fig, ax = plt.subplots(figsize=(10, 8))
        scatter = ax.scatter(pca_data[:, 0], pca_data[:, 1], c=results_df['cluster'],
                           cmap='viridis', alpha=0.7, edgecolors='black', linewidth=0.5)
        ax.set_xlabel(f'Componente Principal 1 ({pca.explained_variance_ratio_[0]:.1%})')
        ax.set_ylabel(f'Componente Principal 2 ({pca.explained_variance_ratio_[1]:.1%})')
        ax.set_title('Visualización de Clusters (PCA)')
        ax.grid(True, alpha=0.3)

        # Añadir centroids si existen
        if self.cluster_centers is not None and hasattr(self, 'n_clusters'):
            centroids_pca = pca.transform(self.cluster_centers)
            ax.scatter(centroids_pca[:, 0], centroids_pca[:, 1], c='red',
                      marker='X', s=200, edgecolors='black', linewidth=2, label='Centroides')
            ax.legend()

        plt.colorbar(scatter, ax=ax, label='Cluster')
        plt.tight_layout()
        plots['clusters_2d'] = self._fig_to_base64(fig)
        plt.close()

        # Método del codo
        fig, ax = plt.subplots(figsize=(8, 6))
        optimal_info = self.determine_optimal_clusters()
        wcss_values = list(optimal_info['wcss_values'].values())
        k_values = list(optimal_info['wcss_values'].keys())

        ax.plot(k_values, wcss_values, 'bo-', linewidth=2, markersize=8)
        ax.set_xlabel('Número de Clusters (k)')
        ax.set_ylabel('WCSS (Within-Cluster Sum of Squares)')
        ax.set_title('Método del Codo para Determinar k Óptimo')
        ax.grid(True, alpha=0.3)

        # Marcar el codo
        elbow_k = optimal_info['elbow_method']
        ax.axvline(x=elbow_k, color='red', linestyle='--', alpha=0.7, label=f'Codo en k={elbow_k}')
        ax.legend()

        plt.tight_layout()
        plots['elbow_method'] = self._fig_to_base64(fig)
        plt.close()

        # Silhouette scores
        fig, ax = plt.subplots(figsize=(8, 6))
        silhouette_scores = list(optimal_info['silhouette_scores'].values())
        k_values_sil = list(optimal_info['silhouette_scores'].keys())

        ax.plot(k_values_sil, silhouette_scores, 'go-', linewidth=2, markersize=8)
        ax.set_xlabel('Número de Clusters (k)')
        ax.set_ylabel('Coeficiente de Silhouette')
        ax.set_title('Coeficiente de Silhouette vs Número de Clusters')
        ax.grid(True, alpha=0.3)
        ax.set_ylim(0, 1)

        # Marcar el mejor k
        best_k = optimal_info['silhouette_method']
        ax.axvline(x=best_k, color='red', linestyle='--', alpha=0.7, label=f'Mejor k={best_k}')
        ax.legend()

        plt.tight_layout()
        plots['silhouette_analysis'] = self._fig_to_base64(fig)
        plt.close()

        return plots

    def _fig_to_base64(self, fig) -> str:
        """Convertir figura matplotlib a base64"""
        buf = io.BytesIO()
        fig.savefig(buf, format='png', dpi=100, bbox_inches='tight')
        buf.seek(0)
        image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
        buf.close()
        return f"data:image/png;base64,{image_base64}"

    def get_clustering_summary(self) -> Dict[str, Any]:
        """Generar resumen completo del análisis de clustering"""
        return {
            'n_clusters_found': self.n_clusters,
            'cluster_metrics': self.cluster_metrics,
            'cluster_sizes': dict(pd.Series(self.cluster_labels).value_counts()) if self.cluster_labels is not None else {},
            'pca_explained_variance': self.pca_components.tolist() if self.pca_components is not None else None
        }
