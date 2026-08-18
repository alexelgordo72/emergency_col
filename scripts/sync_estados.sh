#!/bin/bash

# ============================================================
# SGRD - Sincronizar Estados de Producción a Desarrollo
# ============================================================

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Sincronizar Estados${NC}"
echo -e "${BLUE}  Producción → Desarrollo${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

echo -e "${YELLOW}📤 Exportando estados desde producción...${NC}"

# 1. Exportar estados desde producción
ssh sgrd@192.168.194.1 "docker exec db_sgrd psql -U admin_comunidad -d comunidad_db -c \"
COPY (
    SELECT id, estado_actual, ultima_actualizacion 
    FROM reportes_comunitarios
    WHERE ultima_actualizacion > CURRENT_DATE - INTERVAL '7 days'
) TO STDOUT WITH CSV HEADER;
\"" > /tmp/estados_produccion.csv

echo -e "${GREEN}✅ Estados exportados${NC}"

# 2. Copiar a desarrollo
echo -e "${YELLOW}📥 Copiando a desarrollo...${NC}"
scp /tmp/estados_produccion.csv almofa@10.147.17.2:/tmp/

# 3. Actualizar desarrollo
echo -e "${YELLOW}🔄 Actualizando desarrollo...${NC}"
ssh almofa@10.147.17.2 "docker exec -i db_sgrd psql -U admin_comunidad -d comunidad_db" << 'SQL'
-- Crear tabla temporal
CREATE TEMP TABLE tmp_estados (
    id UUID PRIMARY KEY,
    estado_actual VARCHAR(100),
    ultima_actualizacion TIMESTAMP
);

-- Cargar datos del CSV
\COPY tmp_estados (id, estado_actual, ultima_actualizacion) FROM '/tmp/estados_produccion.csv' WITH CSV HEADER;

-- Actualizar desarrollo
UPDATE reportes_comunitarios r
SET 
    estado_actual = t.estado_actual,
    ultima_actualizacion = t.ultima_actualizacion
FROM tmp_estados t
WHERE r.id = t.id
  AND r.estado_actual != t.estado_actual;

-- Mostrar cuántos registros se actualizaron
SELECT COUNT(*) as registros_actualizados
FROM reportes_comunitarios r
JOIN tmp_estados t ON r.id = t.id
WHERE r.estado_actual = t.estado_actual
  AND r.ultima_actualizacion = t.ultima_actualizacion;

-- Mostrar los cambios recientes
SELECT 
    r.id,
    r.titulo,
    r.estado_actual,
    r.ultima_actualizacion
FROM reportes_comunitarios r
JOIN tmp_estados t ON r.id = t.id
WHERE r.estado_actual = t.estado_actual
  AND r.ultima_actualizacion = t.ultima_actualizacion
ORDER BY r.ultima_actualizacion DESC
LIMIT 10;
SQL

echo ""
echo -e "${GREEN}✅ Sincronización completada${NC}"

# Limpiar
rm -f /tmp/estados_produccion.csv

