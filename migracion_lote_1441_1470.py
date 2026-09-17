import psycopg2
import uuid
import re

DB_CONFIG = {
    "dbname": "comunidad_db",
    "user": "admin_comunidad",
    "password": "TuPasswordSegura2026!",
    "host": "10.147.17.24",
    "port": "5432"
}

LOTES_NUEVOS_RUFE = [
    {
        "num_formulario": "1441", "corregimiento": "Yumbo", "prioridad": "MEDIA",
        "observaciones_evaluador": "Gomez Ortiz Lucero - Afectación moderada en infraestructura física y muros (RDE-1441)[cite: 70].",
        "personas": [{"nombre": "Lucero Gomez Ortiz", "doc": "66995258", "fecha": "01/01/1980", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1442", "corregimiento": "Arroyohondo", "prioridad": "ALTA",
        "observaciones_evaluador": "Watercol S.A.S. - Daños graves en infraestructura y equipos (RDE-1442)[cite: 70].",
        "personas": [{"nombre": "Watercol S.A.S.", "doc": "901193743", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1443", "corregimiento": "San Marcos", "prioridad": "ALTA",
        "observaciones_evaluador": "Tienda Emma - Daños en infraestructura y mercancía (RDE-1443)[cite: 70].",
        "personas": [{"nombre": "Tienda Emma", "doc": "31487282", "fecha": "01/01/1980", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1444", "corregimiento": "Santa Inés", "prioridad": "ALTA",
        "observaciones_evaluador": "Fundación Escocia 2 Turismo Científico - Daños graves en estructura (RDE-1444)[cite: 70].",
        "personas": [{"nombre": "Fundación Escocia 2 Turismo Científico", "doc": "9019227231", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1445", "corregimiento": "Acopi", "prioridad": "ALTA",
        "observaciones_evaluador": "Rincón del Sabor - Daños estructurales importantes (RDE-1445)[cite: 70].",
        "personas": [{"nombre": "Rincón del Sabor", "doc": "1088589028", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1446", "corregimiento": "Agua Clara", "prioridad": "ALTA",
        "observaciones_evaluador": "Granja El Edén / Martha Liliana Maza Medina - Daños en infraestructura física (RDE-1446)[cite: 70].",
        "personas": [{"nombre": "Martha Liliana Maza Medina", "doc": "1130660054", "fecha": "01/01/1980", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1447", "corregimiento": "Yumbo", "prioridad": "ALTA",
        "observaciones_evaluador": "Industria Panificadora Frespan de Colombia S.A.S. - Daños severos en instalaciones y maquinaria (RDE-1447)[cite: 70].",
        "personas": [{"nombre": "Frespan de Colombia S.A.S.", "doc": "800085665", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1448", "corregimiento": "Acopi", "prioridad": "MEDIA",
        "observaciones_evaluador": "Vidrios de Occidente S.A.S. - Daños moderados en infraestructura e inventario (RDE-1448)[cite: 70].",
        "personas": [{"nombre": "Vidrios de Occidente S.A.S.", "doc": "805002966", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1449", "corregimiento": "Mulaló", "prioridad": "MEDIA",
        "observaciones_evaluador": "Otero Cobo Nancy - Afectaciones moderadas en acabados y muros (RDE-1449)[cite: 70].",
        "personas": [{"nombre": "Nancy Otero Cobo", "doc": "1003372446", "fecha": "01/01/1978", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1450", "corregimiento": "Yumbo", "prioridad": "MEDIA",
        "observaciones_evaluador": "Centro Skipe / Urueña Dedadillo James Antonio - Verificación completada (RDE-1450)[cite: 70].",
        "personas": [{"nombre": "James Antonio Urueña Dedadillo", "doc": "7254955", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1451", "corregimiento": "Acopi", "prioridad": "MEDIA",
        "observaciones_evaluador": "Cerdos del Valle SA - Nivel de afectación moderada (RDE-1451)[cite: 71].",
        "personas": [{"nombre": "Cerdos del Valle SA", "doc": "805018495", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1452", "corregimiento": "Fray Peña", "prioridad": "ALTA",
        "observaciones_evaluador": "La Mona de Yumbo / Natalia Chavez - Nivel de afectación crítica (RDE-1452)[cite: 71].",
        "personas": [{"nombre": "Natalia Chavez", "doc": "1006337700", "fecha": "01/01/1990", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1453", "corregimiento": "Yumbo", "prioridad": "MEDIA",
        "observaciones_evaluador": "Aluminio Nacional S.A.S. - Nivel de afectación moderada (RDE-1453)[cite: 71].",
        "personas": [{"nombre": "Aluminio Nacional S.A.S.", "doc": "890300213", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1454", "corregimiento": "Alto Dapa", "prioridad": "ALTA",
        "observaciones_evaluador": "Amarunka Kombucha - Nivel de afectación grave (RDE-1454)[cite: 71].",
        "personas": [{"nombre": "Amarunka Kombucha", "doc": "1113652479", "fecha": "01/01/1990", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1455", "corregimiento": "Acopi", "prioridad": "ALTA",
        "observaciones_evaluador": "M&M Design and Development S.A.S. - Nivel de afectación crítica (RDE-1455)[cite: 71].",
        "personas": [{"nombre": "M&M Design and Development S.A.S.", "doc": "900291680", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1456", "corregimiento": "Yumbo", "prioridad": "BAJA",
        "observaciones_evaluador": "Datecsa S.A. - Nivel de afectación baja (RDE-1456)[cite: 71].",
        "personas": [{"nombre": "Datecsa S.A.", "doc": "800136505", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1457", "corregimiento": "Yumbo", "prioridad": "ALTA",
        "observaciones_evaluador": "Protécnica Ingeniería S.A.S. - Nivel de afectación grave (RDE-1457)[cite: 71].",
        "personas": [{"nombre": "Protécnica Ingeniería S.A.S.", "doc": "890312630", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1458", "corregimiento": "Acopi", "prioridad": "MEDIA",
        "observaciones_evaluador": "Productos Varios Produvarios S.A. - Nivel de afectación moderada (RDE-1458)[cite: 71].",
        "personas": [{"nombre": "Productos Varios Produvarios S.A.", "doc": "890305586", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1459", "corregimiento": "Alto Dapa", "prioridad": "MEDIA",
        "observaciones_evaluador": "Refugio Corazones Verdes - Nivel de afectación moderada (RDE-1459)[cite: 71].",
        "personas": [{"nombre": "Refugio Corazones Verdes", "doc": "31970478", "fecha": "01/01/1980", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1460", "corregimiento": "San Marcos", "prioridad": "MEDIA",
        "observaciones_evaluador": "Julio Cortes - Nivel de afectación moderada (RDE-1460)[cite: 71].",
        "personas": [{"nombre": "Julio Cortes", "doc": "94384393", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1461", "corregimiento": "Mulaló", "prioridad": "MEDIA",
        "observaciones_evaluador": "Rapitienda el lago - Nivel de afectación moderada (RDE-1461)[cite: 72].",
        "personas": [{"nombre": "Rapitienda el lago", "doc": "29940145", "fecha": "01/01/1980", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1462", "corregimiento": "Yumbo", "prioridad": "BAJA",
        "observaciones_evaluador": "Lake Roof Top - Sin clasificación (RDE-1462)[cite: 72].",
        "personas": [{"nombre": "Lake Roof Top", "doc": "1130637019", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1463", "corregimiento": "Uribe", "prioridad": "BAJA",
        "observaciones_evaluador": "Verde Vital / Andrea Ximena - Nivel de afectación baja (RDE-1463)[cite: 72].",
        "personas": [{"nombre": "Andrea Ximena", "doc": "1118305951", "fecha": "01/01/1990", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1464", "corregimiento": "Acopi", "prioridad": "BAJA",
        "observaciones_evaluador": "ACL Logística S.A.S. - Sin clasificación (RDE-1464)[cite: 72].",
        "personas": [{"nombre": "ACL Logística S.A.S.", "doc": "900423131", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1465", "corregimiento": "Dapa", "prioridad": "BAJA",
        "observaciones_evaluador": "Ostinatto S.A.S. - Nivel de afectación baja (RDE-1465)[cite: 72].",
        "personas": [{"nombre": "Ostinatto S.A.S.", "doc": "1151951437", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1466", "corregimiento": "Yumbo", "prioridad": "ALTA",
        "observaciones_evaluador": "Kitovanny Medina Cortos - Nivel de afectación grave (RDE-1466)[cite: 72].",
        "personas": [{"nombre": "Kitovanny Medina Cortos", "doc": "902074328", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1467", "corregimiento": "Panorama", "prioridad": "ALTA",
        "observaciones_evaluador": "Andrea Garez Agencia Publicidad - Nivel de afectación grave (RDE-1467)[cite: 72].",
        "personas": [{"nombre": "Andrea Garez Agencia Publicidad", "doc": "1113537936", "fecha": "01/01/1985", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1468", "corregimiento": "Las Vegas", "prioridad": "ALTA",
        "observaciones_evaluador": "Establecimiento Las Vegas - Nivel de afectación grave (RDE-1468)[cite: 72].",
        "personas": [{"nombre": "Establecimiento Las Vegas", "doc": "1151947949", "fecha": "01/01/1990", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1469", "corregimiento": "Yumbo", "prioridad": "ALTA",
        "observaciones_evaluador": "Yuliana Balanta - Nivel de afectación grave (RDE-1469)[cite: 72].",
        "personas": [{"nombre": "Yuliana Balanta", "doc": "901641980", "fecha": "01/01/1980", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1470", "corregimiento": "Las Cruces", "prioridad": "BAJA",
        "observaciones_evaluador": "EDE Comunicaciones - Sin clasificación (RDE-1470)[cite: 72].",
        "personas": [{"nombre": "EDE Comunicaciones", "doc": "901790097", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    }
]

def obtener_grupo_poblacional(edad):
    if edad is None: return "Sin Registro"
    if edad <= 14: return "1. Primera Infancia y Niños (0-14)"
    elif edad <= 28: return "2. Jóvenes (15-28)"
    elif edad <= 59: return "3. Adultos (29-59)"
    else: return "4. Adultos Mayores (60+)"

def calcular_edad_2026(fecha_str):
    match = re.search(r'(19\d{2}|20\d{2})', str(fecha_str))
    if match: return 2026 - int(match.group(1))
    return None

def main():
    print("Iniciando ENRIQUECIMIENTO FINAL Lote 1441-1470...")
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        conn.autocommit = True
        cur = conn.cursor()
        
        cur.execute("ALTER TABLE public.rufe_personas ADD COLUMN IF NOT EXISTS grupo_poblacional VARCHAR(50);")
        
        formularios_creados, formularios_actualizados = 0, 0
        personas_creadas, personas_actualizadas = 0, 0
        
        cur.execute("SELECT id FROM public.reportes_comunitarios LIMIT 1;")
        res_reporte = cur.fetchone()
        
        if not res_reporte:
            reporte_id = str(uuid.uuid4())
            cur.execute("INSERT INTO public.reportes_comunitarios (id, activo) VALUES (%s, true) ON CONFLICT DO NOTHING;", (reporte_id,))
        else:
            reporte_id = res_reporte[0]
            
        for form in LOTES_NUEVOS_RUFE:
            num_limpio = form["num_formulario"].lstrip('0')
            
            cur.execute("SELECT id FROM public.rufe_formularios WHERE numero_formulario = %s", (num_limpio,))
            resultado = cur.fetchone()
            
            if resultado:
                form_id = resultado[0]
                cur.execute("""
                    UPDATE public.rufe_formularios 
                    SET prioridad = %s, observaciones_evaluador = %s WHERE id = %s;
                """, (form["prioridad"], form["observaciones_evaluador"], form_id))
                formularios_actualizados += 1
            else:
                cur.execute("""
                    INSERT INTO public.rufe_formularios 
                    (reporte_id, numero_formulario, corregimiento, prioridad, observaciones_evaluador)
                    VALUES (%s, %s, %s, %s, %s) RETURNING id;
                """, (reporte_id, num_limpio, form["corregimiento"], form["prioridad"], form["observaciones_evaluador"]))
                form_id = cur.fetchone()[0]
                formularios_creados += 1
                
            for p in form["personas"]:
                if p["doc"] == "0": continue
                edad_calc = calcular_edad_2026(p["fecha"])
                grupo_pob = obtener_grupo_poblacional(edad_calc)
                
                cur.execute("SELECT id FROM public.rufe_personas WHERE REPLACE(documento_identidad, '.', '') = %s", (p["doc"],))
                res_persona = cur.fetchone()
                
                if res_persona:
                    persona_id = res_persona[0]
                    cur.execute("""
                        UPDATE public.rufe_personas 
                        SET fecha_nacimiento = %s, edad = %s, es_jefe_hogar = %s, parentesco = %s, sexo = %s, etnia = %s, grupo_poblacional = %s
                        WHERE id = %s;
                    """, (p["fecha"], edad_calc, p["es_jefe"], p["parentesco"], p["sexo"], p["etnia"], grupo_pob, persona_id))
                    personas_actualizadas += 1
                else:
                    cur.execute("""
                        INSERT INTO public.rufe_personas 
                        (rufe_formulario_id, nombre_completo, documento_identidad, fecha_nacimiento, edad, es_jefe_hogar, parentesco, sexo, etnia, grupo_poblacional)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (form_id, p["nombre"], p["doc"], p["fecha"], edad_calc, p["es_jefe"], p["parentesco"], p["sexo"], p["etnia"], grupo_pob))
                    personas_creadas += 1

        print(f"\n==================================================")
        print(f"MIGRACIÓN LOTE 1441-1470 EXITOSA.")
        print(f"Formularios -> Creados: {formularios_creados} | Actualizados: {formularios_actualizados}")
        print(f"Personas    -> Insertadas: {personas_creadas} | Actualizadas: {personas_actualizadas}")
        print(f"==================================================")
        
    except Exception as e:
        print(f"Error en BD: {e}")
    finally:
        if 'conn' in locals(): cur.close(); conn.close()

if __name__ == "__main__":
    main()
