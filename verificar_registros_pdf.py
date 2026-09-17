import psycopg2

DB_CONFIG = {
    "dbname": "comunidad_db",
    "user": "admin_comunidad",
    "password": "TuPasswordSegura2026!",
    "host": "10.147.17.24",
    "port": "5432"
}

DOCUMENTOS = [
    "29756562", "1116379027", "6341605", "14955885", "31259794",
    "16445318", "31253456", "1118209126", "16446944", "31190587",
    "16738827", "31929413", "6550037", "16940570", "1144039988",
    "1116378390", "1118296476", "29976084", "1123283028", "38667447",
    "1085928432", "38996445", "16461974", "16621428", "31871944",
    "10282998", "29581441"
]

def main():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        print("Consultando registros en la base de datos...\n")
        
        # Consultar en la tabla principal
        cur.execute("""
            SELECT nombre_completo, documento_identidad, fecha_nacimiento
            FROM public.rufe_personas
            WHERE REPLACE(REPLACE(documento_identidad, '.', ''), ' ', '') IN %s
        """, (tuple(DOCUMENTOS),))
        resultados_principal = cur.fetchall()

        # Consultar en la tabla de Sultana
        cur.execute("""
            SELECT CONCAT(nombre, ' ', apellido) AS nombre_completo, numero_documento, fecha_nacimiento
            FROM public.rufe_personas_bs
            WHERE REPLACE(REPLACE(numero_documento, '.', ''), ' ', '') IN %s
        """, (tuple(DOCUMENTOS),))
        resultados_bs = cur.fetchall()

        # Imprimir resultados
        print(f"{'NOMBRE EN BD':<35} | {'DOCUMENTO BD':<15} | {'FECHA ACTUAL':<12} | {'TABLA'}")
        print("-" * 85)

        total_encontrados = 0
        for r in resultados_principal:
            print(f"{str(r[0])[:34]:<35} | {str(r[1]):<15} | {str(r[2]):<12} | rufe_personas")
            total_encontrados += 1

        for r in resultados_bs:
            nombre_limpio = str(r[0]).strip()
            print(f"{nombre_limpio[:34]:<35} | {str(r[1]):<15} | {str(r[2]):<12} | rufe_personas_bs")
            total_encontrados += 1

        print("-" * 85)
        print(f"Total de documentos a buscar: {len(DOCUMENTOS)}")
        print(f"Total de registros encontrados: {total_encontrados}\n")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'conn' in locals():
            cur.close()
            conn.close()

if __name__ == "__main__":
    main()
