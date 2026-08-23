import psycopg2
from psycopg2.extras import RealDictCursor

DB_CONFIG = {
    "dbname": "comunidad_db",
    "user": "admin_comunidad",
    "password": "TuPasswordSegura2026!",
    "host": "10.147.17.2",
    "port": 5432
}

def sincronizar_staging():
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    # 1. Obtenemos los registros pendientes de procesar desde rufe_temporal
    cursor.execute("""
        SELECT id, nombre_archivo_origen, cedula_reportada, nombre_reportado, 
               direccion_inmueble, barrio_sector, descripcion_afectaciones, datos_extra_json
        FROM rufe_temporal
        WHERE procesado = FALSE;
    """)
    
    pendientes = cursor.fetchall()
    print(f"--- Encontrados {len(pendientes)} registros en staging para sincronizar ---")

    for item in pendientes:
        staging_id = item['id']
        cedula = item['cedula_reportada']
        direccion = item['direccion_inmueble']
        archivo = item['nombre_archivo_origen']
        danos = item['descripcion_afectaciones']

        print(f"\nProcesando Staging ID {staging_id} | Cédula: {cedula} | Dirección: {direccion}")

        try:
            # 2. CRUCE COMPUESTO: Buscamos por Cédula Y coincidencia parcial en la dirección o barrio
            # Esto garantiza que si tiene 2 casas, el RUFE de la Calle A actualice solo la Calle A.
            cursor.execute("""
                SELECT id as reporte_id, descripcion_detallada, datos_extra 
                FROM reportes_comunitarios 
                WHERE (datos_extra->>'cedula' = %s OR descripcion_detallada LIKE %s)
                  AND (descripcion_detallada ILIKE %s OR datos_extra->>'direccion' ILIKE %s);
            """, (cedula, f"%{cedula}%", f"%{direccion}%", f"%{direccion}%"))
            
            reporte_coincidente = cursor.fetchone()

            if reporte_coincidente:
                reporte_id = reporte_coincidente['reporte_id']
                
                # Actualización específica para este predio sin afectar los otros inmuebles de la misma cédula
                info_predio = f" | [RUFE Verificado - Archivo {archivo}]: Dirección: {direccion} | {danos}"
                
                cursor.execute("""
                    UPDATE reportes_comunitarios 
                    SET descripcion_detallada = descripcion_detallada || %s,
                        procesado_rufe = TRUE
                    WHERE id = %s;
                """, (info_predio, reporte_id))

                print(f"  [ÉXITO] Match compuesto encontrado. Reporte ID {reporte_id} actualizado correctamente.")
            else:
                print(f"  [AVISO] La cédula {cedula} existe, pero no se encontró un predio con dirección similar ('{direccion}'). Queda pendiente en staging para revisión manual.")

            # 3. Marcar el registro de staging como procesado
            cursor.execute("UPDATE rufe_temporal SET procesado = TRUE WHERE id = %s;", (staging_id,))
            conn.commit()

        except Exception as e:
            conn.rollback()
            print(f"  [ERROR] Falló la sincronización del staging ID {staging_id}: {e}")

    cursor.close()
    conn.close()
    print("\n¡Sincronización de staging a producción finalizada!")

if __name__ == "__main__":
    sincronizar_staging()
