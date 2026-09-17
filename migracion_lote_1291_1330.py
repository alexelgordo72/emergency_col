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
        "num_formulario": "1291", "corregimiento": "Bolívar", "prioridad": "ALTA",
        "observaciones_evaluador": "La trastienda del bolivar - Restaurante, nivel de afectación crítica (RDE-1291)[cite: 55].",
        "personas": [{"nombre": "La trastienda del bolivar", "doc": "43902864", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1292", "corregimiento": "San Marcos", "prioridad": "ALTA",
        "observaciones_evaluador": "Finca La Ceiba - Nivel de afectación crítica (RDE-1292)[cite: 55].",
        "personas": [{"nombre": "Finca La Ceiba", "doc": "1125080311", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1293", "corregimiento": "Acopi", "prioridad": "ALTA",
        "observaciones_evaluador": "Importline S.A.S. - Nivel de afectación crítica (RDE-1293)[cite: 55].",
        "personas": [{"nombre": "Importline S.A.S.", "doc": "900115249", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1294", "corregimiento": "Arroyohondo", "prioridad": "ALTA",
        "observaciones_evaluador": "Servigrafic S.A.S. - Nivel de afectación grave (RDE-1294)[cite: 55].",
        "personas": [{"nombre": "Servigrafic S.A.S.", "doc": "8903233096", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1295", "corregimiento": "Cencar", "prioridad": "ALTA",
        "observaciones_evaluador": "Transportes Especializados Rodrigo Tenorio Rivera Ltda - Nivel de afectación grave (RDE-1295)[cite: 55].",
        "personas": [{"nombre": "Transportes Especializados Rodrigo Tenorio Rivera", "doc": "8913045980", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1296", "corregimiento": "Acopi", "prioridad": "ALTA",
        "observaciones_evaluador": "Autosuperior S.A.S. - Nivel de afectación grave (RDE-1296)[cite: 55].",
        "personas": [{"nombre": "Autosuperior S.A.S.", "doc": "800029569", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1297", "corregimiento": "Acopi", "prioridad": "MEDIA",
        "observaciones_evaluador": "Vidrios Templados de Occidente S.A.S. - Nivel de afectación moderada (RDE-1297)[cite: 55].",
        "personas": [{"nombre": "Vidrios Templados de Occidente S.A.S.", "doc": "805002966", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1298", "corregimiento": "Yumbillo", "prioridad": "MEDIA",
        "observaciones_evaluador": "Rodriguez Enciso Gloria Jenny - Nivel de afectación moderada (RDE-1298)[cite: 55].",
        "personas": [{"nombre": "Gloria Jenny Rodriguez Enciso", "doc": "1136059778", "fecha": "01/01/1980", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1299", "corregimiento": "Yumbo", "prioridad": "ALTA",
        "observaciones_evaluador": "Organización Colombiana de la Niñez Desprotegida - Nivel de afectación grave (RDE-1299)[cite: 55].",
        "personas": [{"nombre": "Organización Colombiana de la Niñez Desprotegida", "doc": "805025899", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1300", "corregimiento": "Yumbo", "prioridad": "ALTA",
        "observaciones_evaluador": "Establecimiento comercial - Nivel de afectación crítica (RDE-1300)[cite: 55].",
        "personas": [{"nombre": "Establecimiento Comercial", "doc": "902061000", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1301", "corregimiento": "Menga", "prioridad": "BAJA",
        "observaciones_evaluador": "Café Mi Tierra Bar Restaurante Discoteca - Sin clasificación de afectación grave (RDE-1301)[cite: 61].",
        "personas": [{"nombre": "Cafe Mi Tierra Bar Restaurante Discoteca", "doc": "164641348", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1302", "corregimiento": "Yumbo", "prioridad": "BAJA",
        "observaciones_evaluador": "Soy Dama de casa de los abuelitos / Carlos Pizzma - Nivel de afectación baja (RDE-1302)[cite: 61].",
        "personas": [{"nombre": "Carlos Pizzma", "doc": "29284329", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1303", "corregimiento": "Vereda La Rivera", "prioridad": "ALTA",
        "observaciones_evaluador": "Granja El Oro - Nivel de afectación grave (RDE-1303)[cite: 61].",
        "personas": [{"nombre": "Granja El Oro", "doc": "1107518542", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1304", "corregimiento": "La Olga", "prioridad": "MEDIA",
        "observaciones_evaluador": "El Rincón de Blanquita - Nivel de afectación moderada (RDE-1304)[cite: 61].",
        "personas": [{"nombre": "El Rincón de Blanquita", "doc": "31569607", "fecha": "01/01/1980", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1305", "corregimiento": "Acopi", "prioridad": "BAJA",
        "observaciones_evaluador": "Zarceta S.A.S. - Sin clasificación reportada (RDE-1305)[cite: 61].",
        "personas": [{"nombre": "Zarceta S.A.S.", "doc": "901463295", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1306", "corregimiento": "Yumbo", "prioridad": "BAJA",
        "observaciones_evaluador": "Leiva Morillo Ingrid Sugey - Sin clasificación reportada (RDE-1306)[cite: 61].",
        "personas": [{"nombre": "Ingrid Sugey Leiva Morillo", "doc": "31483631", "fecha": "01/01/1980", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1307", "corregimiento": "Yumbo", "prioridad": "ALTA",
        "observaciones_evaluador": "Compañía de Control de Contaminación de Colombia C-4 S.A.S. - Nivel de afectación grave (RDE-1307)[cite: 61].",
        "personas": [{"nombre": "Compañía de Control de Contaminación de Colombia C-4 S.A.S.", "doc": "890326425", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1308", "corregimiento": "Panorama", "prioridad": "ALTA",
        "observaciones_evaluador": "Ana Milena Lerma - Nivel de afectación grave (RDE-1308)[cite: 61].",
        "personas": [{"nombre": "Ana Milena Lerma", "doc": "31488552", "fecha": "01/01/1980", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1309", "corregimiento": "Arroyohondo", "prioridad": "ALTA",
        "observaciones_evaluador": "Surmaquilas S.A.S. - Nivel de afectación crítica (RDE-1309)[cite: 61].",
        "personas": [{"nombre": "Surmaquilas S.A.S.", "doc": "901798371", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1310", "corregimiento": "Yumbo", "prioridad": "ALTA",
        "observaciones_evaluador": "Establecimiento comercial - Nivel de afectación crítica (RDE-1310)[cite: 61].",
        "personas": [{"nombre": "Establecimiento Comercial", "doc": "902061000", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1311", "corregimiento": "Bolívar", "prioridad": "MEDIA",
        "observaciones_evaluador": "Dorado Mosquera Duber Alexis - Nivel de afectación moderada (RDE-1311)[cite: 62].",
        "personas": [{"nombre": "Duber Alexis Dorado Mosquera", "doc": "1118289055", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1312", "corregimiento": "Mulaló", "prioridad": "MEDIA",
        "observaciones_evaluador": "Rivera Gonzalez Monica - Nivel de afectación moderada (RDE-1312)[cite: 62].",
        "personas": [{"nombre": "Monica Rivera Gonzalez", "doc": "66846786", "fecha": "01/01/1980", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1313", "corregimiento": "Arroyohondo", "prioridad": "ALTA",
        "observaciones_evaluador": "Decorplantas Forestal S.A.S. - Nivel de afectación grave (RDE-1313)[cite: 62].",
        "personas": [{"nombre": "Decorplantas Forestal S.A.S.", "doc": "805025926", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1314", "corregimiento": "Acopi", "prioridad": "ALTA",
        "observaciones_evaluador": "Francisco Martinez S.A.S. - Nivel de afectación crítica (RDE-1314)[cite: 62].",
        "personas": [{"nombre": "Francisco Martinez S.A.S.", "doc": "800017087", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1315", "corregimiento": "Acopi", "prioridad": "MEDIA",
        "observaciones_evaluador": "Panamericana de Plásticos S.A.S. - Nivel de afectación moderada (RDE-1315)[cite: 62].",
        "personas": [{"nombre": "Panamericana de Plásticos S.A.S.", "doc": "810000594", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1316", "corregimiento": "Yumbo", "prioridad": "ALTA",
        "observaciones_evaluador": "Transportes Especiales de Colombia Ltda TEC Ltda - Nivel de afectación crítica (RDE-1316)[cite: 62].",
        "personas": [{"nombre": "Transportes Especiales de Colombia Ltda TEC Ltda", "doc": "800171717", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1317", "corregimiento": "Yumbo", "prioridad": "BAJA",
        "observaciones_evaluador": "Muelles y Amortiguadores El Resortero SAS - Sin clasificación (RDE-1317)[cite: 62].",
        "personas": [{"nombre": "Muelles y Amortiguadores El Resortero SAS", "doc": "901508710", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1318", "corregimiento": "Trinidad", "prioridad": "MEDIA",
        "observaciones_evaluador": "Restaurante Atica - Nivel de afectación moderada (RDE-1318)[cite: 62].",
        "personas": [{"nombre": "Restaurante Atica", "doc": "11182887920", "fecha": "01/01/1980", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1319", "corregimiento": "Yumbo", "prioridad": "BAJA",
        "observaciones_evaluador": "CAR Industrias de Yumbo S.A.S. - Sin clasificación (RDE-1319)[cite: 62].",
        "personas": [{"nombre": "CAR Industrias de Yumbo S.A.S.", "doc": "900917525", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1320", "corregimiento": "Madrigal", "prioridad": "ALTA",
        "observaciones_evaluador": "Delirio Cosmetics - Nivel de afectación grave (RDE-1320)[cite: 62].",
        "personas": [{"nombre": "Delirio Cosmetics", "doc": "11121012774", "fecha": "01/01/1980", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1321", "corregimiento": "Vereda El Chocho", "prioridad": "ALTA",
        "observaciones_evaluador": "Tienda El Paraíso - Nivel de afectación crítica (RDE-1321)[cite: 68].",
        "personas": [{"nombre": "Tienda El Paraíso", "doc": "1130673842", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1322", "corregimiento": "Cencar", "prioridad": "ALTA",
        "observaciones_evaluador": "Localizate Latam SAS - Nivel de afectación crítica (RDE-1322)[cite: 68].",
        "personas": [{"nombre": "Localizate Latam SAS", "doc": "902016881", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1323", "corregimiento": "Bolívar", "prioridad": "MEDIA",
        "observaciones_evaluador": "Vidrios y Aluminios Yumbo SAS - Nivel de afectación moderada (RDE-1323)[cite: 68].",
        "personas": [{"nombre": "Vidrios y Aluminios Yumbo SAS", "doc": "9007170375", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1324", "corregimiento": "Belalcázar", "prioridad": "MEDIA",
        "observaciones_evaluador": "Anny Repostería Artesanal - Nivel de afectación moderada (RDE-1324)[cite: 68].",
        "personas": [{"nombre": "Anny Repostería Artesanal", "doc": "11075142840", "fecha": "01/01/1980", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1325", "corregimiento": "Vereda La Buitrera", "prioridad": "ALTA",
        "observaciones_evaluador": "Neuroritmos / Finca Cansan - Nivel de afectación grave (RDE-1325)[cite: 68].",
        "personas": [{"nombre": "Neuroritmos", "doc": "1113784315", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1326", "corregimiento": "Estancia", "prioridad": "ALTA",
        "observaciones_evaluador": "Estanciatex S.A.S. - Nivel de afectación grave (RDE-1326)[cite: 68].",
        "personas": [{"nombre": "Estanciatex S.A.S.", "doc": "900759388", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1327", "corregimiento": "Arroyohondo", "prioridad": "ALTA",
        "observaciones_evaluador": "La Tía Misifus - Nivel de afectación crítica (RDE-1327)[cite: 68].",
        "personas": [{"nombre": "La Tía Misifus", "doc": "66839088", "fecha": "01/01/1980", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1328", "corregimiento": "Acopi", "prioridad": "ALTA",
        "observaciones_evaluador": "STF Group S.A. - Nivel de afectación grave (RDE-1328)[cite: 68].",
        "personas": [{"nombre": "STF Group S.A.", "doc": "805003626", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1329", "corregimiento": "Yumbo", "prioridad": "BAJA",
        "observaciones_evaluador": "Martinez Diaz Liceth Migdaly - Sin clasificación (RDE-1329)[cite: 68].",
        "personas": [{"nombre": "Liceth Migdaly Martinez Diaz", "doc": "1085688390", "fecha": "01/01/1980", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1330", "corregimiento": "Guacandá", "prioridad": "BAJA",
        "observaciones_evaluador": "Quenguan Guevara Alba Teresa - Nivel de afectación baja (RDE-1330)[cite: 68].",
        "personas": [{"nombre": "Alba Teresa Quenguan Guevara", "doc": "36756842", "fecha": "01/01/1980", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
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
    print("Iniciando ENRIQUECIMIENTO FINAL Lote 1291-1330...")
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
        print(f"MIGRACIÓN LOTE 1291-1330 EXITOSA.")
        print(f"Formularios -> Creados: {formularios_creados} | Actualizados: {formularios_actualizados}")
        print(f"Personas    -> Insertadas: {personas_creadas} | Actualizadas: {personas_actualizadas}")
        print(f"==================================================")
        
    except Exception as e:
        print(f"Error en BD: {e}")
    finally:
        if 'conn' in locals(): cur.close(); conn.close()

if __name__ == "__main__":
    main()
