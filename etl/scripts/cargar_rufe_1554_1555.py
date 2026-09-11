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
        "numero_rufe": "1554",
        "prioridad": "MEDIA",
        "observaciones_evaluador": "Observacion Sebastian: Vivienda de 1 piso con fisuras leves de reboque. Adicionalmente manifiesta que la vivienda de al lado de 2 pisos mas alta esta poniendo en riesgo la vivienda. Carlos Cobo.",
        "observaciones_animales": None,
        "corregimiento": None,
        "sector_barrio": "La Estancia",
        "direccion": "Calle 15 #21-09",
        "personas": [
            {"nombre": "Sebastian Villa", "doc": "1118307428", "parentesco": "Jefe(a) o cabeza del hogar", "sexo": "M", "fecha_nac": "1996-11-14", "edad": 29, "telefono": "3192037761", "es_jefe": True},
            {"nombre": "Natalia Andrea Sanchez", "doc": "1005911164", "parentesco": "Pareja, Esposa(o)", "sexo": "F", "fecha_nac": "2002-11-20", "edad": 23, "telefono": "3117325224", "es_jefe": False},
            {"nombre": "Juan Sebastian Sanchez Villa", "doc": "1232933294", "parentesco": "Hijo(a), hijastro(a)", "sexo": "M", "fecha_nac": "2024-09-04", "edad": 2, "telefono": None, "es_jefe": False}
        ]
    },
    {
        "numero_rufe": "1555",
        "prioridad": "MEDIA",
        "observaciones_evaluador": "Observacion Alexander: Casa de 1 piso con fisuras en muros parte trasera. Se recomienda reforzamiento columnas y vigas. Carlos Cobo.",
        "observaciones_animales": None,
        "corregimiento": None,
        "sector_barrio": "La Estancia",
        "direccion": "Calle 21 #14A-18",
        "personas": [
            {"nombre": "Alexander Medina", "doc": "79644285", "parentesco": "Jefe(a) o cabeza del hogar", "sexo": "M", "fecha_nac": "1973-03-20", "edad": 53, "telefono": "3126774471", "es_jefe": True},
            {"nombre": "Zeneida Parra Morales", "doc": "52761147", "parentesco": "Pareja, Esposa(o)", "sexo": "F", "fecha_nac": "1973-08-07", "edad": 53, "telefono": "3136878515", "es_jefe": False},
            {"nombre": "Emilin Medina", "doc": "1109926102", "parentesco": "Hijo(a), hijastro(a)", "sexo": "F", "fecha_nac": "2012-04-03", "edad": 14, "telefono": None, "es_jefe": False},
            {"nombre": "Steven Medina", "doc": "1151953257", "parentesco": "Hijo(a), hijastro(a)", "sexo": "M", "fecha_nac": "1994-04-26", "edad": 32, "telefono": "3122999536", "es_jefe": False}
        ]
    }
]

def main():
    print("Iniciando procesamiento de RUFEs 1554 y 1555...")
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
