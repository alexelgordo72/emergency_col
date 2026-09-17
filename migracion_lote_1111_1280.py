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
        "num_formulario": "1112", "corregimiento": "Bolívar", "prioridad": "BAJA",
        "observaciones_evaluador": "Calzado Dos 21 - Establecimiento comercial verificado sin observaciones críticas (RDE-1112).",
        "personas": [{"nombre": "Calzado Dos 21", "doc": "1118292415", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1172", "corregimiento": "Guacandá", "prioridad": "MEDIA",
        "observaciones_evaluador": "Dan Metro - Microempresa industrial operando parcialmente (RDE-1172).",
        "personas": [{"nombre": "Dan Metro", "doc": "1118295197", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1173", "corregimiento": "Madrigal", "prioridad": "BAJA",
        "observaciones_evaluador": "Kuki Pan Madrigal - Panadería funcionando con normalidad (RDE-1173).",
        "personas": [{"nombre": "Kuki Pan Madrigal", "doc": "118284992", "fecha": "01/01/1980", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1174", "corregimiento": "Panorama", "prioridad": "MEDIA",
        "observaciones_evaluador": "Divina Variedad - Comercio con daños leves en mercancía (RDE-1174).",
        "personas": [{"nombre": "Divina Variedad", "doc": "1118310384", "fecha": "01/01/1980", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1175", "corregimiento": "Bolívar", "prioridad": "BAJA",
        "observaciones_evaluador": "Casino Central Park Bolívar - Local operando de manera normal (RDE-1175).",
        "personas": [{"nombre": "Casino Central Park Bolívar", "doc": "1118311317", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1176", "corregimiento": "Buenos Aires", "prioridad": "MEDIA",
        "observaciones_evaluador": "Vidrios y Aluminios Rodríguez - Daños en infraestructura y herramientas (RDE-1176).",
        "personas": [{"nombre": "Vidrios y Aluminios Rodríguez", "doc": "1110591176", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1177", "corregimiento": "Bolívar", "prioridad": "BAJA",
        "observaciones_evaluador": "Depósito de Alimentos Parre - Establecimiento verificado sin novedades (RDE-1177).",
        "personas": [{"nombre": "Depósito de Alimentos Parre", "doc": "6098662", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1178", "corregimiento": "Uribe", "prioridad": "ALTA",
        "observaciones_evaluador": "Hospedaje - Establecimiento con daños estimados en 30 millones y recuperación en 30 días (RDE-1178).",
        "personas": [{"nombre": "Hospedaje", "doc": "16454723", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1179", "corregimiento": "Uribe", "prioridad": "BAJA",
        "observaciones_evaluador": "FEDY - Instalaciones en buen estado (RDE-1179).",
        "personas": [{"nombre": "FEDY", "doc": "1118311177", "fecha": "01/01/1980", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1180", "corregimiento": "Bolívar", "prioridad": "BAJA",
        "observaciones_evaluador": "Auto Garcia - Taller automotriz sin afectaciones (RDE-1180).",
        "personas": [{"nombre": "Auto Garcia", "doc": "16458159", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1201", "corregimiento": "Yumbo", "prioridad": "BAJA",
        "observaciones_evaluador": "Casa de los retazos - Local opera con total normalidad, sin daños (RDE-1201).",
        "personas": [{"nombre": "Casa de los retazos", "doc": "70252054", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1202", "corregimiento": "Yumbo", "prioridad": "MEDIA",
        "observaciones_evaluador": "Cristalería Cesitodo - Solo daños en alguna mercancía (RDE-1202).",
        "personas": [{"nombre": "Cristalería Cesitodo", "doc": "21779013", "fecha": "01/01/1980", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1203", "corregimiento": "Yumbo", "prioridad": "BAJA",
        "observaciones_evaluador": "Laura Sofía Sport - Negocio sin afectaciones, funcionando normalmente (RDE-1203).",
        "personas": [{"nombre": "Laura Sofía Sport", "doc": "3148129525", "fecha": "01/01/1980", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1204", "corregimiento": "Yumbo", "prioridad": "BAJA",
        "observaciones_evaluador": "Calzado Boys - Sin daños reportados en mercancía ni local (RDE-1204).",
        "personas": [{"nombre": "Calzado Boys", "doc": "42027687", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1205", "corregimiento": "Yumbo", "prioridad": "MEDIA",
        "observaciones_evaluador": "Lex Jeans - Ayuda en línea para aumentar las ventas tras la emergencia (RDE-1205).",
        "personas": [{"nombre": "Lex Jeans", "doc": "16455146", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1206", "corregimiento": "Belalcázar", "prioridad": "BAJA",
        "observaciones_evaluador": "Centro Visual Santamaría - Establecimiento en buen estado, sin pérdidas ni riesgos (RDE-1206).",
        "personas": [{"nombre": "Centro Visual Santamaría", "doc": "3175130431", "fecha": "01/01/1980", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1207", "corregimiento": "Yumbo", "prioridad": "ALTA",
        "observaciones_evaluador": "Odontorent Clínica Odontológica - Requiere inspección técnica urgente (RDE-1207).",
        "personas": [{"nombre": "Odontorent", "doc": "1118258900", "fecha": "01/01/1980", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1208", "corregimiento": "Yumbo", "prioridad": "MEDIA",
        "observaciones_evaluador": "Muebles Bestidas - No presenta daños en mercancía ni servicios (RDE-1208).",
        "personas": [{"nombre": "Muebles Bestidas", "doc": "66858660", "fecha": "01/01/1980", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1209", "corregimiento": "Yumbo", "prioridad": "BAJA",
        "observaciones_evaluador": "Papelería Miscelánea La Novena - Sin afectaciones (RDE-1209).",
        "personas": [{"nombre": "Papelería Miscelánea La Novena", "doc": "29813350", "fecha": "01/01/1980", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1210", "corregimiento": "Dapa", "prioridad": "BAJA",
        "observaciones_evaluador": "Tienda Maravillas Naturales - Buen estado, operando normalmente (RDE-1210).",
        "personas": [{"nombre": "Tienda Maravillas Naturales", "doc": "1118311177", "fecha": "01/01/1980", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1211", "corregimiento": "Yumbo", "prioridad": "MEDIA",
        "observaciones_evaluador": "Meam Muebles - Solo fisuras leves en segundo piso (RDE-1211).",
        "personas": [{"nombre": "Meam Muebles", "doc": "42870979", "fecha": "01/01/1980", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1212", "corregimiento": "Yumbo", "prioridad": "ALTA",
        "observaciones_evaluador": "Grupo Empresarial Irlanda - Daños en infraestructura con afectación de ingresos (RDE-1212).",
        "personas": [{"nombre": "Grupo Empresarial Irlanda", "doc": "1118285641", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1213", "corregimiento": "Yumbo", "prioridad": "ALTA",
        "observaciones_evaluador": "Carlos Fredy Calderon - Pérdida total de bodega tras sismo e incendio secundario (RDE-1213).",
        "personas": [{"nombre": "Carlos Fredy Calderon", "doc": "0", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1214", "corregimiento": "Uribe", "prioridad": "BAJA",
        "observaciones_evaluador": "Ruth Ximena Satizabal - Sin afectaciones reportadas (RDE-1214).",
        "personas": [{"nombre": "Ruth Ximena Satizabal", "doc": "3168878720", "fecha": "01/01/1980", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1215", "corregimiento": "Estancia", "prioridad": "BAJA",
        "observaciones_evaluador": "Monica Pulido - Negocio sin afectación reportada (RDE-1215).",
        "personas": [{"nombre": "Monica Pulido", "doc": "3129864970", "fecha": "01/01/1980", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1216", "corregimiento": "Yumbo", "prioridad": "BAJA",
        "observaciones_evaluador": "Sergio Gomez - Inmueble verificado sin novedades (RDE-1216).",
        "personas": [{"nombre": "Sergio Gomez", "doc": "3116111114", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1217", "corregimiento": "Yumbo", "prioridad": "ALTA",
        "observaciones_evaluador": "Andrea del Pilar Rios - Daños en infraestructura, estimada en 30 millones (RDE-1217).",
        "personas": [{"nombre": "Andrea del Pilar Rios", "doc": "8207491650", "fecha": "01/01/1980", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1218", "corregimiento": "Santa Ines", "prioridad": "BAJA",
        "observaciones_evaluador": "Javier Bernal - Inmueble verificado sin afectaciones (RDE-1218).",
        "personas": [{"nombre": "Javier Bernal", "doc": "3225507657", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1219", "corregimiento": "Belalcázar", "prioridad": "BAJA",
        "observaciones_evaluador": "Panadería Nutripan - Sin afectaciones estructurales, operando normalmente (RDE-1219).",
        "personas": [{"nombre": "Panadería Nutripan", "doc": "0", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1220", "corregimiento": "Yumbo", "prioridad": "BAJA",
        "observaciones_evaluador": "Panadería La Principal de Lleras - Sin afectaciones, operando (RDE-1220).",
        "personas": [{"nombre": "Gonzalo de Jesus Gomez Giraldo", "doc": "7082633", "fecha": "19/09/1958", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1221", "corregimiento": "Belalcázar", "prioridad": "MEDIA",
        "observaciones_evaluador": "Almacén La Cubierta / Dary Pabon - Establecimiento con grietas, requiere visita técnica (RDE-1221).",
        "personas": [{"nombre": "Dary Pabon", "doc": "29939526", "fecha": "31/10/1966", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1222", "corregimiento": "Belalcázar", "prioridad": "BAJA",
        "observaciones_evaluador": "Taller de relojería y llaves / Andres Santillana - Sin afectaciones estructurales (RDE-1222).",
        "personas": [{"nombre": "Andres Santillana", "doc": "14837275", "fecha": "12/05/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1223", "corregimiento": "Belalcázar", "prioridad": "BAJA",
        "observaciones_evaluador": "Asadero Quercor / Restaurante / Angela Bernal - Operando normalmente, sin daños estructurales (RDE-1223).",
        "personas": [{"nombre": "Angela Bernal", "doc": "31483397", "fecha": "27/05/1980", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1224", "corregimiento": "Lleras", "prioridad": "MEDIA",
        "observaciones_evaluador": "Delipollo - Daños en infraestructura física, menor afectación (RDE-1224).",
        "personas": [{"nombre": "Hector Hernan Incapie Dugre", "doc": "1037947334", "fecha": "09/05/1990", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1225", "corregimiento": "Belalcázar", "prioridad": "MEDIA",
        "observaciones_evaluador": "Hotel Jacinto Plaza de los Ros - Daños leves en maquinaria y equipo (RDE-1225).",
        "personas": [{"nombre": "Hotel Jacinto", "doc": "16793236", "fecha": "16/08/1970", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1226", "corregimiento": "Belalcázar", "prioridad": "BAJA",
        "observaciones_evaluador": "Grupo Comercial Astroventas / Sibeiro Mezu - Disminución temporal en ventas (RDE-1226).",
        "personas": [{"nombre": "Sibeiro Mezu", "doc": "4865259", "fecha": "01/01/1963", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1227", "corregimiento": "Bolívar", "prioridad": "ALTA",
        "observaciones_evaluador": "Fleximax / Juan Carlos Sanchez Espinoza - Daños en infraestructura física (RDE-1227).",
        "personas": [{"nombre": "Juan Carlos Sanchez Espinoza", "doc": "1118289935", "fecha": "03/11/1988", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1228", "corregimiento": "Dapa", "prioridad": "ALTA",
        "observaciones_evaluador": "El Gangazo paisa / Julia Palma Soto - Pérdida de inventario por cristalería (RDE-1228).",
        "personas": [{"nombre": "Julia Palma Soto", "doc": "29973662", "fecha": "18/07/1983", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1229", "corregimiento": "Yumbo Centro", "prioridad": "BAJA",
        "observaciones_evaluador": "Pompilio Parra - Inmueble comercial verificado sin afectaciones estructurales (RDE-1229).",
        "personas": [{"nombre": "Pompilio Parra", "doc": "1443333", "fecha": "20/02/1944", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1230", "corregimiento": "Yumbo", "prioridad": "BAJA",
        "observaciones_evaluador": "Establecimiento verificado - Operando normalmente tras revisión (RDE-1230).",
        "personas": [{"nombre": "Comercial Yumbo", "doc": "0", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
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
    print("Iniciando ENRIQUECIMIENTO FINAL Lote 1111-1230...")
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
        print(f"MIGRACIÓN LOTE 1111-1230 EXITOSA.")
        print(f"Formularios -> Creados: {formularios_creados} | Actualizados: {formularios_actualizados}")
        print(f"Personas    -> Insertadas: {personas_creadas} | Actualizadas: {personas_actualizadas}")
        print(f"==================================================")
        
    except Exception as e:
        print(f"Error en BD: {e}")
    finally:
        if 'conn' in locals(): cur.close(); conn.close()

if __name__ == "__main__":
    main()
