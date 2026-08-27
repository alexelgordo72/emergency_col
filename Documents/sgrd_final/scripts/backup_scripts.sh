#!/bin/bash

# ============================================================
# BACKUP DE SCRIPTS - SGRD
# ============================================================

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  BACKUP DE SCRIPTS - SGRD${NC}"
echo -e "${BLUE}========================================${NC}"

FECHA=$(date +%Y%m%d_%H%M%S)
cd /Users/admin/Documents/sgrd_final

echo -e "\n${YELLOW}📌 Creando backup de scripts...${NC}"

# 1. Crear un respaldo de todos los scripts
tar -czf scripts_backup_${FECHA}.tar.gz scripts/

echo -e "${GREEN}✅ Backup de scripts creado: scripts_backup_${FECHA}.tar.gz${NC}"

# 2. Listar scripts
echo -e "\n${YELLOW}📋 Scripts respaldados:${NC}"
ls -la scripts/

echo -e "\n${BLUE}========================================${NC}"
echo -e "${GREEN}✅ BACKUP DE SCRIPTS COMPLETADO${NC}"
echo -e "${BLUE}========================================${NC}"
