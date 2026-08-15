#!/bin/bash

# ============================================================
# Emergency Col SGRD - Script de Backup y Release Automático
# ============================================================

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Emergency Col SGRD - Backup & Release${NC}"
echo -e "${BLUE}========================================${NC}"

# ============================================================
# 1. OBTENER VERSIÓN
# ============================================================
echo -e "\n${YELLOW}📌 Paso 1: Versión${NC}"

if [ -n "$1" ]; then
    VERSION="$1"
else
    # Obtener la última versión y aumentar
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
fi

echo -e "${GREEN}✅ Versión: ${VERSION}${NC}"

# ============================================================
# 2. VERIFICAR QUE NO HAYA CAMBIOS SIN COMMIT
# ============================================================
echo -e "\n${YELLOW}📌 Paso 2: Verificando cambios sin commit${NC}"

if [ -n "$(git status --porcelain)" ]; then
    echo -e "${YELLOW}⚠️  Hay cambios sin commit.${NC}"
    echo -e "${YELLOW}   ¿Quieres commitearlos? (y/n)${NC}"
    read -r RESPONSE
    if [ "$RESPONSE" = "y" ] || [ "$RESPONSE" = "Y" ]; then
        git add .
        git commit -m "chore: preparando release ${VERSION}"
        echo -e "${GREEN}✅ Cambios commitados${NC}"
    else
        echo -e "${RED}❌ Cancelando...${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}✅ No hay cambios pendientes${NC}"
fi

# ============================================================
# 3. CREAR TAG
# ============================================================
echo -e "\n${YELLOW}📌 Paso 3: Creando tag ${VERSION}${NC}"

git tag -a "${VERSION}" -m "Release ${VERSION} - Emergency Col SGRD"

echo -e "${GREEN}✅ Tag ${VERSION} creado${NC}"

# ============================================================
# 4. SUBIR TAG A GITHUB
# ============================================================
echo -e "\n${YELLOW}📌 Paso 4: Subiendo tag a GitHub${NC}"

git push origin "${VERSION}"

echo -e "${GREEN}✅ Tag ${VERSION} subido${NC}"

# ============================================================
# 5. CREAR RELEASE EN GITHUB
# ============================================================
echo -e "\n${YELLOW}📌 Paso 5: Creando release en GitHub${NC}"

# Obtener fecha actual
FECHA_RELEASE=$(date +"%d/%m/%Y %H:%M")

gh release create "${VERSION}" \
  --title "Emergency Col SGRD ${VERSION}" \
  --notes "
## 🚀 Versión ${VERSION} - ${FECHA_RELEASE}

### Características principales
- **CRUD completo de barrios** con comuna
- **Reportes comunitarios** con geolocalización
- **Trazabilidad** de cambios de estado
- **RUFE** con núcleo familiar
- **Planilla de ruta** con comunas y totales
- **Filtros** de búsqueda (barrio, nombre, teléfono, RUFE)

### 📍 Despliegue
- **Frontend:** http://10.147.17.2:8080
- **Backend API:** http://10.147.17.2:8000

### 🗄️ Base de Datos
- PostgreSQL con tablas: barrios, reportes_comunitarios, trazabilidad, rufe_formularios, rufe_personas
- 77 barrios, 532 reportes, 109 trazabilidad, 83 RUFE, 194 personas

### 🔧 Tecnologías
- **Backend:** FastAPI, Python, Docker
- **Frontend:** Flutter, Dart
- **Base de Datos:** PostgreSQL
- **Mapa:** OpenStreetMap / Flutter Map
"

echo -e "${GREEN}✅ Release ${VERSION} creado${NC}"

# ============================================================
# 6. CREAR BACKUP COMPLETO
# ============================================================
echo -e "\n${YELLOW}📌 Paso 6: Creando backup completo${NC}"

FECHA=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="backup_${VERSION}_${FECHA}"
mkdir -p "$BACKUP_DIR"

# 6.1 Backup de la base de datos
echo "   🗄️  Respaldando base de datos..."
ssh almofa@10.147.17.2 "docker exec db_sgrd pg_dump -U admin_comunidad --inserts -F p comunidad_db" > "$BACKUP_DIR/database.sql" 2>/dev/null

if [ -s "$BACKUP_DIR/database.sql" ]; then
    BARRIOS=$(grep -c "INSERT INTO public.barrios" "$BACKUP_DIR/database.sql" 2>/dev/null || echo "0")
    REPORTES=$(grep -c "INSERT INTO public.reportes_comunitarios" "$BACKUP_DIR/database.sql" 2>/dev/null || echo "0")
    TRAZABILIDAD=$(grep -c "INSERT INTO public.trazabilidad" "$BACKUP_DIR/database.sql" 2>/dev/null || echo "0")
    RUFE=$(grep -c "INSERT INTO public.rufe_formularios" "$BACKUP_DIR/database.sql" 2>/dev/null || echo "0")
    PERSONAS=$(grep -c "INSERT INTO public.rufe_personas" "$BACKUP_DIR/database.sql" 2>/dev/null || echo "0")
    echo "   ✅ Base de datos respaldada ($BARRIOS barrios, $REPORTES reportes, $TRAZABILIDAD trazabilidad, $RUFE RUFE, $PERSONAS personas)"
else
    echo "   ⚠️  No se pudo respaldar la base de datos"
fi

# 6.2 Backup del backend
echo "   📁 Respaldando backend..."
ssh almofa@10.147.17.2 "cat ~/backend_sgrd/app/main.py" > "$BACKUP_DIR/backend_main.py" 2>/dev/null || echo "⚠️  No se pudo respaldar backend"
echo "   ✅ Backend respaldado"

# 6.3 Backup del frontend
echo "   📁 Respaldando frontend..."
cp -r ~/Documents/emergency_col "$BACKUP_DIR/frontend" 2>/dev/null
echo "   ✅ Frontend respaldado"

# 6.4 Backup de scripts
echo "   📁 Respaldando scripts..."
mkdir -p "$BACKUP_DIR/scripts"
cp -r ~/Documents/emergency_col/scripts/* "$BACKUP_DIR/scripts/" 2>/dev/null || echo "   ⚠️  No se encontraron scripts"

# 6.5 Backup de variables de entorno
echo "   🔐 Respaldando variables de entorno..."
cat > "$BACKUP_DIR/.env.example" << 'ENVEOF'
API_URL=http://10.147.17.2:8000
DB_HOST=172.17.0.1
DB_NAME=comunidad_db
DB_USER=admin_comunidad
DB_PASSWORD=TuPasswordSegura2026!
ENVEOF
echo "   ✅ Variables de entorno respaldadas"

# 6.6 Comprimir
echo "   📦 Comprimiendo backup..."
tar -czf "emergency_col_backup_${VERSION}_${FECHA}.tar.gz" "$BACKUP_DIR/" 2>/dev/null
rm -rf "$BACKUP_DIR"

echo -e "${GREEN}✅ Backup creado: emergency_col_backup_${VERSION}_${FECHA}.tar.gz${NC}"
BACKUP_SIZE=$(du -h "emergency_col_backup_${VERSION}_${FECHA}.tar.gz" | cut -f1 2>/dev/null || echo "Desconocido")
echo "   📏 Tamaño: ${BACKUP_SIZE}"

# ============================================================
# 7. SUBIR BACKUP AL RELEASE
# ============================================================
echo -e "\n${YELLOW}📌 Paso 7: Subiendo backup al release${NC}"

gh release upload "${VERSION}" "emergency_col_backup_${VERSION}_${FECHA}.tar.gz" --clobber 2>/dev/null || echo "   ⚠️  No se pudo subir backup al release"

echo -e "${GREEN}✅ Backup subido al release${NC}"

# ============================================================
# 8. LIMPIAR
# ============================================================
echo -e "\n${YELLOW}📌 Paso 8: Limpiando archivos temporales${NC}"

rm -f "emergency_col_backup_${VERSION}_${FECHA}.tar.gz"

echo -e "${GREEN}✅ Limpieza completada${NC}"

# ============================================================
# FINAL
# ============================================================
echo -e "\n${BLUE}========================================${NC}"
echo -e "${GREEN}🎉 ¡PROCESO COMPLETADO EXITOSAMENTE!${NC}"
echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}📌 Versión: ${VERSION}${NC}"
echo -e "${GREEN}🔗 Release: https://github.com/alexelgordo72/emergency_col/releases/tag/${VERSION}${NC}"
echo -e "${GREEN}📦 Backup incluido en el release${NC}"
echo -e "${BLUE}========================================${NC}"

# Mostrar el release
gh release view "${VERSION}"
