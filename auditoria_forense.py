import psycopg2
import json
import re
import sys
from difflib import SequenceMatcher

# Configuración de tu base de datos PostgreSQL
DB_CONFIG = {
    "host": "10.147.17.24",
    "database": "comunidad_db",
    "user": "admin_comunidad",
    "password": "TuPasswordSegura2026!"
}

def similitud_texto(a, b):
    if not a or not b:
        return 0.0
    return SequenceMatcher(None, a.lower().strip(), b.lower().strip()).ratio()

def auditoria_segura_pendientes():
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    # REGLA DE ORO: Solo seleccionamos los registros que realmente están pendientes o sin estado
    cursor.execute("""
        SELECT id, titulo, sector_barrio, datos_extra, estado_actual 
        FROM reportes_comunitarios
        WHERE estado_actual ILIKE '%PENDIENTE%' OR estado_actual IS NULL
    """)
    reportes = cursor.fetchall()
    total_registros = len(reportes)
    
    print(f"\n-> Iniciando auditoría blindada. Registros pendientes a procesar: {total_registros}\n")
    print("="*70)

    verificados = 0
    siguen_pendientes = 0

    for index, row in enumerate(reportes, start=1):
        rep_id, titulo, sector_barrio, datos_extra, estado_actual = row
        
        datos = datos_extra if isinstance(datos_extra, dict) else json.loads(datos_extra or '{}')
        cedula_rep = str(datos.get('documento')).strip() if datos.get('documento') is not None else ""
        tel_rep = str(datos.get('telefono')).strip() if datos.get('telefono') is not None else ""
        nombre_rep = str(datos.get('ciudadano') or datos.get('nombre') or "").strip()

        match_encontrado = False
        rufe_encontrado = None
        fuente_match = ""

        # 1. Validar RUFE explícito en el título (ej. "RUFE #1652")
        match_titulo_rufe = re.search(r'rufe\D*(\d+)', titulo, re.IGNORECASE)
        if match_titulo_rufe:
            posible_rufe = match_titulo_rufe.group(1)
            cursor.execute("SELECT id FROM rufe_formularios WHERE id::text = %s LIMIT 1", (posible_rufe,))
            if cursor.fetchone():
                rufe_encontrado = posible_rufe
                match_encontrado = True
                fuente_match = f"RUFE Explícito en Título (#{rufe_encontrado})"

        # 2. Búsqueda por Llave Compuesta en la base de datos de personas RUFE
        if not match_encontrado:
            query = """
                SELECT p.rufe_formulario_id, p.documento_identidad, p.nombre_completo, p.telefono
                FROM rufe_personas p
                WHERE (%s != '' AND p.documento_identidad = %s)
                   OR (%s != '' AND p.telefono ILIKE %s)
                   OR (%s != '' AND p.nombre_completo ILIKE %s)
            """
            c_busq = cedula_rep if cedula_rep not in ('0', 'No Informa', '', 'None', 'No registra') else '____'
            t_busq = f"%{tel_rep.split('-')[0].strip()}%" if tel_rep not in ('N/A', 'No Informa', '', 'None', 'No registra') else '____'
            n_busq = f"%{nombre_rep}%" if len(nombre_rep) > 4 else '____'

            cursor.execute(query, (c_busq, c_busq, t_busq, t_busq, n_busq, n_busq))
            candidatos = cursor.fetchall()

            mejor_puntaje = 0
            mejor_rufe = None
            detalle_match = ""

            for cand in candidatos:
                rufe_f_id, doc_db, nom_db, tel_db = cand
                puntaje = 0
                criterios = []

                if c_busq != '____' and doc_db == c_busq:
                    puntaje += 50
                    criterios.append("Cédula Exacta")

                if n_busq != '____' and nom_db:
                    sim = similitud_texto(nombre_rep, nom_db)
                    if sim > 0.75:
                        puntaje += int(sim * 30)
                        criterios.append(f"Nombre Coincidente ({int(sim*100)}%)")

                if t_busq != '____' and tel_db and tel_rep:
                    if tel_rep.split('-')[0].strip() in tel_db:
                        puntaje += 20
                        criterios.append("Teléfono Coincidente")

                if puntaje >= 50 and puntaje > mejor_puntaje:
                    mejor_puntaje = puntaje
                    mejor_rufe = str(rufe_f_id)
                    detalle_match = " + ".join(criterios)

            if mejor_rufe and mejor_puntaje >= 50:
                rufe_encontrado = mejor_rufe
                match_encontrado = True
                fuente_match = f"Llave Compuesta [{detalle_match}] (RUFE #{rufe_encontrado})"

        # Avance en tiempo real
        sys.stdout.write(f"\r[Progreso: {index}/{total_registros}] ID: {rep_id} - ")
        
        if match_encontrado and rufe_encontrado:
            datos['rufe'] = rufe_encontrado
            cursor.execute("""
                UPDATE reportes_comunitarios 
                SET estado_actual = 'VERIFICADO RUFE',
                    datos_extra = %s
                WHERE id = %s
            """, (json.dumps(datos), rep_id))
            conn.commit()
            verificados += 1
            sys.stdout.write(f"[VERIFICADO] Por {fuente_match}\n")
        else:
            # Los que no hagan match se quedan explícitamente en PENDIENTE
            datos['rufe'] = 'Sin RUFE'
            cursor.execute("""
                UPDATE reportes_comunitarios 
                SET estado_actual = 'PENDIENTE',
                    datos_extra = %s
                WHERE id = %s
            """, (json.dumps(datos), rep_id))
            conn.commit()
            siguen_pendientes += 1
            sys.stdout.write(f"[PENDIENTE] Sin match seguro\n")
            
    cursor.close()
    conn.close()
    print("="*70)
    print(f"-> ¡Auditoría blindada finalizada con éxito!")
    print(f"   - Nuevos registros verificados con RUFE: {verificados}")
    print(f"   - Registros que se mantuvieron en PENDIENTE: {siguen_pendientes}")

if __name__ == "__main__":
    auditoria_segura_pendientes()
