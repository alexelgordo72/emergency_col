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
        "numero_rufe": "1520",
        "prioridad": "ALTA",
        "observaciones_evaluador": "La casa esta la diando en las pieza y el baño ta to pory el terreno sedio, tiene fisuras en el piso",
        "observaciones_animales": None,
        "corregimiento": None,
        "sector_barrio": "Cruces",
        "direccion": "mall N 1A 13",
        "personas": [
            {"nombre": "Aally vanese Riasco", "doc": "1007976780", "parentesco": "Jefe(a) o cabeza del hogar", "sexo": "F", "fecha_nac": "2003-11-05", "edad": 22, "telefono": "3216345133", "es_jefe": True},
            {"nombre": "Alexander rodallega", "doc": "1006193345", "parentesco": "Pareja, Esposa(o)", "sexo": "M", "fecha_nac": "1996-09-10", "edad": 30, "telefono": "3238494045", "es_jefe": False},
            {"nombre": "Amy alejandra rodallega", "doc": "1116384501", "parentesco": "Hijo(a), hijastro(a)", "sexo": "F", "fecha_nac": "2022-09-17", "edad": 3, "telefono": None, "es_jefe": False}
        ]
    },
    {
        "numero_rufe": "1521",
        "prioridad": "ALTA",
        "observaciones_evaluador": "La casa es de Madera las guaduas se parteeron el piso se rajo en la cosina huso un derruba le daño el meson parte de las paredes clapso",
        "observaciones_animales": None,
        "corregimiento": None,
        "sector_barrio": "Cruces Alto",
        "direccion": "calle 1 1A06",
        "personas": [
            {"nombre": "gloria amparo Marin Arias", "doc": "31966255", "parentesco": "Jefe(a) o cabeza del hogar", "sexo": "F", "fecha_nac": "1966-01-15", "edad": 60, "telefono": "3207221588", "es_jefe": True},
            {"nombre": "Jhon brando Marin Arias", "doc": None, "parentesco": "Hijo(a), hijastro(a)", "sexo": "M", "fecha_nac": None, "edad": None, "telefono": None, "es_jefe": False}
        ]
    },
    {
        "numero_rufe": "1522",
        "prioridad": "MEDIA ALTA",
        "observaciones_evaluador": "Prioridad: MEDIA ALTA",
        "observaciones_animales": None,
        "corregimiento": None,
        "sector_barrio": "Carlos León Pizarro",
        "direccion": "Calle 13C #15N-63",
        "personas": [
            {"nombre": "Robinson Sanchez Campazano", "doc": "94314546", "parentesco": "Jefe(a) o cabeza del hogar", "sexo": "M", "fecha_nac": "1971-09-22", "edad": 54, "telefono": "3104096731", "es_jefe": True},
            {"nombre": "Patricia Acero paz", "doc": "31534709", "parentesco": "Pareja, Esposa(o)", "sexo": "F", "fecha_nac": "1974-08-03", "edad": 52, "telefono": "3127257502", "es_jefe": False},
            {"nombre": "Lina Marcela Sánchez Acero", "doc": "1118303060", "parentesco": "Hijo(a), hijastro(a)", "sexo": "F", "fecha_nac": "1994-09-18", "edad": 31, "telefono": "3125073221", "es_jefe": False}
        ]
    },
    {
        "numero_rufe": "1523",
        "prioridad": "ALTA",
        "observaciones_evaluador": "Prioridad: ALTA",
        "observaciones_animales": None,
        "corregimiento": None,
        "sector_barrio": "Pizarro",
        "direccion": "Calle 13 CN #15N 76",
        "personas": [
            {"nombre": "Alexander Castillo Collazos", "doc": "16403939", "parentesco": "Jefe(a) o cabeza del hogar", "sexo": "M", "fecha_nac": "1972-05-06", "edad": 54, "telefono": "3168010596", "es_jefe": True},
            {"nombre": "Nancy Elizabeth Maldonado", "doc": None, "parentesco": "Pareja, Esposa(o)", "sexo": "F", "fecha_nac": "1962-05-21", "edad": 64, "telefono": "3168010596", "es_jefe": False}
        ]
    },
    {
        "numero_rufe": "1524",
        "prioridad": "ALTA",
        "observaciones_evaluador": "Prioridad: Alta.",
        "observaciones_animales": None,
        "corregimiento": None,
        "sector_barrio": "Pizarro",
        "direccion": "Calle 13 CN #15N 57",
        "personas": [
            {"nombre": "Robiel Guerrero Serna", "doc": "6252233", "parentesco": "Jefe(a) o cabeza del hogar", "sexo": "M", "fecha_nac": "1960-08-14", "edad": 66, "telefono": "3158139604", "es_jefe": True},
            {"nombre": "Luz Stella Garzón Henao", "doc": "29827151", "parentesco": "Pareja, Esposa(o)", "sexo": "F", "fecha_nac": "1964-12-02", "edad": 61, "telefono": "3183182310", "es_jefe": False},
            {"nombre": "Nadia Fernanda Guerrero Garzón", "doc": "1118302174", "parentesco": "Hijo(a), hijastro(a)", "sexo": "F", "fecha_nac": "1994-04-13", "edad": 32, "telefono": "3156106371", "es_jefe": False},
            {"nombre": "Celeste Collautes Garzón", "doc": "1118313604", "parentesco": "Nieto(a)", "sexo": "F", "fecha_nac": "2023-09-22", "edad": 2, "telefono": "3004222417", "es_jefe": False},
            {"nombre": "María del Carmen Collautes Garzón", "doc": "1094896818", "parentesco": "Hijo(a), hijastro(a)", "sexo": "F", "fecha_nac": "2005-12-07", "edad": 20, "telefono": "3004222417", "es_jefe": False}
        ]
    },
    {
        "numero_rufe": "1525",
        "prioridad": "ALTA",
        "observaciones_evaluador": "Casa es en lata y esterilla, techo de zinc con estructura de guadua y plastico",
        "observaciones_animales": None,
        "corregimiento": None,
        "sector_barrio": "San Fernando",
        "direccion": "cra 9 este - Calle 3",
        "personas": [
            {"nombre": "Maria Edilia Gonzalez", "doc": "29432540", "parentesco": "Jefe(a) o cabeza del hogar", "sexo": "F", "fecha_nac": "1958-05-15", "edad": 68, "telefono": "3171626815", "es_jefe": True}
        ]
    },
    {
        "numero_rufe": "1526",
        "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda de 2 pisos con afectacion grave de fisuras en muros, casa construida sin ningun confinamiento estructural con riesgo alto por colapso. Se recomienda evaluación estructural de especialista para definir reforzamiento o demolición de la vivienda. La presente visita es de tipo ocular preliminar.",
        "observaciones_animales": None,
        "corregimiento": None,
        "sector_barrio": "San Fernando",
        "direccion": "Calle 2 #31-A67",
        "personas": [
            {"nombre": "efrain marquez reyes", "doc": "6207695", "parentesco": "Jefe(a) o cabeza del hogar", "sexo": "M", "fecha_nac": "1966-01-09", "edad": 60, "telefono": "3148180470", "es_jefe": True},
            {"nombre": "Sorangela", "doc": "39564700", "parentesco": "Pareja, Esposa(o)", "sexo": "F", "fecha_nac": "1969-12-10", "edad": 56, "telefono": "3053521806", "es_jefe": False}
        ]
    }
]

def main():
    print("Iniciando procesamiento de RUFEs 1520 a 1526...")
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
