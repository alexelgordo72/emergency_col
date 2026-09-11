import psycopg2
from psycopg2.extras import RealDictCursor
import json
import uuid

DB_CONFIG = {
    "dbname": "comunidad_db",
    "user": "admin_comunidad",
    "password": "TuPasswordSegura2026!",
    "host": "10.147.17.24",
    "port": "5432"
}

DATOS_RUFES = [
    {
        "numero_rufe": "1565",
        "prioridad": "BAJA",
        "observaciones_evaluador": "Sin afectaciones visibles. Hacer seguimiento.",
        "observaciones_animales": None,
        "corregimiento": None,
        "sector_barrio": "Las Cruces",
        "direccion": "Cra 9A #2-28",
        "personas": [
            {"nombre": "Martha Solano", "doc": "31478266", "parentesco": "Jefe(a) o cabeza del hogar", "sexo": "F", "fecha_nac": "1975-08-10", "edad": 51, "telefono": "3216229543", "es_jefe": True}
        ]
    },
    {
        "numero_rufe": "1566",
        "prioridad": "BAJA",
        "observaciones_evaluador": "Sin afectaciones visibles. Hacer seguimiento.",
        "observaciones_animales": None,
        "corregimiento": None,
        "sector_barrio": "San Fernando",
        "direccion": None,
        "personas": [
            {"nombre": "Ingrid Paz", "doc": "1118288586", "parentesco": "Jefe(a) o cabeza del hogar", "sexo": "F", "fecha_nac": "1988-03-14", "edad": 38, "telefono": "3108906159", "es_jefe": True}
        ]
    },
    {
        "numero_rufe": "1567",
        "prioridad": "BAJA",
        "observaciones_evaluador": "Sin afectaciones visibles. Hacer seguimiento.",
        "observaciones_animales": None,
        "corregimiento": None,
        "sector_barrio": "San Fernando",
        "direccion": "Calle 3A #8-33",
        "personas": [
            {"nombre": "Luz Nelly Quintero Calderon", "doc": "31470095", "parentesco": "Jefe(a) o cabeza del hogar", "sexo": "F", "fecha_nac": "1966-01-12", "edad": 60, "telefono": "3162333377", "es_jefe": True}
        ]
    },
    {
        "numero_rufe": "1568",
        "prioridad": "BAJA",
        "observaciones_evaluador": "Sin afectaciones visibles. Hacer seguimiento.",
        "observaciones_animales": None,
        "corregimiento": None,
        "sector_barrio": "San Fernando",
        "direccion": "Calle 2A #6A-18",
        "personas": [
            {"nombre": "Monica Muñoz", "doc": "31476360", "parentesco": "Jefe(a) o cabeza del hogar", "sexo": "F", "fecha_nac": "1973-02-22", "edad": 53, "telefono": "3233606238", "es_jefe": True}
        ]
    },
    {
        "numero_rufe": "1569",
        "prioridad": "BAJA",
        "observaciones_evaluador": "Sin afectaciones visibles. Hacer seguimiento.",
        "observaciones_animales": None,
        "corregimiento": None,
        "sector_barrio": "San Fernando",
        "direccion": "Cra 9A #3-24",
        "personas": [
            {"nombre": "Maria Margarita Bejarano Fernandez", "doc": "31476594", "parentesco": "Jefe(a) o cabeza del hogar", "sexo": "F", "fecha_nac": "1971-08-29", "edad": 55, "telefono": "3226319597", "es_jefe": True}
        ]
    },
    {
        "numero_rufe": "1570",
        "prioridad": "BAJA",
        "observaciones_evaluador": "Sin afectaciones visibles. Hacer seguimiento.",
        "observaciones_animales": None,
        "corregimiento": None,
        "sector_barrio": "Buenos Aires",
        "direccion": "Calle 10A #12-28",
        "personas": [
            {"nombre": "Melisa Lugo Beltran", "doc": "1118292192", "parentesco": "Jefe(a) o cabeza del hogar", "sexo": "F", "fecha_nac": "1989-08-08", "edad": 37, "telefono": "3215361687", "es_jefe": True}
        ]
    }
]

def main():
    print("Iniciando procesamiento de RUFEs 1565 a 1570...")
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        insertados = 0
        temporales = 0
        
        for rufe in DATOS_RUFES:
            num = rufe["numero_rufe"]
            jefe = next((p for p in rufe["personas"] if p["es_jefe"]), rufe["personas"][0])
            
            cur.execute("""
                SELECT id, datos_extra, titulo 
                FROM public.reportes_comunitarios 
                WHERE titulo ILIKE %s OR titulo ILIKE %s
            """, (f"%RUFE%{num}%", f"%{num}%"))
            existe = cur.fetchone()
            
            if existe:
                print(f"[-] RUFE {num} ya existe (ID: {existe['id']}). A tabla temporal...")
                cur.execute("""
                    INSERT INTO public.rufe_temporal_merge (
                        numero_rufe, documento, nombre_ciudadano,
                        reporte_id_existente, datos_nuevos, datos_actuales, estado
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (
                    num,
                    jefe["doc"],
                    jefe["nombre"],
                    existe["id"],
                    json.dumps(rufe),
                    json.dumps(existe["datos_extra"]),
                    "PENDIENTE_MERGE"
                ))
                temporales += 1
            else:
                print(f"[+] RUFE {num} es NUEVO. Insertando en las 4 tablas...")
                
                rep_id = str(uuid.uuid4())
                rep_rufe_id = str(uuid.uuid4())
                titulo_oficial = f"Evaluación RUFE {num} - {jefe['nombre']}"
                
                datos_extra = {
                    "rufe": num,
                    "cedula": jefe["doc"],
                    "nombre": jefe["nombre"],
                    "prioridad": rufe["prioridad"],
                    "observaciones": rufe["observaciones_evaluador"],
                    "observaciones_animales": rufe["observaciones_animales"],
                    "direccion": rufe["direccion"],
                    "total_personas": len(rufe["personas"])
                }
                
                # 1. reportes_comunitarios
                cur.execute("""
                    INSERT INTO public.reportes_comunitarios 
                    (id, titulo, descripcion_detallada, sector_barrio, direccion_referencia, estado_actual, datos_extra, procesado_rufe, migrado_rufe, activo)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, true, true, true)
                """, (
                    rep_id,
                    titulo_oficial,
                    rufe["observaciones_evaluador"],
                    rufe["sector_barrio"],
                    rufe["direccion"],
                    f"Aprobado_{rufe['prioridad']}",
                    json.dumps(datos_extra)
                ))
                
                # 2. rufe_formularios
                cur.execute("""
                    INSERT INTO public.rufe_formularios 
                    (reporte_id, numero_formulario, corregimiento, prioridad, observaciones_animales, observaciones_evaluador)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING id
                """, (
                    rep_id,
                    num,
                    rufe["corregimiento"],
                    rufe["prioridad"],
                    rufe["observaciones_animales"],
                    rufe["observaciones_evaluador"]
                ))
                form_id = cur.fetchone()["id"]
                
                # 3. rufe_personas
                for p in rufe["personas"]:
                    cur.execute("""
                        INSERT INTO public.rufe_personas 
                        (rufe_formulario_id, nombre_completo, documento_identidad, fecha_nacimiento, telefono, es_jefe_hogar, parentesco, sexo, edad)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (
                        form_id,
                        p["nombre"],
                        p["doc"],
                        p["fecha_nac"],
                        p["telefono"],
                        p["es_jefe"],
                        p["parentesco"],
                        p["sexo"],
                        p["edad"]
                    ))
                    
                # 4. reportes_comunitarios_rufe
                cur.execute("""
                    INSERT INTO public.reportes_comunitarios_rufe 
                    (id, rufe_formulario_id, titulo, descripcion_detallada, sector_barrio, direccion_referencia, estado_actual, datos_extra, numero_formulario, prioridad, observaciones_animales, observaciones_evaluador, corregimiento, jefe_hogar_nombre, jefe_hogar_cedula, jefe_hogar_telefono, jefe_hogar_genero, jefe_hogar_parentesco)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    rep_rufe_id,
                    form_id,
                    titulo_oficial,
                    rufe["observaciones_evaluador"],
                    rufe["sector_barrio"],
                    rufe["direccion"],
                    f"Aprobado_{rufe['prioridad']}",
                    json.dumps(datos_extra),
                    num,
                    rufe["prioridad"],
                    rufe["observaciones_animales"],
                    rufe["observaciones_evaluador"],
                    rufe["corregimiento"],
                    jefe["nombre"],
                    jefe["doc"],
                    jefe["telefono"],
                    jefe["sexo"],
                    jefe["parentesco"]
                ))
                
                insertados += 1
                
        conn.commit()
        print("\n" + "="*45)
        print("Sincronización finalizada exitosamente.")
        print(f"-> Insertados en las 4 tablas: {insertados}")
        print(f"-> Enviados a staging (rufe_temporal_merge): {temporales}")
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
