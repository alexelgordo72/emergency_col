"""
etl_rufe_local.py
Procesa formularios RUFE usando Ollama LOCAL (sin API de Gemini).

Uso:
    python etl_rufe_local.py --pdf "30-08-2026/689-691-Rufe.pdf"
    python etl_rufe_local.py --carpeta "30-08-2026"
    python etl_rufe_local.py --todos
"""

import os
import sys
import time
import json
import re
import base64
import argparse
import requests
import subprocess
from pathlib import Path


# ============================================================
# CONFIGURACIÓN
# ============================================================

CARPETA_RAIZ = Path.home() / "Desktop" / "SGRD 2026"
CARPETA_OUTPUT = Path.home() / "etl" / "data" / "output"
CARPETA_TEMP = Path("/tmp/rufe_temp")

MODELO_OLLAMA = "qwen3-vl:4b"
OLLAMA_URL = "http://localhost:11434/api/generate"
TIMEOUT_SEGUNDOS = 600
MAX_REINTENTOS = 2
DPI = 200  # Resolución para conversión de PDF a imágenes

PROMPT_RUFE = """
Eres un experto en digitalizar formularios RUFE (Registro Único de Familias en Emergencia) del SGRD Yumbo, Colombia.

La imagen es un formulario oficial manuscrito. Lee CUIDADOSAMENTE cada campo.

INSTRUCCIONES CRÍTICAS:
1. NO inventes datos. Si no puedes leer algo, pon null.
2. Para CÉDULAS y TELÉFONOS: transcribe SIN puntos, SIN espacios, SIN guiones.
3. Lee la COMPOSICIÓN FAMILIAR completa (todos los miembros).
4. Devuelve SOLO un JSON válido.

Estructura:
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
    "zona": "Urbana|Rural|null"
  },
  "composicion_familiar": [
    {
      "nombres": "string|null",
      "apellidos": "string|null",
      "tipo_documento": "string|null",
      "cedula": "string|null",
      "parentesco": "string|null",
      "sexo": "M|F|null",
      "edad": "number|null"
    }
  ],
  "evaluacion_danos": {
    "nivel_riesgo": "Alto|Medio|Bajo|null",
    "prioridad": "ALTA|MEDIA|BAJA|null",
    "habitabilidad": "Habitable|No Habitable|null",
    "descripcion_danos": "string|null",
    "observaciones_evaluador": "string|null"
  },
  "vivienda": {
    "tipo_vivienda": "string|null",
    "numero_plantas": "number|null",
    "material_paredes": "string|null",
    "material_techo": "string|null",
    "estado_general": "string|null"
  },
  "total_personas_hogar": "number|null"
}

Responde SOLO con el JSON, sin texto adicional.
"""


def normalizar_numero(valor):
    """Normaliza un número eliminando puntos, espacios y guiones."""
    if valor is None:
        return None
    if isinstance(valor, (int, float)):
        return str(int(valor))
    if not isinstance(valor, str):
        return valor
    valor = re.sub(r'[.\s\-()]', '', valor)
    return valor if valor else None


def normalizar_datos(datos):
    """Normaliza cédulas y teléfonos de todos los RUFE."""
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


def limpiar_json(texto):
    """Limpia el texto de markdown y extrae el JSON."""
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


def pdf_a_imagenes(pdf_path, output_dir):
    """Convierte un PDF a imágenes PNG."""
    output_dir.mkdir(parents=True, exist_ok=True)
    base_name = output_dir / pdf_path.stem
    
    cmd = ["pdftoppm", "-png", "-r", str(DPI), str(pdf_path), str(base_name)]
    resultado = subprocess.run(cmd, capture_output=True, text=True)
    
    if resultado.returncode != 0:
        raise RuntimeError(f"Error al convertir PDF: {resultado.stderr}")
    
    imagenes = sorted(output_dir.glob(f"{pdf_path.stem}-*.png"))
    return imagenes


def procesar_imagen_con_ollama(img_path, prompt):
    """Procesa una imagen con Ollama (modelo local)."""
    with open(img_path, "rb") as f:
        img_base64 = base64.b64encode(f.read()).decode("utf-8")
    
    data = {
        "model": MODELO_OLLAMA,
        "prompt": prompt,
        "images": [img_base64],
        "stream": False,
        "options": {
            "temperature": 0.1,
            "num_ctx": 8192
        }
    }
    
    response = requests.post(OLLAMA_URL, json=data, timeout=TIMEOUT_SEGUNDOS)
    response.raise_for_status()
    resultado = response.json()
    
    return resultado.get("response", "")


def procesar_pdf(pdf_path):
    """Procesa un PDF completo con Ollama."""
    print(f"\n📋 Procesando: {pdf_path.name}")
    
    for intento in range(1, MAX_REINTENTOS + 1):
        try:
            print(f"   Intento {intento}/{MAX_REINTENTOS}...")
            inicio = time.time()
            
            # Convertir PDF a imágenes
            temp_dir = CARPETA_TEMP / pdf_path.stem
            imagenes = pdf_a_imagenes(pdf_path, temp_dir)
            print(f"   📄 {len(imagenes)} páginas convertidas")
            
            # Procesar cada imagen con Ollama
            datos_totales = []
            for img in imagenes:
                try:
                    respuesta = procesar_imagen_con_ollama(img, PROMPT_RUFE)
                    texto_limpio = limpiar_json(respuesta)
                    datos = json.loads(texto_limpio)
                    
                    if isinstance(datos, dict):
                        datos = [datos]
                    
                    datos_totales.extend(datos)
                    
                except json.JSONDecodeError as e:
                    print(f"   ⚠️ Página {img.name}: JSON inválido")
                    continue
                except Exception as e:
                    print(f"   ⚠️ Página {img.name}: {str(e)[:100]}")
                    continue
            
            # Normalizar datos
            datos_totales = normalizar_datos(datos_totales)
            
            duracion = time.time() - inicio
            print(f"   ✅ {len(datos_totales)} RUFE extraídos en {duracion:.1f}s")
            
            return datos_totales
            
        except Exception as e:
            print(f"   ❌ Error: {str(e)[:200]}")
            time.sleep(5)
    
    print(f"   ❌ No se pudo procesar {pdf_path.name}")
    return []


def guardar_resultado(datos, pdf_path):
    """Guarda el JSON."""
    CARPETA_OUTPUT.mkdir(parents=True, exist_ok=True)
    output_path = CARPETA_OUTPUT / f"{pdf_path.stem}.json"
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=2, ensure_ascii=False)
    
    print(f"   💾 Guardado en {output_path}")


def main():
    parser = argparse.ArgumentParser(description="ETL de RUFE con Ollama LOCAL")
    parser.add_argument("--pdf", help="Ruta del PDF")
    parser.add_argument("--carpeta", help="Carpeta con PDFs")
    parser.add_argument("--todos", action="store_true", help="Procesar todos")
    
    args = parser.parse_args()
    
    if not any([args.pdf, args.carpeta, args.todos]):
        parser.print_help()
        sys.exit(1)
    
    # Verificar que Ollama está corriendo
    try:
        r = requests.get("http://localhost:11434/api/tags", timeout=5)
        r.raise_for_status()
        print("✅ Ollama está corriendo")
    except:
        print("❌ Ollama NO está corriendo. Ejecuta: ollama serve &")
        sys.exit(1)
    
    # Determinar PDFs
    pdfs = []
    if args.pdf:
        pdfs = [CARPETA_RAIZ / args.pdf]
    elif args.carpeta:
        pdfs = sorted((CARPETA_RAIZ / args.carpeta).glob("*.pdf"))
    elif args.todos:
        pdfs = sorted(CARPETA_RAIZ.rglob("*.pdf"))
    
    print(f"📊 Total PDFs: {len(pdfs)}")
    
    for pdf_path in pdfs:
        if not pdf_path.exists():
            print(f"⚠️ No existe: {pdf_path}")
            continue
        
        datos = procesar_pdf(pdf_path)
        if datos:
            guardar_resultado(datos, pdf_path)


if __name__ == "__main__":
    main()
