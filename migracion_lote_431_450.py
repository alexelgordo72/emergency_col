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
        "num_formulario": "431", "corregimiento": "Bolivar", "prioridad": "BAJA",
        "observaciones_evaluador": "Desprendimiento de cubierta metálica y muro de cerramiento perimetral.",
        "personas": [
            {"nombre": "Ailey Martinez", "doc": "1118292819", "fecha": "01/01/1990", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "432", "corregimiento": "Trinidad 1", "prioridad": "MEDIA",
        "observaciones_evaluador": "Casa de 3 pisos. 3er piso: muro lateral sobre escaleras con desprendimiento, muro suelto sobre la viga.",
        "personas": [
            {"nombre": "Sandra Alegria Cortes", "doc": "66987696", "fecha": "22/11/1964", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Hoover Agudelo Alegria", "doc": "1118307858", "fecha": "14/03/1990", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Laura Camila Agudelo Gonzalez", "doc": "1232823541", "fecha": "08/08/1999", "es_jefe": False, "sexo": "F", "parentesco": "Nieto(a)", "etnia": "Ninguna"},
            {"nombre": "Daniela Alejandra Taborda Velasco", "doc": "1105384328", "fecha": "11/09/2015", "es_jefe": False, "sexo": "F", "parentesco": "Nieto(a)", "etnia": "Ninguna"},
            {"nombre": "Melany Barrera Velasco", "doc": "1109196820", "fecha": "22/06/2017", "es_jefe": False, "sexo": "F", "parentesco": "Nieto(a)", "etnia": "Ninguna"},
            {"nombre": "Daniel Esteban Agudelo Gonzalez", "doc": "12328089226", "fecha": "02/02/2021", "es_jefe": False, "sexo": "M", "parentesco": "Nieto(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "433", "corregimiento": "San Marcos", "prioridad": "BAJA",
        "observaciones_evaluador": "Vivienda en material con fisuras menores en muros. No existen más riesgos en la finca. Es habitable.",
        "personas": [
            {"nombre": "Juan Carlos Vinazco", "doc": "94316151", "fecha": "27/03/1973", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Marker Fernando Fuentes Sanchez", "doc": "27601425", "fecha": "22/12/1998", "es_jefe": False, "sexo": "M", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "434", "corregimiento": "San Marcos", "prioridad": "BAJA",
        "observaciones_evaluador": "Vivienda con fisuras menores y colapso de muro de un galpón. Completamente habitable.",
        "personas": [
            {"nombre": "Elvery Rios Murillo", "doc": "31497654", "fecha": "09/02/1973", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Maria Camila Quirama Rios", "doc": "1007503763", "fecha": "19/10/1999", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Kloe Cordoba Quirama", "doc": "1116383387", "fecha": "25/12/2020", "es_jefe": False, "sexo": "F", "parentesco": "Nieto(a)", "etnia": "Ninguna"},
            {"nombre": "Nicolas David Quirama", "doc": "1118307809", "fecha": "02/12/1996", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Arcesio de Jesus Quirama", "doc": "7230847", "fecha": "09/06/1965", "es_jefe": False, "sexo": "M", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "435", "corregimiento": "San Marcos", "prioridad": "BAJA",
        "observaciones_evaluador": "Vivienda en material, con afectaciones en el soporte de la cubierta, ya fue intervenida. Casa habitable.",
        "personas": [
            {"nombre": "Ana Buitrago", "doc": "316636538", "fecha": "08/08/1955", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Wilson Buitrago", "doc": "0", "fecha": "01/01/1950", "es_jefe": False, "sexo": "M", "parentesco": "Otro", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "436", "corregimiento": "San Marcos", "prioridad": "BAJA",
        "observaciones_evaluador": "Vivienda con desprendimiento de pañete y muro parcialmente colapsado.",
        "personas": [
            {"nombre": "Gregorio Cespedes", "doc": "94373275", "fecha": "19/04/1972", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Nubia Edith Sanchez Caballero", "doc": "52545898", "fecha": "18/09/1979", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Anna Sophia Cespedes Sanchez", "doc": "1109671336", "fecha": "22/08/2009", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "437", "corregimiento": "San Marcos", "prioridad": "MEDIA",
        "observaciones_evaluador": "Vivienda en bahareque y prefabricado con grandes dilataciones en juntas y pequeños desprendimientos. Es habitable.",
        "personas": [
            {"nombre": "Angel Antonio Vergara", "doc": "16445571", "fecha": "19/03/1947", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Maria Lida Prado Gomez", "doc": "41718545", "fecha": "20/09/1956", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "438", "corregimiento": "Finlandia", "prioridad": "MEDIA",
        "observaciones_evaluador": "Vivienda en material con dos muros perimetrales desplomados, pero elementos estructurales en buen estado.",
        "personas": [
            {"nombre": "Carlos Pedroza", "doc": "94509544", "fecha": "23/10/1977", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Jean Carlo Pedroza", "doc": "1104835091", "fecha": "23/07/2014", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "439", "corregimiento": "Panorama", "prioridad": "BAJA",
        "observaciones_evaluador": "Sin afectaciones por sismo. 1 muro colindante en riesgo de colapso por láminas de zinc del colegio vecino.",
        "personas": [
            {"nombre": "Maria Quintana", "doc": "11089800192", "fecha": "14/10/1994", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Cristofer Sandobal", "doc": "1232815483", "fecha": "21/03/2021", "es_jefe": False, "sexo": "M", "parentesco": "Nieto(a)", "etnia": "Ninguna"},
            {"nombre": "Celeste Sandobal", "doc": "11411701777", "fecha": "18/02/2018", "es_jefe": False, "sexo": "F", "parentesco": "Nieto(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "440", "corregimiento": "San Marcos", "prioridad": "BAJA",
        "observaciones_evaluador": "Vivienda en material, baño desprendido y fisuras mínimas en juntas de muro.",
        "personas": [
            {"nombre": "Jorge Olmedo Escobar", "doc": "94362372", "fecha": "22/09/1984", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Ines Sanchez", "doc": "31894875", "fecha": "08/03/1963", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Cristian Camilo Escobar", "doc": "11163755089", "fecha": "18/08/2009", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "441", "corregimiento": "San Marcos", "prioridad": "MEDIA",
        "observaciones_evaluador": "Vivienda en material con fisuras en muros de mampostería y desplome parcial de la cocina.",
        "personas": [
            {"nombre": "Ninfa Amparo Burbano", "doc": "29980171", "fecha": "26/07/1963", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Nicol Valeria Mesa Prado", "doc": "1118256225", "fecha": "28/08/2004", "es_jefe": False, "sexo": "F", "parentesco": "Nieto(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "442", "corregimiento": "San Marcos", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda construida en bahareque. Muros divisorios colapsados, sin posibilidad de habitar.",
        "personas": [
            {"nombre": "Horacio Silva Martinez", "doc": "94360969", "fecha": "23/08/1972", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "443", "corregimiento": "Uribe", "prioridad": "BAJA",
        "observaciones_evaluador": "Edificio con afectaciones menores en el cielo raso, fisuras en paredes de baño y pequeña fisura en una viga.",
        "personas": [
            {"nombre": "Harold Reyes", "doc": "16774969", "fecha": "12/05/1970", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Luz Elena Sierra", "doc": "63489613", "fecha": "23/12/1973", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Santiago Reyes", "doc": "1007489384", "fecha": "18/10/2000", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Isabela Reyes", "doc": "1007541793", "fecha": "15/01/2003", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "444", "corregimiento": "San Jose", "prioridad": "MEDIA",
        "observaciones_evaluador": "Vivienda a dintel pared habitable.",
        "personas": [
            {"nombre": "Gildardo Prado", "doc": "6550037", "fecha": "01/01/1950", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Magnolia Gaviria", "doc": "0", "fecha": "01/01/1950", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Javier Prado", "doc": "0", "fecha": "01/01/1950", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Harry Prado", "doc": "0", "fecha": "01/01/1950", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Monica Prado", "doc": "0", "fecha": "01/01/1950", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "445", "corregimiento": "Montañitas", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda en bahareque. Se presentan fisuras y riesgo inminente de colapso estructural.",
        "personas": [
            {"nombre": "Victor Manuel Salazar", "doc": "6340964", "fecha": "01/01/1950", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Aurora Meneses", "doc": "29398859", "fecha": "01/01/1950", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Elmer Salazar", "doc": "6340300", "fecha": "01/01/1950", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "446", "corregimiento": "Montañitas", "prioridad": "MEDIA",
        "observaciones_evaluador": "Vivienda de bahareque para colapsar en partes.",
        "personas": [
            {"nombre": "Maricela Herrera", "doc": "38964579", "fecha": "01/01/1950", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Naiva Sinisterra", "doc": "31476267", "fecha": "01/01/1950", "es_jefe": False, "sexo": "F", "parentesco": "Otro", "etnia": "Ninguna"},
            {"nombre": "Natividad Garcia", "doc": "25719516", "fecha": "01/01/1950", "es_jefe": False, "sexo": "F", "parentesco": "Otro", "etnia": "Ninguna"},
            {"nombre": "Isidoro Gaviria", "doc": "14962877", "fecha": "01/01/1950", "es_jefe": False, "sexo": "M", "parentesco": "Otro", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "447", "corregimiento": "Santa Ines", "prioridad": "MEDIA",
        "observaciones_evaluador": "Vivienda de bahareque con fisuras por desplazamiento de suelos. Se recomienda demolición de muros afectados.",
        "personas": [
            {"nombre": "Javier Bernal", "doc": "16450369", "fecha": "01/01/1950", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Diego Llanos", "doc": "0", "fecha": "01/01/1950", "es_jefe": False, "sexo": "M", "parentesco": "Otro", "etnia": "Ninguna"},
            {"nombre": "Fernando Llanos", "doc": "0", "fecha": "01/01/1950", "es_jefe": False, "sexo": "M", "parentesco": "Otro", "etnia": "Ninguna"},
            {"nombre": "Mauricio Llanos", "doc": "0", "fecha": "01/01/1950", "es_jefe": False, "sexo": "M", "parentesco": "Otro", "etnia": "Ninguna"},
            {"nombre": "Amparo Villegas", "doc": "0", "fecha": "01/01/1950", "es_jefe": False, "sexo": "F", "parentesco": "Otro", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "448", "corregimiento": "Montañitas", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda en material totalmente colapsada. Inhabitable.",
        "personas": [
            {"nombre": "Abel Alvarado", "doc": "6535560", "fecha": "15/12/1950", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Luz Mary Cruz", "doc": "29739886", "fecha": "11/10/1961", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Diana Ilcia Alvarado", "doc": "1114487509", "fecha": "09/03/1992", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Maria Alejandra Ocampo", "doc": "1116378977", "fecha": "15/04/2015", "es_jefe": False, "sexo": "F", "parentesco": "Nieto(a)", "etnia": "Ninguna"},
            {"nombre": "Hellen Alexandra Alvarado", "doc": "1109940021", "fecha": "02/11/2023", "es_jefe": False, "sexo": "F", "parentesco": "Nieto(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "449", "corregimiento": "Montañitas", "prioridad": "MEDIO",
        "observaciones_evaluador": "Vivienda conformada en bahareque, 50% colapsada. Cubierta en deterioro 100%.",
        "personas": [
            {"nombre": "Hector Edi Morales Mendez", "doc": "6341279", "fecha": "01/01/1950", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Rubilma Garzon Prado", "doc": "79976097", "fecha": "01/01/1950", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "450", "corregimiento": "Montañitas", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda en bahareque colapsada en un 80% con techo de zinc sin estabilidad.",
        "personas": [
            {"nombre": "Teobaldo Collazos", "doc": "14576614", "fecha": "01/01/1950", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Jakeline del Socorro Barreto", "doc": "29581649", "fecha": "01/01/1950", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    }
]

def calcular_edad_2026(fecha_str):
    match = re.search(r'(19\d{2}|20\d{2})', str(fecha_str))
    if match:
        return 2026 - int(match.group(1))
    return None

def main():
    print("Iniciando ENRIQUECIMIENTO FINAL Lote 431-450...")
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        conn.autocommit = True
        cur = conn.cursor()
        
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
                    SET prioridad = %s, observaciones_evaluador = %s
                    WHERE id = %s;
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
                
                cur.execute("SELECT id FROM public.rufe_personas WHERE REPLACE(documento_identidad, '.', '') = %s", (p["doc"],))
                res_persona = cur.fetchone()
                
                if res_persona:
                    persona_id = res_persona[0]
                    cur.execute("""
                        UPDATE public.rufe_personas 
                        SET fecha_nacimiento = %s, edad = %s, es_jefe_hogar = %s, parentesco = %s, sexo = %s, etnia = %s
                        WHERE id = %s;
                    """, (p["fecha"], edad_calc, p["es_jefe"], p["parentesco"], p["sexo"], p["etnia"], persona_id))
                    personas_actualizadas += 1
                else:
                    cur.execute("""
                        INSERT INTO public.rufe_personas 
                        (rufe_formulario_id, nombre_completo, documento_identidad, fecha_nacimiento, edad, es_jefe_hogar, parentesco, sexo, etnia)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (form_id, p["nombre"], p["doc"], p["fecha"], edad_calc, p["es_jefe"], p["parentesco"], p["sexo"], p["etnia"]))
                    personas_creadas += 1

        print(f"\n==================================================")
        print(f"MIGRACIÓN LOTE FINAL EXITOSA.")
        print(f"Formularios -> Creados: {formularios_creados} | Actualizados: {formularios_actualizados}")
        print(f"Personas    -> Insertadas: {personas_creadas} | Actualizadas: {personas_actualizadas}")
        print(f"==================================================")
        
    except Exception as e:
        print(f"Error en BD: {e}")
    finally:
        if 'conn' in locals(): cur.close(); conn.close()

if __name__ == "__main__":
    main()
