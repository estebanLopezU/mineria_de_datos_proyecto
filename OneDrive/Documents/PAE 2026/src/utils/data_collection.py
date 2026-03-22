import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import json
import time
from datetime import datetime
import logging

# Configuración de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def search_datasets(query, limit=20):
    """
    Busca datasets en datos.gov.co relacionados con interoperabilidad
    Mejora: Búsqueda más robusta con manejo de paginación y diferentes selectores
    """
    search_url = "https://www.datos.gov.co/browse"
    params = {
        "q": query, 
        "sortBy": "relevance",
        "page": 1,
        "limit": limit
    }
    
    datasets = []
    page = 1
    
    while True:
        try:
            params["page"] = page
            response = requests.get(search_url, params=params, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Intentar diferentes selectores para mayor robustez
            selectors = [
                'li.dataset-item',
                'div.dataset-item',
                'article.dataset-item',
                '.browse2-result'
            ]
            
            found_items = False
            for selector in selectors:
                items = soup.select(selector)
                if items:
                    found_items = True
                    for item in items:
                        try:
                            # Buscar título
                            title_elem = item.find(['h3', 'h4', 'a'])
                            if title_elem:
                                title = title_elem.get_text(strip=True)
                                url = title_elem.get('href', '')
                                
                                # Buscar descripción
                                desc_elem = item.find(['p', '.description'])
                                description = desc_elem.get_text(strip=True) if desc_elem else ''
                                
                                # Buscar organización
                                org_elem = item.find(['span', '.organization'])
                                organization = org_elem.get_text(strip=True) if org_elem else ''
                                
                                datasets.append({
                                    'title': title,
                                    'url': url,
                                    'description': description,
                                    'organization': organization,
                                    'query': query,
                                    'search_date': datetime.now().isoformat()
                                })
                        except Exception as e:
                            logger.warning(f"Error procesando item: {e}")
                            continue
                    break
            
            if not found_items:
                logger.info(f"No se encontraron datasets en página {page}")
                break
                
            page += 1
            time.sleep(1)  # Evitar sobrecargar el servidor
            
        except requests.RequestException as e:
            logger.error(f"Error en la búsqueda: {e}")
            break
        except Exception as e:
            logger.error(f"Error inesperado: {e}")
            break
    
    return datasets

def get_dataset_details(dataset_url):
    """
    Obtiene detalles específicos de un dataset
    """
    try:
        response = requests.get(dataset_url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        details = {}
        
        # Intentar diferentes selectores para obtener información
        title_selectors = ['h1', '.dataset-title', '.title']
        for selector in title_selectors:
            title_elem = soup.select_one(selector)
            if title_elem:
                details['title'] = title_elem.get_text(strip=True)
                break
        
        # Descripción
        desc_selectors = ['.description', '.notes', 'p']
        for selector in desc_selectors:
            desc_elem = soup.select_one(selector)
            if desc_elem:
                details['description'] = desc_elem.get_text(strip=True)
                break
        
        # Metadatos
        metadata = {}
        meta_selectors = ['.metadata', '.info', '.details']
        for selector in meta_selectors:
            meta_elem = soup.select_one(selector)
            if meta_elem:
                # Extraer información de metadatos
                for item in meta_elem.find_all(['li', 'div']):
                    text = item.get_text(strip=True)
                    if ':' in text:
                        key, value = text.split(':', 1)
                        metadata[key.strip()] = value.strip()
        
        details['metadata'] = metadata
        return details
        
    except Exception as e:
        logger.error(f"Error obteniendo detalles del dataset: {e}")
        return {}

def download_dataset(dataset_info, format_type='csv'):
    """
    Descarga un dataset en el formato especificado
    """
    try:
        # Construir URL de descarga basada en el formato
        base_url = dataset_info['url']
        if format_type.lower() == 'csv':
            download_url = f"{base_url}.csv"
        elif format_type.lower() == 'json':
            download_url = f"{base_url}.json"
        else:
            download_url = f"{base_url}.{format_type}"
        
        response = requests.get(download_url, timeout=30)
        response.raise_for_status()
        
        # Crear nombre de archivo seguro
        filename = f"{dataset_info['title'].replace(' ', '_').replace('/', '_')}_{format_type}.{format_type}"
        filepath = os.path.join('datasets_descargados', filename)
        
        # Crear directorio si no existe
        os.makedirs('datasets_descargados', exist_ok=True)
        
        with open(filepath, 'wb') as f:
            f.write(response.content)
        
        logger.info(f"Descargado: {filename}")
        return filepath
        
    except Exception as e:
        logger.error(f"Error descargando dataset {dataset_info.get('title', 'desconocido')}: {e}")
        return None

def search_api_datasets():
    """
    Busca datasets que tengan API disponible
    """
    api_datasets = []
    
    # URLs de APIs conocidas de datos.gov.co
    api_urls = [
        "https://www.datos.gov.co/api/views/metadata/v1.json",
        "https://www.datos.gov.co/api/catalog/v1?only=datasets"
    ]
    
    for url in api_urls:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                try:
                    data = response.json()
                    if isinstance(data, list):
                        for item in data:
                            if isinstance(item, dict) and 'name' in item:
                                api_datasets.append({
                                    'name': item['name'],
                                    'id': item.get('id', ''),
                                    'url': item.get('url', ''),
                                    'api_available': True
                                })
                except json.JSONDecodeError:
                    logger.warning(f"Respuesta no JSON en {url}")
        except Exception as e:
            logger.error(f"Error consultando API {url}: {e}")
    
    return api_datasets

def main():
    """
    Función principal que coordina la recolección de datos
    """
    logger.info("Iniciando recolección de datos para análisis de interoperabilidad")
    
    # Consultas más específicas para interoperabilidad
    queries = [
        "interoperabilidad gobierno",
        "X-Road Colombia", 
        "Servicios Ciudadanos Digitales",
        "entidades públicas conectadas",
        "datos abiertos gobierno",
        "interoperabilidad sector salud",
        "interoperabilidad sector educación",
        "interoperabilidad sector hacienda"
    ]
    
    all_datasets = []
    
    for query in queries:
        logger.info(f"Buscando datasets para: {query}")
        datasets = search_datasets(query, limit=50)
        all_datasets.extend(datasets)
        logger.info(f"Encontrados {len(datasets)} datasets para '{query}'")
    
    # Guardar lista completa de datasets
    df_datasets = pd.DataFrame(all_datasets)
    df_datasets.to_csv('datasets_encontrados.csv', index=False)
    logger.info(f"Guardada lista de {len(all_datasets)} datasets en datasets_encontrados.csv")
    
    # Intentar descargar datasets relevantes
    downloaded_files = []
    for i, dataset in enumerate(all_datasets[:10]):  # Limitar a 10 para prueba
        logger.info(f"Procesando dataset {i+1}/{len(all_datasets[:10])}: {dataset['title']}")
        
        # Intentar descargar en diferentes formatos
        for format_type in ['csv', 'json']:
            filepath = download_dataset(dataset, format_type)
            if filepath:
                downloaded_files.append({
                    'dataset': dataset['title'],
                    'format': format_type,
                    'filepath': filepath,
                    'download_date': datetime.now().isoformat()
                })
                break  # Si se descarga en un formato, no intentar otros
    
    # Guardar registro de descargas
    if downloaded_files:
        df_downloads = pd.DataFrame(downloaded_files)
        df_downloads.to_csv('datasets_descargados.csv', index=False)
        logger.info(f"Descargados {len(downloaded_files)} datasets")
    
    # Buscar datasets con API
    logger.info("Buscando datasets con API disponible")
    api_datasets = search_api_datasets()
    if api_datasets:
        df_api = pd.DataFrame(api_datasets)
        df_api.to_csv('datasets_con_api.csv', index=False)
        logger.info(f"Encontrados {len(api_datasets)} datasets con API")
    
    # Generar reporte de búsqueda
    report = {
        'search_date': datetime.now().isoformat(),
        'total_queries': len(queries),
        'total_datasets_found': len(all_datasets),
        'datasets_downloaded': len(downloaded_files),
        'datasets_with_api': len(api_datasets),
        'queries': queries
    }
    
    with open('search_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    logger.info("Recolección de datos completada exitosamente")
    print(f"Resumen: {len(all_datasets)} datasets encontrados, {len(downloaded_files)} descargados, {len(api_datasets)} con API disponible")

if __name__ == "__main__":
    main()
