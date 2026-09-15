import psycopg2
from psycopg2.extras import RealDictCursor
import json

DB_CONFIG = {
    "dbname": "comunidad_db",
    "user": "admin_comunidad",
    "password": "TuPasswordSegura2026!",
    "host": "10.147.17.24",
    "port": "5432"
}

CASOS_REPETIDOS = ["001", "008"]
CASOS_NO_REQUIERE_AYUDA = ["077"]
CASOS_SIN_CONTACTO = ["054", "055", "076", "081", "105", "106", "107", "108", "131", "031", "032", "033"]
CASOS_TELEFONO_ERRADO = [
    "022", "029", "039", "040", "041", "042", "044", "045",
    "047", "051", "053", "060", "061", "069", "073", "074",
    "075", "083", "086", "087", "089", "095", "101", "109",
    "110", "112", "114", "116", "120", "122", "124", "125",
    "132", "135", "136", "145", "146", "147"
]

def buscar_registros_por_numero(cur, num_caso):
    num_normalizado = str(int(num_caso)) if num_caso.isdigit() else num_caso
    regex_titulo = rf"RUFE\s*#?\s*{num_normalizado}\b"
    
    cur.execute("""
        SELECT r.id, r.titulo, r.estado_actual, r.datos_extra
        FROM public.reportes_comunitarios r
        WHERE 
            r.datos_extra->>'rufe' = %s
            OR r.datos_extra->>'rufe' = %s
            OR r.datos_extra->>'rufe' ~ %s
            OR r.titulo ~* %s
    """, (
        num_caso,
        num_normalizado,
        rf"^{num_normalizado}[A-Z]?$",
        regex_titulo
    ))
    
    return cur.fetchall()

def main():
    print("="*60)
    print("ACTUALIZACION DE HALLAZGOS - 147 CASOS (V2 CORREGIDA)")
    print("="*60)
    
    conn = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        actualizados = 0
        no_encontrados = []
        
        def actualizar_por_numero(lista_casos, nuevo_estado, observacion_tag, conservar_estado_original=False):
            nonlocal actualizados, no_encontrados
            
            for num_caso in lista_casos:
                rows = buscar_registros_por_numero(cur, num_caso)
                
                if not rows:
                    no_encontrados.append(num_caso)
                    print(f"  [NO ENCONTRADO] Caso {num_caso}")
                    continue
                
                for row in rows:
                    rep_id = row["id"]
                    estado_actual = row["estado_actual"]
                    datos = row["datos_extra"] or {}
                    datos["hallazgo_infraestructura"] = observacion_tag
                    
                    target_state = estado_actual if conservar_estado_original else nuevo_estado
                    
                    cur.execute("""
                        UPDATE public.reportes_comunitarios 
                        SET estado_actual = %s, datos_extra = %s 
                        WHERE id = %s
                    """, (target_state, json.dumps(datos), rep_id))
                    actualizados += 1
                    print(f"  [OK] Caso {num_caso} -> {target_state} | {row['titulo'][:60]}")
        
        print("\n--- SIN CONTACTO ---")
        actualizar_por_numero(CASOS_SIN_CONTACTO, "VERIFICACION_SIN_CONTACTO", 
                              "Sin contacto telefonico (Secretaria de Infraestructura)")
        
        print("\n--- TELEFONO ERRADO ---")
        actualizar_por_numero(CASOS_TELEFONO_ERRADO, "VERIFICACION_TELEFONO_ERRADO", 
                              "Telefono errado o no permite contacto (Secretaria de Infraestructura)")
        
        print("\n--- NO REQUIERE AYUDA ---")
        actualizar_por_numero(CASOS_NO_REQUIERE_AYUDA, None, 
                              "La persona manifesto directamente que no requiere ayuda.",
                              conservar_estado_original=True)
        
        print("\n--- REPETIDOS ---")
        actualizar_por_numero(CASOS_REPETIDOS, "VERIFICACION_REPETIDO", 
                              "Registro repetido pendiente de conciliacion.")
        
        conn.commit()
        
        print("\n" + "="*60)
        print(f"Proceso completado. Total actualizados: {actualizados}")
        if no_encontrados:
            print(f"Casos NO ENCONTRADOS: {len(no_encontrados)}")
            print(f"  {', '.join(no_encontrados)}")
        print("="*60)
        
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"\n[ERROR]: {e}")
    finally:
        if conn:
            cur.close()
            conn.close()

if __name__ == "__main__":
    main()
