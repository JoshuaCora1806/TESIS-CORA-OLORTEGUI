import fitz
import camelot
import re
import pandas as pd
from typing import List, Pattern

# Importamos nuestras constantes
from .constants import (
    PDF_BLOOM,
    BLOOM_TABLE_PAGE
)

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extrae el texto crudo de todas las páginas de un archivo PDF.
    """
    doc = fitz.open(pdf_path)
    full_text = ""
    for page in doc:
        full_text += page.get_text() + "\n"
    doc.close()
    return full_text

def clean_pdf_text(text: str, noise_patterns: Pattern) -> str:
    """
    Limpia el texto crudo eliminando patrones de ruido (encabezados, pies de página)
    y corrigiendo saltos de línea.
    """
    # 1. Eliminar los patrones de ruido definidos en constants.py
    text = noise_patterns.sub("", text)
    
    # 2. Corregir saltos de línea con guion (ej. "conoci-miento")
    text = re.sub(r"-\n", "", text)
    
    # 3. Corregir saltos de línea innecesarios (unir párrafos)
    # Esto reemplaza un solo salto de línea con un espacio,
    # pero mantiene los saltos dobles (nuevos párrafos).
    text = re.sub(r"(?<!\n)\n(?!\n)", " ", text)
    
    # 4. Opcional: eliminar espacios/líneas múltiples
    text = re.sub(r"\s+", " ", text).strip()
    
    return text

def extract_table_from_pdf(pdf_path: str, page: int) -> pd.DataFrame:
    """
    Extrae la primera tabla encontrada en una página específica de un PDF
    usando Camelot.
    """
    print(f"[INFO] Extrayendo tabla de {pdf_path} (página {page})...")
    try:
        # 'lattice' es ideal para tablas con líneas visibles
        tables = camelot.read_pdf(str(pdf_path), pages=str(page), flavor='lattice')
        
        if tables:
            # Convertimos la tabla de camelot a un DataFrame de pandas
            df = tables[0].df
            print("[SUCCESS] Tabla extraída con éxito.")
            return df
        else:
            print("[ERROR] No se encontraron tablas en la página.")
            return pd.DataFrame()
            
    except Exception as e:
        print(f"[ERROR] Ocurrió un error al extraer la tabla: {e}")
        return pd.DataFrame()