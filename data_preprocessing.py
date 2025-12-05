"""
Módulo de Preprocesamiento y Exploración de Datos
Proyecto Final - Minería de Datos
Caracterización de Microclimas y Predicción de Precipitación
"""

import warnings
warnings.filterwarnings('ignore')

# Configurar matplotlib para entorno web (sin GUI)
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.impute import SimpleImputer, KNNImputer
from sklearn.feature_selection import mutual_info_regression
from scipy import stats
import io
import base64
from typing import Dict, List, Tuple, Any

class DataPreprocessor:
    def __init__(self):
        self.original_data = None
        self.processed_data = None
        self.preprocessing_steps = []
        self.missing_data_stats = {}
        self.outlier_stats = {}
        self.correlation_matrix = None
        self.feature_importance = {}

    def load_data(self, data_source, use_fast_mode: bool = False) -> pd.DataFrame:
        """Cargar datos desde archivo o dataframe directamente con opciones de optimización"""
        try:
            # Si es un string (filepath), cargar desde archivo
            if isinstance(data_source, str):
                file_path = data_source
                # Determine file type and read accordingly
                if file_path.lower().endswith(('.xlsx', '.xls')):
                    self.original_data = pd.read_excel(file_path, engine='openpyxl')
                elif file_path.lower().endswith('.csv'):
                    # Para modo rápido, usar configuraciones optimizadas
                    if use_fast_mode:
                        print("Usando modo rápido para carga de datos...")
                        # Leer solo columnas necesarias si es posible
                        try:
                            # Intentar leer una muestra primero para determinar tipos de datos óptimos
                            sample = pd.read_csv(file_path, nrows=1000, encoding='utf-8')
                            usecols = self._get_relevant_columns(sample.columns.tolist())
                            self.original_data = pd.read_csv(file_path, encoding='utf-8',
                                                           usecols=usecols if usecols else None,
                                                           low_memory=False)
                        except:
                            # Fallback a carga normal
                            self.original_data = pd.read_csv(file_path, encoding='utf-8', low_memory=False)
                    else:
                        self.original_data = pd.read_csv(file_path, encoding='utf-8', low_memory=False)
                else:
                    raise ValueError(f"Unsupported file format: {file_path}")

                source_desc = f"desde {file_path}"

            # Si es un DataFrame, usar directamente
            elif isinstance(data_source, pd.DataFrame):
                self.original_data = data_source.copy()
                source_desc = "dataframe combinado"

                # Para modo rápido en dataframes combinados, optimizar columnas
                if use_fast_mode and len(self.original_data.columns) > 15:
                    usecols = self._get_relevant_columns(self.original_data.columns.tolist())
                    if usecols:
                        self.original_data = self.original_data[usecols]
                        print(f"Optimizando dataframe: usando {len(usecols)} columnas relevantes")

            else:
                raise ValueError("data_source debe ser un filepath (str) o un DataFrame")

            # Aplicar limpieza robusta de datos después de cargar
            self.original_data = self._robust_data_cleaning(self.original_data)

            self.processed_data = self.original_data.copy()
            self.preprocessing_steps.append(f"Datos cargados {source_desc} ({len(self.original_data)} filas)")
            return self.original_data
        except Exception as e:
            raise Exception(f"Error al cargar datos: {str(e)}")

    def _robust_data_cleaning(self, df: pd.DataFrame) -> pd.DataFrame:
        """Limpieza robusta de datos para manejar formatos específicos"""
        print("🧹 Aplicando limpieza robusta de datos...")

        # Hacer una copia para no modificar el original
        cleaned_df = df.copy()

        # 1. Manejar valores faltantes representados de diferentes formas
        missing_values = ['-', '--', 'nan', 'NaN', 'NULL', 'null', '', ' ']
        cleaned_df.replace(missing_values, np.nan, inplace=True)

        # 2. Convertir separadores decimales (coma a punto) para columnas numéricas
        potential_numeric_columns = []
        for col in cleaned_df.columns:
            # Skip columnas que claramente no son numéricas
            if col.lower() in ['fecha', 'hora', 'observaciones', '_source_file'] or 'fecha' in col.lower() or 'hora' in col.lower():
                continue

            # Verificar si la columna podría contener números
            sample = cleaned_df[col].dropna().head(100)  # Tomar muestra
            if len(sample) > 0:
                # Verificar si contiene caracteres numéricos o comas/puntos
                sample_str = sample.astype(str)
                has_numbers = sample_str.str.contains(r'[0-9]', regex=True).any()
                has_commas_or_dots = sample_str.str.contains(r'[,.]', regex=True).any()

                if has_numbers or has_commas_or_dots:
                    potential_numeric_columns.append(col)

        # Procesar columnas potencialmente numéricas
        for col in potential_numeric_columns:
            try:
                # Convertir a string primero
                temp_series = cleaned_df[col].astype(str)

                # Reemplazar comas por puntos para decimales
                temp_series = temp_series.str.replace(',', '.', regex=False)

                # Intentar convertir a numérico
                numeric_series = pd.to_numeric(temp_series, errors='coerce')

                # Solo convertir si al menos 50% de los valores son numéricos válidos
                valid_ratio = numeric_series.notna().sum() / len(numeric_series)
                if valid_ratio >= 0.5:
                    cleaned_df[col] = numeric_series
                    print(f"✅ Columna '{col}' convertida a numérica ({valid_ratio:.1%} valores válidos)")
                else:
                    print(f"⚠️  Columna '{col}' mantenida como texto (solo {valid_ratio:.1%} valores numéricos)")

            except Exception as e:
                print(f"⚠️  Error procesando columna '{col}': {e}")

        # 3. Limpiar columnas de texto
        for col in cleaned_df.select_dtypes(include=['object']).columns:
            if col not in ['fecha', 'hora', 'observaciones', '_source_file']:
                # Limpiar espacios extra y caracteres problemáticos
                cleaned_df[col] = cleaned_df[col].astype(str).str.strip()

        print("✅ Limpieza robusta de datos completada")
        return cleaned_df

    def _get_relevant_columns(self, all_columns):
        """Determinar qué columnas son relevantes para el análisis meteorológico"""
        # Columnas críticas que SIEMPRE deben mantenerse (núcleo del análisis)
        critical_patterns = [
            'estacion', 'humedad', 'precipitacion', 'temperatura', 'radiacion',
            'velocidad', 'direccion', 'presion'
        ]

        # Columnas importantes pero no críticas
        important_patterns = [
            'fecha', 'hora', 'caudal', 'nivel', 'evapo'
        ]

        relevant_cols = []
        critical_cols = []

        for col in all_columns:
            col_lower = col.lower().strip()

            # Siempre incluir columnas críticas
            if any(pattern in col_lower for pattern in critical_patterns):
                relevant_cols.append(col)
                critical_cols.append(col)

            # Incluir columnas importantes si no son demasiado específicas
            elif any(pattern in col_lower for pattern in important_patterns):
                relevant_cols.append(col)

        # Si tenemos suficientes columnas críticas, usar enfoque selectivo
        if len(critical_cols) >= 3:  # Al menos estacion, temperatura y una variable meteorológica
            # Asegurar que tenemos al menos algunas columnas importantes
            if len(relevant_cols) < 6 and len(all_columns) > 10:
                # Agregar algunas columnas adicionales si tenemos espacio
                extra_cols = [col for col in all_columns if col not in relevant_cols][:4]  # Máximo 4 adicionales
                relevant_cols.extend(extra_cols)

            print(f"Optimizando carga: usando {len(relevant_cols)} columnas relevantes de {len(all_columns)} totales")
            print(f"Columnas críticas incluidas: {critical_cols}")
            return relevant_cols

        # Si no tenemos suficientes columnas críticas, usar todas (para evitar perder datos)
        print(f"Pocas columnas críticas encontradas ({len(critical_cols)}), usando todas las columnas")
        return None  # Usar todas las columnas

    def analyze_missing_data(self) -> Dict[str, Any]:
        """Analizar datos faltantes"""
        missing_info = {}
        total_rows = len(self.processed_data)

        for column in self.processed_data.columns:
            missing_count = self.processed_data[column].isnull().sum()
            missing_percentage = (missing_count / total_rows) * 100

            missing_info[column] = {
                'count': missing_count,
                'percentage': missing_percentage,
                'data_type': str(self.processed_data[column].dtype)
            }

        self.missing_data_stats = missing_info
        self.preprocessing_steps.append("Análisis de datos faltantes completado")
        return missing_info

    def clean_column_names(self) -> None:
        """Limpiar y estandarizar nombres de columnas"""
        self.processed_data.columns = (
            self.processed_data.columns
            .str.strip()
            .str.lower()
            .str.replace(' ', '_')
            .str.replace(r'[^\w]', '', regex=True)
        )
        self.preprocessing_steps.append("Nombres de columnas limpiados y estandarizados")

    def handle_missing_values(self, strategy: str = 'auto') -> None:
        """Manejar valores faltantes con diferentes estrategias"""
        numeric_columns = self.processed_data.select_dtypes(include=[np.number]).columns
        categorical_columns = self.processed_data.select_dtypes(include=['object']).columns

        # Para columnas numéricas
        if len(numeric_columns) > 0:
            if strategy == 'knn':
                imputer = KNNImputer(n_neighbors=5)
                self.processed_data[numeric_columns] = imputer.fit_transform(self.processed_data[numeric_columns])
                self.preprocessing_steps.append("Imputación KNN aplicada a variables numéricas")
            else:
                imputer = SimpleImputer(strategy='median')
                self.processed_data[numeric_columns] = imputer.fit_transform(self.processed_data[numeric_columns])
                self.preprocessing_steps.append("Imputación con mediana aplicada a variables numéricas")

        # Para columnas categóricas
        if len(categorical_columns) > 0:
            for col in categorical_columns:
                if self.processed_data[col].isnull().any():
                    mode_value = self.processed_data[col].mode()
                    if len(mode_value) > 0:
                        self.processed_data[col].fillna(mode_value[0], inplace=True)
            self.preprocessing_steps.append("Imputación con moda aplicada a variables categóricas")

    def detect_outliers(self, method: str = 'iqr') -> Dict[str, Any]:
        """Detectar outliers usando diferentes métodos"""
        outlier_info = {}
        numeric_columns = self.processed_data.select_dtypes(include=[np.number]).columns

        for column in numeric_columns:
            if method == 'iqr':
                Q1 = self.processed_data[column].quantile(0.25)
                Q3 = self.processed_data[column].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR

                outliers = self.processed_data[
                    (self.processed_data[column] < lower_bound) |
                    (self.processed_data[column] > upper_bound)
                ][column]

                outlier_info[column] = {
                    'count': len(outliers),
                    'percentage': (len(outliers) / len(self.processed_data)) * 100,
                    'lower_bound': lower_bound,
                    'upper_bound': upper_bound
                }
            elif method == 'zscore':
                z_scores = np.abs(stats.zscore(self.processed_data[column]))
                outliers = self.processed_data[z_scores > 3][column]

                outlier_info[column] = {
                    'count': len(outliers),
                    'percentage': (len(outliers) / len(self.processed_data)) * 100,
                    'method': 'Z-Score > 3'
                }

        self.outlier_stats = outlier_info
        self.preprocessing_steps.append(f"Detección de outliers usando método {method}")
        return outlier_info

    def remove_outliers(self, method: str = 'iqr', columns: List[str] = None) -> None:
        """Remover outliers"""
        if columns is None:
            columns = self.processed_data.select_dtypes(include=[np.number]).columns

        for column in columns:
            if method == 'iqr':
                Q1 = self.processed_data[column].quantile(0.25)
                Q3 = self.processed_data[column].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR

                initial_count = len(self.processed_data)
                self.processed_data = self.processed_data[
                    (self.processed_data[column] >= lower_bound) &
                    (self.processed_data[column] <= upper_bound)
                ]
                final_count = len(self.processed_data)

                removed = initial_count - final_count
                self.preprocessing_steps.append(f"Removidos {removed} outliers de {column}")

    def normalize_data(self, method: str = 'standard') -> None:
        """Normalizar datos numéricos"""
        numeric_columns = self.processed_data.select_dtypes(include=[np.number]).columns

        if method == 'standard':
            scaler = StandardScaler()
            self.processed_data[numeric_columns] = scaler.fit_transform(self.processed_data[numeric_columns])
            self.preprocessing_steps.append("Normalización estándar (Z-score) aplicada")
        elif method == 'minmax':
            from sklearn.preprocessing import MinMaxScaler
            scaler = MinMaxScaler()
            self.processed_data[numeric_columns] = scaler.fit_transform(self.processed_data[numeric_columns])
            self.preprocessing_steps.append("Normalización Min-Max aplicada")

    def encode_categorical_variables(self) -> None:
        """Codificar variables categóricas con manejo robusto de tipos mixtos"""
        # Identificar columnas que parecen categóricas pero pueden tener tipos mixtos
        potential_categorical = []

        for column in self.processed_data.columns:
            # Skip columnas que claramente no son categóricas
            if column in ['fecha', 'hora', '_source_file'] or 'fecha' in column.lower() or 'hora' in column.lower():
                continue

            unique_count = self.processed_data[column].nunique()
            total_count = len(self.processed_data[column])

            # Considerar categórica si tiene pocos valores únicos relativos al total
            if unique_count <= min(20, total_count * 0.1):  # Máximo 20 categorías o 10% del total
                potential_categorical.append(column)

        for column in potential_categorical:
            try:
                # Convertir a string primero para manejar tipos mixtos
                temp_series = self.processed_data[column].astype(str)

                # Limpiar valores comunes que no aportan información
                temp_series = temp_series.replace(['nan', 'None', 'NaN', ''], 'missing')

                if temp_series.nunique() <= 10:  # One-hot encoding para categorías limitadas
                    dummies = pd.get_dummies(temp_series, prefix=column)
                    self.processed_data = pd.concat([self.processed_data, dummies], axis=1)
                    self.processed_data.drop(column, axis=1, inplace=True)
                elif temp_series.nunique() <= 50:  # Label encoding para categorías moderadas
                    from sklearn.preprocessing import LabelEncoder
                    le = LabelEncoder()
                    self.processed_data[column] = le.fit_transform(temp_series)
                else:
                    # Para muchas categorías, mantener como está o convertir a frecuencia
                    self.processed_data[column] = temp_series

            except Exception as e:
                print(f"⚠️  Error codificando columna {column}: {e}")
                # En caso de error, convertir a string simple
                self.processed_data[column] = self.processed_data[column].astype(str)

        self.preprocessing_steps.append("Variables categóricas codificadas (con manejo de tipos mixtos)")

    def perform_eda(self) -> Dict[str, Any]:
        """Realizar Análisis Exploratorio de Datos"""
        eda_results = {
            'basic_stats': {},
            'correlation_matrix': {},
            'distributions': {},
            'plots': {}
        }

        # Estadísticas básicas
        numeric_columns = self.processed_data.select_dtypes(include=[np.number]).columns

        # Verificar que tenemos columnas numéricas para analizar
        if len(numeric_columns) == 0:
            print("⚠️  No se encontraron columnas numéricas para el análisis EDA")
            self.preprocessing_steps.append("Análisis Exploratorio de Datos omitido - no hay columnas numéricas")
            return eda_results

        try:
            eda_results['basic_stats'] = self.processed_data[numeric_columns].describe().to_dict()
        except Exception as e:
            print(f"⚠️  Error al calcular estadísticas básicas: {e}")
            eda_results['basic_stats'] = {'error': str(e)}

        # Matriz de correlación
        if len(numeric_columns) > 1:
            correlation_matrix = self.processed_data[numeric_columns].corr()
            self.correlation_matrix = correlation_matrix
            eda_results['correlation_matrix'] = correlation_matrix.to_dict()

        # Análisis de distribuciones
        for column in numeric_columns:
            eda_results['distributions'][column] = {
                'skewness': self.processed_data[column].skew(),
                'kurtosis': self.processed_data[column].kurtosis(),
                'normality_test': stats.shapiro(self.processed_data[column].sample(min(5000, len(self.processed_data))))[1]
            }

        self.preprocessing_steps.append("Análisis Exploratorio de Datos completado")
        return eda_results

    def generate_plots(self) -> Dict[str, str]:
        """Generar gráficos para EDA"""
        plots = {}

        # Configurar estilo de matplotlib
        plt.style.use('default')
        sns.set_palette("husl")

        numeric_columns = self.processed_data.select_dtypes(include=[np.number]).columns

        # Histograma de variables numéricas
        if len(numeric_columns) > 0:
            fig, axes = plt.subplots(len(numeric_columns), 1, figsize=(10, 4 * len(numeric_columns)))
            if len(numeric_columns) == 1:
                axes = [axes]

            for i, col in enumerate(numeric_columns):
                axes[i].hist(self.processed_data[col], bins=30, alpha=0.7, edgecolor='black')
                axes[i].set_title(f'Distribución de {col}')
                axes[i].set_xlabel(col)
                axes[i].set_ylabel('Frecuencia')

            plt.tight_layout()
            plots['histograms'] = self._fig_to_base64(fig)
            plt.close()

        # Matriz de correlación
        if len(numeric_columns) > 1 and self.correlation_matrix is not None:
            fig, ax = plt.subplots(figsize=(10, 8))
            sns.heatmap(self.correlation_matrix, annot=True, cmap='coolwarm', center=0,
                       square=True, ax=ax)
            ax.set_title('Matriz de Correlación')
            plt.tight_layout()
            plots['correlation'] = self._fig_to_base64(fig)
            plt.close()

        # Box plots
        if len(numeric_columns) > 0:
            fig, ax = plt.subplots(figsize=(12, 6))
            self.processed_data[numeric_columns].boxplot(ax=ax)
            ax.set_title('Diagramas de Caja de Variables Numéricas')
            ax.tick_params(axis='x', rotation=45)
            plt.tight_layout()
            plots['boxplots'] = self._fig_to_base64(fig)
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

    def get_summary_report(self) -> Dict[str, Any]:
        """Generar reporte resumen del preprocesamiento"""
        return {
            'original_shape': self.original_data.shape if self.original_data is not None else None,
            'processed_shape': self.processed_data.shape,
            'preprocessing_steps': self.preprocessing_steps,
            'missing_data_stats': self.missing_data_stats,
            'outlier_stats': self.outlier_stats,
            'columns_info': {
                col: str(dtype) for col, dtype in self.processed_data.dtypes.items()
            }
        }
