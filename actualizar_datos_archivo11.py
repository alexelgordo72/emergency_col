import psycopg2

DB_CONFIG = {
    "dbname": "comunidad_db",
    "user": "admin_comunidad",
    "password": "TuPasswordSegura2026!",
    "host": "10.147.17.24",
    "port": "5432"
}

DATOS_ETNIA_VICTIMAS = [
    # --- VÍCTIMAS DEL CONFLICTO (Desplazados) ---
    {"doc": "29331445", "etnia": "Ninguna", "victima": True},
    {"doc": "9401598", "etnia": "Ninguna", "victima": True},
    
    # --- POBLACIÓN RAIZAL (Opción 3) ---
    {"doc": "31469212", "etnia": "Raizal", "victima": False},
    {"doc": "1482091038", "etnia": "Raizal", "victima": False},
    
    # --- POBLACIÓN AFROCOLOMBIANA (Opción 5) ---
    {"doc": "14845041", "etnia": "Afrocolombiano", "victima": False},
    {"doc": "31479290", "etnia": "Afrocolombiano", "victima": False},
    {"doc": "66933928", "etnia": "Afrocolombiano", "victima": False},
    {"doc": "1026016238", "etnia": "Afrocolombiano", "victima": False},
    {"doc": "1109186519", "etnia": "Afrocolombiano", "victima": False},
    {"doc": "94070292", "etnia": "Afrocolombiano", "victima": False},
    {"doc": "14845008", "etnia": "Afrocolombiano", "victima": False},
    {"doc": "6531166", "etnia": "Afrocolombiano", "victima": False},
    {"doc": "38840059", "etnia": "Afrocolombiano", "victima": False},
    {"doc": "6530899", "etnia": "Afrocolombiano", "victima": False},
    {"doc": "29939882", "etnia": "Afrocolombiano", "victima": False},
    {"doc": "1115301000", "etnia": "Afrocolombiano", "victima": False},
    {"doc": "14845044", "etnia": "Afrocolombiano", "victima": False},
    {"doc": "1118309699", "etnia": "Afrocolombiano", "victima": False},
    {"doc": "1493238049", "etnia": "Afrocolombiano", "victima": False},
    {"doc": "1116382105", "etnia": "Afrocolombiano", "victima": False},
    {"doc": "6228035", "etnia": "Afrocolombiano", "victima": False},
    {"doc": "1118313958", "etnia": "Afrocolombiano", "victima": False},
    {"doc": "38840081", "etnia": "Afrocolombiano", "victima": False},
    {"doc": "1130667185", "etnia": "Afrocolombiano", "victima": False},
    {"doc": "80189361", "etnia": "Afrocolombiano", "victima": False},
    {"doc": "1150946700", "etnia": "Afrocolombiano", "victima": False},
    {"doc": "1109198426", "etnia": "Afrocolombiano", "victima": False},
    {"doc": "1143884219", "etnia": "Afrocolombiano", "victima": False}
]

def main():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        conn.autocommit = True
        cur = conn.cursor()
        
        print("1. Verificando estructura (Agregando columna de Víctimas si no existe)...")
        cur.execute("ALTER TABLE public.rufe_personas ADD COLUMN IF NOT EXISTS es_victima BOOLEAN DEFAULT FALSE;")
        
        print("2. Iniciando actualización de registros clave...")
        filas_actualizadas = 0
        
        for persona in DATOS_ETNIA_VICTIMAS:
            doc = persona["doc"]
            etnia = persona["etnia"]
            victima = persona["victima"]
            
            cur.execute("""
                UPDATE public.rufe_personas 
                SET etnia = %s, es_victima = %s 
                WHERE REPLACE(REPLACE(documento_identidad, '.', ''), ' ', '') = %s;
            """, (etnia, victima, doc))
            
            filas_actualizadas += cur.rowcount

        print(f"\n==================================================")
        print(f"¡ACTUALIZACIÓN EXITOSA!")
        print(f"Se enriquecieron {filas_actualizadas} registros con datos de Etnia y Víctimas.")
        print(f"==================================================")
        
    except Exception as e:
        print(f"Error en la base de datos: {e}")
    finally:
        if 'conn' in locals():
            cur.close()
            conn.close()

if __name__ == "__main__":
    main()
