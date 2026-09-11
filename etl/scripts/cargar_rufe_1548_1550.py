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
        "numero_rufe": "1548",
        "prioridad": "MEDIA",
        "observaciones_evaluador": "Vivienda de hace aproximadamente unos 55 años construida. La unica afectación que en el cielo razo que elaborado esterilla y arena. El cual sufrio afectacion y esta sostenido con guaduas y tablas. La señora Carmen tiene discapacidad. Patria Enriquez.",
        "observaciones_animales": None,
        "corregimiento": None,
        "sector_barrio": "Bolivar",
        "direccion": "Calle 12 #5-26",
        "personas": [
            {"nombre": "Elizabeth Martinez", "doc": "38437032", "parentesco": "Jefe(a) o cabeza del hogar", "sexo": "F", "fecha_nac": "1956-03-23", "edad": 70, "telefono": "3225156603", "es_jefe": True},
            {"nombre": "Eduardo Jesus Viña Solis", "doc": "5497024", "parentesco": "Pareja, Esposa(o)", "sexo": "M", "fecha_nac": "1967-05-11", "edad": 59, "telefono": "3225156608", "es_jefe": False},
            {"nombre": "Carmen Vivas Martinez", "doc": "31474269", "parentesco": "Hermano(a), Hermanastro(a)", "sexo": "F", "fecha_nac": "1963-08-14", "edad": 63, "telefono": None, "es_jefe": False},
            {"nombre": "Diego Fernando Delgado", "doc": "16457588", "parentesco": "Hijo(a), hijastro(a)", "sexo": "M", "fecha_nac": "1974-03-23", "edad": 52, "telefono": None, "es_jefe": False}
        ]
    },
    {
        "numero_rufe": "1549",
        "prioridad": "MEDIA",
        "observaciones_evaluador": "Observacion Jose Daniel: Vivienda de 2 pisos con fisuras muros por posible asentamiento. Requiere evaluacion ing. estructural reforzamiento. Carlos Cobo.",
        "observaciones_animales": None,
        "corregimiento": None,
        "sector_barrio": "Estancia Vieja",
        "direccion": "Calle 21 #12-22",
        "personas": [
            {"nombre": "Jose Daniel Basto Alvarez", "doc": "219208", "parentesco": "Jefe(a) o cabeza del hogar", "sexo": "M", "fecha_nac": "1955-11-26", "edad": 70, "telefono": "3135506572", "es_jefe": True},
            {"nombre": "Rosa Maria Yangel", "doc": "28253958", "parentesco": "Pareja, Esposa(o)", "sexo": "F", "fecha_nac": "1956-12-03", "edad": 69, "telefono": "3159178325", "es_jefe": False}
        ]
    },
    {
        "numero_rufe": "1550",
        "prioridad": "MEDIA",
        "observaciones_evaluador": "Observacion Ever: Vivienda de 1 piso con fisuras muros 2 pisos. Requiere visita ing. estructural para reforzamiento. Carlos Cobo.",
        "observaciones_animales": None,
        "corregimiento": None,
        "sector_barrio": "La Estancia",
        "direccion": "Carrera 13B #24-61",
        "personas": [
            {"nombre": "Jose Ever Reyes Lerma", "doc": "14974969", "parentesco": "Jefe(a) o cabeza del hogar", "sexo": "M", "fecha_nac": "1952-03-05", "edad": 74, "telefono": "3117380139", "es_jefe": True},
            {"nombre": "Berta Arango Londoño", "doc": "29680718", "parentesco": "Pareja, Esposa(o)", "sexo": "F", "fecha_nac": "1946-09-28", "edad": 79, "telefono": "3116102260", "es_jefe": False}
        ]
    }
]

def main():
    print("Iniciando procesamiento de RUFEs 1548 a 1550...")
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
