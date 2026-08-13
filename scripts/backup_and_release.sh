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

# Si se pasa un argumento, usarlo como versión
if [ -n "$1" ]; then
    VERSION="$1"
else
    # Obtener la última versión y aumentar
    LATEST=$(git tag | grep -E '^v[0-9]+\.[0-9]+\.[0-9]+$' | sort -V | tail -n 1)
    if [ -z "$LATEST" ]; then
        VERSION="v1.0.0"
    else
        # Aumentar patch version (ej: v1.0.0 -> v1.0.1)
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
FECHA=$(date +"%d/%m/%Y %H:%M")

gh release create "${VERSION}" \
  --title "Emergency Col SGRD ${VERSION}" \
  --notes "
## 🚀 Versión ${VERSION} - ${FECHA}

### Características principales
- **CRUD completo de barrios** con comuna
- **Reportes comunitarios** con geolocalización
- **Mapa interactivo** con marcadores
- **Panel de gestión** de barrios
- **Backend** FastAPI con PostgreSQL
- **Frontend** Flutter para web

### 📍 Despliegue
- **Frontend:** http://10.147.17.2:8080
- **Backend API:** http://10.147.17.2:8000

### 🗄️ Base de Datos
- PostgreSQL con tablas: barrios, reportes_comunitarios, categorias
- Comunas asociadas a barrios

### 🔧 Tecnologías
- **Backend:** FastAPI, Python, Docker
- **Frontend:** Flutter, Dart
- **Base de Datos:** PostgreSQL
- **Mapa:** OpenStreetMap / Flutter Map
"

echo -e "${GREEN}✅ Release ${VERSION} creado${NC}"

# ============================================================
# 6. CREAR BACKUP LOCAL
# ============================================================
echo -e "\n${YELLOW}📌 Paso 6: Creando backup local${NC}"

FECHA_BACKUP=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="backup_${VERSION}_${FECHA_BACKUP}"
mkdir -p "$BACKUP_DIR"

# Backup del backend
echo "   📁 Respaldando backend..."
ssh almofa@10.147.17.2 "cat ~/backend_sgrd/app/main.py" > "$BACKUP_DIR/backend_main.py" 2>/dev/null || echo "⚠️  No se pudo respaldar backend"

# Backup de variables de entorno
echo "   🔐 Respaldando variables de entorno..."
cat > "$BACKUP_DIR/.env" << EOF
API_URL=http://10.147.17.2:8000
DB_HOST=172.17.0.1
DB_NAME=comunidad_db
DB_USER=admin_comunidad
DB_PASSWORD=TuPasswordSegura2026!
