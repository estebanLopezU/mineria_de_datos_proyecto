"""
Módulo de Predicción de Precipitación
Proyecto Final - Minería de Datos
Caracterización de Microclimas y Predicción de Precipitación
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, ExtraTreesRegressor
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.svm import SVR
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler

# Configurar matplotlib para entorno web (sin GUI)
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import io
import base64
from typing import Dict, List, Tuple, Any
import warnings
warnings.filterwarnings('ignore')

class PrecipitationPredictor:
    def __init__(self):
        self.data = None
        self.models = {}
        self.best_model = None
        self.best_score = -np.inf
        self.scaler = StandardScaler()
        self.feature_importance = {}
        self.prediction_results = {}

    def load_clustered_data(self, dataframe: pd.DataFrame) -> None:
        """Cargar datos con información de clusters con optimización para velocidad"""
        self.data = dataframe.copy()

        # Verificar que existe la columna de precipitación
        if 'precipitacion' not in self.data.columns:
            raise ValueError("La columna 'precipitacion' es requerida para la predicción")

        # Optimización ultra-rápida: muestreo adicional agresivo para predicción
        n_samples = len(self.data)
        if n_samples > 50000:  # Si aún tenemos muchos datos, reducir drásticamente
            print(f"Dataset de predicción muy grande ({n_samples} filas), aplicando muestreo ultra-agresivo...")
            sample_size = min(15000, max(3000, n_samples // 50))  # Máximo 15k muestras
            self.data = self.data.sample(n=sample_size, random_state=42).reset_index(drop=True)
            print(f"Dataset de predicción reducido a {len(self.data)} filas para velocidad máxima")

    def prepare_features_and_target(self) -> Tuple[np.ndarray, np.ndarray]:
        """Preparar features y variable objetivo"""
        # Separar features y target
        target = 'precipitacion'
        features = [col for col in self.data.columns if col != target]

        print(f"Preparando datos - Target: {target}")
        print(f"Columnas disponibles: {list(self.data.columns)}")
        print(f"Features seleccionadas: {features}")

        if target not in self.data.columns:
            raise ValueError(f"Columna target '{target}' no encontrada en los datos")

        X = self.data[features]
        y = self.data[target]

        print(f"X shape antes de transformación: {X.shape}")
        print(f"Y shape: {y.shape}")

        # Verificar y convertir target a numérico si es necesario
        if y.dtype == 'object':
            print("Convirtiendo target a numérico...")
            y = pd.to_numeric(y, errors='coerce')
            if y.isna().sum() > 0:
                print(f"⚠️  Eliminando {y.isna().sum()} valores NaN del target")
                # Eliminar filas donde el target es NaN
                valid_indices = ~y.isna()
                X = X[valid_indices]
                y = y[valid_indices]
                print(f"Nuevas shapes - X: {X.shape}, y: {y.shape}")

        # Normalizar features numéricos
        numeric_features = X.select_dtypes(include=[np.number]).columns
        print(f"Features numéricas encontradas: {list(numeric_features)}")

        if len(numeric_features) == 0:
            raise ValueError("No se encontraron features numéricas para el entrenamiento")

        X_scaled = X.copy()
        X_scaled[numeric_features] = self.scaler.fit_transform(X[numeric_features])

        print(f"X final shape: {X_scaled.shape}")
        print(f"Y final shape: {y.shape}")

        return X_scaled.values, y.values

    def train_multiple_models(self, test_size: float = 0.2) -> Dict[str, Any]:
        """Entrenar múltiples modelos de predicción con algoritmos adaptativos según tamaño del dataset"""
        X, y = self.prepare_features_and_target()
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)

        n_samples = len(X_train)
        n_features = X_train.shape[1]

        print(f"Entrenando modelos en dataset de {n_samples} muestras y {n_features} características")
        print(f"Columnas disponibles: {list(X.columns) if hasattr(X, 'columns') else 'N/A'}")
        print(f"Target shape: {y.shape}")

        # Seleccionar modelos según tamaño del dataset
        if n_samples > 50000:  # Datasets muy grandes
            print("Usando algoritmos optimizados para datasets grandes")
            models = {
                'Linear Regression': LinearRegression(),
                'Ridge Regression': Ridge(alpha=1.0),
                'Random Forest': RandomForestRegressor(n_estimators=50, max_depth=10, random_state=42),  # Reducido para velocidad
                'Extra Trees': ExtraTreesRegressor(n_estimators=50, max_depth=10, random_state=42),  # Más rápido que RF
            }
        elif n_samples > 10000:  # Datasets grandes
            print("Usando algoritmos balanceados para datasets medianos")
            models = {
                'Linear Regression': LinearRegression(),
                'Ridge Regression': Ridge(alpha=1.0),
                'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42),
                'Gradient Boosting': GradientBoostingRegressor(n_estimators=50, random_state=42),  # Reducido
                'Extra Trees': ExtraTreesRegressor(n_estimators=100, random_state=42),
            }
        else:  # Datasets pequeños - usar todos los modelos
            print("Usando suite completa de modelos para datasets pequeños")
            models = {
                'Linear Regression': LinearRegression(),
                'Ridge Regression': Ridge(alpha=1.0),
                'Lasso Regression': Lasso(alpha=0.1),
                'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42),
                'Gradient Boosting': GradientBoostingRegressor(n_estimators=100, random_state=42),
                'SVR': SVR(kernel='rbf', C=1.0),
                'Neural Network': MLPRegressor(hidden_layer_sizes=(50, 25), max_iter=500, random_state=42)
            }

        results = {}

        for name, model in models.items():
            try:
                # Entrenar modelo
                model.fit(X_train, y_train)

                # Predicciones
                y_pred_train = model.predict(X_train)
                y_pred_test = model.predict(X_test)

                # Métricas de evaluación
                metrics = {
                    'train_mae': mean_absolute_error(y_train, y_pred_train),
                    'test_mae': mean_absolute_error(y_test, y_pred_test),
                    'train_mse': mean_squared_error(y_train, y_pred_train),
                    'test_mse': mean_squared_error(y_test, y_pred_test),
                    'train_rmse': np.sqrt(mean_squared_error(y_train, y_pred_train)),
                    'test_rmse': np.sqrt(mean_squared_error(y_test, y_pred_test)),
                    'train_r2': r2_score(y_train, y_pred_train),
                    'test_r2': r2_score(y_test, y_pred_test)
                }

                # Cross-validation score
                cv_scores = cross_val_score(model, X, y, cv=5, scoring='r2')
                metrics['cv_r2_mean'] = cv_scores.mean()
                metrics['cv_r2_std'] = cv_scores.std()

                # Guardar modelo y métricas
                self.models[name] = model
                results[name] = {
                    'model': model,
                    'metrics': metrics,
                    'predictions': {
                        'y_test': y_test,
                        'y_pred': y_pred_test
                    }
                }

                # Actualizar mejor modelo
                if metrics['test_r2'] > self.best_score:
                    self.best_score = metrics['test_r2']
                    self.best_model = model
                    self.best_model_name = name

            except Exception as e:
                results[name] = {
                    'error': str(e),
                    'metrics': None,
                    'predictions': None
                }

        self.prediction_results = results
        return results

    def optimize_best_model(self) -> Dict[str, Any]:
        """Optimizar hiperparámetros del mejor modelo encontrado"""
        if self.best_model is None:
            raise ValueError("No se ha entrenado ningún modelo. Ejecutar train_multiple_models() primero.")

        X, y = self.prepare_features_and_target()
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Definir parámetros para optimización según el tipo de modelo
        param_grids = {
            'Random Forest': {
                'n_estimators': [50, 100, 200],
                'max_depth': [None, 10, 20, 30],
                'min_samples_split': [2, 5, 10],
                'min_samples_leaf': [1, 2, 4]
            },
            'Gradient Boosting': {
                'n_estimators': [50, 100, 200],
                'learning_rate': [0.01, 0.1, 0.2],
                'max_depth': [3, 5, 7],
                'subsample': [0.8, 0.9, 1.0]
            },
            'SVR': {
                'C': [0.1, 1, 10, 100],
                'gamma': ['scale', 'auto', 0.01, 0.1, 1],
                'kernel': ['rbf', 'linear']
            },
            'Neural Network': {
                'hidden_layer_sizes': [(50,), (100,), (50, 25), (100, 50)],
                'activation': ['relu', 'tanh'],
                'learning_rate_init': [0.001, 0.01, 0.1]
            }
        }

        model_name = self.best_model_name
        if model_name in param_grids:
            # Usar procesamiento secuencial para evitar conflictos con Flask
            n_jobs = 1 if len(self.data) > 10000 else -1  # Secuencial para datasets grandes

            grid_search = GridSearchCV(
                self.models[model_name],
                param_grids[model_name],
                cv=2 if len(self.data) > 10000 else 3,  # CV reducido para velocidad
                scoring='r2',
                n_jobs=n_jobs,
                verbose=0  # Sin verbose para evitar conflictos
            )

            grid_search.fit(X_train, y_train)

            # Evaluar modelo optimizado
            y_pred_optimized = grid_search.predict(X_test)

            optimized_metrics = {
                'best_params': grid_search.best_params_,
                'test_mae': mean_absolute_error(y_test, y_pred_optimized),
                'test_mse': mean_squared_error(y_test, y_pred_optimized),
                'test_rmse': np.sqrt(mean_squared_error(y_test, y_pred_optimized)),
                'test_r2': r2_score(y_test, y_pred_optimized),
                'cv_best_score': grid_search.best_score_
            }

            return {
                'optimized_model': grid_search.best_estimator_,
                'metrics': optimized_metrics,
                'grid_search_results': grid_search.cv_results_
            }
        else:
            return {
                'message': f"El modelo {model_name} no tiene parámetros para optimizar",
                'original_metrics': self.prediction_results[model_name]['metrics']
            }

    def predict_by_microclimate(self) -> Dict[str, Any]:
        """Realizar predicciones diferenciadas por microclima"""
        if 'cluster' not in self.data.columns:
            raise ValueError("Los datos deben contener información de clusters para predicciones por microclima")

        microclimate_predictions = {}

        for cluster_id in self.data['cluster'].unique():
            cluster_data = self.data[self.data['cluster'] == cluster_id]

            if len(cluster_data) < 10:  # Mínimo de datos para predicción
                microclimate_predictions[f'cluster_{cluster_id}'] = {
                    'message': f'Datos insuficientes para cluster {cluster_id}',
                    'predictions': None
                }
                continue

            # Preparar datos del cluster
            predictor = PrecipitationPredictor()
            predictor.load_clustered_data(cluster_data)
            predictor.train_multiple_models()

            # Usar el mejor modelo del cluster (o None si no hay resultados)
            cluster_best_model = getattr(predictor, 'best_model_name', None)
            if cluster_best_model and cluster_best_model in predictor.prediction_results:
                cluster_metrics = predictor.prediction_results[cluster_best_model]['metrics']
            else:
                # Usar el primer modelo disponible o crear métricas básicas
                available_models = list(predictor.prediction_results.keys())
                if available_models:
                    cluster_best_model = available_models[0]
                    cluster_metrics = predictor.prediction_results[cluster_best_model]['metrics']
                else:
                    cluster_best_model = 'No disponible'
                    cluster_metrics = {'error': 'No se pudieron entrenar modelos para este cluster'}

            microclimate_predictions[f'cluster_{cluster_id}'] = {
                'best_model': cluster_best_model,
                'metrics': cluster_metrics,
                'data_size': len(cluster_data),
                'predictions': predictor.prediction_results[cluster_best_model]['predictions']
            }

        return microclimate_predictions

    def analyze_feature_importance(self) -> Dict[str, Any]:
        """Analizar importancia de características"""
        if not hasattr(self, 'models') or 'Random Forest' not in self.models:
            return {'message': 'Random Forest no disponible para análisis de importancia'}

        rf_model = self.models['Random Forest']
        X, y = self.prepare_features_and_target()

        # Obtener importancia de características
        feature_names = [col for col in self.data.columns if col != 'precipitacion']
        feature_importance = dict(zip(feature_names, rf_model.feature_importances_))

        # Ordenar por importancia
        sorted_features = sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)

        return {
            'feature_importance': dict(sorted_features),
            'top_features': sorted_features[:10]
        }

    def generate_prediction_plots(self) -> Dict[str, str]:
        """Generar gráficos de análisis de predicciones"""
        plots = {}

        if not self.prediction_results:
            return plots

        # Comparación de modelos
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Comparación de Modelos de Predicción de Precipitación', fontsize=16)

        model_names = []
        r2_scores = []
        mae_scores = []
        rmse_scores = []

        for name, result in self.prediction_results.items():
            if result['metrics'] is not None:
                model_names.append(name)
                r2_scores.append(result['metrics']['test_r2'])
                mae_scores.append(result['metrics']['test_mae'])
                rmse_scores.append(result['metrics']['test_rmse'])

        # Gráfico de R²
        axes[0, 0].bar(model_names, r2_scores, color='skyblue', alpha=0.8)
        axes[0, 0].set_title('Coeficiente de Determinación (R²)')
        axes[0, 0].set_ylabel('R² Score')
        axes[0, 0].tick_params(axis='x', rotation=45)

        # Gráfico de MAE
        axes[0, 1].bar(model_names, mae_scores, color='lightcoral', alpha=0.8)
        axes[0, 1].set_title('Error Absoluto Medio (MAE)')
        axes[0, 1].set_ylabel('MAE')
        axes[0, 1].tick_params(axis='x', rotation=45)

        # Gráfico de RMSE
        axes[1, 0].bar(model_names, rmse_scores, color='lightgreen', alpha=0.8)
        axes[1, 0].set_title('Raíz del Error Cuadrático Medio (RMSE)')
        axes[1, 0].set_ylabel('RMSE')
        axes[1, 0].tick_params(axis='x', rotation=45)

        # Mejor modelo - Predicciones vs Valores Reales
        if self.best_model is not None:
            best_result = self.prediction_results[self.best_model_name]
            y_test = best_result['predictions']['y_test']
            y_pred = best_result['predictions']['y_pred']

            axes[1, 1].scatter(y_test, y_pred, alpha=0.6, color='blue')
            axes[1, 1].plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()],
                           'r--', linewidth=2, label='Línea ideal')
            axes[1, 1].set_xlabel('Valores Reales')
            axes[1, 1].set_ylabel('Predicciones')
            axes[1, 1].set_title(f'Predicciones vs Reales\n({self.best_model_name})')
            axes[1, 1].legend()
            axes[1, 1].grid(True, alpha=0.3)

        plt.tight_layout()
        plots['model_comparison'] = self._fig_to_base64(fig)
        plt.close()

        # Importancia de características (si está disponible)
        feature_importance = self.analyze_feature_importance()
        if 'feature_importance' in feature_importance:
            fig, ax = plt.subplots(figsize=(10, 6))

            features = list(feature_importance['feature_importance'].keys())[:10]
            importance = list(feature_importance['feature_importance'].values())[:10]

            bars = ax.barh(features, importance, color='lightblue', alpha=0.8)
            ax.set_xlabel('Importancia')
            ax.set_title('Top 10 Características Más Importantes\n(Random Forest)')
            ax.grid(True, alpha=0.3)

            # Añadir valores en las barras
            for bar, value in zip(bars, importance):
                ax.text(bar.get_width() + 0.001, bar.get_y() + bar.get_height()/2,
                       f'{value:.3f}', va='center', fontsize=10)

            plt.tight_layout()
            plots['feature_importance'] = self._fig_to_base64(fig)
            plt.close()

        return plots

    def generate_microclimate_insights(self) -> Dict[str, Any]:
        """Generar insights específicos por microclima con validación inteligente de datos"""
        if 'cluster' not in self.data.columns:
            return {'message': 'No hay información de clusters disponible'}

        insights = {}

        for cluster_id in sorted(self.data['cluster'].unique()):
            cluster_data = self.data[self.data['cluster'] == cluster_id]

            cluster_stats = {
                'size': len(cluster_data),
                'cluster_id': int(cluster_id)
            }

            # Función inteligente para calcular estadísticas de forma segura
            def safe_stat_calculation(series, stat_name):
                """Calcula estadísticas de forma segura manejando tipos mixtos"""
                try:
                    # Limpiar y convertir a numérico si es necesario
                    if series.dtype == 'object':
                        # Intentar convertir strings numéricos
                        cleaned = pd.to_numeric(series, errors='coerce')
                        if cleaned.isna().all():
                            return None  # No se puede convertir
                        series = cleaned

                    # Calcular estadística solicitada
                    if stat_name == 'mean':
                        return float(series.mean())
                    elif stat_name == 'std':
                        return float(series.std())
                    elif stat_name == 'min':
                        return float(series.min())
                    elif stat_name == 'max':
                        return float(series.max())
                    elif stat_name == 'count':
                        return int(series.count())

                except Exception as e:
                    print(f"⚠️  Error calculando {stat_name} para cluster {cluster_id}: {e}")
                    return None

            # Calcular estadísticas de precipitación con validación
            precip_stats = {}
            for stat in ['mean', 'std', 'min', 'max']:
                result = safe_stat_calculation(cluster_data['precipitacion'], stat)
                if result is not None:
                    precip_stats[f'precipitation_{stat}'] = result

            cluster_stats.update(precip_stats)

            # Estadísticas de otras variables meteorológicas
            cluster_stats['other_variables'] = {}
            meteorological_vars = ['humedad', 'temperatura', 'radiacion', 'velocidad', 'direccion', 'presion']

            for col in cluster_data.columns:
                if col in meteorological_vars:
                    col_stats = {}
                    for stat in ['mean', 'std']:
                        result = safe_stat_calculation(cluster_data[col], stat)
                        if result is not None:
                            col_stats[stat] = result

                    if col_stats:  # Solo incluir si hay estadísticas válidas
                        cluster_stats['other_variables'][col] = col_stats

            # Agregar metadatos útiles
            cluster_stats['data_quality'] = {
                'total_records': len(cluster_data),
                'valid_precipitation_records': cluster_data['precipitacion'].notna().sum(),
                'precipitation_completeness': round(cluster_data['precipitacion'].notna().sum() / len(cluster_data) * 100, 1)
            }

            insights[f'microclimate_{cluster_id}'] = cluster_stats

        return insights

    def _fig_to_base64(self, fig) -> str:
        """Convertir figura matplotlib a base64"""
        buf = io.BytesIO()
        fig.savefig(buf, format='png', dpi=100, bbox_inches='tight')
        buf.seek(0)
        image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
        buf.close()
        return f"data:image/png;base64,{image_base64}"

    def get_prediction_summary(self) -> Dict[str, Any]:
        """Generar resumen completo de predicciones"""
        return {
            'best_model': self.best_model_name if hasattr(self, 'best_model_name') else None,
            'best_score': self.best_score,
            'models_trained': list(self.models.keys()),
            'data_size': len(self.data) if self.data is not None else 0,
            'feature_count': len(self.data.columns) - 1 if self.data is not None else 0
        }
