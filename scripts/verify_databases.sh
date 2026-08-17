#!/bin/bash

# ============================================================
# Emergency Col SGRD - Verificación de Bases de Datos
# ============================================================

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Verificación de Bases de Datos${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Verificar desarrollo
echo -e "${YELLOW}📊 DESARROLLO (10.147.17.2):${NC}"
DESARROLLO=$(ssh almofa@10.147.17.2 "docker exec db_sgrd psql -U admin_comunidad -d comunidad_db -t -c \"
SELECT 
    COUNT(*) as total_reportes,
    (SELECT COUNT(*) FROM barrios) as total_barrios,
    (SELECT COUNT(*) FROM rufe_formularios) as total_rufe,
    (SELECT COUNT(*) FROM trazabilidad) as total_trazabilidad,
    (SELECT COUNT(*) FROM ahe_entregas) as total_ahe
FROM reportes_comunitarios;
\"" 2>/dev/null)

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Conexión exitosa${NC}"
    echo "$DESARROLLO"
else
    echo -e "${RED}❌ Error al conectar con desarrollo${NC}"
    DESARROLLO=""
fi

echo ""

# Verificar producción
echo -e "${YELLOW}📊 PRODUCCIÓN (192.168.194.1):${NC}"
PRODUCCION=$(ssh sgrd@192.168.194.1 "docker exec db_sgrd psql -U admin_comunidad -d comunidad_db -t -c \"
SELECT 
    COUNT(*) as total_reportes,
    (SELECT COUNT(*) FROM barrios) as total_barrios,
    (SELECT COUNT(*) FROM rufe_formularios) as total_rufe,
    (SELECT COUNT(*) FROM trazabilidad) as total_trazabilidad,
    (SELECT COUNT(*) FROM ahe_entregas) as total_ahe
FROM reportes_comunitarios;
\"" 2>/dev/null)

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Conexión exitosa${NC}"
    echo "$PRODUCCION"
else
    echo -e "${RED}❌ Error al conectar con producción${NC}"
    PRODUCCION=""
fi

echo ""
echo -e "${BLUE}========================================${NC}"

# Comparar resultados
if [ -n "$DESARROLLO" ] && [ -n "$PRODUCCION" ]; then
    # Extraer números
    DEV_REPORTES=$(echo "$DESARROLLO" | awk '{print $1}')
    PROD_REPORTES=$(echo "$PRODUCCION" | awk '{print $1}')
    
    if [ "$DEV_REPORTES" == "$PROD_REPORTES" ]; then
        echo -e "${GREEN}✅ BASES DE DATOS SINCERONIZADAS${NC}"
        echo -e "${GREEN}   Reportes: $DEV_REPORTES ✅${NC}"
    else
        echo -e "${YELLOW}⚠️  BASES DE DATOS DIFERENTES${NC}"
        echo -e "${RED}   Desarrollo: $DEV_REPORTES${NC}"
        echo -e "${RED}   Producción: $PROD_REPORTES${NC}"
        echo ""
        echo -e "${YELLOW}   Ejecuta: ./sync_databases.sh${NC}"
    fi
fi

echo -e "${BLUE}========================================${NC}"
