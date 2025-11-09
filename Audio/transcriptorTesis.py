# transcriptorTesis.py

# 1. IMPORTS
import speech_recognition as sr

# 2. INICIALIZACIÓN GLOBAL
# El objeto recognizer se inicializa una sola vez cuando el servidor (backend) arranca.
recognizer = sr.Recognizer()

# 3. FUNCIÓN DE TRANSCRIPCIÓN CENTRAL
def transcribir_audio(audio_data: sr.AudioData, idioma: str = "es-ES") -> str:
    """
    Transcribe datos de audio usando la API de Google Speech Recognition.
    """
    try:
        texto = recognizer.recognize_google(audio_data, language=idioma)
        return texto
    except sr.UnknownValueError:
        return f"ERROR_TRANSCRIPCION: No se pudo entender el audio en el idioma '{idioma}'."
    except sr.RequestError as e:
        return f"ERROR_CONEXION: Fallo al solicitar resultados a Google API; {e}"

# 4. FUNCIÓN DE CAPTURA Y PRUEBA (Opcional, solo para pruebas locales)
# verificar que el micrófono y la transcripción funcionen sin la necesidad del backend web. 
# No se usa en producción web.
def capturar_y_transcribir_desde_microfono(idioma: str = "es-ES") -> str:
    """
    Captura audio del micrófono localmente y llama a la transcripción.
    """
    print(f"\n--- INICIANDO CAPTURA en {idioma} ---")
    with sr.Microphone() as source:
        print("Por favor, hable ahora...")
        recognizer.adjust_for_ambient_noise(source)
        
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            print("Audio capturado. Procesando...")
        except sr.WaitTimeoutError:
            return "ERROR_TIMEOUT: No se detectó voz dentro del límite de tiempo."
        except Exception as e:
            return f"ERROR_MICROFONO: Problema al acceder al micrófono: {e}"
        
    return transcribir_audio(audio, idioma)

# 5. BLOQUE DE EJECUCIÓN (Para demostración o pruebas unitarias)
if __name__ == '__main__':
    print("Ejecutando demostración local del servicio de transcripción...")
    
    # Ejemplo de uso:
    resultado_es = capturar_y_transcribir_desde_microfono(idioma="es-ES")
    print(f"\n[Resultado ES]: {resultado_es}")
    
    resultado_en = capturar_y_transcribir_desde_microfono(idioma="en-US")
    print(f"\n[Resultado EN]: {resultado_en}")