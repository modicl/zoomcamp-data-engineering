import os
import gzip
import shutil
from datetime import datetime
from pathlib import Path
from typing import Optional
import logging
import requests

logger = logging.getLogger(__name__)


def download_and_extract_taxi_data(
    start_year: int = 2019,
    start_month: int = 1,
    end_year: int = 2021,
    end_month: int = 12,
    output_dir: str = "data/green_taxi",
    skip_on_error: bool = True
) -> dict:
    """
    Descarga datos de taxis verdes de NYC y los descomprime.

    Args:
        start_year: Año de inicio (default: 2019)
        start_month: Mes de inicio (default: 1)
        end_year: Año de fin (default: 2021)
        end_month: Mes de fin (default: 12)
        output_dir: Directorio donde guardar los archivos (default: "data/green_taxi")
        skip_on_error: Si True, continúa con el siguiente archivo si falla uno (default: True)

    Returns:
        dict con estadísticas de descarga: {'downloaded': int, 'failed': int, 'errors': list}
    """

    Path(output_dir).mkdir(parents=True, exist_ok=True)

    base_url = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green"

    stats = {
        'downloaded': 0,
        'failed': 0,
        'errors': []
    }

    # Generar lista de fechas
    current = datetime(start_year, start_month, 1)
    end = datetime(end_year, end_month, 1)

    while current <= end:
        year_month = current.strftime("%Y-%m")
        filename = f"green_tripdata_{year_month}.csv.gz"
        url = f"{base_url}/{filename}"

        try:
            logger.info(f"Descargando {filename}...")

            # Descargar archivo
            response = requests.get(url, timeout=30)
            response.raise_for_status()

            # Guardar archivo comprimido temporalmente
            gz_path = Path(output_dir) / filename
            csv_path = Path(output_dir) / filename.replace('.gz', '')

            with open(gz_path, 'wb') as f:
                f.write(response.content)

            # Descomprimir
            logger.info(f"Descomprimiendo {filename}...")
            with gzip.open(gz_path, 'rb') as f_in:
                with open(csv_path, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)

            # Eliminar archivo comprimido
            gz_path.unlink()

            logger.info(f"✓ {filename} descargado y descomprimido exitosamente")
            stats['downloaded'] += 1

        except Exception as e:
            error_msg = f"Error descargando {filename}: {str(e)}"
            logger.warning(error_msg)
            stats['failed'] += 1
            stats['errors'].append(error_msg)

            if not skip_on_error:
                raise

        # Pasar al siguiente mes
        if current.month == 12:
            current = datetime(current.year + 1, 1, 1)
        else:
            current = datetime(current.year, current.month + 1, 1)

    logger.info(f"\n=== RESUMEN ===")
    logger.info(f"Descargados exitosamente: {stats['downloaded']}")
    logger.info(f"Errores: {stats['failed']}")

    if stats['errors']:
        logger.warning("Errores encontrados:")
        for error in stats['errors']:
            logger.warning(f"  - {error}")

    return stats
