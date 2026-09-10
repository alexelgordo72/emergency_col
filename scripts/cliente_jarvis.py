import urllib.request
import urllib.error
import json
import subprocess
import os
import ssl
import speech_recognition as sr

API_URL = "http://localhost:8000/jarvis/analizar"

# --- CONFIGURACIÓN ELEVENLABS ---
ELEVEN_API_KEY = "sk_4fb6de6133c9619913540a6183f9183a3ef097a996a1b17a"
VOICE_ID = "pNInz6obpgDQGcFmaJgB" # Adam
AUDIO_FILE = "jarvis_response.mp3"

# Contexto SSL inseguro para evitar el error de certificados en Python en macOS
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def hablar(texto):
    print("[JARVIS sintetizando voz cinematográfica con ElevenLabs...]")
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVEN_API_KEY
    }
    
    payload = {
        "text": texto,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.8
        }
    }
    
    try:
        req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers, method='POST')
        # Pasamos el contexto SSL personalizado para saltar el bloqueo de certificados
        with urllib.request.urlopen(req, context=ctx) as response:
            with open(AUDIO_FILE, 'wb') as f:
                f.write(response.read())
        
        subprocess.run(["afplay", AUDIO_FILE])
        
        if os.path.exists(AUDIO_FILE):
            os.remove(AUDIO_FILE)
            
    except Exception as e:
        print(f"[Error en ElevenLabs]: {e}. Usando respaldo local de macOS...")
        subprocess.run(["say", "-v", "Paulina", f"[[rate 220]] {texto}"])

def escuchar():
    print(f"\n[🎙️ JARVIS está escuchando... Hable con calma, Señor (30 segundos)]")
    r = sr.Recognizer()
    r.energy_threshold = 300
    r.pause_threshold = 1.5
    
    try:
        with sr.Microphone(sample_rate=16000) as source:
            r.adjust_for_ambient_noise(source, duration=0.8)
            audio = r.listen(source, timeout=30, phrase_time_limit=30)
        
        print("[Procesando audio...]")
        texto = r.recognize_google(audio, language="es-CO")
        print(f"Usted dijo: {texto}")
        return texto
    except sr.WaitTimeoutError:
        print("[No se detectó voz a tiempo]")
        return None
    except sr.UnknownValueError:
        print("[No se entendió el audio. Hable más cerca del micrófono]")
        return None
    except Exception as e:
        print(f"[Aviso de captura]: {e}")
        fallback = input("Escriba su orden directamente (Plan B): ")
        return fallback if fallback.strip() else None

def consultar_jarvis(pregunta, operador):
    pregunta = pregunta.strip('"').strip("'")
    datos = json.dumps({"pregunta": pregunta, "operador": operador}).encode('utf-8')
    req = urllib.request.Request(API_URL, data=datos, headers={'Content-Type': 'application/json'})
    
    print("JARVIS consultando bases de datos y registros territoriales en GCP...")
    try:
        # Petición local a FastAPI (tampoco requiere verificación externa, pero usamos el mismo contexto por si acaso)
        with urllib.request.urlopen(req) as response:
            resultado = json.loads(response.read().decode('utf-8'))
            respuesta_texto = resultado.get("respuesta_jarvis", "No pude generar una respuesta.")
            
            print(f"\nJARVIS: {respuesta_texto}\n")
            hablar(respuesta_texto)
    except urllib.error.HTTPError as e:
        print(f"\n[ERROR 500]: {e.read().decode('utf-8')}")
    except Exception as e:
        print(f"\n[ERROR DE RED]: {e}")

if __name__ == "__main__":
    print("=== SISTEMA DE VOZ JARVIS (ELEVENLABS) INICIADO ===")
    operador_actual = input("Indique quién está al mando [Alex / Marcela]: ").strip()
    if not operador_actual:
        operador_actual = "Alex"
    print(f"\n[Modo activo: Operador {operador_actual}]")
    
    while True:
        opcion = input("\nPresione [ENTER] para hablar (o escriba 'salir'): ")
        if opcion.lower() == 'salir':
            break
        if opcion.strip() and opcion.lower() != 'salir':
            consultar_jarvis(opcion, operador_actual)
        else:
            orden = escuchar()
            if orden:
                consultar_jarvis(orden, operador_actual)
