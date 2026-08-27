#!/bin/bash

# ============================================================
# DEPLOY DIRECTO - SIN SUDO INTERACTIVO
# ============================================================

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  DEPLOY DIRECTO - SGRD${NC}"
echo -e "${BLUE}========================================${NC}"

# 1. Compilar
echo -e "\n${YELLOW}📌 Paso 1: Compilando...${NC}"
cd /Users/admin/Documents/sgrd_final

flutter clean
rm -rf build/ .dart_tool/ pubspec.lock
flutter pub get
flutter build web --release

echo -e "${GREEN}✅ Compilación exitosa${NC}"

# 2. Copiar archivos al servidor
echo -e "\n${YELLOW}📌 Paso 2: Copiando archivos al servidor...${NC}"

cd build/web

echo "   📤 Copiando archivos a /tmp/emergency_col_new..."
scp -r * almofa@10.147.17.2:/tmp/emergency_col_new/

# 3. Mover archivos en el servidor
echo -e "\n${YELLOW}📌 Paso 3: Moviendo archivos en el servidor...${NC}"

ssh almofa@10.147.17.2 << 'EOF'
echo "   📦 Moviendo archivos a /var/www/emergency_col/..."
sudo mv /tmp/emergency_col_new/* /var/www/emergency_col/ 2>/dev/null || echo "   ✅ Archivos ya movidos"
sudo chown -R almofa:almofa /var/www/emergency_col/
sudo systemctl reload nginx
echo "✅ Frontend desplegado"
