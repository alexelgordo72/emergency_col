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
        "numero_rufe": "1536",
        "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda Antigua de dos columnas. Paredes Fracturadas, paredes con deformacion, Piso con desplazamiento",
        "observaciones_animales": None,
        "corregimiento": None,
        "sector_barrio": None,
        "direccion": "Calle 11 No 9-45",
        "personas": [
            {"nombre": "Martha Milena Hurtado Hernandez", "doc": "67016021", "parentesco": "Jefe(a) o cabeza del hogar", "sexo": "F", "fecha_nac": "1978-05-03", "edad": 48, "telefono": "3182917094", "es_jefe": True},
            {"nombre": "Maria Victoria Hurtado Hernandez", "doc": "31974001", "parentesco": "Hermano(a), Hermanastro(a)", "sexo": "F", "fecha_nac": "1966-12-26", "edad": 59, "telefono": "3146539390", "es_jefe": False},
            {"nombre": "Oscar Marino Riascos Arias", "doc": "6531067", "parentesco": "Cuñado, Cuñada", "sexo": "M", "fecha_nac": "1965-07-04", "edad": 61, "telefono": "3113638243", "es_jefe": False},
            {"nombre": "Maria Andrea Hernandez", "doc": "1109190347", "parentesco": "Hijo(a), hijastro(a)", "sexo": "F", "fecha_nac": "2008-08-29", "edad": 18, "telefono": "3112400638", "es_jefe": False}
        ]
    },
    {
        "numero_rufe": "1537",
        "prioridad": "MEDIA",
        "observaciones_evaluador": "Vivienda de bareque presenta grietas a nivel de la union de paredes con cielo falso",
        "observaciones_animales": None,
        "corregimiento": None,
        "sector_barrio": None,
        "direccion": "cra 6 #12-03",
        "personas": [
            {"nombre": "Jakeline Alzate Quintero", "doc": "31484862", "parentesco": "Hijo(a), hijastro(a)", "sexo": "F", "fecha_nac": "1980-03-07", "edad": 46, "telefono": "3106790020", "es_jefe": False},
            {"nombre": "Ana Beiba Quintero Ramirez", "doc": "29978474", "parentesco": "Jefe(a) o cabeza del hogar", "sexo": "F", "fecha_nac": "1963-06-21", "edad": 63, "telefono": "3206516678", "es_jefe": True},
            {"nombre": "Maira Edelmira Mejia Quintero", "doc": "1118284234", "parentesco": "Hijo(a), hijastro(a)", "sexo": "F", "fecha_nac": "1986-07-23", "edad": 40, "telefono": "3157703076", "es_jefe": False},
            {"nombre": "Nilson Antonio Mejia Quintero", "doc": "1118292353", "parentesco": "Hijo(a), hijastro(a)", "sexo": "M", "fecha_nac": "1989-08-22", "edad": 37, "telefono": "3147312373", "es_jefe": False},
            {"nombre": "Daniela Zuñiga Quintero", "doc": "1118308461", "parentesco": "Nieto(a)", "sexo": "F", "fecha_nac": "1997-03-07", "edad": 29, "telefono": "3027399936", "es_jefe": False},
            {"nombre": "Eva Luna Rivera Zuñiga", "doc": "1116383713", "parentesco": "Otro pariente", "sexo": "F", "fecha_nac": "2021-05-24", "edad": 5, "telefono": "3027399936", "es_jefe": False},
            {"nombre": "Alejandro Mejia Ramirez", "doc": "1116384404", "parentesco": "Nieto(a)", "sexo": "M", "fecha_nac": "2022-06-26", "edad": 4, "telefono": "3157703076", "es_jefe": False}
        ]
    },
    {
        "numero_rufe": "1538",
        "prioridad": "MEDIA",
        "observaciones_evaluador": "Fractura del fondo de la vivienda y division de la pared fractura fuerte",
        "observaciones_animales": None,
        "corregimiento": None,
        "sector_barrio": None,
        "direccion": "Carrera 7 #12-29",
        "personas": [
            {"nombre": "Jose Leonardo Gonzalez", "doc": "14947936", "parentesco": "Jefe(a) o cabeza del hogar", "sexo": "M", "fecha_nac": "1947-12-08", "edad": 78, "telefono": "3012797637", "es_jefe": True},
            {"nombre": "Ana Celia Velasco", "doc": "31231813", "parentesco": "Pareja, Esposa(o)", "sexo": "F", "fecha_nac": "1951-08-30", "edad": 75, "telefono": "3012797637", "es_jefe": False},
            {"nombre": "Ernesto Velasco Ortiz", "doc": "14934644", "parentesco": "Cuñado, Cuñada", "sexo": "M", "fecha_nac": "1947-08-13", "edad": 79, "telefono": "3012747637", "es_jefe": False}
        ]
    },
    {
        "numero_rufe": "1539",
        "prioridad": "MEDIA",
        "observaciones_evaluador": "Fractura a nivel inferior de la pared de donde las dos habitaciones",
        "observaciones_animales": None,
        "corregimiento": None,
        "sector_barrio": None,
        "direccion": "Calle 6 #8-25",
        "personas": [
            {"nombre": "Nidia Prado", "doc": "31471888", "parentesco": "Jefe(a) o cabeza del hogar", "sexo": "F", "fecha_nac": "1964-10-02", "edad": 61, "telefono": "3176898190", "es_jefe": True},
            {"nombre": "Isabella Puente Prado", "doc": "1118310466", "parentesco": "Hijo(a), hijastro(a)", "sexo": "F", "fecha_nac": "1998-11-14", "edad": 27, "telefono": "3192528751", "es_jefe": False}
        ]
    },
    {
        "numero_rufe": "1540",
        "prioridad": "MEDIA",
        "observaciones_evaluador": "Asentamientos y grietas en baldosa.",
        "observaciones_animales": "1 Perro, 1 Gato",
        "corregimiento": None,
        "sector_barrio": "San Fernando",
        "direccion": "Calle 27 F #9-04",
        "personas": [
            {"nombre": "Luz Adriana Rivera", "doc": "29973229", "parentesco": "Jefe(a) o cabeza del hogar", "sexo": "F", "fecha_nac": "1983-10-12", "edad": 42, "telefono": "3016751241", "es_jefe": True},
            {"nombre": "Jesus David Rivera", "doc": "1192916751", "parentesco": "Hijo(a), hijastro(a)", "sexo": "M", "fecha_nac": "1999-12-24", "edad": 26, "telefono": None, "es_jefe": False},
            {"nombre": "Luis Eduardo Molano", "doc": "1116383454", "parentesco": "Hijo(a), hijastro(a)", "sexo": "M", "fecha_nac": "2010-06-16", "edad": 16, "telefono": None, "es_jefe": False},
            {"nombre": "Gabriela Molano", "doc": None, "parentesco": "Hijo(a), hijastro(a)", "sexo": "F", "fecha_nac": "2021-01-05", "edad": 5, "telefono": None, "es_jefe": False}
        ]
    },
    {
        "numero_rufe": "1541",
        "prioridad": "ALTA",
        "observaciones_evaluador": "Asentamientos, grietas en el suelo, inclinacion de la casa.",
        "observaciones_animales": "1 Gato",
        "corregimiento": None,
        "sector_barrio": "Techo Azul",
        "direccion": "Carrera 11 #1A-13",
        "personas": [
            {"nombre": "Alexander Rodallega", "doc": "1006193345", "parentesco": "Jefe(a) o cabeza del hogar", "sexo": "M", "fecha_nac": "1996-09-10", "edad": 30, "telefono": "3238494045", "es_jefe": True},
            {"nombre": "Angie Vanesa Amechea", "doc": "1007976780", "parentesco": "Pareja, Esposa(o)", "sexo": "F", "fecha_nac": "2003-11-05", "edad": 22, "telefono": "3216345133", "es_jefe": False},
            {"nombre": "Anny Alejandra Rodallega", "doc": "1116384501", "parentesco": "Hijo(a), hijastro(a)", "sexo": "F", "fecha_nac": "2022-09-17", "edad": 3, "telefono": None, "es_jefe": False}
        ]
    },
    {
        "numero_rufe": "1542",
        "prioridad": "MEDIA",
        "observaciones_evaluador": "Dificultad para desplazarse la hija y es muda.",
        "observaciones_animales": None,
        "corregimiento": None,
        "sector_barrio": "Altos Las Cruces",
        "direccion": "Calle 15 - Callejon Alto",
        "personas": [
            {"nombre": "Benito Hoyos Muñoz", "doc": "11840009", "parentesco": "Jefe(a) o cabeza del hogar", "sexo": "M", "fecha_nac": "1970-07-14", "edad": 56, "telefono": "3218016016", "es_jefe": True},
            {"nombre": "Flor Maria Díaz", "doc": "38835020", "parentesco": "Pareja, Esposa(o)", "sexo": "F", "fecha_nac": "1972-07-12", "edad": 54, "telefono": "3105194928", "es_jefe": False},
            {"nombre": "Luz Adriana Hoyos", "doc": "1118297207", "parentesco": "Hijo(a), hijastro(a)", "sexo": "F", "fecha_nac": "1983-07-26", "edad": 43, "telefono": None, "es_jefe": False}
        ]
    },
    {
        "numero_rufe": "1543",
        "prioridad": "BAJA",
        "observaciones_evaluador": "Asentamiento en el patio de la casa. Sin grietas en la estructura.",
        "observaciones_animales": "3 Perros",
        "corregimiento": None,
        "sector_barrio": "San Fernando",
        "direccion": "Carrera 9 #2-32",
        "personas": [
            {"nombre": "Karen Daniela Rivera", "doc": "1118288907", "parentesco": "Jefe(a) o cabeza del hogar", "sexo": "F", "fecha_nac": "2005-10-04", "edad": 20, "telefono": "3128182005", "es_jefe": True},
            {"nombre": "Rigoberto Rivera", "doc": None, "parentesco": "Abuelo(a)", "sexo": "M", "fecha_nac": None, "edad": None, "telefono": "3127981929", "es_jefe": False},
            {"nombre": "Manases Rivera", "doc": None, "parentesco": "Abuelo(a)", "sexo": "M", "fecha_nac": None, "edad": None, "telefono": None, "es_jefe": False}
        ]
    }
]

def main():
    print("Iniciando procesamiento de RUFEs 1536 a 1543...")
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
