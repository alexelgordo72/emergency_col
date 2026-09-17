import psycopg2

DB_CONFIG = {
    "dbname": "comunidad_db",
    "user": "admin_comunidad",
    "password": "TuPasswordSegura2026!",
    "host": "10.147.17.24",
    "port": "5432"
}

DATOS_A_ACTUALIZAR = [
    {"doc": "29756562", "fecha": "17/09/1968", "etnia": "Ninguna"},
    {"doc": "1116379027", "fecha": "22/05/2015", "etnia": "Ninguna"},
    {"doc": "6341605", "fecha": "20/09/1964", "etnia": "Ninguna"},
    {"doc": "14955885", "fecha": "14/11/1948", "etnia": "Ninguna"},
    {"doc": "31259794", "fecha": "14/08/1951", "etnia": "Ninguna"},
    {"doc": "16445318", "fecha": "27/05/1951", "etnia": "Ninguna"},
    {"doc": "31253456", "fecha": "21/04/1953", "etnia": "Ninguna"},
    {"doc": "1118209126", "fecha": "12/08/1988", "etnia": "Ninguna"},
    {"doc": "16446944", "fecha": "19/10/1955", "etnia": "Ninguna"},
    {"doc": "31190587", "fecha": "19/02/1956", "etnia": "Ninguna"},
    {"doc": "16738827", "fecha": "19/01/1967", "etnia": "Ninguna"},
    {"doc": "31929413", "fecha": "07/08/1954", "etnia": "Ninguna"},
    {"doc": "6550037", "fecha": "12/11/1955", "etnia": "Ninguna"},
    {"doc": "16940570", "fecha": "02/01/1982", "etnia": "Ninguna"},
    {"doc": "1144039988", "fecha": "10/10/1940", "etnia": "Ninguna"},
    {"doc": "1116378390", "fecha": "27/07/2014", "etnia": "Ninguna"},
    {"doc": "1118296476", "fecha": "24/07/1991", "etnia": "Indígena"},
    {"doc": "29976084", "fecha": "31/01/1946", "etnia": "Indígena"},
    {"doc": "1123283028", "fecha": "29/02/2024", "etnia": "Ninguna"},
    {"doc": "38667447", "fecha": "16/03/1974", "etnia": "Ninguna"},
    {"doc": "1085928432", "fecha": "08/12/1991", "etnia": "Ninguna"},
    {"doc": "38996445", "fecha": "14/09/1947", "etnia": "Ninguna"},
    {"doc": "16461974", "fecha": "20/08/1981", "etnia": "Ninguna"},
    {"doc": "16621428", "fecha": "07/03/1959", "etnia": "Ninguna"},
    {"doc": "31871944", "fecha": "14/02/1959", "etnia": "Ninguna"},
    {"doc": "10282998", "fecha": "15/08/1955", "etnia": "Ninguna"},
    {"doc": "29581441", "fecha": "18/09/1963", "etnia": "Ninguna"},
]

def main():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        conn.autocommit = True
        cur = conn.cursor()
        
        print("1. Verificando estructura de las tablas...")
        cur.execute("ALTER TABLE public.rufe_personas ADD COLUMN IF NOT EXISTS etnia VARCHAR(50);")
        
        print("2. Iniciando actualización masiva de registros...")
        filas_actualizadas = 0
        
        for persona in DATOS_A_ACTUALIZAR:
            doc = persona["doc"]
            fecha = persona["fecha"]
            etnia = persona["etnia"]
            
            cur.execute("""
                UPDATE public.rufe_personas 
                SET fecha_nacimiento = %s, etnia = %s 
                WHERE REPLACE(REPLACE(documento_identidad, '.', ''), ' ', '') = %s;
            """, (fecha, etnia, doc))
            
            filas_actualizadas += cur.rowcount

        print(f"\n==================================================")
        print(f"¡ACTUALIZACIÓN EXITOSA!")
        print(f"Se corrigieron {filas_actualizadas} registros en total.")
        print(f"==================================================")
        
    except Exception as e:
        print(f"Error en la base de datos: {e}")
    finally:
        if 'conn' in locals():
            cur.close()
            conn.close()

if __name__ == "__main__":
    main()
