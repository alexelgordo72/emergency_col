"""
etl_rufe.py
Script principal del ETL para procesar formularios RUFE desde PDFs.
Con manejo inteligente de cuota (429) y reintentos.

Uso:
    python etl_rufe.py --pdf "30-08-2026/689-691-Rufe.pdf"
    python etl_rufe.py --carpeta "30-08-2026"
    python etl_rufe.py --todos
    python etl_rufe.py --reanudar
"""

import os
import sys
import time
import json
import re
import argparse
from pathlib import Path
from google import genai

# ============================================================
# CONFIGURACIÓN
# ============================================================

CARPETA_RAIZ = Path.home() / "Desktop" / "SGRD 2026"
CARPETA_OUTPUT = Path.home() / "etl" / "data" / "output"
CARPETA_LOGS = Path.home() / "etl" / "logs"
ARCHIVO_PROGRESO = Path.home() / "etl" / "data" / "progreso.json"

MODELO_GEMINI = "gemini-3.6-flash"
TIMEOUT_SEGUNDOS = 120
MAX_REINTENTOS = 5
PAUSA_ENTRE_PDFS = 5

PROMPT_RUFE = """
Eres un experto en digitalizar formularios RUFE (Registro Único de Familias en Emergencia) del SGRD Yumbo, Colombia.

El PDF contiene múltiples formularios RUFE manuscritos. Para CADA formulario, extrae TODA la información posible.

INSTRUCCIONES CRÍTICAS:
1. NO inventes datos. Si no puedes leer algo, pon null.
2. Lee CUIDADOSAMENTE todos los campos, incluso los manuscritos.
3. Para CÉDULAS y TELÉFONOS: transcribe los números SIN puntos, SIN espacios, SIN guiones.
4. Presta especial atención a:
   - La COMPOSICIÓN FAMILIAR (todos los miembros, no solo el jefe de hogar)
   - El PARENTESCO de cada miembro (Jefe de Hogar, Nieto/a, Yerno/Nuera, etc.)
   - El GÉNERO y EDAD de cada miembro
   - El EVALUADOR (nombre del ingeniero)
   - La PRIORIDAD explícita (ALTA, MEDIA, BAJA)
5. Devuelve un ARRAY JSON con TODOS los formularios del PDF.

Estructura del JSON para CADA formulario:

{
  "numero_rufe": "string",
  "fecha_evaluacion": "string|null",
  "evaluador": "string|null",
  "jefe_hogar": {
    "nombres": "string|null",
    "apellidos": "string|null",
    "tipo_documento": "CC|TI|CE|PA|null",
    "cedula": "string|null",
    "fecha_nacimiento": "string|null",
    "sexo": "M|F|null",
    "edad": "number|null",
    "telefono": "string|null",
    "direccion": "string|null",
    "barrio": "string|null",
    "comuna": "string|null",
    "corregimiento": "string|null",
    "zona": "Urbana|Rural|null"
  },
  "composicion_familiar": [
    {
      "nombres": "string|null",
      "apellidos": "string|null",
      "tipo_documento": "CC|TI|CE|PA|null",
      "cedula": "string|null",
      "parentesco": "string|null",
      "sexo": "M|F|null",
      "edad": "number|null",
      "discapacidad": "string|null",
      "enfermedad": "string|null"
    }
  ],
  "total_personas_hogar": "number|null",
  "evaluacion_danos": {
    "nivel_riesgo": "Alto|Medio|Bajo|null",
    "prioridad": "ALTA|MEDIA|BAJA|null",
    "habitabilidad": "Habitable|No Habitable|null",
    "tipo_afectacion": "string|null",
    "descripcion_danos": "string|null",
    "observaciones_evaluador": "string|null"
  },
  "vivienda": {
    "tipo_vivienda": "string|null",
    "numero_plantas": "number|null",
    "material_paredes": "string|null",
    "material_pisos": "string|null",
    "material_techo": "string|null",
    "estado_general": "string|null"
  },
  "necesidades": {
    "alimentacion": "boolean|null",
    "alojamiento": "boolean|null",
    "salud": "boolean|null",
    "agua_potable": "boolean|null",
    "saneamiento": "boolean|null",
    "educacion": "boolean|null",
    "vestuario": "boolean|null",
    "otros": "string|null"
  },
  "animales": {
    "tiene_animales": "boolean|null",
    "cantidad_perros": "number|null",
    "cantidad_gatos": "number|null",
    "cantidad_aves": "number|null",
    "otros_animales": "string|null"
  },
  "datos_adicionales": {
    "fuente_origen": "string|null",
    "fecha_registro": "string|null",
    "observaciones_generales": "string|null"
  }
}

Devuelve SOLO el JSON, sin texto adicional.
"""


def normalizar_numero(valor):
    if valor is None:
        return None
    if isinstance(valor, (int, float)):
        return str(int(valor))
    if not isinstance(valor, str):
        return valor
    valor = re.sub(r'[.\s\-()]', '', valor)
    return valor if valor else None


def normalizar_datos(datos):
    for rufe in datos:
        if "jefe_hogar" in rufe and rufe["jefe_hogar"]:
            jefe = rufe["jefe_hogar"]
            if "cedula" in jefe:
                jefe["cedula"] = normalizar_numero(jefe["cedula"])
            if "telefono" in jefe:
                jefe["telefono"] = normalizar_numero(jefe["telefono"])
        if "composicion_familiar" in rufe and rufe["composicion_familiar"]:
            for miembro in rufe["composicion_familiar"]:
                if "cedula" in miembro:
                    miembro["cedula"] = normalizar_numero(miembro["cedula"])
    return datos


def crear_cliente():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("La variable GEMINI_API_KEY no está configurada")
    return genai.Client(api_key=api_key)


def limpiar_json(texto):
    texto = texto.strip()
    if texto.startswith("```json"):
        texto = texto[7:]
    elif texto.startswith("```"):
        texto = texto[3:]
    if texto.endswith("```"):
        texto = texto[:-3]
    texto = texto.strip()
    inicio = texto.find("[")
    if inicio == -1:
        inicio = texto.find("{")
    fin = texto.rfind("]")
    if fin == -1:
        fin = texto.rfind("}")
    if inicio != -1 and fin != -1:
        texto = texto[inicio:fin+1]
    return texto


def cargar_progreso():
    if ARCHIVO_PROGRESO.exists():
        with open(ARCHIVO_PROGRESO, "r") as f:
            return json.load(f)
    return {"procesados": [], "fallidos": []}


def guardar_progreso(progreso):
    ARCHIVO_PROGRESO.parent.mkdir(parents=True, exist_ok=True)
    with open(ARCHIVO_PROGRESO, "w") as f:
        json.dump(progreso, f, indent=2)


def procesar_pdf(pdf_path, client):
    print(f"\n📋 Procesando: {pdf_path.name}")
    
    for intento in range(1, MAX_REINTENTOS + 1):
        try:
            print(f"   Intento {intento}/{MAX_REINTENTOS}...")
            inicio = time.time()
            
            archivo = client.files.upload(file=str(pdf_path))
            
            while archivo.state.name == "PROCESSING":
                time.sleep(2)
                archivo = client.files.get(name=archivo.name)
            
            if archivo.state.name == "FAILED":
                raise RuntimeError("El PDF falló al procesarse")
            
            response = client.models.generate_content(
                model=MODELO_GEMINI,
                contents=[PROMPT_RUFE, archivo]
            )
            
            duracion = time.time() - inicio
            texto_limpio = limpiar_json(response.text)
            datos = json.loads(texto_limpio)
            
            if isinstance(datos, dict):
                datos = [datos]
            
            datos = normalizar_datos(datos)
            
            print(f"   ✅ {len(datos)} RUFE extraídos en {duracion:.1f}s")
            
            try:
                client.files.delete(name=archivo.name)
            except:
                pass
            
            return datos
            
        except json.JSONDecodeError as e:
            print(f"   ⚠️ JSON inválido: {str(e)[:100]}")
            continue
            
        except Exception as e:
            error_msg = str(e)
            
            if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
                wait_time = min(60 * intento, 300)
                print(f"   ⚠️ 429 (cuota). Esperando {wait_time}s...")
                time.sleep(wait_time)
            elif "503" in error_msg or "UNAVAILABLE" in error_msg:
                wait_time = 2 ** intento
                print(f"   ⚠️ 503 (saturado). Esperando {wait_time}s...")
                time.sleep(wait_time)
            else:
                print(f"   ❌ Error: {error_msg[:200]}")
                time.sleep(5)
    
    print(f"   ❌ No se pudo procesar {pdf_path.name}")
    return []


def guardar_resultado(datos, pdf_path):
    CARPETA_OUTPUT.mkdir(parents=True, exist_ok=True)
    output_path = CARPETA_OUTPUT / f"{pdf_path.stem}.json"
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=2, ensure_ascii=False)
    
    print(f"   💾 Guardado en {output_path}")
    return output_path


def main():
    parser = argparse.ArgumentParser(description="ETL de RUFE")
    parser.add_argument("--pdf", help="Ruta del PDF")
    parser.add_argument("--carpeta", help="Carpeta con PDFs")
    parser.add_argument("--todos", action="store_true", help="Procesar todos")
    parser.add_argument("--reanudar", action="store_true", help="Reanudar")
    
    args = parser.parse_args()
    
    if not any([args.pdf, args.carpeta, args.todos, args.reanudar]):
        parser.print_help()
        sys.exit(1)
    
    client = crear_cliente()
    progreso = cargar_progreso()
    
    pdfs = []
    if args.pdf:
        pdfs = [CARPETA_RAIZ / args.pdf]
    elif args.carpeta:
        pdfs = sorted((CARPETA_RAIZ / args.carpeta).glob("*.pdf"))
    elif args.todos or args.reanudar:
        pdfs = sorted(CARPETA_RAIZ.rglob("*.pdf"))
    
    if args.reanudar:
        pdfs = [p for p in pdfs if str(p) not in progreso["procesados"]]
        print(f"📊 Reanudando: {len(pdfs)} PDFs pendientes")
    else:
        print(f"📊 Total: {len(pdfs)} PDFs")
    
    for i, pdf_path in enumerate(pdfs):
        if not pdf_path.exists():
            print(f"⚠️ No existe: {pdf_path}")
            continue
        
        datos = procesar_pdf(pdf_path, client)
        
        if datos:
            guardar_resultado(datos, pdf_path)
            progreso["procesados"].append(str(pdf_path))
        else:
            progreso["fallidos"].append(str(pdf_path))
        
        guardar_progreso(progreso)
        
        if i < len(pdfs) - 1:
            time.sleep(PAUSA_ENTRE_PDFS)
    
    print(f"\n{'='*60}")
    print(f"✅ RESUMEN: {len(progreso['procesados'])} procesados, {len(progreso['fallidos'])} fallidos")


if __name__ == "__main__":
    main()
