#!/bin/bash

# ============================================================
# Emergency Col SGRD - Sincronizar Producción → Desarrollo
# ============================================================

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Sincronizar Producción → Desarrollo${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

echo -e "${YELLOW}⚠️  Esta acción reemplazará la base de datos de desarrollo${NC}"
echo -e "${YELLOW}   con los datos de producción${NC}"
echo ""
read -p "¿Continuar? (s/n): " CONFIRMAR

if [[ "$CONFIRMAR" != "s" && "$CONFIRMAR" != "S" ]]; then
    echo -e "${RED}❌ Cancelado${NC}"
    exit 0
fi

echo ""
echo -e "${YELLOW}📤 Exportando base de datos de producción...${NC}"

# Exportar desde producción
ssh sgrd@192.168.194.1 "docker exec db_sgrd pg_dump -U admin_comunidad -d comunidad_db --no-owner --no-acl" > /tmp/comunidad_db_prod.sql

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Error al exportar desde producción${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Exportación completada${NC}"

echo -e "${YELLOW}📥 Restaurando en desarrollo...${NC}"

# Restaurar en desarrollo
ssh almofa@10.147.17.2 "docker stop api_sgrd 2>/dev/null; docker stop db_sgrd 2>/dev/null; docker rm db_sgrd 2>/dev/null"
ssh almofa@10.147.17.2 "docker run -d --name db_sgrd --network sgrd_network -e POSTGRES_DB=comunidad_db -e POSTGRES_USER=admin_comunidad -e POSTGRES_PASSWORD=TuPasswordSegura2026! -p 5432:5432 postgres:16"
sleep 10
ssh almofa@10.147.17.2 "docker exec -i db_sgrd psql -U admin_comunidad -d comunidad_db" < /tmp/comunidad_db_prod.sql
ssh almofa@10.147.17.2 "docker start api_sgrd"

echo -e "${GREEN}✅ Sincronización completada${NC}"

# Limpiar
rm -f /tmp/comunidad_db_prod.sql

echo ""
echo -e "${GREEN}🎉 ¡Base de datos de desarrollo sincronizada!${NC}"
echo -e "${GREEN}   Ahora desarrollo tiene los mismos datos que producción${NC}"
