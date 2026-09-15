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

CASOS_SIN_CONTACTO = ["054", "055", "076", "081", "105", "106", "107", "108", "131", "031", "032", "033"]
CASOS_TELEFONO_ERRADO = [
    "022", "029", "039", "040", "041", "042", "044", "045",
    "047", "051", "053", "060", "061", "069", "073", "074",
    "075", "083", "086", "087", "089", "095", "101", "109",
    "110", "112", "114", "116", "120", "122", "124", "125",
    "132", "135", "136", "145", "146", "147"
]
CASOS_NO_REQUIERE_AYUDA = ["077"] # Mantiene su prioridad original, se actualiza solo observación
CASOS_REPETIDOS = ["001", "008"]

def main():
    print("Iniciando actualización refinada basada en los hallazgos de los 147 casos...")
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        actualizados = 0
        
        def actualizar_por_numero(lista_casos, nuevo_estado, observacion_tag, conservar_estado_original=False):
            nonlocal actualizados
            for num_caso in lista_casos:
                cur.execute("""
                    SELECT r.id, r.estado_actual, r.datos_extra 
                    FROM public.reportes_comunitarios r
                    LEFT JOIN public.rufe_formularios f ON f.reporte_id = r.id
                    WHERE f.numero_formulario ILIKE %s OR r.titulo ILIKE %s
                """, (f"%{num_caso}%", f"%RUFE%{num_caso}%"))
                
                rows = cur.fetchall()
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
                    print(f"[ACTUALIZADO] Caso {num_caso} -> Estado: {target_state} | Observación: {observacion_tag} (Reporte ID: {rep_id})")

        print("\nActualizando casos SIN CONTACTO...")
        actualizar_por_numero(CASOS_SIN_CONCIERTO if 'CASOS_SIN_CONCIERTO' in locals() else CASOS_SIN_CONTACTO, "VERIFICACION_SIN_CONTACTO", "Sin contacto telefónico (Secretaría de Infraestructura)")

        print("\nActualizando casos TELEFONO ERRADO...")
        actualizar_por_numero(CASOS_TELEFONO_ERRADO, "VERIFICACION_TELEFONO_ERRADO", "Teléfono errado o no permite contacto (Secretaría de Infraestructura)")

        print("\nActualizando casos NO REQUIERE AYUDA (conservando prioridad original)...")
        actualizar_por_numero(CASOS_NO_REQUIERE_AYUDA, None, "La persona manifestó directamente que no requiere ayuda a pesar de la pérdida total reportada por incendio.", conservar_estado_original=True)

        print("\nActualizando casos REPETIDOS...")
        actualizar_por_numero(CASOS_REPETIDOS, "VERIFICACION_REPETIDO", "Registro repetido pendiente de conciliación entre registros similares en Alto Dapa")

        conn.commit()
        print("\n" + "="*45)
        print(f"Proceso completado con éxito. Total de registros actualizados: {actualizados}")
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
