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
        "numero_rufe": "1515",
        "prioridad": "MEDIA",
        "observaciones_evaluador": "La Casa Presenta algunos daños estructurales, derrumbe por rocas 4 techo averiado, Fisuras y daño de su cocina por culpa del deslizamiento",
        "observaciones_animales": None,
        "corregimiento": None,
        "sector_barrio": "Nuevo Horizonte",
        "direccion": None,
        "personas": [
            {"nombre": "Luz Melida Campo", "doc": "34797382", "parentesco": "Jefe(a) o cabeza del hogar", "sexo": "F", "fecha_nac": "1979-06-30", "edad": 47, "telefono": "3232523139", "es_jefe": True},
            {"nombre": "Arneyo Deless Hernandez", "doc": "1148800032", "parentesco": "Hijo(a), hijastro(a)", "sexo": "F", "fecha_nac": "1950-07-18", "edad": 76, "telefono": "3225530554", "es_jefe": False}
        ]
    },
    {
        "numero_rufe": "1516",
        "prioridad": "MEDIA",
        "observaciones_evaluador": "La casa tuvo algunas afectaciones y fisuras parte de la pared se despego y afectacion en una columna del segundo piso",
        "observaciones_animales": None,
        "corregimiento": None,
        "sector_barrio": "Nuevo Horizonte",
        "direccion": None,
        "personas": [
            {"nombre": "Mayra Rosalba Casamachin", "doc": "1118303024", "parentesco": "Jefe(a) o cabeza del hogar", "sexo": "F", "fecha_nac": "1994-01-23", "edad": 32, "telefono": "3206605910", "es_jefe": True},
            {"nombre": "Carlos Enrique Valdes", "doc": "1118300406", "parentesco": "Pareja, Esposa(o)", "sexo": "M", "fecha_nac": "1993-05-10", "edad": 33, "telefono": "3207301496", "es_jefe": False},
            {"nombre": "Hilary Sofia Valdes Casamachin", "doc": "1116376314", "parentesco": "Hijo(a), hijastro(a)", "sexo": "F", "fecha_nac": "2018-10-23", "edad": 7, "telefono": None, "es_jefe": False},
            {"nombre": "Elkin Dario Pescador", "doc": "71940806", "parentesco": "Padre, Madre, Suegro, Suegra", "sexo": "M", "fecha_nac": "1971-10-28", "edad": 54, "telefono": None, "es_jefe": False},
            {"nombre": "Diago Palomino", "doc": "6091079", "parentesco": "Padre, Madre, Suegro, Suegra", "sexo": "M", "fecha_nac": "1941-10-23", "edad": 84, "telefono": "3205664356", "es_jefe": False}
        ]
    },
    {
        "numero_rufe": "1517",
        "prioridad": "MEDIA",
        "observaciones_evaluador": "Al revisar la casa la parte de al frente resulto afectada, colapso. Algunas partes resultaron afectadas hubo un pequeño derrumbe al caerse la parte frontal de la vivienda.",
        "observaciones_animales": None,
        "corregimiento": None,
        "sector_barrio": "Nuevo Horizonte",
        "direccion": None,
        "personas": [
            {"nombre": "Michael Brayden Obando", "doc": "1148309796", "parentesco": "Jefe(a) o cabeza del hogar", "sexo": "M", "fecha_nac": "1998-05-01", "edad": 28, "telefono": "3117800647", "es_jefe": True},
            {"nombre": "Marelyn Ortega", "doc": "1118084791", "parentesco": "Pareja, Esposa(o)", "sexo": "F", "fecha_nac": "1999-05-23", "edad": 27, "telefono": None, "es_jefe": False},
            {"nombre": "Violet Obando", "doc": "1146381328", "parentesco": "Hijo(a), hijastro(a)", "sexo": "F", "fecha_nac": None, "edad": None, "telefono": None, "es_jefe": False}
        ]
    },
    {
        "numero_rufe": "1518",
        "prioridad": "MEDIA",
        "observaciones_evaluador": "Grietas cerca a la tuberia de gas y diferentes grietas en varios lugares de la casa",
        "observaciones_animales": None,
        "corregimiento": None,
        "sector_barrio": "La Trinidad",
        "direccion": None,
        "personas": [
            {"nombre": "Alexis Bedoya", "doc": "16458693", "parentesco": "Jefe(a) o cabeza del hogar", "sexo": "M", "fecha_nac": "1979-07-28", "edad": 47, "telefono": "3053259215", "es_jefe": True},
            {"nombre": "Yaritza Palacios", "doc": "4863890", "parentesco": "Pareja, Esposa(o)", "sexo": "F", "fecha_nac": "1988-06-27", "edad": 38, "telefono": "3152858138", "es_jefe": False},
            {"nombre": "Hornadys Palacio", "doc": "6467834", "parentesco": "Hijo(a), hijastro(a)", "sexo": "F", "fecha_nac": "2016-12-25", "edad": 9, "telefono": None, "es_jefe": False}
        ]
    },
    {
        "numero_rufe": "1519",
        "prioridad": "MEDIA",
        "observaciones_evaluador": "Vivienda de 2 pisos, segundo piso averiado escaleras externas afectadas",
        "observaciones_animales": None,
        "corregimiento": None,
        "sector_barrio": "San Fernando",
        "direccion": "Calle 2A #8-36",
        "personas": [
            {"nombre": "Marlon Stevan Sandoval", "doc": "1118288376", "parentesco": "Jefe(a) o cabeza del hogar", "sexo": "M", "fecha_nac": "1987-03-03", "edad": 39, "telefono": "3166349598", "es_jefe": True},
            {"nombre": "Yesenica Bolaños", "doc": "1118288140", "parentesco": "Pareja, Esposa(o)", "sexo": "F", "fecha_nac": "1988-12-20", "edad": 37, "telefono": "3105174088", "es_jefe": False},
            {"nombre": "Sharick Sandoval", "doc": "1116377948", "parentesco": "Hijo(a), hijastro(a)", "sexo": "F", "fecha_nac": "2016-01-22", "edad": 10, "telefono": None, "es_jefe": False},
            {"nombre": "Juan Stevan Sandoval", "doc": "1116380266", "parentesco": "Hijo(a), hijastro(a)", "sexo": "M", "fecha_nac": "2014-10-26", "edad": 11, "telefono": None, "es_jefe": False}
        ]
    }
]

def main():
    print("Iniciando procesamiento de RUFEs 1515 a 1519...")
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
