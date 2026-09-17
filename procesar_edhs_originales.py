import psycopg2

DB_CONFIG = {
    "dbname": "comunidad_db",
    "user": "admin_comunidad",
    "password": "TuPasswordSegura2026!",
    "host": "10.147.17.24",
    "port": "5432"
}

DATOS_EDHS = [
    {
        "formulario_edhs": "256",
        "cedula": "7494927",
        "evaluador": "Iris D Semanate",
        "prioridad": "ALTA",
        "recomendacion": "[EDHS-256] Restricción Parcial. Reparación de cubierta. Pared de bahareque resentida con posible caída."
    },
    {
        "formulario_edhs": "255",
        "cedula": "25417115",
        "evaluador": "Gerson Rivera D.",
        "prioridad": "ALTA - EVACUACIÓN",
        "recomendacion": "[EDHS-255] Riesgo inminente de colapso. Evacuar vivienda. Demolición de muros divisorios y reparación de cubierta."
    }
]

def main():
    print("Iniciando inyección de EDHS a las tablas ORIGINALES...")
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        conn.autocommit = True
        cur = conn.cursor()
        
        actualizados = 0
        
        for eval_tecnica in DATOS_EDHS:
            cedula = eval_tecnica["cedula"]
            
            # 1. Buscar a la persona en la tabla original para obtener el ID de su formulario
            cur.execute("""
                SELECT rufe_formulario_id FROM public.rufe_personas 
                WHERE REPLACE(REPLACE(documento_identidad, '.', ''), ' ', '') = %s
                LIMIT 1;
            """, (cedula,))
            
            resultado = cur.fetchone()
            
            if resultado:
                form_id = resultado[0]
                
                # 2. Actualizar el formulario original con los datos del ingeniero
                cur.execute("""
                    UPDATE public.rufe_formularios 
                    SET observaciones_evaluador = %s, ingeniero_evaluador = %s, prioridad = %s
                    WHERE id = %s;
                """, (eval_tecnica["recomendacion"], eval_tecnica["evaluador"], eval_tecnica["prioridad"], form_id))
                
                actualizados += 1
                print(f"[+] EDHS #{eval_tecnica['formulario_edhs']} vinculado exitosamente a la C.C. {cedula}")
            else:
                print(f"[-] C.C. {cedula} no encontrada en la tabla 'rufe_personas'.")
                
        print("\n==================================================")
        print(f"PROCESO FINALIZADO. Formularios actualizados: {actualizados}")
        print("==================================================")
        
    except Exception as e:
        print(f"Error en la base de datos: {e}")
    finally:
        if 'conn' in locals():
            cur.close()
            conn.close()

if __name__ == "__main__":
    main()
