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

def main():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        # Buscar el caso 077 (Edinso Gavilanes o RUFE asociado al 077)
        cur.execute("""
            SELECT r.id, r.estado_actual, r.datos_extra, f.prioridad 
            FROM public.reportes_comunitarios r
            LEFT JOIN public.rufe_formularios f ON f.reporte_id = r.id
            WHERE f.numero_formulario ILIKE '%077%' OR r.titulo ILIKE '%077%' OR r.titulo ILIKE '%Edinso%'
        """)
        rows = cur.fetchall()
        for row in rows:
            rep_id = row["id"]
            # Restaurar estado original basado en su prioridad o dejarlo como Aprobado_ALTA según reporte original
            estado_original = "Aprobado_ALTA"
            datos = row["datos_extra"] or {}
            datos["hallazgo_infraestructura"] = "La persona manifestó directamente que no requiere ayuda a pesar de la pérdida total reportada por incendio."
            
            cur.execute("""
                UPDATE public.reportes_comunitarios 
                SET estado_actual = %s, datos_extra = %s 
                WHERE id = %s
            """, (estado_original, json.dumps(datos), rep_id))
            print(f"[CORREGIDO] Caso 077 restaurado a estado: {estado_original} con observación técnica.")
            
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
