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

# Listas exactas de casos reportados por la Secretaría de Infraestructura
CASOS_SIN_CONTACTO = ["054", "055", "076", "081", "105", "106", "107", "108", "131", "031", "032", "033"]
CASOS_TELEFONO_ERRADO = [
    "022", "029", "039", "040", "041", "042", "044", "045",
    "047", "051", "053", "060", "061", "069", "073", "074",
    "075", "083", "086", "087", "089", "095", "101", "109",
    "110", "112", "114", "116", "120", "122", "124", "125",
    "132", "135", "136", "145", "146", "147"
]
CASOS_NO_REQUIERE_AYUDA = ["077"]
CASOS_REPETIDOS = ["001", "008"]

def main():
    print("Iniciando limpieza y corrección estricta de los 147 casos...")
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        # 1. Limpiar todos los hallazgos masivos erróneos y restaurar estado PENDIENTE o el anterior si aplica
        cur.execute("""
            UPDATE public.reportes_comunitarios 
            SET estado_actual = 'PENDIENTE', 
                datos_extra = datos_extra - 'hallazgo_infraestructura'
            WHERE datos_extra ? 'hallazgo_infraestructura';
        """)
        print(f"Registros masivos limpiados: {cur.rowcount}")
        
        # Función para actualizar usando coincidencia exacta de número de formulario RUFE o sufijo exacto del caso
        def actualizar_exacto(lista_casos, nuevo_estado, observacion_tag, conservar_estado=False):
            actualizados = 0
            for num_caso in lista_casos:
                # Normalizar para buscar sin ceros a la izquierda o con formato exacto (ej. RUFE 54, RUFE 054, etc.)
                num_limpio = str(int(num_caso))
                cur.execute("""
                    SELECT r.id, r.estado_actual, r.datos_extra 
                    FROM public.reportes_comunitarios r
                    LEFT JOIN public.rufe_formularios f ON f.reporte_id = r.id
                    WHERE f.numero_formulario = %s 
                       OR f.numero_formulario = %s
                       OR r.titulo ~* %s
                """, (num_caso, num_limpio, f"(RUFE|Caso)\\D*{num_caso}\\b"))
                
                rows = cur.fetchall()
                for row in rows:
                    rep_id = row["id"]
                    estado_actual = row["estado_actual"]
                    datos = row["datos_extra"] or {}
                    datos["hallazgo_infraestructura"] = observacion_tag
                    
                    target_state = estado_actual if conservar_estado else nuevo_estado
                    
                    cur.execute("""
                        UPDATE public.reportes_comunitarios 
                        SET estado_actual = %s, datos_extra = %s 
                        WHERE id = %s
                    """, (target_state, json.dumps(datos), rep_id))
                    actualizados += 1
                    print(f"[ESTRICTO] Caso {num_caso} -> Estado: {target_state} (ID: {rep_id})")
            return actualizados

        c1 = actualizar_exacto(CASOS_SIN_CONTACTO, "VERIFICACION_SIN_CONTACTO", "Sin contacto telefónico (Secretaría de Infraestructura)")
        c2 = actualizar_exacto(CASOS_TELEFONO_ERRADO, "VERIFICACION_TELEFONO_ERRADO", "Teléfono errado o no permite contacto (Secretaría de Infraestructura)")
        c3 = actualizar_exacto(CASOS_NO_REQUIERE_AYUDA, None, "La persona manifestó directamente que no requiere ayuda a pesar de la pérdida total reportada por incendio.", conservar_estado=True)
        c4 = actualizar_exacto(CASOS_REPETIDOS, "VERIFICACION_REPETIDO", "Registro repetido pendiente de conciliación entre registros similares en Alto Dapa")

        conn.commit()
        print("\n" + "="*45)
        print(f"Corrección estricta finalizada con éxito.")
        print(f"Total casos precisos actualizados: {c1 + c2 + c3 + c4}")
        print("="*45)

    except Exception as e:
        if 'conn' in locals():
            conn.rollback()
        print(f"\n[ERROR]: {e}")
    finally:
        if 'conn' in locals():
            cur.close()
            conn.close()

if __name__ == "__main__":
    main()
