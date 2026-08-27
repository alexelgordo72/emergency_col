#!/bin/bash

# ============================================================
# BACKUP DEL PROYECTO SGRD - DENTRO DEL PROYECTO
# ============================================================

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  BACKUP PROYECTO SGRD - sgrd_final${NC}"
echo -e "${BLUE}========================================${NC}"

# Obtener la ruta del proyecto
PROJECT_DIR=$(pwd)
FECHA=$(date +%Y%m%d_%H%M%S)
FECHA_LEGIBLE=$(date +"%d/%m/%Y %H:%M")

# ============================================================
# 1. BACKUP DEL PROYECTO ACTUAL (sgrd_final)
# ============================================================
echo -e "\n${YELLOW}📌 Paso 1: Backup de sgrd_final${NC}"

cd ..
BACKUP_NUEVO="sgrd_final_backup_${FECHA}.tar.gz"

echo "   📁 Respaldando sgrd_final..."
tar -czf "${BACKUP_NUEVO}" \
  --exclude="build" \
  --exclude=".dart_tool" \
  --exclude="pubspec.lock" \
  --exclude="*.tar.gz" \
  --exclude="backup_*" \
  sgrd_final

echo -e "${GREEN}✅ Backup creado: ${BACKUP_NUEVO}${NC}"
echo "   📏 Tamaño: $(du -h ${BACKUP_NUEVO} | cut -f1)"

# ============================================================
# 2. BACKUP DEL PROYECTO ANTERIOR (emergency_col) - OPCIONAL
# ============================================================
echo -e "\n${YELLOW}📌 Paso 2: Backup de emergency_col (opcional)${NC}"
echo -e "${YELLOW}   ¿Quieres incluir el backup de emergency_col? (y/n)${NC}"
read -r RESPONSE

if [ "$RESPONSE" = "y" ] || [ "$RESPONSE" = "Y" ]; then
    BACKUP_ANTERIOR="emergency_col_backup_${FECHA}.tar.gz"
    echo "   📁 Respaldando emergency_col..."
    tar -czf "${BACKUP_ANTERIOR}" \
      --exclude="build" \
      --exclude=".dart_tool" \
      --exclude="pubspec.lock" \
      --exclude="*.tar.gz" \
      --exclude="backup_*" \
      emergency_col 2>/dev/null || echo "   ⚠️  No se encontró emergency_col"
    
    if [ -f "${BACKUP_ANTERIOR}" ]; then
        echo -e "${GREEN}✅ Backup de emergency_col creado${NC}"
        echo "   📏 Tamaño: $(du -h ${BACKUP_ANTERIOR} | cut -f1)"
    fi
fi

# ============================================================
# 3. SUBIR A GITHUB (OPCIONAL)
# ============================================================
echo -e "\n${YELLOW}📌 Paso 3: Subir a GitHub${NC}"
echo -e "${YELLOW}   ¿Quieres subir los backups a GitHub? (y/n)${NC}"
read -r RESPONSE

if [ "$RESPONSE" = "y" ] || [ "$RESPONSE" = "Y" ]; then
    cd /Users/admin/Documents/sgrd_final
    
    # Obtener versión
    LATEST=$(git tag | grep -E '^v[0-9]+\.[0-9]+\.[0-9]+$' | sort -V | tail -n 1)
    if [ -z "$LATEST" ]; then
        VERSION="v1.0.0"
    else
        BASE=${LATEST#v}
        MAJOR=$(echo $BASE | cut -d. -f1)
        MINOR=$(echo $BASE | cut -d. -f2)
        PATCH=$(echo $BASE | cut -d. -f3)
        NEW_PATCH=$((PATCH + 1))
        VERSION="v${MAJOR}.${MINOR}.${NEW_PATCH}"
    fi
    
    echo -e "${YELLOW}📌 Versión: ${VERSION}${NC}"
    
    # Commitear cambios
    git add .
    git commit -m "feat: Dashboard con mapa y filtros - ${VERSION}" 2>/dev/null || echo "   ✅ Sin cambios nuevos"
    
    # Crear tag
    git tag -a "${VERSION}" -m "Release ${VERSION} - Dashboard con mapa y filtros" 2>/dev/null || echo "   ✅ Tag ya existe"
    
    # Subir tag
    git push origin "${VERSION}" 2>/dev/null || echo "   ✅ Tag ya subido"
    
    # Crear release
    cd /Users/admin/Documents
    gh release create "${VERSION}" \
      --title "SGRD Yumbo ${VERSION} - Backup Completo" \
      --notes "
## 📦 Backup Completo - ${FECHA_LEGIBLE}

### Proyectos incluidos:
- **sgrd_final** (proyecto nuevo con dashboard y mapa)

### 🗺️ Nuevo Dashboard:
- Mapa interactivo con controles de zoom
- Filtros por barrio, nombre y teléfono
- Lista de reportes con colores según estado
- Layout responsive (horizontal/vertical)

### 📍 Despliegue:
- Frontend: http://10.147.17.2:8081
- Backend API: http://10.147.17.2:8001
"
    
    # Subir backups
    echo -e "\n${YELLOW}📤 Subiendo backups al release...${NC}"
    gh release upload "${VERSION}" "sgrd_final_backup_${FECHA}.tar.gz" --clobber
    
    if [ -f "emergency_col_backup_${FECHA}.tar.gz" ]; then
        gh release upload "${VERSION}" "emergency_col_backup_${FECHA}.tar.gz" --clobber
    fi
    
    echo -e "${GREEN}✅ Backups subidos al release${NC}"
    echo -e "${GREEN}🔗 https://github.com/alexelgordo72/emergency_col/releases/tag/${VERSION}${NC}"
fi

# ============================================================
# 4. LIMPIAR
# ============================================================
echo -e "\n${YELLOW}📌 Paso 4: Limpiando archivos temporales${NC}"
cd /Users/admin/Documents
rm -f sgrd_final_backup_${FECHA}.tar.gz 2>/dev/null
rm -f emergency_col_backup_${FECHA}.tar.gz 2>/dev/null
echo -e "${GREEN}✅ Limpieza completada${NC}"

# ============================================================
# FINAL
# ============================================================
echo -e "\n${BLUE}========================================${NC}"
echo -e "${GREEN}🎉 ¡BACKUP COMPLETADO EXITOSAMENTE!${NC}"
echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}📌 Fecha: ${FECHA_LEGIBLE}${NC}"
echo -e "${BLUE}========================================${NC}"
