from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import psycopg2
import psycopg2.extras
import os
import json

app = FastAPI(title="API SGRD", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db_connection():
    db_host = os.getenv("DB_HOST", "172.17.0.1")
    return psycopg2.connect(
        host=db_host,
        database="comunidad_db",
        user="admin_comunidad",
        password="TuPasswordSegura2026!"
    )

class ReporteCreate(BaseModel):
    categoria_id: int
    titulo: str
    descripcion_detallada: str
    sector_barrio: str
    direccion_referencia: str
    latitud: float
    longitud: float
    datos_extra: dict = None

@app.get("/")
def read_root():
    return {"status": "ok", "message": "API SGRD funcionando correctamente"}

@app.get("/api/barrios")
@app.get("/api/barrios/")
def get_barrios_universal():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        for tabla in ["barrios", "barrios por visitar", "sector", "sectores"]:
            try:
                cur.execute(f"SELECT id, nombre, comuna FROM {tabla} ORDER BY id ASC;")
                rows = cur.fetchall()
                if rows:
                    cur.close()
                    conn.close()
                    return [{"id": r[0], "nombre": str(r[1]).strip().upper(), "comuna": r[2] if r[2] is not None else 0} for r in rows]
            except Exception:
                conn.rollback()
                
            try:
                cur.execute(f"SELECT id, nombre FROM {tabla} ORDER BY id ASC;")
                rows = cur.fetchall()
                if rows:
                    cur.close()
                    conn.close()
                    return [{"id": r[0], "nombre": str(r[1]).strip().upper(), "comuna": 0} for r in rows]
            except Exception:
                conn.rollback()
        
        cur.execute("SELECT DISTINCT barrio FROM reportes_comunitarios WHERE barrio IS NOT NULL;")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return [{"id": i+1, "nombre": str(r[0]).strip().upper(), "comuna": 0} for i, r in enumerate(rows)]
    except Exception as e:
        return []

@app.get("/api/reportes")
@app.get("/api/reportes/")
def obtener_reportes(barrio: str = None, nombre: str = None, telefono: str = None):
    try:
        print(f"🔍 Filtros recibidos - barrio: {barrio}, nombre: {nombre}, telefono: {telefono}")
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        query = """
            SELECT 
                id, categoria_id, titulo, descripcion_detallada, 
                sector_barrio, direccion_referencia, latitud, longitud, 
                datos_extra, estado_actual, comuna
            FROM reportes_comunitarios
            WHERE 1=1
        """
        params = []
        
        if barrio and barrio.strip():
            query += " AND UPPER(sector_barrio) LIKE UPPER(%s)"
            params.append(f"%{barrio.strip()}%")
            print(f"   ➜ Filtro barrio aplicado: {barrio}")
        
        if nombre and nombre.strip():
            query += " AND datos_extra->>'ciudadano' ILIKE %s"
            params.append(f"%{nombre.strip()}%")
            print(f"   ➜ Filtro nombre aplicado: {nombre}")
        
        if telefono and telefono.strip():
            query += " AND datos_extra->>'telefono' ILIKE %s"
            params.append(f"%{telefono.strip()}%")
            print(f"   ➜ Filtro telefono aplicado: {telefono}")
        
        query += " ORDER BY fecha_creacion DESC;"
        
        print(f"📊 Query: {query}")
        print(f"📊 Params: {params}")
        
        cur.execute(query, params)
        rows = cur.fetchall()
        cur.close()
        conn.close()
        
        reportes = []
        for r in rows:
            reportes.append({
                "id": str(r[0]),
                "categoria_id": r[1],
                "titulo": r[2],
                "descripcion_detallada": r[3],
                "sector_barrio": r[4],
                "direccion_referencia": r[5],
                "latitud": r[6],
                "longitud": r[7],
                "datos_extra": r[8],
                "estado_actual": r[9] if len(r) > 9 else "Pendiente",
                "comuna": r[10] or 0 if len(r) > 10 else 0
            })
        return reportes
    except Exception as e:
        print(f"❌ ERROR: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# NUEVO ENDPOINT: Consultar detalle de formulario RUFE y personas
@app.get("/api/reportes/{reporte_id}/rufe")
@app.get("/api/reportes/{reporte_id}/rufe/")
def obtener_detalle_rufe(reporte_id: str):
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        
        # 1. Buscar el formulario RUFE asociado al ID del reporte
        cur.execute("SELECT * FROM rufe_formularios WHERE reporte_id = %s;", (reporte_id,))
        formulario = cur.fetchone()
        
        if not formulario:
            cur.close()
            conn.close()
            raise HTTPException(status_code=404, detail="Formulario RUFE no encontrado para este reporte")
            
        # 2. Buscar todas las personas asociadas a ese formulario (jefe de hogar primero)
        cur.execute("SELECT * FROM rufe_personas WHERE rufe_formulario_id = %s ORDER BY es_jefe_hogar DESC;", (formulario['id'],))
        personas = cur.fetchall()
        
        cur.close()
        conn.close()
        
        # Convertir IDs UUID a string para evitar errores de serialización JSON
        formulario['reporte_id'] = str(formulario['reporte_id'])
        
        return {
            "status": "success",
            "formulario": formulario,
            "nucleo_familiar": personas
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/reportes")
@app.post("/api/reportes/")
def crear_reporte(reporte: ReporteCreate):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        query = """
            INSERT INTO reportes_comunitarios 
            (categoria_id, titulo, descripcion_detallada, sector_barrio, direccion_referencia, latitud, longitud, datos_extra)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id;
        """
        datos_extra_json = json.dumps(reporte.datos_extra) if reporte.datos_extra else None
        
        cur.execute(query, (
            reporte.categoria_id,
            reporte.titulo,
            reporte.descripcion_detallada,
            reporte.sector_barrio,
            reporte.direccion_referencia,
            reporte.latitud,
            reporte.longitud,
            datos_extra_json
        ))
        
        nuevo_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        
        return {"status": "success", "id": nuevo_id, "message": "Reporte creado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/reportes/{reporte_id}/estado")
@app.put("/api/reportes/{reporte_id}/estado/")
def actualizar_estado_reporte(reporte_id: str, update: dict):
    try:
        estado = update.get('estado')
        observacion = update.get('observacion', '')
        
        print(f"📝 Actualizando estado: reporte={reporte_id}, estado={estado}, observacion={observacion}")
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Verificar si el reporte existe
        cur.execute("SELECT estado_actual FROM reportes_comunitarios WHERE id = %s;", (reporte_id,))
        row = cur.fetchone()
        if not row:
            cur.close()
            conn.close()
            raise HTTPException(status_code=404, detail="Reporte no encontrado")
        
        estado_anterior = row[0]
        
        # Actualizar estado
        cur.execute("""
            UPDATE reportes_comunitarios 
            SET estado_actual = %s, ultima_actualizacion = CURRENT_TIMESTAMP
            WHERE id = %s;
        """, (estado, reporte_id))
        
        # Registrar en trazabilidad
        cur.execute("""
            INSERT INTO trazabilidad (reporte_id, estado_anterior, estado_nuevo, observacion, usuario)
            VALUES (%s, %s, %s, %s, %s);
        """, (reporte_id, estado_anterior, estado, observacion, "Operador SGRD"))
        
        conn.commit()
        cur.close()
        conn.close()
        
        return {
            "status": "success",
            "message": f"Estado actualizado de '{estado_anterior}' a '{estado}'",
            "estado_anterior": estado_anterior,
            "estado_nuevo": estado
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ ERROR: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/trazabilidad/{reporte_id}")
@app.get("/api/trazabilidad/{reporte_id}/")
def obtener_trazabilidad(reporte_id: str):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT id, estado_anterior, estado_nuevo, observacion, usuario, fecha_cambio
            FROM trazabilidad
            WHERE reporte_id = %s
            ORDER BY fecha_cambio DESC;
        """, (reporte_id,))
        rows = cur.fetchall()
        cur.close()
        conn.close()
        
        return [{
            "id": r[0],
            "estado_anterior": r[1],
            "estado_nuevo": r[2],
            "observacion": r[3] or "",
            "usuario": r[4],
            "fecha_cambio": r[5].isoformat() if r[5] else None
        } for r in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/reportes/{reporte_id}")
@app.put("/api/reportes/{reporte_id}/")
def actualizar_reporte(reporte_id: str, reporte: ReporteCreate):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Verificar si el reporte existe
        cur.execute("SELECT id FROM reportes_comunitarios WHERE id = %s;", (reporte_id,))
        if not cur.fetchone():
            cur.close()
            conn.close()
            raise HTTPException(status_code=404, detail="Reporte no encontrado")
        
        # Obtener comuna del barrio
        comuna = 0
        if reporte.sector_barrio:
            cur.execute("SELECT comuna FROM barrios WHERE UPPER(nombre) = UPPER(%s);", (reporte.sector_barrio,))
            row = cur.fetchone()
            if row:
                comuna = row[0] or 0
        
        # Actualizar reporte
        query = """
            UPDATE reportes_comunitarios 
            SET 
                categoria_id = %s,
                titulo = %s,
                descripcion_detallada = %s,
                sector_barrio = %s,
                direccion_referencia = %s,
                latitud = %s,
                longitud = %s,
                datos_extra = %s,
                comuna = %s,
                ultima_actualizacion = CURRENT_TIMESTAMP
            WHERE id = %s
            RETURNING id;
        """
        datos_extra_json = json.dumps(reporte.datos_extra) if reporte.datos_extra else None
        
        cur.execute(query, (
            reporte.categoria_id,
            reporte.titulo,
            reporte.descripcion_detallada,
            reporte.sector_barrio,
            reporte.direccion_referencia,
            reporte.latitud,
            reporte.longitud,
            datos_extra_json,
            comuna,
            reporte_id
        ))
        
        if not cur.fetchone():
            cur.close()
            conn.close()
            raise HTTPException(status_code=404, detail="Reporte no encontrado")
        
        conn.commit()
        cur.close()
        conn.close()
        
        return {
            "status": "success",
            "message": "Reporte actualizado exitosamente",
            "comuna": comuna
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
