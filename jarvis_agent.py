import os
from fastapi import FastAPI, HTTPException
import httpx
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI(title="JARVIS SGRD API", version="4.8 Router-Robusto")

DB_URL = "postgresql://admin_comunidad:TuPasswordSegura2026!@35.239.228.238:5432/comunidad_db"
OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
MODEL_NAME = "llama3"

class ConsultaRequest(BaseModel):
    pregunta: str
    operador: str = "Alex"

def ejecutar_sql(sql_query: str):
    try:
        conn = psycopg2.connect(DB_URL, connect_timeout=5, cursor_factory=RealDictCursor)
        cur = conn.cursor()
        cur.execute(sql_query)
        resultados = cur.fetchall()
        cur.close()
        conn.close()
        return resultados
    except Exception as e:
        return [{"error_db": str(e)}]

@app.post("/jarvis/analizar")
async def analizar_datos(req: ConsultaRequest):
    p = req.pregunta.lower()
    
    # Enrutamiento inteligente y rápido según la intención del operador
    if any(k in p for k in ["pendiente", "pendientes"]):
        sql_limpio = "SELECT count(*) as total_pendientes FROM reportes_comunitarios WHERE estado_actual ILIKE 'PENDIENTE';"
    elif any(k in p for k in ["visitado", "visitados"]):
        sql_limpio = "SELECT count(*) as total_visitados FROM reportes_comunitarios WHERE estado_actual ILIKE '%VISITADO%';"
    elif any(k in p for k in ["total", "cuantos", "reportes"]):
        sql_limpio = "SELECT count(*) as total_general FROM reportes_comunitarios;"
    else:
        # Consulta segura por defecto muy ligera
        sql_limpio = "SELECT estado_actual as estado, count(*) as total FROM reportes_comunitarios GROUP BY estado_actual LIMIT 5;"

    datos = ejecutar_sql(sql_limpio)
    
    prompt_jarvis = (
        f"Eres JARVIS. Operador: {req.operador}. Pregunta: '{req.pregunta}'. "
        f"Cifras oficiales: {str(datos)}. "
        "Responde en ESPAÑOL, directo y ejecutivo. Máximo 15 palabras. Ve al grano."
    )
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            resp2 = await client.post(OLLAMA_URL, json={
                "model": MODEL_NAME, 
                "prompt": prompt_jarvis, 
                "stream": False,
                "options": {"num_predict": 30, "temperature": 0.1}
            })
            resp2.raise_for_status()
            return {"sql_generado": sql_limpio, "respuesta_jarvis": resp2.json().get("response", "").strip()}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
