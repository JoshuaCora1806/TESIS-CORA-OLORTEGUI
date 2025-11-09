import re

# --- RUTAS DE ARCHIVOS ---
# Usamos pathlib para manejar las rutas de forma robusta
from pathlib import Path

# Ruta base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Rutas de datos RAW
DATA_RAW_DIR = BASE_DIR / "data" / "raw"
PDF_ZDP = DATA_RAW_DIR / "ZonaDeDesarrolloProximo.pdf"
PDF_BLOOM = DATA_RAW_DIR / "TaxonomiaDeBloom.pdf"
PDF_FLOW = DATA_RAW_DIR / "TeoriaDelFlow.pdf"

# Rutas de datos PROCESSED
DATA_PROCESSED_DIR = BASE_DIR / "data" / "processed"
TXT_ZDP_CLEAN = DATA_PROCESSED_DIR / "zdp_clean.txt"
TXT_FLOW_CLEAN = DATA_PROCESSED_DIR / "flow_clean.txt"
JSON_BLOOM_TABLE = DATA_PROCESSED_DIR / "bloom_table.json"
JSON_KG = DATA_PROCESSED_DIR / "knowledge_graph.json"


# --- PATRONES DE LIMPIEZA ---
# Patrones a eliminar del PDF de ZDP
ZDP_CLEANUP_PATTERNS = re.compile(
    r"Didasc@lia: Didáctica y Educación\."
    r"|Michel Enrique Gamboa Graus"
    r"|ISSN 2224-2643"
    r"|Vol\. X\. Año 2019\. Número 4, Octubre-Diciembre"
    r"|Revista Didasc@lia: D&E\. Publicación del CEPUT - Las Tunas, CUBA"
    r"|LA ZONA DE DESARROLLO PRÓXIMO"
    r"|\d{1,2}\n?$"
)

# Patrones a eliminar del PDF de Bloom
BLOOM_CLEANUP_PATTERNS = re.compile(
    r"Reflexiones y experiencias investigativas para la innovación"
    r"|Revista Innovaciones Educativas / ISSN 2215-4132/Vol\. 25 / Número 38 / Enero - Junio, 2023"
    r"|Innovaciones\nEducativas"
    r"|GAMBOA SOLANO/GUEVARA MORA/\nMENA/UMAÑA MATA"
    r"|REVISTA INNOVACIONES EDUCATIVAS\nCorreo: innoveducativas@uned\.ac\.cr"
    r"|Artículo protegido por licencia Creative Commons"
    r"|\d{3}\n?$"
)

# Patrones a eliminar del PDF de Flow
FLOW_CLEANUP_PATTERNS = re.compile(
    r"Flow: una perspectiva\ndicotómica"
    r"|Rosa M Abdón Ferré"
    r"|Trabajo Final de Grado de Criminología"
    r"|Dirigido por Sergi Rufí Cano"
    r"|Curso 2013-2014"
    r"|\d{1,2}\n?$"
)
# --- CONSTANTES ESPECÍFICAS ---
# Página que contiene la tabla clave en el PDF de Bloom
BLOOM_TABLE_PAGE = 5