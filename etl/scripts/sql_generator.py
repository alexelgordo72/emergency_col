"""
sql_generator.py
Genera el SQL de UPSERT (INSERT OR UPDATE) para las tablas:
- reportes_comunitarios
- rufe_formularios
- rufe_personas

Uso:
    python sql_generator.py <ruta_json>
    python sql_generator.py --todos
"""

import os
import sys
import json
import re
import argparse
from pathlib import Path
from datetime import datetime


CARPETA_OUTPUT = Path.home() / "etl" / "data" / "output"
CARPETA_SQL = Path.home() / "etl" / "data" / "output" / "sql"


def normalizar_numero(valor):
    """Normaliza un número eliminando puntos, espacios y guiones."""
    if valor is None:
        return None
    if isinstance(valor, (int, float)):
        return str(int(valor))
    if not isinstance(valor, str):
        return valor
    
    valor = re.sub(r'[.\s\-()]', '', valor)
    
    if not valor:
        return None
    
    return valor


def escapar_sql(texto):
    """Escapa comillas simples para SQL."""
    if texto is None:
        return "NULL"
    if isinstance(texto, (int, float)):
        return str(texto)
    if isinstance(texto, bool):
        return "TRUE" if texto else "FALSE"
    texto = str(texto).replace("'", "''")
    return f"'{texto}'"


def generar_sql_para_rufe(datos: dict) -> str:
    """Genera el SQL de UPSERT para un solo RUFE."""
    
    numero_rufe = datos.get("numero_rufe", "DESCONOCIDO")
    jefe = datos.get("jefe_hogar", {})
    evaluacion = datos.get("evaluacion_danos", {})
    vivienda = datos.get("vivienda", {})
    necesidades = datos.get("necesidades", {})
    animales = datos.get("animales", {})
    familia = datos.get("composicion_familiar", [])
    datos_adicionales = datos.get("datos_adicionales", {})
    
    # Normalizar cédula y teléfono
    cedula_jefe = normalizar_numero(jefe.get("cedula"))
    telefono_jefe = normalizar_numero(jefe.get("telefono"))
    
    # Determinar estado_actual basado en la prioridad
    prioridad = evaluacion.get("prioridad", "MEDIA")
    if prioridad == "ALTA":
        estado_actual = "Aprobado_Prioritario"
    elif prioridad == "MEDIA":
        estado_actual = "Aprobado_Medio"
    else:
        estado_actual = "Visitado_DE"
    
    # Construir el JSONB de datos_extra
    datos_extra = {
        "rufe": numero_rufe,
        "cedula": cedula_jefe,
        "telefono": telefono_jefe,
        "ciudadano": f"{jefe.get('nombres', '')} {jefe.get('apellidos', '')}".strip(),
        "nivel_riesgo_tecnico": evaluacion.get("nivel_riesgo"),
        "habitabilidad_tecnica": evaluacion.get("habitabilidad"),
        "prioridad": prioridad,
        "evaluador": datos.get("evaluador"),
        "fuente_origen": datos_adicionales.get("fuente_origen", "ETL SGRD"),
        "fecha_evaluacion": datos.get("fecha_evaluacion"),
        "vivienda": vivienda,
        "necesidades": necesidades,
        "animales": animales,
        "total_personas_hogar": datos.get("total_personas_hogar")
    }
    
    # Filtrar valores None del JSONB
    datos_extra = {k: v for k, v in datos_extra.items() if v is not None}
    datos_extra_json = json.dumps(datos_extra, ensure_ascii=False).replace("'", "''")
    
    # SQL con UPSERT
    sql = f"""
-- ============================================================
-- UPSERT RUFE {numero_rufe}
-- ============================================================

DO $$
DECLARE
    v_reporte_id UUID;
    v_formulario_id INTEGER;
BEGIN
    -- 1. Buscar si ya existe un reporte con este RUFE
    SELECT id INTO v_reporte_id
    FROM public.reportes_comunitarios
    WHERE datos_extra->>'rufe' = {escapar_sql(numero_rufe)}
    LIMIT 1;
    
    -- 2. Si existe, ACTUALIZAR; si no, INSERTAR
    IF v_reporte_id IS NOT NULL THEN
        -- ACTUALIZAR reporte existente
        UPDATE public.reportes_comunitarios
        SET 
            titulo = {escapar_sql(f'RUFE #{numero_rufe} - {jefe.get("nombres", "")} {jefe.get("apellidos", "")}')},
            estado_actual = {escapar_sql(estado_actual)},
            sector_barrio = {escapar_sql(jefe.get("barrio"))},
            direccion_referencia = {escapar_sql(jefe.get("direccion"))},
            descripcion_detallada = {escapar_sql(evaluacion.get("descripcion_danos"))},
            datos_extra = COALESCE(datos_extra, '{{}}'::jsonb) || '{datos_extra_json}'::jsonb,
            ultima_actualizacion = CURRENT_TIMESTAMP
        WHERE id = v_reporte_id;
        
        RAISE NOTICE '✅ RUFE {numero_rufe} actualizado';
    ELSE
        -- INSERTAR nuevo reporte
        INSERT INTO public.reportes_comunitarios (
            titulo, estado_actual, sector_barrio, direccion_referencia,
            descripcion_detallada, datos_extra
        ) VALUES (
            {escapar_sql(f'RUFE #{numero_rufe} - {jefe.get("nombres", "")} {jefe.get("apellidos", "")}')},
            {escapar_sql(estado_actual)},
            {escapar_sql(jefe.get("barrio"))},
            {escapar_sql(jefe.get("direccion"))},
            {escapar_sql(evaluacion.get("descripcion_danos"))},
            '{datos_extra_json}'::jsonb
        )
        RETURNING id INTO v_reporte_id;
        
        RAISE NOTICE '✅ RUFE {numero_rufe} insertado';
    END IF;
    
    -- 3. Buscar si ya existe el formulario
    SELECT id INTO v_formulario_id
    FROM public.rufe_formularios
    WHERE reporte_id = v_reporte_id
    LIMIT 1;
    
    -- 4. Si existe, ACTUALIZAR; si no, INSERTAR
    IF v_formulario_id IS NOT NULL THEN
        UPDATE public.rufe_formularios
        SET 
            numero_formulario = {escapar_sql(numero_rufe)},
            prioridad = {escapar_sql(prioridad)},
            observaciones_evaluador = {escapar_sql(evaluacion.get("observaciones_evaluador"))}
        WHERE id = v_formulario_id;
    ELSE
        INSERT INTO public.rufe_formularios (
            reporte_id, numero_formulario, prioridad,
            observaciones_evaluador
        ) VALUES (
            v_reporte_id,
            {escapar_sql(numero_rufe)},
            {escapar_sql(prioridad)},
            {escapar_sql(evaluacion.get("observaciones_evaluador"))}
        )
        RETURNING id INTO v_formulario_id;
    END IF;
    
    -- 5. Eliminar los miembros anteriores (para re-insertar los nuevos)
    DELETE FROM public.rufe_personas
    WHERE rufe_formulario_id = v_formulario_id;
"""
    
    # Insertar los miembros de la familia (siempre, después de borrar)
    if familia:
        for i, miembro in enumerate(familia):
            nombre_completo = f"{miembro.get('nombres', '')} {miembro.get('apellidos', '')}".strip()
            es_jefe = miembro.get("parentesco") == "Jefe de Hogar"
            cedula_miembro = normalizar_numero(miembro.get("cedula"))
            
            sql += f"""
    -- Miembro {i+1}: {nombre_completo}
    INSERT INTO public.rufe_personas (
        rufe_formulario_id, nombre_completo, documento_identidad,
        telefono, parentesco, sexo, edad, es_jefe_hogar
    ) VALUES (
        v_formulario_id,
        {escapar_sql(nombre_completo)},
        {escapar_sql(cedula_miembro)},
        {escapar_sql(telefono_jefe if es_jefe else None)},
        {escapar_sql(miembro.get('parentesco'))},
        {escapar_sql(miembro.get('sexo'))},
        {miembro.get('edad') if miembro.get('edad') else 'NULL'},
        {'TRUE' if es_jefe else 'FALSE'}
    );
"""
    
    sql += "\nEND $$;\n"
    
    return sql


def generar_sql_para_archivo(json_path: Path) -> str:
    """Genera el SQL para todos los RUFE de un archivo JSON."""
    
    with open(json_path, "r", encoding="utf-8") as f:
        datos = json.load(f)
    
    if isinstance(datos, dict):
        datos = [datos]
    
    sql_completo = f"""
-- ============================================================
-- SQL generado automáticamente por el ETL SGRD
-- Archivo: {json_path.name}
-- Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
-- Total RUFE: {len(datos)}
-- Modo: UPSERT (actualiza si existe, inserta si no)
-- ============================================================

BEGIN;

"""
    
    for rufe in datos:
        sql_completo += generar_sql_para_rufe(rufe)
    
    sql_completo += "\nCOMMIT;\n"
    
    return sql_completo


def main():
    parser = argparse.ArgumentParser(description="Generador de SQL para RUFE (UPSERT)")
    parser.add_argument("json_path", nargs="?", help="Ruta del JSON")
    parser.add_argument("--todos", action="store_true", help="Procesar todos los JSON")
    
    args = parser.parse_args()
    
    if not args.json_path and not args.todos:
        parser.print_help()
        sys.exit(1)
    
    CARPETA_SQL.mkdir(parents=True, exist_ok=True)
    
    if args.todos:
        archivos = sorted(CARPETA_OUTPUT.glob("*.json"))
    else:
        archivos = [Path(args.json_path)]
    
    for json_path in archivos:
        if not json_path.exists():
            print(f"⚠️ No existe: {json_path}")
            continue
        
        print(f"\n📄 Procesando: {json_path.name}")
        sql = generar_sql_para_archivo(json_path)
        
        # Guardar el SQL
        sql_path = CARPETA_SQL / f"{json_path.stem}.sql"
        with open(sql_path, "w", encoding="utf-8") as f:
            f.write(sql)
        
        print(f"   ✅ SQL generado: {sql_path}")


if __name__ == "__main__":
    main()
