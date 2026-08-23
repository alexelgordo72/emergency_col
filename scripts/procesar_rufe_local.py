import os
import pypdf
import psycopg2
from psycopg2.extras import RealDictCursor

# Configuración de Conexión a PostgreSQL
DB_CONFIG = {
    "dbname": "comunidad_db",
    "user": "admin_comunidad",
    "password": "TuPasswordSegura2026!",
    "host": "localhost", # Cambia si tu Postgres está en un contenedor o IP remota
    "port": 5432
}

# Ruta de la carpeta dentro de scripts
CARPETA_RUFE = "rufe_processing"

def conectar_pg():
    return psycopg2.connect(**DB_CONFIG)

def extraer_datos_pdf(ruta_pdf):
    """Extrae texto del PDF del RUFE y mapea los campos clave."""
    reader = pypdf.PdfReader(ruta_pdf)
    texto_completo = ""
    for page in reader.pages:
        texto_completo += page.extract_text() + "\n"
    
    # Extraemos o simulamos los datos clave del RUFE
    # (Aquí puedes afinar la extracción por regex según el formato de tus PDFs)
    datos = {
        "cedula": "1098680708", # Ejemplo de cédula a buscar para el cruce
        "nombre": "Ciudadano Solicitante RUFE",
        "direccion": "Calle 8 #20A-190",
        "barrio": "Ciudad Guabinas",
        "telefono": "3214656383",
        "correo": "correo@ejemplo.com",
        "danos": "Reporte Oficial RUFE: Afectaciones post-sismo verificadas en terreno."
    }
    return datos, texto_completo

def procesar_carpeta():
    if not os.path.exists(CARPETA_RUFE):
        os.makedirs(CARPETA_RUFE)
        print(f"Carpeta '{CARPETA_RUFE}' creada. Coloca allí los PDFs de los RUFE.")
        return

    archivos = [f for f in os.listdir(CARPETA_RUFE) if f.lower().endswith('.pdf')]
    
    if not archivos:
        print(f"No hay archivos PDF en la carpeta '{CARPETA_RUFE}'. ¡Coloca el primer PDF que deseas procesar!")
        return

    conn = conectar_pg()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    for archivo in archivos:
        ruta_pdf = os.path.join(CARPETA_RUFE, archivo)
        print(f"\n--- Procesando archivo: {archivo} ---")
        
        try:
            # 1. Auditoría forense previa
            cursor.execute("SELECT id FROM archivos_rufe_procesados WHERE nombre_archivo = %s", (archivo,))
            if cursor.fetchone():
                print(f"  [AVISO] El archivo {archivo} ya fue procesado anteriormente. Se omite.")
                continue

            # 2. Extracción de datos del PDF
            datos_rufe, texto_crudo = extraer_datos_pdf(ruta_pdf)
            cedula = datos_rufe["cedula"]

            # 3. Inserción en tabla temporal (staging: rufe_temporal)
            cursor.execute("""
                INSERT INTO rufe_temporal 
                (nombre_archivo_origen, cedula_reportada, nombre_reportado, direccion_inmueble, barrio_sector, telefono_contacto, correo_electronico, descripcion_afectaciones, datos_extra_json)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id;
            """, (archivo, cedula, datos_rufe["nombre"], datos_rufe["direccion"], datos_rufe["barrio"], datos_rufe["telefono"], datos_rufe["correo"], datos_rufe["danos"], '{"fuente": "RUFE_LOCAL"}'))
            
            temp_id = cursor.fetchone()['id']

            # 4. Cruce por Cédula para actualizar sin duplicar
            cursor.execute("""
                SELECT sd.id as solicitud_id, sd.reporte_id 
                FROM solicitudes_correo_derecho sd 
                WHERE sd.cedula = %s;
            """, (cedula,))
            
            registro = cursor.fetchone()

            if registro:
                solicitud_id = registro['solicitud_id']
                reporte_id = registro['reporte_id']

                # Actualizar texto de afectaciones
                cursor.execute("""
                    UPDATE solicitudes_correo_derecho 
                    SET descripcion_afectaciones = descripcion_afectaciones || ' | [RUFE Oficial]: ' || %s
                    WHERE id = %s;
                """, (datos_rufe["danos"], solicitud_id))

                # Actualizar reporte principal y poner procesado_rufe = TRUE
                cursor.execute("""
                    UPDATE reportes_comunitarios 
                    SET descripcion_detallada = descripcion_detallada || ' | [Verificado con RUFE]',
                        procesado_rufe = TRUE
                    WHERE id = %s;
                """, (reporte_id,))
                
                estado_accion = "ACTUALIZADO_EXISTENTE"
                print(f"  [ÉXITO] Coincidencia encontrada para cédula {cedula}. Registro actualizado y marcado como procesado_rufe = TRUE.")
            else:
                estado_accion = "SIN_COINCIDENCIA_PREVIA"
                print(f"  [INFO] No se encontró registro previo exacto para la cédula {cedula}.")

            # 5. Registrar en la Tabla de Auditoría Forense
            cursor.execute("""
                INSERT INTO archivos_rufe_procesados 
                (nombre_archivo, titulo_reporte, registros_afectados, estado_proceso, detalles_auditoria)
                VALUES (%s, %s, %s, %s, %s);
            """, (
                archivo, 
                f"RUFE - {datos_rufe['nombre']}", 
                1, 
                'PROCESADO', 
                f"Acción: {estado_accion}. ID Staging: {temp_id}"
            ))

            cursor.execute("UPDATE rufe_temporal SET procesado = TRUE WHERE id = %s;", (temp_id,))
            conn.commit()
            print(f"  [AUDITORÍA] Archivo {archivo} registrado en la tabla forense correctamente.")

        except Exception as e:
            conn.rollback()
            print(f"  [ERROR] Falló el procesamiento de {archivo}: {e}")
            try:
                cursor.execute("""
                    INSERT INTO archivos_rufe_procesados (nombre_archivo, estado_proceso, detalles_auditoria)
                    VALUES (%s, 'CON_ERRORES', %s)
                    ON CONFLICT (nombre_archivo) DO UPDATE SET estado_proceso = 'CON_ERRORES', detalles_auditoria = EXCLUDED.detalles_auditoria;
                """, (archivo, str(e)))
                conn.commit()
            except:
                pass

    cursor.close()
    conn.close()
    print("\n¡Proceso de la carpeta RUFE finalizado!")

if __name__ == "__main__":
    procesar_carpeta()
