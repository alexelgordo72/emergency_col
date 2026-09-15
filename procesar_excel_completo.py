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

NUEVAS_SOLICITUDES = [
    {
        "nombre": "Servicold me sas",
        "cedula": None,
        "telefono": "3234132848",
        "direccion": "cra 34 10-300",
        "barrio_vereda": "ARROYOHONDO",
        "observaciones": "EMPRESA"
    },
    {
        "nombre": "ANA MIRIAN",
        "cedula": None,
        "telefono": "3223859787",
        "direccion": "CRA 7 #4-29",
        "barrio_vereda": "BELALCAZAR",
        "observaciones": ""
    },
    {
        "nombre": "CRISTELIA MUÑOZ",
        "cedula": "38710079",
        "telefono": "3044833368 - 3008781124",
        "direccion": "CALLE 9 #4-30",
        "barrio_vereda": "BELALCAZAR",
        "observaciones": ""
    },
    {
        "nombre": "milton cesar montilla rios",
        "cedula": None,
        "telefono": "3234810818",
        "direccion": "calle 6N #8-68",
        "barrio_vereda": "BELLAVISTA",
        "observaciones": "REPORTA LLAMAR CON TIEMPO PARA LA VISITA"
    },
    {
        "nombre": "BLANCA NELLY MORALES",
        "cedula": "31467775",
        "telefono": "3187754242",
        "direccion": "CALLE 8 #12-100",
        "barrio_vereda": "Buenos aires",
        "observaciones": ""
    },
    {
        "nombre": "luz edy ospina",
        "cedula": None,
        "telefono": "3216266210",
        "direccion": "calle 10 #14-26",
        "barrio_vereda": "Buenos aires",
        "observaciones": ""
    },
    {
        "nombre": "JUAN GULLERMO GUERRA",
        "cedula": None,
        "telefono": "3006125937",
        "direccion": "CALLE 11 OESTE 2N-53",
        "barrio_vereda": "CAMPESTRE REAL",
        "observaciones": ""
    },
    {
        "nombre": "mireya campo castillo - sandra esperanza",
        "cedula": None,
        "telefono": "3167581140 - 3233762691",
        "direccion": "CALLE 9 #20B-404 TORRE I",
        "barrio_vereda": "Ciudad Guabinas",
        "observaciones": "PRPIETARIA MIREYA CAMPO- ARRENDATARIA SANDRA ESPERANZA"
    },
    {
        "nombre": "KEVIN STIVEN CEPEDA FLOREZ",
        "cedula": None,
        "telefono": "3176587597",
        "direccion": "CRA 20A #6-93 APTO 101 TORRE 1",
        "barrio_vereda": "Ciudad Guabinas",
        "observaciones": "conjunto residencial macondo"
    },
    {
        "nombre": "JEIMY JULIETH SEGURA ESPAÑA",
        "cedula": "1113626155",
        "telefono": "3186086447",
        "direccion": "CALLE 7 #20A 110 APTO 1001 TORRE 2",
        "barrio_vereda": "Ciudad Guabinas",
        "observaciones": "APTO 1001 TORRE 2"
    },
    {
        "nombre": "LEIDY AVILA BEJARANO",
        "cedula": None,
        "telefono": "3235015370",
        "direccion": "Casa 14, Manzana 3, Nuevo Vivir Pedregal",
        "barrio_vereda": "CORREGIMIENTO PEDREGAL",
        "observaciones": "CASA 14 MANZANA 3"
    },
    {
        "nombre": "Maria del socorro rodriguez",
        "cedula": None,
        "telefono": "3225127345",
        "direccion": "DAPA CALLE DE LAS FLORES",
        "barrio_vereda": "DAPA",
        "observaciones": "CASA LAS CRISALIDAS"
    },
    {
        "nombre": "luz marina ospina",
        "cedula": None,
        "telefono": "3145128242",
        "direccion": "pilas de dapa casa 68",
        "barrio_vereda": "dapa",
        "observaciones": ""
    },
    {
        "nombre": "sonia maria del pilar",
        "cedula": None,
        "telefono": "3145128242",
        "direccion": "pilas de dapa",
        "barrio_vereda": "dapa",
        "observaciones": ""
    },
    {
        "nombre": "constanza ospina",
        "cedula": None,
        "telefono": "3145128242",
        "direccion": "kilometro 2 via a dapa",
        "barrio_vereda": "dapa",
        "observaciones": ""
    },
    {
        "nombre": "MARIBEL BAENA",
        "cedula": None,
        "telefono": "3236213869",
        "direccion": "CALLE 15B #2-41",
        "barrio_vereda": "FRAYPEÑA",
        "observaciones": "ADULTO MAYOR"
    },
    {
        "nombre": "JOHAN GILBERTO PANTOJA",
        "cedula": None,
        "telefono": "3104405970",
        "direccion": "CRA 18E#7-26",
        "barrio_vereda": "GUABINAS",
        "observaciones": "APTO 102 TORRE 21 CONJUTO TAIRONA"
    },
    {
        "nombre": "ANAGELLY MORENO",
        "cedula": None,
        "telefono": "3225190460",
        "direccion": "DIRECCION 14D",
        "barrio_vereda": "JUAN PABLO",
        "observaciones": "MURO DE CONTENCION CONSTRUIDO POR LA ALCALDIA"
    },
    {
        "nombre": "luz estela daza",
        "cedula": None,
        "telefono": "3113283818",
        "direccion": "cra 2 #14-19",
        "barrio_vereda": "la trinidad",
        "observaciones": ""
    },
    {
        "nombre": "luisa fernanda",
        "cedula": None,
        "telefono": "3502723499",
        "direccion": "cra 3n #1-44",
        "barrio_vereda": "las vegas",
        "observaciones": ""
    },
    {
        "nombre": "Gladis Orozco",
        "cedula": None,
        "telefono": "3174597921",
        "direccion": "por la tiena los amigos",
        "barrio_vereda": "panorama",
        "observaciones": ""
    },
    {
        "nombre": "CAMILA SALAZAR",
        "cedula": None,
        "telefono": "3148217679",
        "direccion": "CRA 17 #6A-37",
        "barrio_vereda": "panorama",
        "observaciones": ""
    },
    {
        "nombre": "LILIANA FLOR CORDOBA",
        "cedula": None,
        "telefono": "3127886014",
        "direccion": "CALLE 20 9A 13",
        "barrio_vereda": "PARQUES DEL PINAR",
        "observaciones": ""
    },
    {
        "nombre": "ANA LUCIA CONDE CONDE",
        "cedula": None,
        "telefono": "3235527184",
        "direccion": "SAN MARCOS-VEREDA MANGA VIEJA",
        "barrio_vereda": "SAN MARCOS",
        "observaciones": "FINCA LA ISABELA"
    },
    {
        "nombre": "Roberto sanchez barrera",
        "cedula": None,
        "telefono": "3136672994 - 3208011769",
        "direccion": "cra 11 #7-33",
        "barrio_vereda": "uribe",
        "observaciones": "2 adultos mayores"
    },
    {
        "nombre": "MARIA AIDEE ZUÑIGA",
        "cedula": "31474797",
        "telefono": "3103606772",
        "direccion": "CALLE 11 9-23",
        "barrio_vereda": "uribe",
        "observaciones": ""
    }
]

def main():
    print("Iniciando procesamiento de solicitudes desde el reporte Excel...")
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        registrados = 0
        duplicados_o_rufe = 0
        
        for sol in NUEVAS_SOLICITUDES:
            nom = sol["nombre"]
            ced = sol["cedula"]
            tel = sol["telefono"]
            dir_ref = sol["direccion"]
            barrio = sol["barrio_vereda"]
            obs = sol["observaciones"]
            
            # Validación de duplicados o RUFE previo
            cur.execute("""
                SELECT id, titulo, procesado_rufe, datos_extra 
                FROM public.reportes_comunitarios 
                WHERE activo = true 
                  AND (
                    (datos_extra->>'cedula' = %s AND %s IS NOT NULL) OR
                    (titulo ILIKE %s) OR
                    (direccion_referencia ILIKE %s AND %s IS NOT NULL)
                  )
            """, (ced, ced, f"%{nom}%", dir_ref, dir_ref))
            
            existente = cur.fetchone()
            
            if existente:
                print(f"[!] Solicitud para '{nom}' OMITIDA: Ya cuenta con registro previo o RUFE asociado.")
                duplicados_o_rufe += 1
                continue
                
            rep_id = str(uuid.uuid4())
            ced_str = f" (CC: {ced})" if ced else ""
            titulo_oficial = f"Solicitud - {nom}{ced_str}"
            
            descripcion = f"Observaciones: {obs}" if obs else "Solicitud reportada vía WhatsApp/Celular SGRD."
            
            datos_extra = {
                "nombre": nom,
                "cedula": ced,
                "telefono": tel,
                "direccion": dir_ref,
                "barrio_vereda": barrio,
                "observaciones": obs,
                "origen": "excel_reportes_wp_cel_sgrd_08_09_2026"
            }
            
            cur.execute("""
                INSERT INTO public.reportes_comunitarios 
                (id, titulo, descripcion_detallada, sector_barrio, direccion_referencia, estado_actual, datos_extra, procesado_rufe, migrado_rufe, activo)
                VALUES (%s, %s, %s, %s, %s, 'PENDIENTE', %s, false, false, true)
            """, (
                rep_id,
                titulo_oficial,
                descripcion,
                barrio,
                dir_ref,
                json.dumps(datos_extra)
            ))
            
            print(f"[+] Solicitud para '{nom}' registrada como PENDIENTE.")
            registrados += 1
            
        conn.commit()
        print("\n" + "="*45)
        print(f"Proceso finalizado. Nuevas solicitudes registradas: {registrados} | Omitidas (Duplicadas): {duplicados_o_rufe}")
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
