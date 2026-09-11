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
        "numero_rufe": "1581",
        "prioridad": "BAJA",
        "observaciones_evaluador": "Sin afectaciones visibles. Hacer seguimiento.",
        "observaciones_animales": None,
        "corregimiento": "Mis Amiguitos ICBF",
        "sector_barrio": "Lleras",
        "direccion": "Calle 9N #5-03",
        "personas": [
            {"nombre": "Maria Valentina Londoño", "doc": "1006435412", "parentesco": "Jefe(a) o cabeza del hogar", "sexo": "F", "fecha_nac": "2001-03-21", "edad": 25, "telefono": "3182203399", "es_jefe": True}
        ]
    },
    {
        "numero_rufe": "1582",
        "prioridad": "BAJA",
        "observaciones_evaluador": "Sin afectaciones visibles. Realizaron adecuaciones. Hacer seguimiento.",
        "observaciones_animales": None,
        "corregimiento": "Los Pitufos",
        "sector_barrio": "Lleras",
        "direccion": None,
        "personas": [
            {"nombre": "Elizabeth Gomez Muñoz", "doc": "31478223", "parentesco": "Jefe(a) o cabeza del hogar", "sexo": "F", "fecha_nac": "1975-03-01", "edad": 51, "telefono": "3108933440", "es_jefe": True}
        ]
    },
    {
        "numero_rufe": "1583",
        "prioridad": "BAJA",
        "observaciones_evaluador": "Sin afectaciones visibles.",
        "observaciones_animales": None,
        "corregimiento": "Oso Meloso",
        "sector_barrio": "Lleras",
        "direccion": "Calle 9N #10N-39",
        "personas": [
            {"nombre": "Zandra Perdomo Gonzalez", "doc": "31477384", "parentesco": "Jefe(a) o cabeza del hogar", "sexo": "F", "fecha_nac": "1974-06-01", "edad": 52, "telefono": "3188710374", "es_jefe": True}
        ]
    },
    {
        "numero_rufe": "1584",
        "prioridad": "BAJA",
        "observaciones_evaluador": "Sin afectaciones visibles.",
        "observaciones_animales": None,
        "corregimiento": "Mis Pequeños Sabios",
        "sector_barrio": "Lleras",
        "direccion": "Calle 6 #4-86",
        "personas": [
            {"nombre": "Maria Alejandra Montoya Cuenca", "doc": "1118283832", "parentesco": "Jefe(a) o cabeza del hogar", "sexo": "F", "fecha_nac": "1986-06-06", "edad": 40, "telefono": "3188061210", "es_jefe": True}
        ]
    },
    {
        "numero_rufe": "1585",
        "prioridad": "BAJA",
        "observaciones_evaluador": "Sin afectaciones visibles. Pendiente por adecuaciones fisuras minimas.",
        "observaciones_animales": None,
        "corregimiento": "Golondrinas",
        "sector_barrio": "Lleras",
        "direccion": "Calle 6 #3-47",
        "personas": [
            {"nombre": "Geraldine Delgado Noguera", "doc": "1116372138", "parentesco": "Jefe(a) o cabeza del hogar", "sexo": "F", "fecha_nac": "2000-08-29", "edad": 26, "telefono": "3218063983", "es_jefe": True}
        ]
    }
]

def main():
    print("Iniciando procesamiento de RUFEs 1581 a 1585 (ICBF / Lleras)...")
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
