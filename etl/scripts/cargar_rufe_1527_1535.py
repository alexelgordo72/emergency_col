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
        "numero_rufe": "1527",
        "prioridad": "MEDIA",
        "observaciones_evaluador": "Señora ana livia padece de Polineuropatia de fibras pequeñas. Deficit de memoria.",
        "observaciones_animales": None,
        "corregimiento": None,
        "sector_barrio": "Bolivar",
        "direccion": "Calle 13 2-22",
        "personas": [
            {"nombre": "Pedro Luis Patiño", "doc": "7248997", "parentesco": "Jefe(a) o cabeza del hogar", "sexo": "M", "fecha_nac": "1961-03-07", "edad": 65, "telefono": "3136160523", "es_jefe": True},
            {"nombre": "Ana Livia Carvajal", "doc": "29940543", "parentesco": "Pareja, Esposa(o)", "sexo": "F", "fecha_nac": "1972-02-05", "edad": 54, "telefono": "3103755904", "es_jefe": False},
            {"nombre": "Belen Acevedo", "doc": "1116378015", "parentesco": "Hijo(a), hijastro(a)", "sexo": "F", "fecha_nac": "2014-02-26", "edad": 12, "telefono": None, "es_jefe": False}
        ]
    },
    {
        "numero_rufe": "1528",
        "prioridad": "MEDIA",
        "observaciones_evaluador": "Se realiza reparación de tejado por cuenta propia, aun existe riesgo con pared vecina.",
        "observaciones_animales": None,
        "corregimiento": None,
        "sector_barrio": "Bolivar",
        "direccion": "Cra 4 13-61",
        "personas": [
            {"nombre": "Gustavo Aparicio", "doc": "78015130", "parentesco": "Jefe(a) o cabeza del hogar", "sexo": "M", "fecha_nac": "1952-11-14", "edad": 73, "telefono": "3124074802", "es_jefe": True},
            {"nombre": "Viviana Aparicio", "doc": "1118291190", "parentesco": "Hijo(a), hijastro(a)", "sexo": "F", "fecha_nac": "1989-04-06", "edad": 37, "telefono": "3167479456", "es_jefe": False},
            {"nombre": "Santiago Hurtado A.", "doc": "1232831867", "parentesco": "Nieto(a)", "sexo": "M", "fecha_nac": "2024-05-22", "edad": 2, "telefono": None, "es_jefe": False},
            {"nombre": "Luana Hurtado A.", "doc": "1232805699", "parentesco": "Nieto(a)", "sexo": "F", "fecha_nac": "2018-08-04", "edad": 8, "telefono": None, "es_jefe": False},
            {"nombre": "Manuela Arteaga", "doc": "30060087", "parentesco": "Pareja, Esposa(o)", "sexo": "F", "fecha_nac": "1960-04-02", "edad": 66, "telefono": "3113334621", "es_jefe": False}
        ]
    },
    {
        "numero_rufe": "1529",
        "prioridad": "ALTA",
        "observaciones_evaluador": "Vecina de edificio de 5 pisos con averia estructural, a punto de colapsar.",
        "observaciones_animales": None,
        "corregimiento": None,
        "sector_barrio": "Bolivar",
        "direccion": "Calle 12 No 4-18",
        "personas": [
            {"nombre": "Piedad Muñoz Pizarro", "doc": "31940003", "parentesco": "Jefe(a) o cabeza del hogar", "sexo": "F", "fecha_nac": "1965-09-05", "edad": 61, "telefono": "3226585613", "es_jefe": True}
        ]
    },
    {
        "numero_rufe": "1530",
        "prioridad": "MEDIA",
        "observaciones_evaluador": "Casa habitada por adultos mayores Cielorazo de esterilla y cemento Averiados. Fisura en una columna de lado izquierdo",
        "observaciones_animales": None,
        "corregimiento": None,
        "sector_barrio": "Bolivar",
        "direccion": "Calle 12 No 5-26",
        "personas": [
            {"nombre": "Elizabeth Martinez Galarza", "doc": "38437032", "parentesco": "Jefe(a) o cabeza del hogar", "sexo": "F", "fecha_nac": "1956-03-23", "edad": 70, "telefono": "3225156603", "es_jefe": True},
            {"nombre": "Edvardo Viña Solis", "doc": "5497024", "parentesco": "Pareja, Esposa(o)", "sexo": "M", "fecha_nac": "1967-05-11", "edad": 59, "telefono": "3225156608", "es_jefe": False},
            {"nombre": "Diego Delgado Martinez", "doc": "1457588", "parentesco": "Hijo(a), hijastro(a)", "sexo": "M", "fecha_nac": "1974-03-23", "edad": 52, "telefono": "3156399893", "es_jefe": False},
            {"nombre": "Oliva Martinez Galarza", "doc": "31474269", "parentesco": "Hermano(a), Hermanastro(a)", "sexo": "F", "fecha_nac": "1963-08-14", "edad": 63, "telefono": None, "es_jefe": False}
        ]
    },
    {
        "numero_rufe": "1531",
        "prioridad": "MEDIA",
        "observaciones_evaluador": "Segundo piso, Pared exterior averiada Fracturada.",
        "observaciones_animales": None,
        "corregimiento": None,
        "sector_barrio": "Bolivar",
        "direccion": "Calle 12 No 4-26",
        "personas": [
            {"nombre": "Veryined Zuleta Muñoz", "doc": "31478358", "parentesco": "Jefe(a) o cabeza del hogar", "sexo": "F", "fecha_nac": "1975-11-29", "edad": 50, "telefono": "3154427266", "es_jefe": True},
            {"nombre": "Neffer Sofi Zuleta Muñoz", "doc": "1031629497", "parentesco": "Hermano(a), Hermanastro(a)", "sexo": "F", "fecha_nac": "1969-12-27", "edad": 56, "telefono": "3168661605", "es_jefe": False}
        ]
    },
    {
        "numero_rufe": "1532",
        "prioridad": "ALTA",
        "observaciones_evaluador": "Parapeto Fracturado, habitacion que corre riesgo de colapsar",
        "observaciones_animales": None,
        "corregimiento": None,
        "sector_barrio": "Bolivar",
        "direccion": "Calle 12 No 4-47",
        "personas": [
            {"nombre": "Edeniver Pabon Astudillo", "doc": "31467264", "parentesco": "Jefe(a) o cabeza del hogar", "sexo": "F", "fecha_nac": "1958-07-12", "edad": 68, "telefono": "3136180119", "es_jefe": True},
            {"nombre": "Miriam Pabon Astudillo", "doc": "31468661", "parentesco": "Hermano(a), Hermanastro(a)", "sexo": "F", "fecha_nac": "1962-08-16", "edad": 64, "telefono": "3127546458", "es_jefe": False},
            {"nombre": "Maira Aldana", "doc": None, "parentesco": "Otro no pariente", "sexo": "F", "fecha_nac": None, "edad": None, "telefono": "3136180119", "es_jefe": False}
        ]
    },
    {
        "numero_rufe": "1533",
        "prioridad": "ALTA",
        "observaciones_evaluador": "Casa Parcialmente colapsada. Parte delantera, habitacion (2) Sala comedor",
        "observaciones_animales": None,
        "corregimiento": None,
        "sector_barrio": "Bolivar",
        "direccion": "Calle 12 No 4-53",
        "personas": [
            {"nombre": "Maria del Pilar Wuman Orejuela", "doc": "31924694", "parentesco": "Jefe(a) o cabeza del hogar", "sexo": "F", "fecha_nac": "1962-11-13", "edad": 63, "telefono": "3225240376", "es_jefe": True},
            {"nombre": "Henry Alberto Pachajoa Erazo", "doc": "16448955", "parentesco": "Pareja, Esposa(o)", "sexo": "M", "fecha_nac": "1960-01-05", "edad": 66, "telefono": "3222540376", "es_jefe": False},
            {"nombre": "Cristhian Pachajoa Wuman", "doc": "1144207930", "parentesco": "Hijo(a), hijastro(a)", "sexo": "M", "fecha_nac": "1998-09-18", "edad": 27, "telefono": "3222540370", "es_jefe": False}
        ]
    },
    {
        "numero_rufe": "1534",
        "prioridad": "MEDIA",
        "observaciones_evaluador": "Piso levantado, Pared de habitacion agrietada en el marco de puerta. Cuarto trasero Paredes agrietadas",
        "observaciones_animales": None,
        "corregimiento": None,
        "sector_barrio": "Bolivar",
        "direccion": "Calle 12 No 3-68",
        "personas": [
            {"nombre": "Rubiela Astudiza Zambrano", "doc": "31956442", "parentesco": "Jefe(a) o cabeza del hogar", "sexo": "F", "fecha_nac": "1966-11-16", "edad": 59, "telefono": "304592564", "es_jefe": True},
            {"nombre": "Diana Marcela Polanco Astudiza", "doc": "1118304990", "parentesco": "Hijo(a), hijastro(a)", "sexo": "F", "fecha_nac": "1995-08-14", "edad": 31, "telefono": "3002404539", "es_jefe": False},
            {"nombre": "Juan Jose Astudiza Zambrano", "doc": None, "parentesco": "Hijo(a), hijastro(a)", "sexo": "M", "fecha_nac": "1999-04-10", "edad": 27, "telefono": "3054276764", "es_jefe": False}
        ]
    },
    {
        "numero_rufe": "1535",
        "prioridad": "ALTA",
        "observaciones_evaluador": "Techo a punto de colapsarde Tejas y esterilla Piso levantado, Pared Fracturada en el Cuarto de atras.",
        "observaciones_animales": None,
        "corregimiento": None,
        "sector_barrio": "Bolivar",
        "direccion": "Calle 12 No 2-37",
        "personas": [
            {"nombre": "Sandra Eugenia Zamora Franco", "doc": "31998022", "parentesco": "Jefe(a) o cabeza del hogar", "sexo": "F", "fecha_nac": "1969-08-04", "edad": 57, "telefono": "3234534304", "es_jefe": True},
            {"nombre": "Ingrid Juliana Urrea Zamora", "doc": "1193075537", "parentesco": "Hijo(a), hijastro(a)", "sexo": "F", "fecha_nac": "2001-12-10", "edad": 24, "telefono": "3234534701", "es_jefe": False}
        ]
    }
]

def main():
    print("Iniciando procesamiento de RUFEs 1527 a 1535...")
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
