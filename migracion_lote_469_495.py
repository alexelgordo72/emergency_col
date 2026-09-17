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
        "num_formulario": "469", "corregimiento": "Estancia Antigua", "prioridad": "MEDIA",
        "observaciones_evaluador": "Presenta grietas prolongadas en mampostería.",
        "personas": [
            {"nombre": "Natalia Ordoñez", "doc": "31485664", "fecha": "27/03/1981", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Jhon Jairo Giron", "doc": "16458974", "fecha": "13/09/1979", "es_jefe": False, "sexo": "M", "parentesco": "Esposo(a)", "etnia": "Ninguna"},
            {"nombre": "Jacobo Giron", "doc": "1107836782", "fecha": "16/09/2004", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "470", "corregimiento": "Antigua Estancia", "prioridad": "MEDIA",
        "observaciones_evaluador": "Presenta grietas en mampostería, afectación en muro compartido con la vecina, riesgo de colapso.",
        "personas": [
            {"nombre": "Fabiola Piñedos", "doc": "34539521", "fecha": "11/04/1956", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "471", "corregimiento": "Estancia Antigua", "prioridad": "BAJA",
        "observaciones_evaluador": "Presenta grietas en mampostería, principalmente en el marco de la puerta.",
        "personas": [
            {"nombre": "Elizabeth Pera", "doc": "38943172", "fecha": "01/01/1956", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Javier Medina", "doc": "16448789", "fecha": "14/12/1952", "es_jefe": False, "sexo": "M", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "472", "corregimiento": "Hacienda Verde", "prioridad": "BAJA",
        "observaciones_evaluador": "Grietas superficiales en mampostería y humedad en cielo raso por daño hidráulico del apartamento superior.",
        "personas": [
            {"nombre": "Albert De la Cruz Potosi", "doc": "1088294135", "fecha": "19/01/1992", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Amanda De la Cruz", "doc": "1118318463", "fecha": "08/03/1994", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Escarlet Sofia De la Cruz", "doc": "1232808109", "fecha": "22/01/2022", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "473", "corregimiento": "Manga Vieja", "prioridad": "MEDIA",
        "observaciones_evaluador": "Vivienda con susceptibilidad de caída de tierra (remoción en masa latente).",
        "personas": [
            {"nombre": "Huber Ney Delgado", "doc": "94361707", "fecha": "30/07/1978", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "474", "corregimiento": "Manga Vieja", "prioridad": "BAJA",
        "observaciones_evaluador": "Vivienda en material sin afectaciones graves, completamente habitable.",
        "personas": [
            {"nombre": "Alcides Vergara", "doc": "6552402", "fecha": "18/06/1951", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Silvia Melo", "doc": "31476787", "fecha": "08/09/1950", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Lina Melo", "doc": "1006435831", "fecha": "30/03/1993", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Jaime Vasquez", "doc": "14835402", "fecha": "29/09/1977", "es_jefe": False, "sexo": "M", "parentesco": "Otro", "etnia": "Ninguna"},
            {"nombre": "Miguel Delgado", "doc": "1140168646", "fecha": "05/08/2013", "es_jefe": False, "sexo": "M", "parentesco": "Nieto(a)", "etnia": "Ninguna"},
            {"nombre": "Esteban Delgado", "doc": "1104830195", "fecha": "07/02/2011", "es_jefe": False, "sexo": "M", "parentesco": "Nieto(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "475", "corregimiento": "Manga Vieja", "prioridad": "BAJA",
        "observaciones_evaluador": "Vivienda en bahareque con material y fisuras mínimas, pequeños desprendimientos.",
        "personas": [
            {"nombre": "Blanca Fernandez", "doc": "31487744", "fecha": "09/12/1982", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Eder Daza", "doc": "16455842", "fecha": "30/08/2019", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Celine Daza", "doc": "1104846582", "fecha": "01/01/2021", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "476", "corregimiento": "Manga Vieja", "prioridad": "MEDIA",
        "observaciones_evaluador": "Vivienda en material con cubierta levantada en la mitad de la casa, desprendimiento de revoque y grietas perimetrales.",
        "personas": [
            {"nombre": "Emir Vergara", "doc": "194361393", "fecha": "30/03/1975", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "477", "corregimiento": "Manga Vieja", "prioridad": "ALTA",
        "observaciones_evaluador": "Cercamiento con pedestales inestables, en malas condiciones. Vivienda no garantiza seguridad.",
        "personas": [
            {"nombre": "Karen Garcia", "doc": "41954094", "fecha": "14/10/1982", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Emmanuel Garcia", "doc": "1118293305", "fecha": "14/02/2008", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Junior Sotelo", "doc": "1118310478", "fecha": "20/12/2016", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Lisbet Sotelo", "doc": "1116383908", "fecha": "02/09/2021", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "478", "corregimiento": "San Marcos", "prioridad": "BAJA",
        "observaciones_evaluador": "Vivienda en material, sin afectaciones en el piso. Solo fisuras mínimas. Completamente habitable.",
        "personas": [
            {"nombre": "Damaris Maldonado", "doc": "29980197", "fecha": "02/02/1965", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Sigifredo Arango", "doc": "6552147", "fecha": "15/05/1964", "es_jefe": False, "sexo": "M", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "479", "corregimiento": "San Marcos", "prioridad": "BAJA",
        "observaciones_evaluador": "Vivienda en material con fisuras superficiales de mampostería. Habitable.",
        "personas": [
            {"nombre": "Amanda Arango", "doc": "329980191", "fecha": "31/10/1959", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "480", "corregimiento": "San Marcos", "prioridad": "BAJA",
        "observaciones_evaluador": "Vivienda con fisuras leves en muros de mampostería (ya arreglado). Sin riesgo. Habitable.",
        "personas": [
            {"nombre": "Oliva Oviedo", "doc": "29980191", "fecha": "09/05/1949", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Yanin Miranda", "doc": "6550614", "fecha": "21/08/1985", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "481", "corregimiento": "Buenos Aires", "prioridad": "BAJA",
        "observaciones_evaluador": "Vivienda con tejas caídas y fisuras menores en muros, sin riesgo alguno. Habitable.",
        "personas": [
            {"nombre": "Luis Oviedo", "doc": "6552137", "fecha": "23/04/1962", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Cilia Guevara", "doc": "29019930", "fecha": "05/01/1926", "es_jefe": False, "sexo": "F", "parentesco": "Esposo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "482", "corregimiento": "Alto Dapa", "prioridad": "ALTA",
        "observaciones_evaluador": "Casa en bahareque muy antigua, en muy mal estado. Se recomienda demolerla. Adulto mayor (80 años).",
        "personas": [
            {"nombre": "Marlene Montes", "doc": "29398080", "fecha": "01/01/1946", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "483", "corregimiento": "Alto Dapa", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda de dos pisos con daños por golpe de edificio vecino. Paredes fisuradas y techo con vigas de madera precarias. Se recomienda deshabitar.",
        "personas": [
            {"nombre": "Jenner Ancrea Higuita", "doc": "1118256592", "fecha": "13/12/1987", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Andria Patricia Velez Castro", "doc": "329940041", "fecha": "20/02/1965", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "484", "corregimiento": "Juan Pablo II", "prioridad": "ALTA",
        "observaciones_evaluador": "Estructura rudimentaria construida en materiales livianos. Condiciones precarias de estabilidad y riesgo para ocupantes adultos mayores.",
        "personas": [
            {"nombre": "Ortiz Rodriguez", "doc": "16455013", "fecha": "01/01/1960", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Gloria Carmenza Ramos Mosquera", "doc": "31468850", "fecha": "12/06/1962", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "485", "corregimiento": "Antigua Estancia", "prioridad": "BAJA",
        "observaciones_evaluador": "Vivienda con prioridad baja ya que sufrió afectación en parte de la mampostería.",
        "personas": [
            {"nombre": "Maritza Erlinda Viveros Garcia", "doc": "29979443", "fecha": "11/12/1960", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "486", "corregimiento": "Alto Dapa", "prioridad": "MEDIA",
        "observaciones_evaluador": "Vivienda de un piso antigua con muros altos de 4 metros, machiche y teja de barro. Muro y techo con fisuras, se recomienda cambiar techo de madera y desalojar.",
        "personas": [
            {"nombre": "Dilan Castillo", "doc": "11163761623", "fecha": "08/11/1995", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Lina Maria Castillo Gomez", "doc": "1118305367", "fecha": "13/10/1995", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Jaime Arturo Castillo Gomez", "doc": "1118283771", "fecha": "24/07/1986", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "487", "corregimiento": "Buenos Aires", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda de 2 pisos con terraza, fuertemente afectada con vigas y columnas agrietadas y muros con desprendimientos. Riesgo alto.",
        "personas": [
            {"nombre": "Eduardo Lopez Zuluaga", "doc": "16741416", "fecha": "15/11/1968", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Ana Milena Pacheco Lopez", "doc": "31473742", "fecha": "08/04/2004", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Daniela Lopez Pacheco", "doc": "1109114854", "fecha": "27/07/1967", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Emmanuel Lopez Pacheco", "doc": "1109117750", "fecha": "19/05/2007", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "488", "corregimiento": "Alto Dapa", "prioridad": "BAJA",
        "observaciones_evaluador": "Vivienda de 2 pisos con fisuras en muros, se recomienda reparación de los fisurados.",
        "personas": [
            {"nombre": "Maria Jenny Escarpeta", "doc": "26582494", "fecha": "14/01/1966", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Jose Danilo Sanabria E.", "doc": "13791051", "fecha": "07/02/1967", "es_jefe": False, "sexo": "M", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "James Yesid Sanabria E.", "doc": "111601425", "fecha": "31/03/1991", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Ode David Sanabria E.", "doc": "1116291121", "fecha": "12/09/1994", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "489", "corregimiento": "Montañitas", "prioridad": "MEDIA",
        "observaciones_evaluador": "Vivienda de 1 piso, presenta fisuras en muros y piso de relleno, problemas de asentamiento por pilotes. Requiere evaluación estructural.",
        "personas": [
            {"nombre": "Flor Maria Lozada Molano", "doc": "65715348", "fecha": "23/08/1964", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Daniel Lozada", "doc": "1178289782", "fecha": "27/09/1988", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Solangela Arango Ortiz", "doc": "1118308978", "fecha": "06/09/1997", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Oscar Fabio Lozada Molano", "doc": "1178293492", "fecha": "28/03/1990", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "490", "corregimiento": "Pizarro", "prioridad": "BAJA",
        "observaciones_evaluador": "Vivienda de dos pisos, presenta fisuras menores en mampostería. Se recomienda reparación de fisuras.",
        "personas": [
            {"nombre": "Fraydile Conjal", "doc": "31476145", "fecha": "05/01/1973", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Jefferson Corvaid", "doc": "1118305345", "fecha": "30/10/1992", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Yuberney Muñoz", "doc": "1116377144", "fecha": "15/06/2002", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Wendy Muñoz", "doc": "0", "fecha": "05/05/2006", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "491", "corregimiento": "San Marcos", "prioridad": "BAJA",
        "observaciones_evaluador": "Vivienda en material con fisuras superficiales de mampostería, sin afectaciones en el piso. Habitable.",
        "personas": [
            {"nombre": "Oswaldo Parra", "doc": "5935586", "fecha": "26/06/1987", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Eduardo Parra", "doc": "0", "fecha": "01/01/1960", "es_jefe": False, "sexo": "M", "parentesco": "Otro", "etnia": "Ninguna"},
            {"nombre": "Maria Yalaiva Gutierrez", "doc": "0", "fecha": "01/01/1965", "es_jefe": False, "sexo": "F", "parentesco": "Otro", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "492", "corregimiento": "Amenidia", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda de dos pisos con desplome hacia el frente tras el sismo. Habitable restringido.",
        "personas": [
            {"nombre": "Nolberto Rojas", "doc": "14983152", "fecha": "26/08/1950", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Nubia Edith Sanchez Caballero", "doc": "52545898", "fecha": "18/09/1979", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Diana Carolina Lopez Rojas", "doc": "1007779161", "fecha": "12/01/1999", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Wilmar Dinas Rojas", "doc": "1118295689", "fecha": "27/03/1991", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Enelia Humeridia Bonilla Carabali", "doc": "2762682", "fecha": "13/03/1954", "es_jefe": False, "sexo": "F", "parentesco": "Otro", "etnia": "Ninguna"},
            {"nombre": "Gloria Cecilia Rojas Olave", "doc": "66933239", "fecha": "25/06/1973", "es_jefe": False, "sexo": "F", "parentesco": "Otro", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "493", "corregimiento": "Panorama", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda de 3 niveles con daños severos en columnas, vigas, parales y pisos. Daños graves, no habitable.",
        "personas": [
            {"nombre": "Beatriz Socorro Ramirez Ordoñez", "doc": "869918964", "fecha": "16/01/1977", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Arnd Stiven Garzon Ordoñez", "doc": "1060078088", "fecha": "22/01/2022", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Jorge Armando Herrera Ramirez", "doc": "1144209223", "fecha": "18/10/1996", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "494", "corregimiento": "Panorama", "prioridad": "MEDIA",
        "observaciones_evaluador": "Vivienda de dos pisos con fisuras en muros no estructurales.",
        "personas": [
            {"nombre": "Michael Dayana Aragon", "doc": "1118310384", "fecha": "06/12/1998", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Kylian Joao Sandobal Aragon", "doc": "1118313342", "fecha": "07/04/2023", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "495", "corregimiento": "Panorama", "prioridad": "BAJA",
        "observaciones_evaluador": "Vivienda de dos pisos en pórticos de concreto con fisuras superficiales leves en elementos no estructurales.",
        "personas": [
            {"nombre": "Viviana Ilamo Solarte", "doc": "1118286944", "fecha": "21/06/1987", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Luis Esteban Ramirez", "doc": "1108253265", "fecha": "14/01/2006", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
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
    print("Iniciando ENRIQUECIMIENTO Lote 469-495...")
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
        print(f"MIGRACIÓN LOTE 469-495 EXITOSA.")
        print(f"Formularios -> Creados: {formularios_creados} | Actualizados: {formularios_actualizados}")
        print(f"Personas    -> Insertadas: {personas_creadas} | Actualizadas: {personas_actualizadas}")
        print(f"==================================================")
        
    except Exception as e:
        print(f"Error en BD: {e}")
    finally:
        if 'conn' in locals(): cur.close(); conn.close()

if __name__ == "__main__":
    main()
