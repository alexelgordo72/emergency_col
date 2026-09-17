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
        "num_formulario": "1471", "corregimiento": "Yumbo", "prioridad": "ALTA",
        "observaciones_evaluador": "Magaly Sánchez - Inventario de mercancía verificado, nivel de afectación grave (RDE-1471)[cite: 73].",
        "personas": [{"nombre": "Magaly Sánchez", "doc": "900095615", "fecha": "01/01/1980", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1472", "corregimiento": "Arroyohondo", "prioridad": "BAJA",
        "observaciones_evaluador": "Agro Integral Andina - Comercio al por mayor y menor operando normalmente (RDE-1472)[cite: 74].",
        "personas": [{"nombre": "Agro Integral Andina", "doc": "860511458", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1473", "corregimiento": "Arroyohondo", "prioridad": "BAJA",
        "observaciones_evaluador": "STF Group S.A. - 11-50 trabajadores, reducción de clientes, operando con normalidad y seguro (RDE-1473)[cite: 74].",
        "personas": [{"nombre": "STF Group S.A.", "doc": "9011132319", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1474", "corregimiento": "Estancia", "prioridad": "MEDIA",
        "observaciones_evaluador": "Servicasa Yumbo 2000 - Servicios administrativos con daños estructurales (RDE-1474)[cite: 74].",
        "personas": [{"nombre": "Servicasa Yumbo 2000", "doc": "91207637", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1475", "corregimiento": "Alto San Jorge", "prioridad": "MEDIA",
        "observaciones_evaluador": "Blanca - Unidad comercial verificada con afectación moderada (RDE-1475)[cite: 74].",
        "personas": [{"nombre": "Blanca", "doc": "800157508", "fecha": "01/01/1980", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1476", "corregimiento": "Montañitas", "prioridad": "ALTA",
        "observaciones_evaluador": "Museo Arqueológico Montañitas Yumbo - Daños graves en infraestructura y techo (RDE-1476)[cite: 74].",
        "personas": [{"nombre": "Museo Arqueológico Montañitas", "doc": "38964579", "fecha": "01/01/1970", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1477", "corregimiento": "Yumbo", "prioridad": "ALTA",
        "observaciones_evaluador": "Cafetería Rincón Viajero / Luis Ramiro Erazo Arteaga - Daños en infraestructura y equipos (RDE-1477)[cite: 74].",
        "personas": [{"nombre": "Luis Ramiro Erazo Arteaga", "doc": "87718232", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1478", "corregimiento": "Parques del Pinar", "prioridad": "MEDIA",
        "observaciones_evaluador": "Artesanía Iku / María Gladis Barrera Guencia - Comercio con inventario o mercancía afectada (RDE-1478)[cite: 74].",
        "personas": [{"nombre": "María Gladis Barrera Guencia", "doc": "31913378", "fecha": "01/01/1980", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1479", "corregimiento": "Guacandá", "prioridad": "BAJA",
        "observaciones_evaluador": "Panadería Kuki Pan Guacandá - Establecimiento comercial sin afectaciones estructurales (RDE-1479)[cite: 74].",
        "personas": [{"nombre": "Kuki Pan Guacandá", "doc": "1118309495", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1480", "corregimiento": "Belalcázar", "prioridad": "MEDIA",
        "observaciones_evaluador": "Mystic Estanco / Carlos Eduardo Peña María - Comercio con necesidad de capital de trabajo (RDE-1480)[cite: 74].",
        "personas": [{"nombre": "Carlos Eduardo Peña María", "doc": "16464398", "fecha": "01/01/1970", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1481", "corregimiento": "Montañitas", "prioridad": "MEDIA",
        "observaciones_evaluador": "Mirador Pedasito del Cielo - Afectación moderada, pérdidas en infraestructura menor (RDE-1481).",
        "personas": [{"nombre": "Mirador Pedasito del Cielo", "doc": "31479851", "fecha": "01/01/1975", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1482", "corregimiento": "Miravalle", "prioridad": "MEDIA",
        "observaciones_evaluador": "Dimension Fisica S.A.S. - Afectación moderada en instalaciones (RDE-1482).",
        "personas": [{"nombre": "Dimension Fisica S.A.S.", "doc": "67026937", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1483", "corregimiento": "Acopi", "prioridad": "ALTA",
        "observaciones_evaluador": "Innova quimica S.A.S. - Daños severos en infraestructura y maquinaria (RDE-1483).",
        "personas": [{"nombre": "Innova quimica S.A.S.", "doc": "16750052", "fecha": "01/01/1970", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1484", "corregimiento": "La Olga", "prioridad": "MEDIA",
        "observaciones_evaluador": "Casino de los primos - Afectación moderada en inventarios (RDE-1484).",
        "personas": [{"nombre": "Casino de los primos", "doc": "16453891", "fecha": "01/01/1975", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1485", "corregimiento": "El Pedregal", "prioridad": "MEDIA",
        "observaciones_evaluador": "Rancho Dos Años - Pérdidas moderadas en equipos (RDE-1485).",
        "personas": [{"nombre": "Rancho Dos Años", "doc": "1107845715", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1486", "corregimiento": "Vista Hermosa", "prioridad": "BAJA",
        "observaciones_evaluador": "Nails Eli Garzón - Servicios estéticos sin afectación severa (RDE-1486).",
        "personas": [{"nombre": "Nails Eli Garzón", "doc": "1193473062", "fecha": "01/01/1985", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1487", "corregimiento": "Acopi", "prioridad": "ALTA",
        "observaciones_evaluador": "Maquite S.A. - Daños graves en equipos y planta física (RDE-1487).",
        "personas": [{"nombre": "Maquite S.A.", "doc": "800070655", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1488", "corregimiento": "Yumbo", "prioridad": "MEDIA",
        "observaciones_evaluador": "Donde Leiver - Operación parcial, daños menores (RDE-1488).",
        "personas": [{"nombre": "Donde Leiver", "doc": "1118296663", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1489", "corregimiento": "Estancia", "prioridad": "BAJA",
        "observaciones_evaluador": "Diana Milena Buritica Mendoza - Afectación baja, operando (RDE-1489).",
        "personas": [{"nombre": "Diana Milena Buritica Mendoza", "doc": "29975617", "fecha": "01/01/1980", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1490", "corregimiento": "Yumbo", "prioridad": "ALTA",
        "observaciones_evaluador": "Establecimiento comercial verificado - Daños graves estructurales (RDE-1490).",
        "personas": [{"nombre": "Establecimiento Comercial", "doc": "0", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
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
    print("Iniciando ENRIQUECIMIENTO FINAL Lote 1471-1490...")
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
        print(f"MIGRACIÓN LOTE 1471-1490 EXITOSA.")
        print(f"Formularios -> Creados: {formularios_creados} | Actualizados: {formularios_actualizados}")
        print(f"Personas    -> Insertadas: {personas_creadas} | Actualizadas: {personas_actualizadas}")
        print(f"==================================================")
        
    except Exception as e:
        print(f"Error en BD: {e}")
    finally:
        if 'conn' in locals(): cur.close(); conn.close()

if __name__ == "__main__":
    main()
