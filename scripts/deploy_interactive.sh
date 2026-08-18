#!/bin/bash

# ============================================================
# Emergency Col SGRD - Despliegue Interactivo
# ============================================================

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Emergency Col SGRD - Despliegue${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# ============================================================
# SOLICITAR CLAVES SSH
# ============================================================
echo -e "${YELLOW}🔐 Ingresa las contraseñas SSH (no se mostrarán mientras escribes)${NC}"
echo ""

read -sp "🔑 Clave para desarrollo (almofa@10.147.17.2): " PASS_DEV
echo ""
read -sp "🔑 Clave para producción (sgrd@192.168.194.1): " PASS_PROD
echo ""
echo ""

# ============================================================
# MENÚ DE DESPLIEGUE
# ============================================================
echo -e "${YELLOW}Selecciona el entorno de despliegue:${NC}"
echo "  1) Desarrollo (10.147.17.2)"
echo "  2) Producción (192.168.194.1)"
echo "  3) Salir"
echo ""
read -p "Opción [1-3]: " OPCION

case $OPCION in
  1)
    ENTORNO="desarrollo"
    URL_API="http://10.147.17.2:8001"
    USUARIO="almofa"
    IP="10.147.17.2"
    RUTA="/var/www/emergency_col"
    URL_FRONTEND="http://10.147.17.2:8081"
    PERMISOS="sudo chown -R $USUARIO:$USUARIO $RUTA && sudo chmod -R 755 $RUTA"
    PASS="$PASS_DEV"
    ;;
  2)
    ENTORNO="produccion"
    URL_API="http://192.168.194.1:8001"
    USUARIO="sgrd"
    IP="192.168.194.1"
    RUTA="/home/sgrd/frontend_sgrd"
    URL_FRONTEND="http://192.168.194.1:8081"
    PERMISOS="sudo chown -R www-data:www-data $RUTA && sudo chmod -R 755 $RUTA && sudo systemctl restart nginx"
    PASS="$PASS_PROD"
    ;;
  3)
    echo -e "${YELLOW}👋 Saliendo...${NC}"
    exit 0
    ;;
  *)
    echo -e "${RED}❌ Opción inválida${NC}"
    exit 1
    ;;
esac

echo ""
echo -e "${GREEN}✅ Desplegando en $ENTORNO${NC}"
echo "  URL API: $URL_API"
echo "  Servidor: $IP"
echo "  Usuario: $USUARIO"
echo "  Frontend: $URL_FRONTEND"
echo ""

read -p "¿Continuar? (s/n): " CONFIRMAR
if [[ "$CONFIRMAR" != "s" && "$CONFIRMAR" != "S" ]]; then
    echo -e "${YELLOW}👋 Cancelado${NC}"
    exit 0
fi

# ============================================================
# FUNCIÓN SSH CON CONTRASEÑA
# ============================================================
ssh_cmd() {
    expect -c "
        set timeout 30
        spawn ssh -o StrictHostKeyChecking=no $USUARIO@$IP $1
        expect {
            \"password:\" { send \"$PASS\r\"; exp_continue }
            \"Password:\" { send \"$PASS\r\"; exp_continue }
            \"yes/no\" { send \"yes\r\"; exp_continue }
            timeout { exit 1 }
            eof { exit 0 }
        }
    " 2>/dev/null
}

scp_cmd() {
    expect -c "
        set timeout 30
        spawn scp -o StrictHostKeyChecking=no -r $1 $USUARIO@$IP:$2
        expect {
            \"password:\" { send \"$PASS\r\"; exp_continue }
            \"Password:\" { send \"$PASS\r\"; exp_continue }
            \"yes/no\" { send \"yes\r\"; exp_continue }
            timeout { exit 1 }
            eof { exit 0 }
        }
    " 2>/dev/null
}

# ============================================================
# COMPILACIÓN
# ============================================================
echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}📦 Paso 1: Compilando frontend...${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

cd ~/Documents/emergency_col

flutter clean
flutter build web --release --dart-define=API_URL=$URL_API

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Error en la compilación${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Compilación completada${NC}"

# ============================================================
# COPIA DE ARCHIVOS
# ============================================================
echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}📤 Paso 2: Copiando archivos al servidor...${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

# Crear carpeta temporal
ssh_cmd "mkdir -p /tmp/frontend_temp"

# Copiar archivos
scp_cmd build/web/* /tmp/frontend_temp/

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Error al copiar archivos${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Archivos copiados a carpeta temporal${NC}"

# ============================================================
# MOVER ARCHIVOS
# ============================================================
echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}🔧 Paso 3: Moviendo archivos a la carpeta final...${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

ssh_cmd "
    sudo rm -rf $RUTA/* 2>/dev/null
    sudo cp -r /tmp/frontend_temp/* $RUTA/
    sudo chown -R $USUARIO:$USUARIO $RUTA
    sudo chmod -R 755 $RUTA
    rm -rf /tmp/frontend_temp
    echo '✅ Archivos movidos y permisos ajustados'
"

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Error al mover archivos${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Archivos movidos correctamente${NC}"

# Si es producción, ajustar permisos para Nginx
if [ "$ENTORNO" == "produccion" ]; then
    echo ""
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${YELLOW}🔧 Paso 4: Configurando permisos para Nginx...${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    
    ssh_cmd "
        sudo chown -R www-data:www-data $RUTA
        sudo chmod -R 755 $RUTA
        sudo systemctl restart nginx
        echo '✅ Nginx reiniciado'
    "
    
    echo -e "${GREEN}✅ Permisos de Nginx ajustados${NC}"
fi

# ============================================================
# VERIFICACIÓN FINAL
# ============================================================
echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}🎉 ¡DESPLIEGUE COMPLETADO!${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${GREEN}📌 URL: ${URL_FRONTEND}${NC}"
echo ""
echo -e "${YELLOW}📋 Comandos útiles:${NC}"
echo "  Ver logs del backend: ssh $USUARIO@$IP 'docker logs api_sgrd --tail 20'"
echo "  Reiniciar backend: ssh $USUARIO@$IP 'docker restart api_sgrd'"
echo "  Ver logs de Nginx: ssh $USUARIO@$IP 'sudo tail -20 /var/log/nginx/access.log'"
echo ""

# Limpiar variables por seguridad
unset PASS_DEV PASS_PROD PASS

