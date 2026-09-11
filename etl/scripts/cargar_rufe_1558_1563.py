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
        "numero_rufe": "1558",
        "prioridad": "MEDIA",
        "observaciones_evaluador": "Observaciones Jaime: Vivienda de 2 pisos de interes social con muros agrietados. Se recomienda evaluacion estructural para reforzamiento estructural. Carlos Cobo.",
        "observaciones_animales": None,
        "corregimiento": None,
        "sector_barrio": "Nueva Estancia",
        "direccion": "Carrera 12 #18-66",
        "personas": [
            {"nombre": "Jaime Neira Aladate", "doc": "1118283573", "parentesco": "Jefe(a) o cabeza del hogar", "sexo": "M", "fecha_nac": "1996-07-08", "edad": 30, "telefono": "3103984785", "es_jefe": True},
            {"nombre": "Jaime Javier Neira Mera", "doc": "16448897", "parentesco": "Padre, Madre, Suegro, Suegra", "sexo": "M", "fecha_nac": "1960-09-23", "edad": 65, "telefono": None, "es_jefe": False},
            {"nombre": "Gloria Estela Alvarado", "doc": "29739112", "parentesco": "Padre, Madre, Suegro, Suegra", "sexo": "F", "fecha_nac": "1960-10-16", "edad": 65, "telefono": None, "es_jefe": False}
        ]
    },
    {
        "numero_rufe": "1559",
        "prioridad": "MEDIA",
        "observaciones_evaluador": "Observaciones Jhon Calpa: Vivienda de 2 pisos. Existe una columna que quedo afectada por concentracion de esfuerzos terminada en armadura y muros con grietas aparentemente negativas. Se recomienda reforzamiento con columna y vigas. Carlos Cobo.",
        "observaciones_animales": None,
        "corregimiento": None,
        "sector_barrio": "La Estancia",
        "direccion": "Cra 12 #18-72",
        "personas": [
            {"nombre": "Jhon Elicio Calpa Sanchez", "doc": "1062775279", "parentesco": "Jefe(a) o cabeza del hogar", "sexo": "M", "fecha_nac": "1987-09-15", "edad": 38, "telefono": "3113376511", "es_jefe": True},
            {"nombre": "Yenifer Mercedes Sanchez", "doc": "1062776719", "parentesco": "Pareja, Esposa(o)", "sexo": "F", "fecha_nac": None, "edad": None, "telefono": "3136615519", "es_jefe": False},
            {"nombre": "Aliseth Valeria Calpa Sanchez", "doc": "1062777747", "parentesco": "Hijo(a), hijastro(a)", "sexo": "F", "fecha_nac": "2009-11-20", "edad": 16, "telefono": None, "es_jefe": False},
            {"nombre": "Dilan Felipe Calpa Sanchez", "doc": "1105387788", "parentesco": "Hijo(a), hijastro(a)", "sexo": "M", "fecha_nac": "2013-12-15", "edad": 12, "telefono": None, "es_jefe": False}
        ]
    },
    {
        "numero_rufe": "1560",
        "prioridad": "MEDIA",
        "observaciones_evaluador": "Observaciones Lucely: Vivienda de 1 piso fisuras en muros. Se recomienda reforzamiento estructural. Carlos Cobo.",
        "observaciones_animales": None,
        "corregimiento": None,
        "sector_barrio": "La Estancia",
        "direccion": "Cra 12B #20-09",
        "personas": [
            {"nombre": "Lucelly Cordoba", "doc": "40363084", "parentesco": "Jefe(a) o cabeza del hogar", "sexo": "F", "fecha_nac": "1976-09-30", "edad": 49, "telefono": "3103659328", "es_jefe": True},
            {"nombre": "Ene Noguera", "doc": "1086222071", "parentesco": "Pareja, Esposa(o)", "sexo": "M", "fecha_nac": "1986-05-03", "edad": 40, "telefono": "3229010671", "es_jefe": False},
            {"nombre": "Heidy Cordoba", "doc": "1192770397", "parentesco": "Hijo(a), hijastro(a)", "sexo": "F", "fecha_nac": "2000-01-30", "edad": 26, "telefono": "3113745067", "es_jefe": False},
            {"nombre": "Shatol Cordoba", "doc": "1113225619", "parentesco": "Nieto(a)", "sexo": "F", "fecha_nac": "2010-01-03", "edad": 16, "telefono": "3122279436", "es_jefe": False},
            {"nombre": "Stefany Cordoba", "doc": "1114622179", "parentesco": "Nieto(a)", "sexo": "F", "fecha_nac": "2007-05-02", "edad": 19, "telefono": "3217242147", "es_jefe": False},
            {"nombre": "Emily Guzman", "doc": "1112231971", "parentesco": "Nieto(a)", "sexo": "F", "fecha_nac": "2017-06-19", "edad": 9, "telefono": None, "es_jefe": False},
            {"nombre": "Aileny Acero", "doc": "1118314239", "parentesco": "Nieto(a)", "sexo": "F", "fecha_nac": "2026-04-22", "edad": 0, "telefono": None, "es_jefe": False},
            {"nombre": "Yuris Katherina Cordoba", "doc": "1112231887", "parentesco": "Hijo(a), hijastro(a)", "sexo": "F", "fecha_nac": "1999-05-27", "edad": 27, "telefono": "3148480577", "es_jefe": False},
            {"nombre": "Dilan Polo Acero", "doc": "1114625321", "parentesco": "Nieto(a)", "sexo": "M", "fecha_nac": "2020-09-20", "edad": 5, "telefono": None, "es_jefe": False},
            {"nombre": "Eyik Polo Acero", "doc": "1112233053", "parentesco": "Nieto(a)", "sexo": "M", "fecha_nac": "2024-02-22", "edad": 2, "telefono": None, "es_jefe": False}
        ]
    },
    {
        "numero_rufe": "1562",
        "prioridad": "MEDIA",
        "observaciones_evaluador": "Observaciones Jackeline: Vivienda de 2 pisos con muros agrietados. Se recomienda evaluacion estructural para reforzamiento de la vivienda. Carlos Cobo.",
        "observaciones_animales": None,
        "corregimiento": None,
        "sector_barrio": "La Estancia",
        "direccion": "Cra 16F #22-66",
        "personas": [
            {"nombre": "Jose Alberto Gutierrez", "doc": "1118825165", "parentesco": "Jefe(a) o cabeza del hogar", "sexo": "M", "fecha_nac": "1991-03-17", "edad": 35, "telefono": "3173080615", "es_jefe": True},
            {"nombre": "Yerson Blandon", "doc": "1073323981", "parentesco": "Pareja, Esposa(o)", "sexo": "M", "fecha_nac": None, "edad": None, "telefono": None, "es_jefe": False},
            {"nombre": "Yakeline Caicedo", "doc": "66849479", "parentesco": "Padre, Madre, Suegro, Suegra", "sexo": "F", "fecha_nac": "1972-09-23", "edad": 53, "telefono": "3154229570", "es_jefe": False}
        ]
    },
    {
        "numero_rufe": "1562B",
        "prioridad": "MEDIA",
        "observaciones_evaluador": "Observaciones Aida: Vivienda de 2 pisos con fisuras en muros. Se recomienda evaluacion estructural para reforzamiento. Carlos Cobo.",
        "observaciones_animales": None,
        "corregimiento": None,
        "sector_barrio": "La Estancia",
        "direccion": "Cra 12 #18-66",
        "personas": [
            {"nombre": "Nestor Tibaduiza", "doc": "14377374", "parentesco": "Jefe(a) o cabeza del hogar", "sexo": "M", "fecha_nac": "1950-01-23", "edad": 76, "telefono": "3148456696", "es_jefe": True},
            {"nombre": "Aida Toro", "doc": "29973557", "parentesco": "Pareja, Esposa(o)", "sexo": "F", "fecha_nac": "1982-03-11", "edad": 44, "telefono": None, "es_jefe": False},
            {"nombre": "Josue Tibaduiza", "doc": "1111551609", "parentesco": "Hijo(a), hijastro(a)", "sexo": "M", "fecha_nac": "2010-10-21", "edad": 15, "telefono": None, "es_jefe": False},
            {"nombre": "Emanuel Tibaduiza", "doc": "1232796677", "parentesco": "Hijo(a), hijastro(a)", "sexo": "M", "fecha_nac": "2016-05-17", "edad": 10, "telefono": None, "es_jefe": False}
        ]
    },
    {
        "numero_rufe": "1563",
        "prioridad": "MEDIA",
        "observaciones_evaluador": "Observaciones Jackeline: Vivienda de 2 pisos de interes social (Muyumbo) con fisuras y desprendimientos de losa en la sala y muros en 1 y 2 nivel. Se recomienda revision estructural de especialista para reforzamiento en zona afectada. Carlos Cobo.",
        "observaciones_animales": None,
        "corregimiento": None,
        "sector_barrio": "Muyumbo",
        "direccion": "Kra 12 #18B-18",
        "personas": [
            {"nombre": "Marino Mina", "doc": "6247850", "parentesco": "Jefe(a) o cabeza del hogar", "sexo": "M", "fecha_nac": "1967-07-14", "edad": 59, "telefono": "3210780903", "es_jefe": True},
            {"nombre": "Erica Escobar", "doc": "29942112", "parentesco": "Pareja, Esposa(o)", "sexo": "F", "fecha_nac": "1972-01-14", "edad": 54, "telefono": "3204713154", "es_jefe": False}
        ]
    }
]

def main():
    print("Iniciando procesamiento de RUFEs 1558 a 1563...")
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
