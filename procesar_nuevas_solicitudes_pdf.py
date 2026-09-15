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
        "descripcion": "Solicitud de revisión por afectaciones post-sismo.",
        "sector_barrio": "La Estancia",
        "direccion": "Cra 14 #22-57",
        "nombre_ciudadano": "Maria Crecencia Gaviria / Manuel Capitia",
        "cedula": "136992",
        "telefono": "3012442336"
    },
    {
        "descripcion": "Solicitud de evaluación por sismo.",
        "sector_barrio": "Bocazur",
        "direccion": "Calle 7 #3-13",
        "nombre_ciudadano": "Maria Victoria Lopez",
        "cedula": "31470994",
        "telefono": "3164215264"
    },
    {
        "descripcion": "Revisión en torre de propiedad horizontal.",
        "sector_barrio": "Parques de Pinar",
        "direccion": "Calle 20 #11-30 Torre 5 Apto 606",
        "nombre_ciudadano": "Sandra Milena Betancourth Gomez",
        "cedula": "29105786",
        "telefono": "3176408900"
    },
    {
        "descripcion": "Inspección de vivienda por daños.",
        "sector_barrio": "Las Cruces",
        "direccion": "Calle 20 #12-20",
        "nombre_ciudadano": "Angie Lorene Guacanem Gonzalez",
        "cedula": "1014219688",
        "telefono": "3138736674"
    },
    {
        "descripcion": "Revisión de instalaciones corporativas.",
        "sector_barrio": "Cencar",
        "direccion": "Cl 14B #20 #10 Bloque Oficina 206",
        "nombre_ciudadano": "Lina Maria Lopez (SI SA CARGO)",
        "cedula": "1118308613",
        "telefono": "3043130388"
    },
    {
        "descripcion": "Revisión en conjunto residencial.",
        "sector_barrio": "Guabinas",
        "direccion": "Calle 8 #20A-37 Torre 8 Piso 10 Apto 1005",
        "nombre_ciudadano": "Alexander Velasco",
        "cedula": "16796466",
        "telefono": "3206965568"
    },
    {
        "descripcion": "Revisión por afectación estructural menor.",
        "sector_barrio": "Guacanda",
        "direccion": "Cl 15AN #1A-79",
        "nombre_ciudadano": "Ligia Perez Roman",
        "cedula": "31970669",
        "telefono": "3128640462"
    },
    {
        "descripcion": "Revisión de predio en zona rural.",
        "sector_barrio": "Mulalo",
        "direccion": "Carrera 60 #5-240",
        "nombre_ciudadano": "Emerita Navia",
        "cedula": "38840038",
        "telefono": "3113535872"
    },
    {
        "descripcion": "Atención urgente por afectaciones.",
        "sector_barrio": "Panorama",
        "direccion": "Calle 18B #24",
        "nombre_ciudadano": "Brenda Lucia Montilla",
        "cedula": "31478856",
        "telefono": "3135104900"
    },
    {
        "descripcion": "Inspección post-sismo en urbanización.",
        "sector_barrio": "KaaNZana 1",
        "direccion": "Calle 14A #15N-36 Segunda Etapa",
        "nombre_ciudadano": "Marina Taisa",
        "cedula": "6877631",
        "telefono": "3218744840"
    },
    {
        "descripcion": "Revisión de vivienda en ladera.",
        "sector_barrio": "Uribe Parte Alta",
        "direccion": "Calle 9 #12-57",
        "nombre_ciudadano": "Etudier Garcia",
        "cedula": "16785110",
        "telefono": "3183346068"
    }
]

def main():
    print("Iniciando procesamiento de nuevas solicitudes del documento...")
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        registrados = 0
        duplicados_o_rufe = 0
        
        for sol in NUEVAS_SOLICITUDES:
            ced = sol.get("cedula")
            nom = sol["nombre_ciudadano"]
            tel = sol.get("telefono")
            dir_ref = sol.get("direccion")
            
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
                print(f"[!] Solicitud para '{nom}' (CC: {ced}) OMITIDA: Ya cuenta con registro previo o RUFE asociado.")
                duplicados_o_rufe += 1
                continue
                
            rep_id = str(uuid.uuid4())
            titulo_oficial = f"Solicitud - {nom} (CC: {ced})"
            
            datos_extra = {
                "nombre": nom,
                "cedula": ced,
                "telefono": tel,
                "direccion": dir_ref,
                "origen": "documento_solicitudes_08_09_2026"
            }
            
            cur.execute("""
                INSERT INTO public.reportes_comunitarios 
                (id, titulo, descripcion_detallada, sector_barrio, direccion_referencia, estado_actual, datos_extra, procesado_rufe, migrado_rufe, activo)
                VALUES (%s, %s, %s, %s, %s, 'PENDIENTE', %s, false, false, true)
            """, (
                rep_id,
                titulo_oficial,
                sol["descripcion"],
                sol.get("sector_barrio"),
                dir_ref,
                json.dumps(datos_extra)
            ))
            
            print(f"[+] Solicitud para '{nom}' registrada como PENDIENTE con título optimizado.")
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
