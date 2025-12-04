"""
Proyecto Final - Minería de Datos
Tema: Caracterización de Microclimas y Predicción de Precipitación en Zonas Urbanas Utilizando Algoritmos de Minería de Datos

Integrante del proyecto:
- Daniel Mejia Suaza
"""

import pandas as pd
import os

# Import high-performance libraries for adaptive processing
try:
    import polars as pl
    POLARS_AVAILABLE = True
except ImportError:
    POLARS_AVAILABLE = False
    print("Polars no disponible, usando pandas estándar")

try:
    import dask.dataframe as dd
    DASK_AVAILABLE = True
except ImportError:
    DASK_AVAILABLE = False
    print("Dask no disponible, usando procesamiento estándar")

def read_excel_by_name(filename, sample_size=None, chunk_size=None):
    """
    Function to read Excel or CSV files by its name with optimized loading for large files.

    Parameters:
    filename (str): The name of the Excel/CSV file to read (including extension, e.g., 'data.xlsx' or 'data.csv')
    sample_size (int, optional): If specified, randomly sample this many rows for faster processing
    chunk_size (int, optional): If specified, read file in chunks of this size

    Returns:
    pd.DataFrame: The DataFrame containing the data, or None if file not found or error occurs
    """
    try:
        # Check if file exists in current directory
        if not os.path.isfile(filename):
            print(f"Error: File '{filename}' not found in the current directory.")
            return None

        # Get file size for optimization decisions
        file_size = os.path.getsize(filename) / (1024 * 1024)  # Size in MB
        print(f"File size: {file_size:.2f} MB")

        # Read the file based on extension
        if filename.lower().endswith(('.xlsx', '.xls')):
            # Read Excel file
            df = pd.read_excel(filename, engine='openpyxl')
            print(f"Successfully read Excel file: {filename}")
        elif filename.lower().endswith('.csv'):
            # Optimized CSV reading for large files
            if file_size > 100:  # Files larger than 100MB
                print("Large file detected, using optimized loading...")

                # First, read just the header to get column info
                header_df = pd.read_csv(filename, nrows=0, encoding='utf-8')
                print(f"Columns detected: {list(header_df.columns)}")

                # Determine optimal chunk size based on file size
                if chunk_size is None:
                    chunk_size = min(50000, max(10000, int(file_size * 1000)))  # Adaptive chunk size

                print(f"Reading in chunks of {chunk_size} rows...")

                # Read in chunks for memory efficiency
                chunks = []
                total_rows = 0

                for chunk in pd.read_csv(filename, encoding='utf-8', chunksize=chunk_size,
                                       low_memory=False, dtype=get_optimal_dtypes(filename)):
                    chunks.append(chunk)
                    total_rows += len(chunk)

                    # For very large files, limit to reasonable sample
                    if sample_size and total_rows >= sample_size * 2:
                        print(f"Reached sample limit, processing {total_rows} rows...")
                        break

                # Combine chunks efficiently
                df = pd.concat(chunks, ignore_index=True)

                # Apply sampling if requested
                if sample_size and len(df) > sample_size:
                    print(f"Sampling {sample_size} rows from {len(df)} total rows...")
                    df = df.sample(n=sample_size, random_state=42).reset_index(drop=True)

            else:
                # Standard reading for smaller files
                df = pd.read_csv(filename, encoding='utf-8', low_memory=False,
                               dtype=get_optimal_dtypes(filename))
                print(f"Successfully read CSV file: {filename}")

        else:
            print(f"Error: Unsupported file format. Only .xlsx, .xls, and .csv files are supported.")
            return None

        print(f"Final shape: {df.shape}")
        print(f"Memory usage: {df.memory_usage(deep=True).sum() / (1024*1024):.2f} MB")
        print("First 5 rows:")
        print(df.head())

        return df

    except UnicodeDecodeError:
        # Try different encodings for CSV files
        try:
            if filename.lower().endswith('.csv'):
                df = pd.read_csv(filename, encoding='latin1', low_memory=False)
                print(f"Successfully read CSV file with latin1 encoding: {filename}")
                print(f"Shape: {df.shape}")
                return df
        except Exception as e2:
            print(f"Error reading CSV file with different encodings '{filename}': {str(e2)}")
            return None
    except Exception as e:
        print(f"Error reading file '{filename}': {str(e)}")
        return None


def get_optimal_dtypes(filename):
    """
    Determine optimal data types for CSV columns to reduce memory usage.
    """
    # Read a small sample to infer dtypes
    try:
        sample = pd.read_csv(filename, nrows=1000, encoding='utf-8', low_memory=False)

        dtypes = {}
        for col in sample.columns:
            if col.lower() in ['fecha', 'hora', 'date', 'time']:
                # Keep datetime columns as object for now
                dtypes[col] = 'str'
            elif sample[col].dtype == 'object':
                # For categorical columns, check unique values
                unique_ratio = sample[col].nunique() / len(sample)
                if unique_ratio < 0.5:  # Less than 50% unique values
                    dtypes[col] = 'category'
                else:
                    dtypes[col] = 'str'
            else:
                # Keep numeric types as is
                dtypes[col] = sample[col].dtype

        return dtypes
    except:
        return None  # Fall back to pandas default inference

def read_csv_adaptive(filename, sample_size=None):
    """
    Adaptive CSV reader that chooses the best library based on data size and requirements.

    Strategy:
    - Small files (< 50k rows): Standard pandas
    - Medium files (50k-500k rows): Polars for speed
    - Large files (>500k rows): Dask for distributed processing
    - Very large files: Aggressive sampling + best available library
    """
    try:
        if not os.path.isfile(filename):
            print(f"Error: File '{filename}' not found.")
            return None

        # Get file size and estimate row count
        file_size_mb = os.path.getsize(filename) / (1024 * 1024)

        # Quick row count estimation (rough)
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                sample_lines = []
                for i, line in enumerate(f):
                    if i < 10:
                        sample_lines.append(line)
                    if i >= 1000:  # Sample first 1000 lines
                        break

            avg_line_length = sum(len(line) for line in sample_lines) / len(sample_lines)
            estimated_rows = int((file_size_mb * 1024 * 1024) / avg_line_length)
        except:
            estimated_rows = int(file_size_mb * 10000)  # Rough fallback estimate

        print(f"📊 File analysis: {file_size_mb:.1f}MB, ~{estimated_rows:,} estimated rows")

        # Choose optimal strategy based on data size
        if estimated_rows < 50000:  # Small datasets
            print("🟢 Using optimized pandas for small dataset")
            return read_csv_small(filename, sample_size)

        elif estimated_rows < 500000 and POLARS_AVAILABLE:  # Medium datasets
            print("🟡 Using Polars for medium dataset (fast processing)")
            return read_csv_polars(filename, sample_size)

        elif DASK_AVAILABLE:  # Large datasets
            print("🟠 Using Dask for large dataset (distributed processing)")
            return read_csv_dask(filename, sample_size)

        else:  # Fallback with aggressive sampling
            print("🔴 Using pandas with aggressive sampling (limited libraries)")
            effective_sample = min(sample_size or 30000, estimated_rows)
            return read_csv_small(filename, effective_sample)

    except Exception as e:
        print(f"❌ Error in adaptive reading: {e}")
        # Fallback to standard pandas
        return read_csv_small(filename, sample_size)


def read_csv_small(filename, sample_size=None):
    """Standard pandas reading with optimizations."""
    try:
        dtypes = get_optimal_dtypes(filename)
        df = pd.read_csv(filename, encoding='utf-8', dtype=dtypes, low_memory=False)

        if sample_size and len(df) > sample_size:
            df = df.sample(n=sample_size, random_state=42).reset_index(drop=True)
            print(f"Sampled to {len(df)} rows")

        return df
    except:
        # Fallback without dtypes
        df = pd.read_csv(filename, encoding='utf-8', low_memory=False)
        if sample_size and len(df) > sample_size:
            df = df.sample(n=sample_size, random_state=42).reset_index(drop=True)
        return df


def read_csv_polars(filename, sample_size=None):
    """Polars reading for medium datasets (much faster than pandas)."""
    try:
        # Read with Polars
        df_pl = pl.read_csv(filename, encoding='utf-8')

        # Convert to pandas for compatibility with existing code
        df = df_pl.to_pandas()

        if sample_size and len(df) > sample_size:
            df = df.sample(n=sample_size, random_state=42).reset_index(drop=True)
            print(f"Polars + sampling: {len(df)} rows")

        return df
    except Exception as e:
        print(f"Polars reading failed: {e}, falling back to pandas")
        return read_csv_small(filename, sample_size)


def read_csv_dask(filename, sample_size=None):
    """Dask reading for large datasets (distributed processing)."""
    try:
        # Read with Dask
        ddf = dd.read_csv(filename, encoding='utf-8', blocksize="64MB")

        # Sample if requested
        if sample_size:
            # For large datasets, sample a fraction first, then take exact amount
            fraction = min(1.0, (sample_size * 2) / ddf.shape[0].compute())
            ddf_sampled = ddf.sample(frac=fraction, random_state=42)
            df = ddf_sampled.compute()

            if len(df) > sample_size:
                df = df.sample(n=sample_size, random_state=42)
        else:
            df = ddf.compute()

        print(f"Dask processing completed: {len(df)} rows")
        return df

    except Exception as e:
        print(f"Dask reading failed: {e}, falling back to pandas")
        return read_csv_small(filename, sample_size)


# Example usage
if __name__ == "__main__":
    # Replace 'your_excel_file.xlsx' with the actual filename
    result = read_excel_by_name('your_excel_file.xlsx')
    if result is not None:
        print("Data loaded successfully!")
    else:
        print("Failed to load data.")
