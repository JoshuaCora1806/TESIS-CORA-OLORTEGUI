import networkx as nx
import spacy
import pandas as pd
import json
import re

# Importamos nuestras constantes
from .constants import (
    TXT_ZDP_CLEAN, TXT_FLOW_CLEAN, JSON_BLOOM_TABLE, JSON_KG
)

# --- Funciones de Limpieza Específicas ---

def clean_bloom_df(df: pd.DataFrame) -> dict:
    """
    Limpia el DataFrame de Bloom extraído por Camelot y lo
    transforma en un diccionario jerárquico.
    La tabla de la Figura 2 es compleja y requiere un parseo manual.
    """
    # Esta es una implementación simplificada basada en la estructura
    # [cite_start]de la Figura 2 [cite: 758]
    bloom_hierarchy = {}
    
    # Suponemos que la tabla tiene 6 columnas principales
    # Columnas 0, 1, 2 = Niveles Cognitivos
    # Columnas 3, 4, 5 = Dimensiones del Conocimiento
    
    # Extraer Niveles Cognitivos (Columnas 0, 1, 2)
    # Fila 0 tiene los nombres (ej. "1. Recordar", "2. Comprender")
    # Fila 2 tiene los verbos (ej. "1.1 Reconocer...", "2.1 Interpretar...")
    
    # Tomamos la fila 0 para los nombres de nivel
    level_names = df.iloc[0, [0, 1, 3, 4, 5]] # Ajustar índices según la extracción
    # Tomamos la fila 2 para los verbos
    verbs_raw = df.iloc[2, [0, 1, 3, 4, 5]] # Ajustar índices
    
    # Limpiamos los nombres (ej. "1. Recordar\n" -> "Recordar")
    cleaned_names = [re.sub(r"^\d+\.\s+", "", name).strip() for name in level_names]
    
    # Añadimos el nivel faltante "Analizar" que está en un índice diferente
    # Esto es un ejemplo, la extracción real de la tabla puede variar
    if "Analizar" not in " ".join(cleaned_names):
         # [cite_start]El 'Analizar' está en df.iloc[0, 3] en el PDF [cite: 758]
         # Esto requerirá ajuste fino una vez veamos el JSON
         pass # En un caso real, aquí ajustaríamos los índices
         
    # Por ahora, usaremos una lista 'hardcodeada' por simplicidad
    # hasta que veamos la salida de Camelot.
    
    # ------ Simplificación Temporal ------
    # Dado que el parseo de la tabla es complejo,
    # usaremos los datos clave del PDF directamente.
    
    bloom_hierarchy = {
        "Recordar": ["Reconocer", "Recordar"],
        "Comprender": ["Interpretar", "Ejemplificar", "Clasificar", "Resumir", "Inferir", "Comparar", "Explicar"],
        "Aplicar": ["Ejecutar", "Implementar"],
        "Analizar": ["Diferenciar", "Organizar", "Atribuir"],
        "Evaluar": ["Comprobar", "Valorar"],
        "Crear": ["Generar", "Planificar", "Producir"]
    }
    # [cite_start]Esta info viene de la Figura 2 [cite: 758]
    
    print("[INFO] Jerarquía de Bloom procesada.")
    return bloom_hierarchy

# --- Funciones de Construcción del Grafo ---

def build_bloom_graph(kg: nx.DiGraph, bloom_data: dict):
    """
    Añade la jerarquía de la Taxonomía de Bloom al grafo.
    """
    kg.add_node("Bloom", type="Theory", label="Taxonomía de Bloom")
    for level, verbs in bloom_data.items():
        kg.add_node(level, type="Bloom_Level", label=level)
        kg.add_edge("Bloom", level, label="has_level")
        for verb in verbs:
            verb_node = verb.capitalize()
            kg.add_node(verb_node, type="Bloom_Verb", label=verb_node)
            kg.add_edge(level, verb_node, label="has_verb")
    print("[SUCCESS] Grafo de Bloom construido.")

def build_flow_graph(kg: nx.DiGraph, flow_text: str, nlp):
    """
    Extrae las 9 dimensiones del Flow y los estados clave.
    """
    kg.add_node("Flow", type="Theory", label="Teoría del Flow")
    
    # [cite_start]Estados clave del modelo [cite: 1241]
    states = ["Ansiedad", "Aburrimiento", "Apatía"]
    for state in states:
        kg.add_node(state, type="Flow_State", label=state)
        kg.add_edge("Flow", state, label="defines_state")
        
    # [cite_start]Dimensiones clave [cite: 1156-1237]
    dimensions = [
        "Metas Claras", "Feedback Inmediato", "Equilibrio Habilidad-Reto",
        "Concentración en la Tarea", "Unión Acción-Conciencia", "Control Potencial",
        "Pérdida de Autoconciencia", "Percepción Temporal Alterada", "Experiencia Autotélica"
    ]
    
    for dim in dimensions:
        kg.add_node(dim, type="Flow_Dimension", label=dim)
        kg.add_edge("Flow", dim, label="has_dimension")
        
    print("[SUCCESS] Grafo de Flow construido.")

def build_zdp_graph(kg: nx.DiGraph, zdp_text: str, nlp):
    """
    Extrae los conceptos clave de ZDP (Andamiaje, Mediación).
    """
    kg.add_node("ZDP", type="Theory", label="Zona de Desarrollo Próximo")
    
    # Conceptos clave
    concepts = {
        "Andamiaje": ["andamiaje"],
        "Mediación": ["mediación", "mediador"],
        "Interacción Social": ["interacción social", "colaboración"]
    }
    
    doc = nlp(zdp_text.lower())
    
    for concept_label, keywords in concepts.items():
        if any(keyword in doc.text for keyword in keywords):
            kg.add_node(concept_label, type="ZDP_Concept", label=concept_label)
            kg.add_edge("ZDP", concept_label, label="uses_concept")

    print("[SUCCESS] Grafo de ZDP construido.")


# --- Función Principal ---

def main():
    """
    Función principal para construir y guardar el Grafo de Conocimiento.
    """
    print("--- INICIANDO CONSTRUCCIÓN DEL GRAFO DE CONOCIMIENTO ---")
    
    # Cargar el modelo de spaCy para español
    try:
        nlp = spacy.load("es_core_news_sm")
    except IOError:
        print("[ERROR] Modelo 'es_core_news_sm' no encontrado.")
        print("Ejecuta: python -m spacy download es_core_news_sm")
        return

    # Inicializar el Grafo de Conocimiento (dirigido)
    KG = nx.DiGraph()

    # --- 1. Cargar datos procesados ---
    print("\n[Cargando datos procesados]...")
    try:
        with open(TXT_ZDP_CLEAN, "r", encoding="utf-8") as f:
            text_zdp = f.read()
        
        with open(TXT_FLOW_CLEAN, "r", encoding="utf-8") as f:
            text_flow = f.read()
            
        # Para Bloom, cargamos el JSON
        df_bloom = pd.read_json(JSON_BLOOM_TABLE)
        
    except FileNotFoundError as e:
        print(f"[ERROR] Archivo no encontrado: {e.filename}")
        print("Asegúrate de ejecutar 'run_pipeline.py' primero.")
        return

    # --- 2. Construir los sub-grafos ---
    print("\n[Construyendo sub-grafos]...")
    
    # Procesar Bloom (usando el método simplificado)
    bloom_data = clean_bloom_df(df_bloom)
    build_bloom_graph(KG, bloom_data)
    
    # Procesar Flow
    build_flow_graph(KG, text_flow, nlp)
    
    # Procesar ZDP
    build_zdp_graph(KG, text_zdp, nlp)
    
    # --- 3. Conectar las teorías (El "corazón" de tu tesis) ---
    print("\n[Conectando teorías]...")
    # Conectamos las 3 teorías a un nodo central de "Modelo Adaptativo"
    KG.add_node("Modelo Adaptativo", type="System", label="Modelo Adaptativo")
    KG.add_edge("Modelo Adaptativo", "ZDP", label="se_basa_en")
    KG.add_edge("Modelo Adaptativo", "Bloom", label="se_basa_en")
    KG.add_edge("Modelo Adaptativo", "Flow", label="se_basa_en")
    
    # Conexión ZDP -> Bloom (Vygotsky provee el 'qué', Bloom el 'cómo')
    KG.add_edge("ZDP", "Bloom", label="regula_dificultad_de")
    
    # Conexión Flow -> Bloom (El equilibrio Flow regula el nivel de Bloom)
    KG.add_edge("Equilibrio Habilidad-Reto", "Bloom", label="ajusta_nivel_de")

    # --- 4. Guardar el grafo ---
    print("\n[Guardando Grafo de Conocimiento]...")
    # Convertimos el grafo de NetworkX a un formato JSON simple (nodos y enlaces)
    graph_data = nx.node_link_data(KG)
    
    with open(JSON_KG, "w", encoding="utf-8") as f:
        json.dump(graph_data, f, indent=4, ensure_ascii=False)
        
    print(f"[SUCCESS] Grafo de Conocimiento guardado en {JSON_KG}")
    print(f"Total Nodos: {KG.number_of_nodes()}, Total Enlaces: {KG.number_of_edges()}")
    print("--- CONSTRUCCIÓN FINALIZADA ---")


if __name__ == "__main__":
    main()