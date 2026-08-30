from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import psycopg2
import os
import json
import uuid
from datetime import datetime

app = FastAPI(title="SGRD Yumbo API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db_connection():
    return psycopg2.connect(
        host="10.147.17.24",
        database="comunidad_db",
        user="admin_comunidad",
        password="TuPasswordSegura2026!"
    )

# ============================================================
# ENDPOINT DE LOGIN
# ============================================================
@app.post("/api/login")
def login(request: dict):
    usuario = request.get("usuario")
    contrasena = request.get("contrasena")
    
    if not usuario or not contrasena:
        return JSONResponse(
            status_code=400,
            content={"success": False, "message": "Usuario y contraseña requeridos"}
        )
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute(
            "SELECT id, usuario, contrasena, rol, nombre FROM usuarios WHERE usuario = %s AND activo = TRUE",
            (usuario,)
        )
        row = cur.fetchone()
        
        if not row:
            return JSONResponse(
                status_code=401,
                content={"success": False, "message": "Usuario no encontrado"}
            )
        
        user_id, db_usuario, db_contrasena, rol, nombre = row
        
        if contrasena != db_contrasena:
            return JSONResponse(
                status_code=401,
                content={"success": False, "message": "Contraseña incorrecta"}
            )
        
        cur.execute(
            "UPDATE usuarios SET ultimo_acceso = CURRENT_TIMESTAMP WHERE id = %s",
            (user_id,)
        )
        conn.commit()
        
        return {
            "success": True,
            "message": "Login exitoso",
            "data": {
                "id": user_id,
                "usuario": db_usuario,
                "rol": rol,
                "nombre": nombre
            }
        }
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": f"Error: {str(e)}"}
        )
    finally:
        cur.close()
        conn.close()

# ============================================================
# ENDPOINT DE ESTADOS
# ============================================================
@app.get("/api/estados")
def get_estados():
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("""
            SELECT nombre, color, orden 
            FROM estados_reporte 
            WHERE activo = TRUE 
            ORDER BY orden ASC
        """)
        rows = cur.fetchall()
        cur.close()
        conn.close()
        
        return [{"nombre": r[0], "color": r[1], "orden": r[2]} for r in rows]
    except Exception as e:
        return {"error": str(e)}

# ============================================================
# ENDPOINTS DE REPORTES
# ============================================================
@app.get("/api/reportes")
def get_reportes(limit: int = 10, offset: int = 0, q: str = None):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        base_query = '''
            SELECT r.id, r.titulo, r.sector_barrio, r.direccion_referencia, 
                   COALESCE(r.datos_extra->>'ciudadano', 'Anónimo') as ciudadano,
                   COALESCE(r.datos_extra->>'telefono', 'N/A') as telefono,
                   COALESCE(r.estado_actual, r.estado, 'Pendiente') as estado,
                   COALESCE(b.comuna, 0) as comuna,
                   r.descripcion_detallada, r.latitud, r.longitud, r.datos_extra,
                   f.numero_formulario
            FROM reportes_comunitarios r
            LEFT JOIN barrios b ON UPPER(TRIM(r.sector_barrio)) = UPPER(TRIM(b.nombre))
            LEFT JOIN rufe_formularios f ON r.id = f.reporte_id
            WHERE r.estado_actual IS NOT NULL
        '''
        
        params = []
        if q and q.strip():
            filtro_limpio = q.strip()
            import re
            match_digitos = re.search(r'\d+', filtro_limpio)
            solo_numero = match_digitos.group() if match_digitos else filtro_limpio

            query_filtro = f"%{filtro_limpio}%"
            query_numero = f"%{solo_numero}%"

            base_query += '''
                AND (r.titulo ILIKE %s 
                   OR r.descripcion_detallada ILIKE %s 
                   OR r.sector_barrio ILIKE %s 
                   OR r.direccion_referencia ILIKE %s
                   OR f.numero_formulario = %s
                   OR f.numero_formulario ILIKE %s)
            '''
            params = [query_filtro, query_filtro, query_filtro, query_filtro, solo_numero, query_numero]
        
        base_query += " ORDER BY r.fecha_creacion DESC LIMIT %s OFFSET %s"
        params.extend([limit, offset])
        
        cur.execute(base_query, params)
        rows = cur.fetchall()
        
        # Obtener total - convertirlo a int
        count_query = "SELECT COUNT(*) FROM reportes_comunitarios r WHERE r.estado_actual IS NOT NULL"
        if q and q.strip():
            count_query += " AND (r.titulo ILIKE %s OR r.descripcion_detallada ILIKE %s OR r.sector_barrio ILIKE %s OR r.direccion_referencia ILIKE %s)"
            cur.execute(count_query, (query_filtro, query_filtro, query_filtro, query_filtro))
        else:
            cur.execute(count_query)
        total = int(cur.fetchone()[0])  # Convertir a int explícitamente
        
        cur.close()
        conn.close()
         
        resultado = []
        for r in rows:
            resultado.append({
                "id": r[0],
                "titulo": r[1],
                "sector_barrio": r[2],
                "direccion_referencia": r[3],
                "ciudadano": r[4],
                "telefono": r[5],
                "estado": r[6],
                "comuna": r[7],
                "descripcion_detallada": r[8],
                "latitud": r[9],
                "longitud": r[10],
                "datos_extra": r[11],
                "numero_formulario": r[12]
            })
        return {
            "data": resultado,
            "total": total,
            "limit": limit,
            "offset": offset,
            "status": "success"
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/barrios")
def get_barrios():
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("SELECT id, nombre FROM barrios ORDER BY nombre ASC;")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        
        if rows:
            return [{"id": r[0], "nombre": str(r[1]).strip().upper()} for r in rows]
        else:
            return []
    except Exception as e:
        cur.close()
        conn.close()
        return {"error": str(e)}

# ============================================================
# ENDPOINTS DE TRAZABILIDAD
# ============================================================
@app.get("/api/trazabilidad/{reporte_id}")
def get_trazabilidad(reporte_id: str):
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("""
            SELECT id, titulo, estado_actual, sector_barrio, 
                   direccion_referencia, datos_extra, fecha_creacion,
                   descripcion_detallada
            FROM reportes_comunitarios 
            WHERE id = %s
        """, (reporte_id,))
        reporte = cur.fetchone()
        
        if not reporte:
            return {"error": "Reporte no encontrado"}, 404
        
        cur.execute("""
            SELECT estado_anterior, estado_nuevo, observacion, 
                   usuario, fecha_cambio
            FROM trazabilidad_eventos
            WHERE reporte_id = %s
            ORDER BY fecha_cambio DESC
        """, (reporte_id,))
        historial = cur.fetchall()
        
        historial_list = []
        for h in historial:
            historial_list.append({
                "estado_anterior": h[0],
                "estado_nuevo": h[1],
                "observacion": h[2],
                "usuario": h[3],
                "fecha_cambio": h[4].isoformat() if h[4] else None
            })
        
        cur.execute("""
            SELECT nombre FROM estados_reporte 
            WHERE activo = TRUE 
            ORDER BY orden ASC
        """)
        estados_rows = cur.fetchall()
        estados_disponibles = [r[0] for r in estados_rows]
        
        return {
            "reporte": {
                "id": reporte[0],
                "titulo": reporte[1],
                "estado_actual": reporte[2],
                "barrio": reporte[3],
                "direccion": reporte[4],
                "datos_extra": reporte[5],
                "fecha_creacion": reporte[6].isoformat() if reporte[6] else None,
                "descripcion": reporte[7]
            },
            "historial": historial_list,
            "estados_disponibles": estados_disponibles
        }
        
    except Exception as e:
        return {"error": str(e)}, 500
    finally:
        cur.close()
        conn.close()

@app.post("/api/trazabilidad/{reporte_id}")
def cambiar_estado(reporte_id: str, request: dict):
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        nuevo_estado = request.get("estado_nuevo")
        observacion = request.get("observacion", "")
        usuario = request.get("usuario", "Sistema")
        
        if not nuevo_estado:
            return {"error": "Estado nuevo es requerido"}, 400
        
        cur.execute("SELECT estado_actual FROM reportes_comunitarios WHERE id = %s", (reporte_id,))
        row = cur.fetchone()
        if not row:
            return {"error": "Reporte no encontrado"}, 404
        
        estado_anterior = row[0]
        
        if estado_anterior == nuevo_estado:
            return {"error": f"El reporte ya está en estado {nuevo_estado}"}, 400
        
        cur.execute("SELECT nombre FROM estados_reporte WHERE nombre = %s AND activo = TRUE", (nuevo_estado,))
        if cur.rowcount == 0:
            return {"error": f"Estado '{nuevo_estado}' no válido"}, 400
        
        cur.execute(
            "UPDATE reportes_comunitarios SET estado_actual = %s, ultima_actualizacion = CURRENT_TIMESTAMP WHERE id = %s",
            (nuevo_estado, reporte_id)
        )
        
        cur.execute("""
            INSERT INTO trazabilidad_eventos 
            (reporte_id, estado_anterior, estado_nuevo, observacion, usuario)
            VALUES (%s, %s, %s, %s, %s)
        """, (reporte_id, estado_anterior, nuevo_estado, observacion, usuario))
        
        conn.commit()
        
        return {
            "message": "Estado actualizado correctamente",
            "estado_anterior": estado_anterior,
            "estado_nuevo": nuevo_estado
        }
        
    except Exception as e:
        conn.rollback()
        return {"error": str(e)}, 500
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
