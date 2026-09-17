import psycopg2
import uuid
import re

DB_CONFIG = {
    "dbname": "comunidad_db",
    "user": "admin_comunidad",
    "password": "TuPasswordSegura2026!",
    "host": "10.147.17.24",
    "port": "5432"
}

# Lote de entregas AHE extraídas de los formatos oficiales de agosto de 2026
LOTE_AHE = [
    # --- SANTA INES ---
    {"nombre": "Javier Bernal", "doc": "16450369", "sector": "Santa Ines", "kit_alim": True, "kit_aseo": True, "colchonetas": True, "arriendo": False},
    {"nombre": "Alexander Burgos", "doc": "16900570", "sector": "Santa Ines", "kit_alim": True, "kit_aseo": True, "colchonetas": True, "arriendo": False},
    {"nombre": "Javier Hoyos", "doc": "16445318", "sector": "Santa Ines", "kit_alim": True, "kit_aseo": True, "colchonetas": True, "arriendo": False},
    {"nombre": "Aurora Galindo Daza", "doc": "31929413", "sector": "Santa Ines", "kit_alim": True, "kit_aseo": True, "colchonetas": True, "arriendo": False},
    
    # --- PANORAMA ---
    {"nombre": "Luis Horacio Gil Valencia", "doc": "14970066", "sector": "Panorama", "kit_alim": True, "kit_aseo": True, "colchonetas": True, "arriendo": True},
    {"nombre": "Yorlady Villegas Gomez", "doc": "1118288625", "sector": "Panorama", "kit_alim": True, "kit_aseo": True, "colchonetas": True, "arriendo": False},
    
    # --- OTROS SECTORES ---
    {"nombre": "Jesica Julian Fuentes", "doc": "68296084", "sector": "Guacanda / Gaitan", "kit_alim": True, "kit_aseo": True, "colchonetas": True, "arriendo": False},
    {"nombre": "Rosalbina Mejoy", "doc": "31467429", "sector": "Guacanda / Gaitan", "kit_alim": True, "kit_aseo": True, "colchonetas": True, "arriendo": False},
    {"nombre": "Margarita Viafara", "doc": "31915601", "sector": "Guacanda / Gaitan", "kit_alim": True, "kit_aseo": True, "colchonetas": True, "arriendo": False}
]

def main():
    print("Iniciando registro de Asistencia Humanitaria (AHE)...")
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        conn.autocommit = True
        cur = conn.cursor()
        
        # Asegurar columnas para control de AHE en la base de datos
        cur.execute("ALTER TABLE public.rufe_personas ADD COLUMN IF NOT EXISTS ahe_recibida BOOLEAN DEFAULT TRUE;")
        cur.execute("ALTER TABLE public.rufe_personas ADD COLUMN IF NOT EXISTS detalle_ayuda TEXT;")
        
        actualizados = 0
        insertados = 0
        
        for ahe in LOTE_AHE:
            doc_limpio = ahe["doc"].replace(".", "").strip()
            
            # Verificar si la persona ya existe en la base de datos
            cur.execute("SELECT id, rufe_formulario_id FROM public.rufe_personas WHERE REPLACE(documento_identidad, '.', '') = %s", (doc_limpio,))
            resultado = cur.fetchone()
            
            detalle = f"Sector: {ahe['sector']} | Kit Alim: {ahe['kit_alim']} | Kit Aseo: {ahe['kit_aseo']} | Colchonetas: {ahe['colchonetas']} | Subsidio Arriendo: {ahe['arriendo']}"
            
            if resultado:
                persona_id = resultado[0]
                cur.execute("""
                    UPDATE public.rufe_personas 
                    SET ahe_recibida = true, detalle_ayuda = %s
                    WHERE id = %s;
                """, (detalle, persona_id))
                actualizados += 1
            else:
                # Si no existe la persona, la creamos vinculada a un reporte general
                cur.execute("SELECT id FROM public.reportes_comunitarios LIMIT 1;")
                res_rep = cur.fetchone()
                reporte_id = res_rep[0] if res_rep else str(uuid.uuid4())
                
                cur.execute("""
                    INSERT INTO public.rufe_formularios (reporte_id, corregimiento, prioridad, observaciones_evaluador)
                    VALUES (%s, %s, 'MEDIA', 'Registro desde formato de entrega AHE') RETURNING id;
                """, (reporte_id, ahe["sector"]))
                form_id = cur.fetchone()[0]
                
                cur.execute("""
                    INSERT INTO public.rufe_personas 
                    (rufe_formulario_id, nombre_completo, documento_identidad, es_jefe_hogar, ahe_recibida, detalle_ayuda)
                    VALUES (%s, %s, %s, true, true, %s)
                """, (form_id, ahe["nombre"], ahe["doc"], detalle))
                insertados += 1

        print(f"\n==================================================")
        print(f"REGISTRO AHE COMPLETADO.")
        print(f"Personas con asistencia actualizada: {actualizados}")
        print(f"Nuevos registros creados con asistencia: {insertados}")
        print(f"==================================================")
        
    except Exception as e:
        print(f"Error en BD: {e}")
    finally:
        if 'conn' in locals(): cur.close(); conn.close()

if __name__ == "__main__":
    main()
