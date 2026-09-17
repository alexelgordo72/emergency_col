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
        "num_formulario": "951", "corregimiento": "Manga Vieja", "prioridad": "ALTA",
        "observaciones_evaluador": "Afectaciones económicas y estructurales graves en unidad comercial (RDE-951).",
        "personas": [
            {"nombre": "Gricela Ruano Hoyos", "doc": "31480822", "fecha": "12/08/1965", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "952", "corregimiento": "Manga Vieja", "prioridad": "ALTA",
        "observaciones_evaluador": "Afectaciones graves en industria manufacturera con operación parcial (RDE-952).",
        "personas": [
            {"nombre": "Claudia Patricia Roncancio Velosa", "doc": "51959168", "fecha": "01/01/1980", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "953", "corregimiento": "San Marcos", "prioridad": "MEDIA",
        "observaciones_evaluador": "Restaurante con daños en instalaciones y operación parcial (RDE-953).",
        "personas": [
            {"nombre": "Diana Enelia Tovar Parra", "doc": "28612902", "fecha": "01/01/1982", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "954", "corregimiento": "Dapa", "prioridad": "MEDIA",
        "observaciones_evaluador": "Restaurante con afectaciones físicas e infraestructura de maquinaria (RDE-954).",
        "personas": [
            {"nombre": "Restaurante Casona", "doc": "6736937", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "955", "corregimiento": "Rincón Dapa", "prioridad": "BAJA",
        "observaciones_evaluador": "Establecimiento de comercio al por mayor y detal con daños menores en infraestructura (RDE-955).",
        "personas": [
            {"nombre": "Jessica Rincon Astaiza", "doc": "1118300557", "fecha": "01/06/1993", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "956", "corregimiento": "Yumbo Urbano", "prioridad": "BAJA",
        "observaciones_evaluador": "Inventarios de mercancía sin afectaciones críticas operativas (RDE-956).",
        "personas": [
            {"nombre": "Alejandro Pulido Mesa", "doc": "7225910", "fecha": "01/01/1975", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "957", "corregimiento": "Acopi", "prioridad": "MEDIA",
        "observaciones_evaluador": "Empresa de construcción con daños en infraestructura y maquinaria (RDE-957).",
        "personas": [
            {"nombre": "Pedro Antonio Limas Ortiz", "doc": "90054450", "fecha": "01/01/1970", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "958", "corregimiento": "Belalcazar", "prioridad": "BAJA",
        "observaciones_evaluador": "Establecimiento de comercio con afectación moderada en inventarios (RDE-958).",
        "personas": [
            {"nombre": "Carlos Eduardo Peña Maria", "doc": "16464398", "fecha": "01/01/1970", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "959", "corregimiento": "Lleras", "prioridad": "BAJA",
        "observaciones_evaluador": "Comercio de reparación de vehículos con afectaciones menores (RDE-959).",
        "personas": [
            {"nombre": "Magic Celeste Ceron Ayala", "doc": "1144040592", "fecha": "01/01/1995", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "960", "corregimiento": "Vista Hermosa", "prioridad": "BAJA",
        "observaciones_evaluador": "Establecimiento comercial de servicios estéticos sin afectaciones críticas (RDE-960).",
        "personas": [
            {"nombre": "Nails Eli Garzón", "doc": "3193473062", "fecha": "01/01/1985", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "961", "corregimiento": "Guacandá", "prioridad": "BAJA",
        "observaciones_evaluador": "Panadería sin afectaciones reportadas en infraestructura principal (RDE-961).",
        "personas": [
            {"nombre": "Panadería Kuki Pan", "doc": "0", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "962", "corregimiento": "Mulaló", "prioridad": "MEDIA",
        "observaciones_evaluador": "Comercio al por mayor y menor con daños en maquinaria y equipos (RDE-962).",
        "personas": [
            {"nombre": "Nancy Otero Cabo", "doc": "100337446", "fecha": "01/01/1978", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "963", "corregimiento": "Arroyohondo", "prioridad": "ALTA",
        "observaciones_evaluador": "Empresa de construcción con suspensión temporal de operaciones y daños severos (RDE-963).",
        "personas": [
            {"nombre": "Luisa Fernando Goncales Padilla", "doc": "900184057", "fecha": "01/01/1975", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "964", "corregimiento": "Dapa", "prioridad": "BAJA",
        "observaciones_evaluador": "Comercio menor con afectaciones operativas parciales (RDE-964).",
        "personas": [
            {"nombre": "Ostinatto SAS", "doc": "320679413", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "965", "corregimiento": "Acopi", "prioridad": "MEDIA",
        "observaciones_evaluador": "Empresa de manufactura con operación parcial e infraestructura afectada (RDE-965).",
        "personas": [
            {"nombre": "Multideas SAS", "doc": "805015345", "fecha": "01/01/1975", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "966", "corregimiento": "Bolívar", "prioridad": "ALTA",
        "observaciones_evaluador": "Alojamiento y servicios de comida con afectación económica crítica (RDE-966).",
        "personas": [
            {"nombre": "Diana Maria Orozco", "doc": "1073920764", "fecha": "01/01/1982", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "967", "corregimiento": "Montañitas", "prioridad": "ALTA",
        "observaciones_evaluador": "Museo Arqueológico de Montañitas con daños graves en infraestructura (RDE-967).",
        "personas": [
            {"nombre": "Maricela Elena Herrera Denavy", "doc": "310426643", "fecha": "01/01/1970", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "968", "corregimiento": "Norte de Cali", "prioridad": "ALTA",
        "observaciones_evaluador": "Empresa de hospedaje y alimentación con afectación grave en infraestructura y equipos (RDE-968).",
        "personas": [
            {"nombre": "Diego Fernando Osorio Toro", "doc": "900736802", "fecha": "01/01/1978", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "969", "corregimiento": "Uribe", "prioridad": "ALTA",
        "observaciones_evaluador": "Establecimiento de servicios de alojamiento y comida con daños graves (RDE-969).",
        "personas": [
            {"nombre": "Claudia Lorena Soto", "doc": "1007521945", "fecha": "01/01/1985", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "970", "corregimiento": "Miravalle", "prioridad": "ALTA",
        "observaciones_evaluador": "Empresa turística operando de manera parcial con daños estructurales (RDE-970).",
        "personas": [
            {"nombre": "Diego Fernando Salazar Ocampo", "doc": "800159974", "fecha": "01/01/1975", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "971", "corregimiento": "Acopi", "prioridad": "ALTA",
        "observaciones_evaluador": "Empresa con situación crítica por daños en infraestructura y maquinaria (RDE-971).",
        "personas": [
            {"nombre": "Jose David Hernandez", "doc": "9901956021", "fecha": "01/01/1975", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "972", "corregimiento": "Yumbo Urbano", "prioridad": "MEDIA",
        "observaciones_evaluador": "Negocio con reducción de clientes e inventarios afectados (RDE-972).",
        "personas": [
            {"nombre": "Magaly Sanchez", "doc": "900095615", "fecha": "01/01/1980", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "973", "corregimiento": "Santa Ines", "prioridad": "MEDIA",
        "observaciones_evaluador": "Unidad económica con pérdidas económicas moderadas (RDE-973).",
        "personas": [
            {"nombre": "Yolanda Edilma Muñoz Ordoñez", "doc": "1081592974", "fecha": "01/01/1980", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "974", "corregimiento": "Montañitas", "prioridad": "MEDIA",
        "observaciones_evaluador": "Establecimiento con daños moderados en infraestructura (RDE-974).",
        "personas": [
            {"nombre": "Luz Marina Gallego M.", "doc": "31479851", "fecha": "01/01/1965", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "975", "corregimiento": "Nueva Estancia", "prioridad": "BAJA",
        "observaciones_evaluador": "Comercio menor con afectaciones económicas leves (RDE-975).",
        "personas": [
            {"nombre": "Lida Andrea Cruz", "doc": "25292899", "fecha": "01/01/1990", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "976", "corregimiento": "Hacienda Verde", "prioridad": "MEDIA",
        "observaciones_evaluador": "Empresa comercial operando parcialmente (RDE-976).",
        "personas": [
            {"nombre": "Fernando Leon Murillo", "doc": "93379771", "fecha": "01/01/1970", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "977", "corregimiento": "Panorama", "prioridad": "MEDIA",
        "observaciones_evaluador": "Establecimiento comercial con pérdida de inventarios (RDE-977).",
        "personas": [
            {"nombre": "Alexander Renteria", "doc": "1118298713", "fecha": "01/01/1985", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "978", "corregimiento": "Acopi", "prioridad": "ALTA",
        "observaciones_evaluador": "Empresa de comercio con pérdidas económicas graves (RDE-978).",
        "personas": [
            {"nombre": "Ximena Alexandra Rodriguez F.", "doc": "901506103", "fecha": "01/01/1985", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "979", "corregimiento": "Acopi", "prioridad": "ALTA",
        "observaciones_evaluador": "Metalmecánica con daños en maquinaria y operación suspendida (RDE-979).",
        "personas": [
            {"nombre": "Rigoberto Velazco", "doc": "16750052", "fecha": "01/01/1965", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "980", "corregimiento": "Acopi", "prioridad": "ALTA",
        "observaciones_evaluador": "Empresa industrial con daños críticos en infraestructura y equipos (RDE-980).",
        "personas": [
            {"nombre": "Metalmecanica de Occidente", "doc": "900772779", "fecha": "01/01/1970", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "981", "corregimiento": "Uribe", "prioridad": "BAJA",
        "observaciones_evaluador": "Unidad comercial con afectación menor en equipos (RDE-981).",
        "personas": [
            {"nombre": "Edidardo Valencia Hurtado", "doc": "1118306714", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "982", "corregimiento": "Yumbo", "prioridad": "BAJA",
        "observaciones_evaluador": "Comercio local verificado con baja afectación (RDE-982).",
        "personas": [
            {"nombre": "Andres Fernando", "doc": "1130637019", "fecha": "01/01/1985", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "983", "corregimiento": "Media Peña", "prioridad": "MEDIA",
        "observaciones_evaluador": "Establecimiento comercial con daños en infraestructura (RDE-983).",
        "personas": [
            {"nombre": "Chavez 2", "doc": "1006337700", "fecha": "01/01/1990", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "984", "corregimiento": "Acopi", "prioridad": "ALTA",
        "observaciones_evaluador": "Empresa química con daños graves en equipos e infraestructura (RDE-984).",
        "personas": [
            {"nombre": "Ivan Acosta", "doc": "16750052", "fecha": "01/01/1970", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Innova Quimica S.A.S.", "doc": "900772779", "fecha": "01/01/1970", "es_jefe": False, "sexo": "M", "parentesco": "Otro", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "985", "corregimiento": "Uribe", "prioridad": "MEDIA",
        "observaciones_evaluador": "Establecimiento comercial con daños moderados (RDE-985).",
        "personas": [
            {"nombre": "Silvia Juliana Mejia", "doc": "38893682", "fecha": "01/01/1980", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "986", "corregimiento": "Nueva Estancia", "prioridad": "MEDIA",
        "observaciones_evaluador": "Planificadora de pan con daños considerables en equipos y operación parcial (RDE-986).",
        "personas": [
            {"nombre": "Lavia Botero", "doc": "5218428", "fecha": "01/01/1970", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Industria Planificadora Frespan", "doc": "800085665", "fecha": "01/01/1970", "es_jefe": False, "sexo": "M", "parentesco": "Otro", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "987", "corregimiento": "Guacandá", "prioridad": "MEDIA",
        "observaciones_evaluador": "Negocio de uñas y estética con afectación económica moderada (RDE-987).",
        "personas": [
            {"nombre": "Maria Teresa Guevara", "doc": "31412243", "fecha": "01/01/1980", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "988", "corregimiento": "Acopi", "prioridad": "ALTA",
        "observaciones_evaluador": "Empresa comercial con daños críticos y operaciones detenidas (RDE-988).",
        "personas": [
            {"nombre": "Daniel", "doc": "1113639461", "fecha": "01/01/1990", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Design and Development", "doc": "900291680", "fecha": "01/01/1990", "es_jefe": False, "sexo": "M", "parentesco": "Otro", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "989", "corregimiento": "Acopi", "prioridad": "ALTA",
        "observaciones_evaluador": "Colombia Industrial Automotriz S.A.S. con afectaciones severas (RDE-989).",
        "personas": [
            {"nombre": "Colombia Industrial Automotriz S.A.S.", "doc": "805011264", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "990", "corregimiento": "La Olga", "prioridad": "MEDIA",
        "observaciones_evaluador": "Casino de los primos con daños en infraestructura (RDE-990).",
        "personas": [
            {"nombre": "Freddy Jair Zuñiga Galindez", "doc": "16453891", "fecha": "01/01/1975", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
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
    print("Iniciando ENRIQUECIMIENTO FINAL Lote 951-990...")
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
        print(f"MIGRACIÓN LOTE 951-990 EXITOSA.")
        print(f"Formularios -> Creados: {formularios_creados} | Actualizados: {formularios_actualizados}")
        print(f"Personas    -> Insertadas: {personas_creadas} | Actualizadas: {personas_actualizadas}")
        print(f"==================================================")
        
    except Exception as e:
        print(f"Error en BD: {e}")
    finally:
        if 'conn' in locals(): cur.close(); conn.close()

if __name__ == "__main__":
    main()
