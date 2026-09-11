"""
procesar_todo.py
Procesa TODAS las carpetas de PDFs de RUFE.

Uso:
    python procesar_todo.py
"""

import sys
import time
from pathlib import Path
from etl_rufe import crear_cliente, procesar_pdf, guardar_resultado

CARPETA_RAIZ = Path.home() / "Desktop" / "SGRD 2026"

# Carpetas a procesar (en orden)
CARPETAS = [
    "15-08-2026",
    "18-08-2026",
    "19-08-2026/Rufe",
    "19-08-2026",
    "21-08-2026",
    "23-08-2026",
    "26-08-2026",  # Ya procesada parcialmente
    "27-08-2026",
    "29-08-2026",
    "30-08-2026",  # Ya procesada
    "31-08-2026",
    "02-09-2026",
    "05-09-2026",
    "07-09-2026/RUFE",
]


def main():
    client = crear_cliente()
    
    total_pdfs = 0
    total_rufe = 0
    
    for carpeta_nombre in CARPETAS:
        carpeta = CARPETA_RAIZ / carpeta_nombre
        if not carpeta.exists():
            print(f"⚠️ No existe: {carpeta}")
            continue
        
        pdfs = sorted(carpeta.glob("*.pdf"))
        if not pdfs:
            print(f"⚠️ Sin PDFs en: {carpeta}")
            continue
        
        print(f"\n{'='*60}")
        print(f"📁 Procesando carpeta: {carpeta_nombre}")
        print(f"📄 PDFs encontrados: {len(pdfs)}")
        print(f"{'='*60}")
        
        for pdf in pdfs:
            datos = procesar_pdf(pdf, client)
            if datos:
                guardar_resultado(datos, pdf)
                total_rufe += len(datos)
            total_pdfs += 1
        
        print(f"\n✅ Carpeta {carpeta_nombre} completada")
    
    print(f"\n{'='*60}")
    print(f"✅ RESUMEN FINAL")
    print(f"{'='*60}")
    print(f"Total PDFs procesados: {total_pdfs}")
    print(f"Total RUFE extraídos: {total_rufe}")
    print(f"Resultados en: {Path.home() / 'etl' / 'data' / 'output'}")


if __name__ == "__main__":
    main()
