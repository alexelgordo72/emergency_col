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
        "numero_rufe": "1507",
        "prioridad": "BAJA",
        "observaciones_evaluador": "La casa se ve que no esta afectada la tienen de bodega y taller y las afectaciones son muy pocas.",
        "observaciones_animales": None,
        "corregimiento": None,
        "sector_barrio": "Cruces Alta",
        "direccion": "15 N-58",
        "personas": [
            {"nombre": "Benito Hoyos Muñoz", "doc": "11840009", "parentesco": "Jefe(a) o cabeza del hogar", "sexo": "M", "fecha_nac": "1947-07-14", "edad": 79, "telefono": "3218016016", "es_jefe": True},
            {"nombre": "Flor Maria Arce", "doc": "3883502", "parentesco": "Pareja, Esposa(o)", "sexo": "F", "fecha_nac": "1962-06-12", "edad": 64, "telefono": "3105194828", "es_jefe": False},
            {"nombre": "Luz Adriana Hoyos Arce", "doc": "1118297203", "parentesco": "Hijo(a), hijastro(a)", "sexo": "F", "fecha_nac": "1983-06-26", "edad": 43, "telefono": None, "es_jefe": False},
            {"nombre": "Alba Maria Arce", "doc": "29975055", "parentesco": "Padre, Madre, Suegro, Suegra", "sexo": "F", "fecha_nac": "1933-10-16", "edad": 92, "telefono": None, "es_jefe": False}
        ]
    },
    {
        "numero_rufe": "1508",
        "prioridad": "BAJA",
        "observaciones_evaluador": "Al revisar la casa encontre que las escaleras al segundo piso estan totalmente derrumbadas, la planta baja tiene algunas fisuras y parte del tejado colapso y el suelo tambien tiene algunas fisuras",
        "observaciones_animales": None,
        "corregimiento": None,
        "sector_barrio": "Nuevo Horizonte",
        "direccion": "Carrera 9 oeste",
        "personas": [
            {"nombre": "Alba Lidia Quiñones", "doc": "31486583", "parentesco": "Jefe(a) o cabeza del hogar", "sexo": "F", "fecha_nac": "1963-05-02", "edad": 63, "telefono": "3135123159", "es_jefe": True},
            {"nombre": "Emanuel Andres Quiñones", "doc": "1116375001", "parentesco": "Hijo(a), hijastro(a)", "sexo": "M", "fecha_nac": "2007-09-27", "edad": 18, "telefono": "3006768086", "es_jefe": False},
            {"nombre": "Luisa Fernanda Quiñones", "doc": "1007779297", "parentesco": "Hijo(a), hijastro(a)", "sexo": "F", "fecha_nac": "1998-02-26", "edad": 28, "telefono": "3114214012", "es_jefe": False},
            {"nombre": "Ethan Gael Quiñones", "doc": "1146385560", "parentesco": "Hijo(a), hijastro(a)", "sexo": "M", "fecha_nac": "2026-02-25", "edad": 0, "telefono": None, "es_jefe": False},
            {"nombre": "Jean Pool Flor Quiñones", "doc": "1148308301", "parentesco": "Nieto(a)", "sexo": "M", "fecha_nac": "2015-04-21", "edad": 11, "telefono": None, "es_jefe": False},
            {"nombre": "Jeiron Alexis Ospina", "doc": "100606721", "parentesco": "Otro no pariente", "sexo": "M", "fecha_nac": "2002-02-16", "edad": 24, "telefono": "3207041050", "es_jefe": False}
        ]
    },
    {
        "numero_rufe": "1509",
        "prioridad": "BAJA",
        "observaciones_evaluador": "Riesgo Bajo.",
        "observaciones_animales": None,
        "corregimiento": None,
        "sector_barrio": "Pizarro",
        "direccion": "Calle 13 CN #15N 40",
        "personas": [
            {"nombre": "German Alviz Castro", "doc": "16271790", "parentesco": "Jefe(a) o cabeza del hogar", "sexo": "M", "fecha_nac": "1964-02-15", "edad": 62, "telefono": "3205363809", "es_jefe": True},
            {"nombre": "Margarita Piamba Paz", "doc": "31153088", "parentesco": "Pareja, Esposa(o)", "sexo": "F", "fecha_nac": "1959-10-25", "edad": 66, "telefono": "3233968939", "es_jefe": False},
            {"nombre": "Elizabeth Alviz Piamba", "doc": "1118301444", "parentesco": "Hijo(a), hijastro(a)", "sexo": "F", "fecha_nac": "1993-11-15", "edad": 32, "telefono": "3127963873", "es_jefe": False}
        ]
    },
    {
        "numero_rufe": "1510",
        "prioridad": "BAJA",
        "observaciones_evaluador": "Solo tiene fisuras minimas. No tiene nada grave.",
        "observaciones_animales": None,
        "corregimiento": None,
        "sector_barrio": "Carlos Leon Pizarro",
        "direccion": "Calle 13CN #15N-87",
        "personas": [
            {"nombre": "Fabian Hector Pachajoa Erazo", "doc": "16703422", "parentesco": "Jefe(a) o cabeza del hogar", "sexo": "M", "fecha_nac": "1964-09-17", "edad": 61, "telefono": "3136930516", "es_jefe": True},
            {"nombre": "Martha Isabel Velasco Lozada", "doc": "67013454", "parentesco": "Pareja, Esposa(o)", "sexo": "F", "fecha_nac": "1998-01-08", "edad": 28, "telefono": "3053762087", "es_jefe": False},
            {"nombre": "Fabian David Pachajoa Velasco", "doc": "1105388444", "parentesco": "Hijo(a), hijastro(a)", "sexo": "M", "fecha_nac": "2014-02-01", "edad": 12, "telefono": None, "es_jefe": False}
        ]
    },
    {
        "numero_rufe": "1511",
        "prioridad": "BAJA",
        "observaciones_evaluador": "Prioridad: BAJA",
        "observaciones_animales": None,
        "corregimiento": None,
        "sector_barrio": "Carlos Leon Pizarro",
        "direccion": "Calle 13 #15N-46",
        "personas": [
            {"nombre": "Marjori Consuelo Gueche Paredes", "doc": "29741702", "parentesco": "Jefe(a) o cabeza del hogar", "sexo": "F", "fecha_nac": "1972-05-08", "edad": 54, "telefono": "3113745137", "es_jefe": True}
        ]
    },
    {
        "numero_rufe": "1512",
        "prioridad": "BAJA",
        "observaciones_evaluador": "PRIORIDAD BAJA",
        "observaciones_animales": None,
        "corregimiento": None,
        "sector_barrio": "San Fernando",
        "direccion": "Cra 8 #1-34 Oeste",
        "personas": [
            {"nombre": "Alexander Arias", "doc": "16927744", "parentesco": "Jefe(a) o cabeza del hogar", "sexo": "M", "fecha_nac": "1980-05-02", "edad": 46, "telefono": "3152699648", "es_jefe": True},
            {"nombre": "Tatyana Andrea Ayala", "doc": "1112107111", "parentesco": "Pareja, Esposa(o)", "sexo": "F", "fecha_nac": "1997-12-26", "edad": 28, "telefono": "3170196139", "es_jefe": False},
            {"nombre": "Henry Ayala", "doc": "6113934", "parentesco": "Padre, Madre, Suegro, Suegra", "sexo": "M", "fecha_nac": "1956-05-10", "edad": 70, "telefono": None, "es_jefe": False},
            {"nombre": "Luz Marina Restrepo", "doc": "324863679", "parentesco": "Padre, Madre, Suegro, Suegra", "sexo": "F", "fecha_nac": "1947-06-03", "edad": 79, "telefono": None, "es_jefe": False}
        ]
    },
    {
        "numero_rufe": "1513",
        "prioridad": "BAJA",
        "observaciones_evaluador": "Vivienda con grietas leves en diferentes lugares.",
        "observaciones_animales": None,
        "corregimiento": None,
        "sector_barrio": "San Fernando",
        "direccion": "Calle 2A #8-80",
        "personas": [
            {"nombre": "Valentina Trujillo", "doc": "1118308019", "parentesco": "Pareja, Esposa(o)", "sexo": "F", "fecha_nac": "1997-02-22", "edad": 29, "telefono": "3176773314", "es_jefe": False},
            {"nombre": "Jesus Alberto Ruiz Sanchez", "doc": "1118303647", "parentesco": "Jefe(a) o cabeza del hogar", "sexo": "M", "fecha_nac": "1994-12-01", "edad": 31, "telefono": "3176773392", "es_jefe": True},
            {"nombre": "Ma Victoria Ruiz Trujillo", "doc": "1191224723", "parentesco": "Hijo(a), hijastro(a)", "sexo": "F", "fecha_nac": "2021-10-28", "edad": 4, "telefono": None, "es_jefe": False}
        ]
    },
    {
        "numero_rufe": "1514",
        "prioridad": "BAJA",
        "observaciones_evaluador": "Vivienda con fisura en diferentes partes.",
        "observaciones_animales": None,
        "corregimiento": None,
        "sector_barrio": "San Fernando",
        "direccion": "Calle 3 #8-03",
        "personas": [
            {"nombre": "Luis Antonio Gil", "doc": "10475491", "parentesco": "Jefe(a) o cabeza del hogar", "sexo": "M", "fecha_nac": "1940-11-10", "edad": 85, "telefono": "3143762402", "es_jefe": True},
            {"nombre": "Sandra Ines Gil", "doc": "34599440", "parentesco": "Hijo(a), hijastro(a)", "sexo": "F", "fecha_nac": "1969-01-22", "edad": 57, "telefono": "3136060902", "es_jefe": False},
            {"nombre": "Ma Flor Alvear", "doc": "1005895476", "parentesco": "Nieto(a)", "sexo": "F", "fecha_nac": "2003-07-14", "edad": 23, "telefono": "3103617474", "es_jefe": False},
            {"nombre": "Angie Marcela Alvear", "doc": "1118303146", "parentesco": "Nieto(a)", "sexo": "F", "fecha_nac": "1994-09-23", "edad": 31, "telefono": None, "es_jefe": False},
            {"nombre": "Anthony Ramirez", "doc": "1116379982", "parentesco": "Nieto(a)", "sexo": "M", "fecha_nac": "2016-06-26", "edad": 10, "telefono": None, "es_jefe": False}
        ]
    }
]

def main():
    print("Iniciando procesamiento ajustado al esquema exacto...")
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
                
                # 2. rufe_formularios (id es SERIAL, usamos RETURNING id)
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
