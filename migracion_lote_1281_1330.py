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
        "num_formulario": "1281", "corregimiento": "Bolívar", "prioridad": "MEDIA",
        "observaciones_evaluador": "El Talco / Francy Garzón Trejos - Restaurante mexicano, afectación moderada en ventas y disminución de clientes (RDE-1281)[cite: 73].",
        "personas": [{"nombre": "Francy Garzón Trejos", "doc": "66918721", "fecha": "01/01/1980", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1282", "corregimiento": "Uribe", "prioridad": "MEDIA",
        "observaciones_evaluador": "Ricos Uribe / Cristhian Javier Giraldo - Restaurante con grietas moderadas en infraestructura (RDE-1282)[cite: 73].",
        "personas": [{"nombre": "Cristhian Javier Giraldo", "doc": "1118307328", "fecha": "01/01/1990", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1283", "corregimiento": "Belalcázar", "prioridad": "BAJA",
        "observaciones_evaluador": "Joyería y Bisutería / Patricia Linamar Morales - Afectación leve, pérdidas menores a $200.000 (RDE-1283)[cite: 73].",
        "personas": [{"nombre": "Patricia Linamar Morales", "doc": "4478904", "fecha": "01/01/1980", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1284", "corregimiento": "Guacandá", "prioridad": "ALTA",
        "observaciones_evaluador": "Cooperativa de Transportes Ciudad Yumbo - 45 empleados, daños en infraestructura (RDE-1284)[cite: 73].",
        "personas": [{"nombre": "Cooperativa de Transportes Ciudad Yumbo", "doc": "74342076", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1285", "corregimiento": "Uribe", "prioridad": "MEDIA",
        "observaciones_evaluador": "Miscelánea / Wilson Armando Arcentales - Papelería, pérdidas menores a 5 millones (RDE-1285)[cite: 73].",
        "personas": [{"nombre": "Wilson Armando Arcentales", "doc": "6531374", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1286", "corregimiento": "Bolívar", "prioridad": "MEDIA",
        "observaciones_evaluador": "Restaurante El Buen Gusto / Jhonny Mosquera - 8 empleados, daños en infraestructura física (RDE-1286)[cite: 73].",
        "personas": [{"nombre": "Jhonny Mosquera", "doc": "1143844253", "fecha": "01/01/1990", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1287", "corregimiento": "Yumbo", "prioridad": "MEDIA",
        "observaciones_evaluador": "Grupo Empresarial Multired Guna / Blanca Valleys - 30 empleados, disminución de ventas (RDE-1287)[cite: 73].",
        "personas": [{"nombre": "Blanca Valleys", "doc": "66705300", "fecha": "01/01/1980", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1288", "corregimiento": "Acopi", "prioridad": "MEDIA",
        "observaciones_evaluador": "Soluciones y Servicios AP S.A.S. / Lina Maria Ramirez Cardona - Taller de vehículos, operación parcial (RDE-1288)[cite: 73].",
        "personas": [{"nombre": "Lina Maria Ramirez Cardona", "doc": "1118286773", "fecha": "01/01/1990", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1289", "corregimiento": "Belalcázar", "prioridad": "BAJA",
        "observaciones_evaluador": "Relojería y Llaves QHQ / Andres Santillana - Venta de relojes y accesorios, sin daños (RDE-1289)[cite: 73].",
        "personas": [{"nombre": "Andres Santillana", "doc": "308813040", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1290", "corregimiento": "Guacandá", "prioridad": "MEDIA",
        "observaciones_evaluador": "Mercamedellín / Alirio Suarez - Tienda de abarrotes, interrupción de servicios públicos (RDE-1290)[cite: 73].",
        "personas": [{"nombre": "Alirio Suarez", "doc": "70826017", "fecha": "01/01/1975", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
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
    print("Iniciando ENRIQUECIMIENTO FINAL Lote 1281-1330...")
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
        print(f"MIGRACIÓN LOTE 1281-1330 EXITOSA.")
        print(f"Formularios -> Creados: {formularios_creados} | Actualizados: {formularios_actualizados}")
        print(f"Personas    -> Insertadas: {personas_creadas} | Actualizadas: {personas_actualizadas}")
        print(f"==================================================")
        
    except Exception as e:
        print(f"Error en BD: {e}")
    finally:
        if 'conn' in locals(): cur.close(); conn.close()

if __name__ == "__main__":
    main()
