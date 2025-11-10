import pandas as pd

# Importamos nuestras funciones y constantes
from .constants import (
    PDF_ZDP, PDF_BLOOM, PDF_FLOW,
    ZDP_CLEANUP_PATTERNS, BLOOM_CLEANUP_PATTERNS, FLOW_CLEANUP_PATTERNS,
    BLOOM_TABLE_PAGE,
    TXT_ZDP_CLEAN, TXT_FLOW_CLEAN, JSON_BLOOM_TABLE
)

from .pdf_parser import (
    extract_text_from_pdf,
    clean_pdf_text,
    extract_table_from_pdf
)

def main():
    """
    Función principal para ejecutar el pipeline de extracción de texto.
    """
    print("--- INICIANDO PIPELINE DE MINERÍA DE TEXTO ---")
    
    # --- 1. Procesar ZONA DE DESARROLLO PRÓXIMO ---
    print("\n[Procesando ZDP]...")
    raw_text_zdp = extract_text_from_pdf(PDF_ZDP)
    clean_text_zdp = clean_pdf_text(raw_text_zdp, ZDP_CLEANUP_PATTERNS)
    
    # Guardar el texto limpio
    with open(TXT_ZDP_CLEAN, "w", encoding="utf-8") as f:
        f.write(clean_text_zdp)
    print(f"[ZDP] Texto limpio guardado en {TXT_ZDP_CLEAN}")
    print(f"[ZDP Sample] {clean_text_zdp[:200]}...") # Muestra los primeros 200 caracteres


    # --- 2. Procesar TEORÍA DEL FLOW ---
    print("\n[Procesando FLOW]...")
    raw_text_flow = extract_text_from_pdf(PDF_FLOW)
    clean_text_flow = clean_pdf_text(raw_text_flow, FLOW_CLEANUP_PATTERNS)
    
    # Guardar el texto limpio
    with open(TXT_FLOW_CLEAN, "w", encoding="utf-8") as f:
        f.write(clean_text_flow)
    print(f"[FLOW] Texto limpio guardado en {TXT_FLOW_CLEAN}")
    print(f"[FLOW Sample] {clean_text_flow[:200]}...")


    # --- 3. Procesar TAXONOMÍA DE BLOOM (Tabla) ---
    print("\n[Procesando BLOOM]...")
    # Configurar pandas para mostrar todas las columnas
    pd.set_option('display.max_columns', None)
    
    df_bloom = extract_table_from_pdf(PDF_BLOOM, BLOOM_TABLE_PAGE)
    
    if not df_bloom.empty:
        # Guardar la tabla como JSON
        df_bloom.to_json(JSON_BLOOM_TABLE, orient="records", indent=4)
        print(f"[BLOOM] Tabla guardada en {JSON_BLOOM_TABLE}")
        print("[BLOOM Sample]\n", df_bloom.head())

    print("\n--- PIPELINE FINALIZADO ---")

if __name__ == "__main__":
    main()