import psycopg2
from psycopg2.extras import RealDictCursor
import json

# ==========================================
# 1. CONFIGURACIÓN DE CONEXIONES
# ==========================================
DB_USER = "admin_comunidad"
DB_PASSWORD = "TuPasswordSegura2026!"
DB_HOST = "10.147.17.24" 
DB_PORT = "5432"

DB_BACKUP = {
    "dbname": "sgrd_backup_restore",
    "user": DB_USER,
    "password": DB_PASSWORD,
    "host": DB_HOST,
    "port": DB_PORT
}

DB_PROD = {
    "dbname": "comunidad_db",
    "user": DB_USER,
    "password": DB_PASSWORD,
    "host": DB_HOST,
    "port": DB_PORT
}

def generar_query_insert(tabla, diccionario_fila):
    """Genera un query de INSERT seguro a partir de un diccionario."""
    columnas = list(diccionario_fila.keys())
    valores = []
    
    # Manejar los campos JSONB (diccionarios en Python) para que se inserten correctamente
    for col in columnas:
        val = diccionario_fila[col]
        if isinstance(val, dict):
            valores.append(json.dumps(val))
        else:
            valores.append(val)
            
    nombres_columnas = ", ".join(columnas)
    placeholders = ", ".join(["%s"] * len(columnas))
    
    # Usamos ON CONFLICT DO NOTHING por seguridad extrema
    query = f"INSERT INTO public.{tabla} ({nombres_columnas}) VALUES ({placeholders}) ON CONFLICT DO NOTHING"
    return query, tuple(valores)

def main():
    print("Iniciando proceso de validación y sincronización segura...")
    
    try:
        # Conectar a ambas bases de datos
        conn_backup = psycopg2.connect(**DB_BACKUP)
        conn_prod = psycopg2.connect(**DB_PROD)
        
        # Usamos RealDictCursor para obtener los resultados como diccionarios
        cur_backup = conn_backup.cursor(cursor_factory=RealDictCursor)
        cur_prod = conn_prod.cursor()
        
        # Obtener todos los reportes del backup
        cur_backup.execute("SELECT * FROM public.reportes_comunitarios;")
        reportes_backup = cur_backup.fetchall()
        
        registros_recuperados = 0
        
        for reporte in reportes_backup:
            reporte_id = str(reporte['id'])
            
            # 1. Verificar si el reporte ya existe en la BD de producción
            cur_prod.execute("SELECT 1 FROM public.reportes_comunitarios WHERE id = %s", (reporte_id,))
            existe = cur_prod.fetchone()
            
            if existe:
                # Si ya existe, lo saltamos por completo. Cero alteraciones.
                continue
                
            print(f"-> Registro faltante detectado: {reporte.get('titulo', reporte_id)}. Recuperando...")
            
            # ==========================================
            # 2. INSERTAR EN reportes_comunitarios
            # ==========================================
            query_rep, params_rep = generar_query_insert("reportes_comunitarios", reporte)
            cur_prod.execute(query_rep, params_rep)
            
            # ==========================================
            # 3. RECUPERAR E INSERTAR rufe_formularios
            # ==========================================
            cur_backup.execute("SELECT * FROM public.rufe_formularios WHERE reporte_id = %s", (reporte_id,))
            formularios = cur_backup.fetchall()
            
            for form in formularios:
                form_id = form['id']
                query_form, params_form = generar_query_insert("rufe_formularios", form)
                cur_prod.execute(query_form, params_form)
                
                # ==========================================
                # 4. RECUPERAR E INSERTAR rufe_personas
                # ==========================================
                cur_backup.execute("SELECT * FROM public.rufe_personas WHERE rufe_formulario_id = %s", (form_id,))
                personas = cur_backup.fetchall()
                for persona in personas:
                    query_pers, params_pers = generar_query_insert("rufe_personas", persona)
                    cur_prod.execute(query_pers, params_pers)
                    
            # ==========================================
            # 5. RECUPERAR E INSERTAR reportes_comunitarios_rufe
            # ==========================================
            cur_backup.execute("SELECT * FROM public.reportes_comunitarios_rufe WHERE id = %s", (reporte_id,))
            reportes_unificados = cur_backup.fetchall()
            
            for rep_uni in reportes_unificados:
                query_uni, params_uni = generar_query_insert("reportes_comunitarios_rufe", rep_uni)
                cur_prod.execute(query_uni, params_uni)
                
            # Guardamos los cambios de esta iteración
            conn_prod.commit()
            registros_recuperados += 1
            
        print(f"\nProceso finalizado. Se recuperaron exitosamente {registros_recuperados} solicitudes faltantes.")

    except Exception as e:
        # Si ocurre un error, hacemos rollback automático en producción para no dejar datos a medias
        if 'conn_prod' in locals():
            conn_prod.rollback()
        print(f"\n[ERROR] Ocurrió un problema durante la sincronización: {e}")
        
    finally:
        if 'conn_backup' in locals():
            cur_backup.close()
            conn_backup.close()
        if 'conn_prod' in locals():
            cur_prod.close()
            conn_prod.close()

if __name__ == "__main__":
    main()
