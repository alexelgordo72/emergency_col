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
        "numero_rufe": "1571",
        "prioridad": "BAJA",
        "observaciones_evaluador": "Sin afectaciones visibles. Hacer seguimiento.",
        "observaciones_animales": None,
        "corregimiento": None,
        "sector_barrio": "Buenos Aires",
        "direccion": "Cra 13 con calle 11 #13-06",
        "personas": [
            {"nombre": "Edel Nieto", "doc": "31477929", "parentesco": "Jefe(a) o cabeza del hogar", "sexo": "F", "fecha_nac": "1964-01-01", "edad": 62, "telefono": "3167904900", "es_jefe": True}
        ]
    },
    {
        "numero_rufe": "1572",
        "prioridad": "BAJA",
        "observaciones_evaluador": "Sin afectaciones visibles. Hacer seguimiento.",
        "observaciones_animales": None,
        "corregimiento": None,
        "sector_barrio": "Buenos Aires",
        "direccion": "Calle 11A #12-36",
        "personas": [
            {"nombre": "Ana Lucia Ortega", "doc": "31475773", "parentesco": "Jefe(a) o cabeza del hogar", "sexo": "F", "fecha_nac": "1970-11-19", "edad": 55, "telefono": "3104411102", "es_jefe": True}
        ]
    },
    {
        "numero_rufe": "1573",
        "prioridad": "BAJA",
        "observaciones_evaluador": "Prioridad baja.",
        "observaciones_animales": None,
        "corregimiento": None,
        "sector_barrio": "Guabinas - Filandia Torre 20 Apto 103",
        "direccion": "Cra 19B #19B-07",
        "personas": [
            {"nombre": "Deivison Puente Osorio", "doc": "6550797", "parentesco": "Jefe(a) o cabeza del hogar", "sexo": "M", "fecha_nac": "1985-10-14", "edad": 40, "telefono": "313039469", "es_jefe": True},
            {"nombre": "Gladis Osorio", "doc": "31469995", "parentesco": "Padre, Madre, Suegro, Suegra", "sexo": "F", "fecha_nac": "1959-11-16", "edad": 66, "telefono": "320549797", "es_jefe": False}
        ]
    },
    {
        "numero_rufe": "1574",
        "prioridad": "BAJA",
        "observaciones_evaluador": "Sin afectaciones visibles. Ya se realizaron adecuaciones. Hacer seguimiento.",
        "observaciones_animales": None,
        "corregimiento": None,
        "sector_barrio": "Pizarro Hogar ICBF",
        "direccion": "Calle 14N #11BN-52",
        "personas": [
            {"nombre": "Luz Adriana Osorio", "doc": "66973808", "parentesco": "Jefe(a) o cabeza del hogar", "sexo": "F", "fecha_nac": "1976-02-15", "edad": 50, "telefono": "3138891010", "es_jefe": True}
        ]
    },
    {
        "numero_rufe": "1575",
        "prioridad": "BAJA",
        "observaciones_evaluador": "Sin afectaciones visibles. Hacer seguimiento.",
        "observaciones_animales": None,
        "corregimiento": "Los Chamitos",
        "sector_barrio": "Pizarro ICBF",
        "direccion": "Calle 14N #11BN-52",
        "personas": [
            {"nombre": "Karen Dayana Pedroza Osorio", "doc": "1144187556", "parentesco": "Jefe(a) o cabeza del hogar", "sexo": "F", "fecha_nac": "1995-07-18", "edad": 31, "telefono": "3145040303", "es_jefe": True}
        ]
    },
    {
        "numero_rufe": "1576",
        "prioridad": "BAJA",
        "observaciones_evaluador": "Afectaciones menores, fisuras. Realizar adecuaciones.",
        "observaciones_animales": None,
        "corregimiento": "Capullitos",
        "sector_barrio": "Pizarro",
        "direccion": "Calle 14 #11N-27",
        "personas": [
            {"nombre": "Oneida Alicia Gomez", "doc": "59831625", "parentesco": "Jefe(a) o cabeza del hogar", "sexo": "F", "fecha_nac": "1975-11-24", "edad": 50, "telefono": "3214209208", "es_jefe": True}
        ]
    },
    {
        "numero_rufe": "1577",
        "prioridad": "BAJA",
        "observaciones_evaluador": "Afectaciones menores, fisuras y dilataciones. Recomendacion realizar adecuaciones.",
        "observaciones_animales": None,
        "corregimiento": None,
        "sector_barrio": "Las Cruces",
        "direccion": "Calle 7 #15-12",
        "personas": [
            {"nombre": "Maria Isabel Tarquino", "doc": "29975835", "parentesco": "Jefe(a) o cabeza del hogar", "sexo": "F", "fecha_nac": "1986-07-09", "edad": 40, "telefono": "3006096364", "es_jefe": True}
        ]
    },
    {
        "numero_rufe": "1578",
        "prioridad": "BAJA",
        "observaciones_evaluador": "Sin afectaciones visibles. Hacer seguimiento.",
        "observaciones_animales": None,
        "corregimiento": None,
        "sector_barrio": "Las Cruces",
        "direccion": "Calle 7 #15-31",
        "personas": [
            {"nombre": "Alexandra Trujillo", "doc": "31481768", "parentesco": "Jefe(a) o cabeza del hogar", "sexo": "F", "fecha_nac": "1979-07-28", "edad": 47, "telefono": "3128022187", "es_jefe": True}
        ]
    },
    {
        "numero_rufe": "1579",
        "prioridad": "BAJA",
        "observaciones_evaluador": "Sin afectaciones visibles.",
        "observaciones_animales": None,
        "corregimiento": "Los Bulliciosos",
        "sector_barrio": "Pizarro",
        "direccion": "Calle 13CN #12N-81",
        "personas": [
            {"nombre": "Lina Marcela Lopez Mosquera", "doc": "1006072519", "parentesco": "Jefe(a) o cabeza del hogar", "sexo": "F", "fecha_nac": "2000-02-16", "edad": 26, "telefono": "3135043386", "es_jefe": True}
        ]
    },
    {
        "numero_rufe": "1580",
        "prioridad": "BAJA",
        "observaciones_evaluador": "Sin afectaciones visibles. Hacer seguimiento.",
        "observaciones_animales": None,
        "corregimiento": "Rango Destino",
        "sector_barrio": None,
        "direccion": "Calle 15 #14-96",
        "personas": [
            {"nombre": "Fabiola Rivera", "doc": "31476092", "parentesco": "Jefe(a) o cabeza del hogar", "sexo": "F", "fecha_nac": "1940-10-15", "edad": 85, "telefono": "3187076447", "es_jefe": True}
        ]
    }
]

def main():
    print("Iniciando procesamiento de RUFEs 1571 a 1580 (ICBF / Bajo)...")
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
