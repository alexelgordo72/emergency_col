import os
import re
import psycopg2
import pandas as pd
import fitz  # PyMuPDF

DB_CONFIG = {
    "dbname": "comunidad_db",
    "user": "admin_comunidad",
    "password": "TuPasswordSegura2026!",
    "host": "10.147.17.24",
    "port": "5432"
}

RUTA_CARPETA = os.path.expanduser("~/Desktop/SGRD 2026")

def obtener_rufes_bd():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("""
            SELECT numero_formulario FROM public.rufe_formularios
            UNION
            SELECT numero_formulario FROM public.rufe_formularios_bs
        """)
        rufes_bd = set(str(row[0]).strip() for row in cur.fetchall() if row[0])
        conn.close()
        return rufes_bd
    except Exception as e:
        print(f"Error conectando a la BD: {e}")
        return set()

def analizar_pdf(ruta_pdf):
    rufes_encontrados = set()
    nombre_archivo = os.path.basename(ruta_pdf)
    
    # 1. Buscar en el nombre del archivo (ej: 1612-1613-Rufe.pdf)
    rango_match = re.search(r'(\d{4})-(\d{4})', nombre_archivo)
    if rango_match:
        inicio, fin = int(rango_match.group(1)), int(rango_match.group(2))
        for i in range(inicio, fin + 1):
            rufes_encontrados.add(str(i))
    else:
        solo_match = re.search(r'(\d{4})', nombre_archivo)
        if solo_match:
            rufes_encontrados.add(solo_match.group(1))

    # 2. Leer el interior para pescar RUFEs ocultos (ej: doc017...)
    try:
        doc = fitz.open(ruta_pdf)
        for pagina in doc:
            texto = pagina.get_text()
            numeros = re.findall(r'\b\d{4}\b', texto)
            for n in numeros:
                # Ignorar años comunes que se confunden con formularios
                if n not in ['2024', '2025', '2026', '1900', '1703']:
                    rufes_encontrados.add(n)
        doc.close()
    except Exception:
        pass

    return list(rufes_encontrados)

def main():
    print(f"Conectando a la BD en {DB_CONFIG['host']}...")
    rufes_en_bd = obtener_rufes_bd()
    print(f"-> Total de RUFEs ya registrados: {len(rufes_en_bd)}")

    print(f"\nEscaneando carpetas y PDFs en: {RUTA_CARPETA}")
    if not os.path.exists(RUTA_CARPETA):
        print("¡Error! No se encontró la carpeta. Verifica que esté en el Escritorio con el nombre 'SGRD 2026'.")
        return

    resultados = []
    archivos_procesados = 0

    for root, dirs, files in os.walk(RUTA_CARPETA):
        for file in files:
            if file.lower().endswith(".pdf"):
                archivos_procesados += 1
                ruta_completa = os.path.join(root, file)
                carpeta_origen = os.path.basename(root)

                posibles_rufes = analizar_pdf(ruta_completa)

                for rufe in posibles_rufes:
                    estado = "OK - En Base de Datos" if rufe in rufes_en_bd else "FALTA POR SUBIR"
                    resultados.append({
                        "Carpeta": carpeta_origen,
                        "Archivo PDF": file,
                        "Numero RUFE": rufe,
                        "Estado": estado
                    })

    print(f"-> Se analizaron {archivos_procesados} archivos PDF.")

    if resultados:
        df = pd.DataFrame(resultados)
        df = df[df["Numero RUFE"].str.match(r'^\d{4}$')]
        df = df.sort_values(by=["Estado", "Numero RUFE"])

        ruta_salida = os.path.expanduser("~/Desktop/Auditoria_RUFES.csv")
        df.to_csv(ruta_salida, index=False, encoding="utf-8")
        
        faltantes = df[df["Estado"] == "FALTA POR SUBIR"]
        print(f"\n==================================================")
        print(f"¡AUDITORÍA TERMINADA!")
        print(f"Faltan {len(faltantes)} formularios por subir a la BD.")
        print(f"El reporte detallado se guardó en tu escritorio como 'Auditoria_RUFES.csv'.")
        print(f"==================================================")
    else:
        print("No se encontraron números válidos para auditar.")

if __name__ == "__main__":
    main()
