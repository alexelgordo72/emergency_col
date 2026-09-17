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
        "num_formulario": "1651", "corregimiento": "Dionisio", "prioridad": "ALTA",
        "observaciones_evaluador": "Martha Lucia Herrera Cano - Vivienda de 2 pisos con fisuras en muros, se recomienda reforzamiento de columnas y vigas (RUFE-1651)[cite: 43].",
        "personas": [
            {"nombre": "Martha Lucia Herrera Cano", "doc": "31470254", "fecha": "20/08/1960", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Jan Camilo Sanchez Herrera", "doc": "1700601717", "fecha": "29/08/2003", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Daniela Gonzalez Herrera", "doc": "1118297360", "fecha": "30/08/1991", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Than Sebastian Escobar", "doc": "1118303259", "fecha": "21/10/1994", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Tomas Villafañe Gonzalez", "doc": "1109560013", "fecha": "23/01/2016", "es_jefe": False, "sexo": "M", "parentesco": "Nieto(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1652", "corregimiento": "Bellavista", "prioridad": "BAJA",
        "observaciones_evaluador": "Ayde Rubiano Hidalgo - Beneficiarios del futuro, sin afectaciones visibles (RUFE-1652)[cite: 44].",
        "personas": [
            {"nombre": "Ayde Rubiano Hidalgo", "doc": "29740742", "fecha": "20/06/1991", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1653", "corregimiento": "Mulaló", "prioridad": "BAJA",
        "observaciones_evaluador": "Melba Lucia Barcia Ramirez - Pequeños Pitufos, sin afectaciones visibles (RUFE-1653)[cite: 44].",
        "personas": [
            {"nombre": "Melba Lucia Barcia Ramirez", "doc": "35410233", "fecha": "20/09/1964", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1654", "corregimiento": "Bellavista", "prioridad": "BAJA",
        "observaciones_evaluador": "Sandra Milena Villada Taborda - La Casita Encantada, prioridad baja (RUFE-1654)[cite: 44].",
        "personas": [
            {"nombre": "Sandra Milena Villada Taborda", "doc": "1018290481", "fecha": "15/10/1988", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1655", "corregimiento": "La Ceiba", "prioridad": "BAJA",
        "observaciones_evaluador": "Nancy Tatiana Carvajal - Hos Juguetonas, prioridad baja (RUFE-1655)[cite: 44].",
        "personas": [
            {"nombre": "Nancy Tatiana Carvajal", "doc": "29975504", "fecha": "29/09/1985", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1656", "corregimiento": "Las Vegas", "prioridad": "BAJA",
        "observaciones_evaluador": "Nohemi Johana Garzón - Pollito los Las Vegas, prioridad baja (RUFE-1656)[cite: 44].",
        "personas": [
            {"nombre": "Nohemi Johana Garzón", "doc": "31485571", "fecha": "07/06/1981", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1657", "corregimiento": "Nuevo Horizonte", "prioridad": "BAJA",
        "observaciones_evaluador": "Heimy Alexandra Zambrano Ruiz - Pequeños Personitas, prioridad baja (RUFE-1657)[cite: 44].",
        "personas": [
            {"nombre": "Heimy Alexandra Zambrano Ruiz", "doc": "1006037584", "fecha": "04/03/2001", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1658", "corregimiento": "Cruces", "prioridad": "BAJA",
        "observaciones_evaluador": "Yolima Toro - Amiguitos Hos Mused, prioridad baja (RUFE-1658)[cite: 44].",
        "personas": [
            {"nombre": "Yolima Toro", "doc": "31481126", "fecha": "23/10/1978", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1659", "corregimiento": "Horizonte", "prioridad": "MEDIA",
        "observaciones_evaluador": "Maira Alejandra Escobar Salazar - Osito Logical, prioridad media (RUFE-1659)[cite: 45].",
        "personas": [
            {"nombre": "Maira Alejandra Escobar Salazar", "doc": "1118282555", "fecha": "21/03/1986", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
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
    print("Iniciando ENRIQUECIMIENTO FINAL Lote 1651-1659...")
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
                
                cur.execute("SELECT id FROM public.rufe_personas WHERE documento_identidad = %s", (p["doc"],))
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
        print(f"MIGRACIÓN LOTE 1651-1659 EXITOSA.")
        print(f"Formularios -> Creados: {formularios_creados} | Actualizados: {formularios_actualizados}")
        print(f"Personas    -> Insertadas: {personas_creadas} | Actualizadas: {personas_actualizadas}")
        print(f"==================================================")
        
    except Exception as e:
        print(f"Error en BD: {e}")
    finally:
        if 'conn' in locals(): cur.close(); conn.close()

if __name__ == "__main__":
    main()
