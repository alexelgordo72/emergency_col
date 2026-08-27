#!/bin/bash

# ============================================================
# DEPLOY AL SERVIDOR - SGRD
# ============================================================

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  DEPLOY AL SERVIDOR - SGRD${NC}"
echo -e "${BLUE}========================================${NC}"

# ============================================================
# 1. COMPILAR
# ============================================================
echo -e "\n${YELLOW}📌 Paso 1: Compilando proyecto${NC}"
cd /Users/admin/Documents/sgrd_final

flutter clean
rm -rf build/ .dart_tool/ pubspec.lock
flutter pub get
flutter build web --release

echo -e "${GREEN}✅ Compilación exitosa${NC}"

# ============================================================
# 2. SUBIR AL SERVIDOR
# ============================================================
echo -e "\n${YELLOW}📌 Paso 2: Subiendo al servidor${NC}"

cd build/web
tar -czf /tmp/sgrd_final_deploy.tar.gz *

echo "   📤 Subiendo archivos..."
scp /tmp/sgrd_final_deploy.tar.gz almofa@10.147.17.2:/tmp/

echo "   📦 Extrayendo en el servidor..."
ssh almofa@10.147.17.2 << 'EOF'
cd /var/www/emergency_col/
sudo rm -rf *
sudo tar -xzf /tmp/sgrd_final_deploy.tar.gz -C .
sudo chown -R almofa:almofa .
sudo systemctl reload nginx
echo "✅ Frontend desplegado"
