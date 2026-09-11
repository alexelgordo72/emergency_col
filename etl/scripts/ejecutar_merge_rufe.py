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

def main():
    print("Iniciando proceso de Merge y Consolidación de rufe_temporal_merge...")
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        cur.execute("""
            SELECT id, numero_rufe, reporte_id_existente, datos_nuevos, estado
            FROM public.rufe_temporal_merge
            WHERE estado != 'RESOLVED'
            ORDER BY fecha_creacion ASC;
        """)
        registros = cur.fetchall()
        print(f"Total de registros a procesar: {len(registros)}")
        
        procesados = 0
        for reg in registros:
            staging_id = reg["id"]
            num = reg["numero_rufe"]
            rep_id_existente = reg["reporte_id_existente"]
            datos = reg["datos_nuevos"]
            estado = reg["estado"]
            
            # Obtener personas de forma segura según el formato guardado
            personas = datos.get("personas") or []
            if not personas and "nombre" in datos:
                personas = [{
                    "nombre": datos.get("nombre"),
                    "doc": datos.get("cedula"),
                    "parentesco": "Jefe(a) o cabeza del hogar",
                    "sexo": "M",
                    "fecha_nac": None,
                    "edad": None,
                    "telefono": None,
                    "es_jefe": True
                }]
                
            if not personas:
                personas = [{
                    "nombre": f"Ciudadano RUFE {num}",
                    "doc": "000000",
                    "parentesco": "Jefe(a) o cabeza del hogar",
                    "sexo": "M",
                    "fecha_nac": None,
                    "edad": None,
                    "telefono": None,
                    "es_jefe": True
                }]

            jefe = next((p for p in personas if p.get("es_jefe")), personas[0])
            prioridad = datos.get("prioridad", "BAJA")
            observaciones = datos.get("observaciones_evaluador") or datos.get("observaciones", "Sin observaciones")
            
            if estado == 'NUEVO' or not rep_id_existente:
                rep_id = str(uuid.uuid4())
                rep_rufe_id = str(uuid.uuid4())
                titulo_oficial = f"Evaluación RUFE {num} - {jefe['nombre']}"
                
                datos_extra = {
                    "rufe": num,
                    "cedula": jefe.get("doc"),
                    "nombre": jefe["nombre"],
                    "prioridad": prioridad,
                    "observaciones": observaciones,
                    "observaciones_animales": datos.get("observaciones_animales"),
                    "direccion": datos.get("direccion"),
                    "total_personas": len(personas)
                }
                
                # 1. reportes_comunitarios
                cur.execute("""
                    INSERT INTO public.reportes_comunitarios 
                    (id, titulo, descripcion_detallada, sector_barrio, direccion_referencia, estado_actual, datos_extra, procesado_rufe, migrado_rufe, activo)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, true, true, true)
                """, (
                    rep_id,
                    titulo_oficial,
                    observaciones,
                    datos.get("sector_barrio"),
                    datos.get("direccion"),
                    f"Aprobado_{prioridad}",
                    json.dumps(datos_extra)
                ))
                
                # 2. rufe_formularios
                cur.execute("""
                    INSERT INTO public.rufe_formularios 
                    (reporte_id, numero_formulario, corregimiento, prioridad, observaciones_animales, observaciones_evaluador)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING id
                """, (
                    rep_id,
                    num,
                    datos.get("corregimiento"),
                    prioridad,
                    datos.get("observaciones_animales"),
                    observaciones
                ))
                form_id = cur.fetchone()["id"]
                
                # 3. rufe_personas
                for p in personas:
                    cur.execute("""
                        INSERT INTO public.rufe_personas 
                        (rufe_formulario_id, nombre_completo, documento_identidad, fecha_nacimiento, telefono, es_jefe_hogar, parentesco, sexo, edad)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (
                        form_id,
                        p.get("nombre", "Sin Nombre"),
                        p.get("doc"),
                        p.get("fecha_nac"),
                        p.get("telefono"),
                        p.get("es_jefe", False),
                        p.get("parentesco"),
                        p.get("sexo"),
                        p.get("edad")
                    ))
                    
                # 4. reportes_comunitarios_rufe
                cur.execute("""
                    INSERT INTO public.reportes_comunitarios_rufe 
                    (id, rufe_formulario_id, titulo, descripcion_detallada, sector_barrio, direccion_referencia, estado_actual, datos_extra, numero_formulario, prioridad, observaciones_animales, observaciones_evaluador, corregimiento, jefe_hogar_nombre, jefe_hogar_cedula, jefe_hogar_telefono, jefe_hogar_genero, jefe_hogar_parentesco)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    rep_rufe_id,
                    form_id,
                    titulo_oficial,
                    observaciones,
                    datos.get("sector_barrio"),
                    datos.get("direccion"),
                    f"Aprobado_{prioridad}",
                    json.dumps(datos_extra),
                    num,
                    prioridad,
                    datos.get("observaciones_animales"),
                    observaciones,
                    datos.get("corregimiento"),
                    jefe["nombre"],
                    jefe.get("doc"),
                    jefe.get("telefono"),
                    jefe.get("sexo"),
                    jefe.get("parentesco")
                ))
                
            elif estado == 'PENDIENTE_MERGE' and rep_id_existente:
                cur.execute("SELECT id FROM public.rufe_formularios WHERE reporte_id = %s", (rep_id_existente,))
                form_res = cur.fetchone()
                
                if form_res:
                    existing_form_id = form_res["id"]
                    for p in personas:
                        doc_p = p.get("doc")
                        if doc_p:
                            cur.execute("SELECT id FROM public.rufe_personas WHERE rufe_formulario_id = %s AND documento_identidad = %s", (existing_form_id, doc_p))
                        else:
                            cur.execute("SELECT id FROM public.rufe_personas WHERE rufe_formulario_id = %s AND nombre_completo = %s", (existing_form_id, p.get("nombre")))
                        
                        if not cur.fetchone():
                            cur.execute("""
                                INSERT INTO public.rufe_personas 
                                (rufe_formulario_id, nombre_completo, documento_identidad, fecha_nacimiento, telefono, es_jefe_hogar, parentesco, sexo, edad)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                            """, (
                                existing_form_id,
                                p.get("nombre", "Sin Nombre"),
                                p.get("doc"),
                                p.get("fecha_nac"),
                                p.get("telefono"),
                                p.get("es_jefe", False),
                                p.get("parentesco"),
                                p.get("sexo"),
                                p.get("edad")
                            ))
                
                cur.execute("""
                    UPDATE public.reportes_comunitarios 
                    SET descripcion_detallada = %s, estado_actual = %s 
                    WHERE id = %s
                """, (observaciones, f"Aprobado_Merge_{prioridad}", rep_id_existente))

            cur.execute("UPDATE public.rufe_temporal_merge SET estado = 'RESOLVED' WHERE id = %s", (staging_id,))
            procesados += 1
            
        conn.commit()
        print("\n" + "="*45)
        print(f"¡Merge y consolidación completados con éxito! Registros procesados: {procesados}")
        print("="*45)

    except Exception as e:
        if 'conn' in locals():
            conn.rollback()
        print(f"\n[ERROR EN MERGE]: {e}")
    finally:
        if 'conn' in locals():
            cur.close()
            conn.close()

if __name__ == "__main__":
    main()
