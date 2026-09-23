#!/bin/bash

# ==========================================
# CONFIGURACIÓN DE RUTAS (¡Ajustar aquí!)
# ==========================================
# Rutas en tu Mac local
MAC_FRONTEND_DIR="$HOME/ruta_a_tu_proyecto_frontend_mac"

# Rutas en el servidor Ubuntu (sgrd-yumbo-vm)
SERVER_USER="alexelgordo"
SERVER_IP="10.147.17.24"
SERVER_BACKEND_DIR="~/ruta_a_tu_backend"
SERVER_FRONTEND_COMPILADO_DIR="/var/www/html" # O la ruta de Nginx/Apache donde esté servido

# Configuración de Base de Datos
DB_HOST="10.147.17.24"
DB_PORT="5432"
DB_NAME="comunidad_db"
DB_USER="admin_comunidad"
export PGPASSWORD="TuPasswordSegura2026!"

# ==========================================
# PREPARACIÓN DE DIRECTORIOS
# ==========================================
FECHA=$(date +"%Y%m%d_%H%M%S")
BACKUP_BASE_DIR="$HOME/Downloads/RUFE_Backup_$FECHA"

echo "Iniciando copia de seguridad total del proyecto RUFE..."
mkdir -p "$BACKUP_BASE_DIR/1_Base_Datos"
mkdir -p "$BACKUP_BASE_DIR/2_Frontend_Mac"
mkdir -p "$BACKUP_BASE_DIR/3_Backend_Servidor"
mkdir -p "$BACKUP_BASE_DIR/4_Frontend_Compilado"

# ==========================================
# 1. BASE DE DATOS (Estructura y Datos)
# ==========================================
echo "-> 1/4 Extrayendo base de datos PostgreSQL..."
# Formato .sql plano (leíble y auditable)
pg_dump -h $DB_HOST -p $DB_PORT -U $DB_USER -F p --inserts --clean -f "$BACKUP_BASE_DIR/1_Base_Datos/comunidad_db_$FECHA.sql" $DB_NAME
# Formato .backup comprimido (ideal para pg_restore en caso de desastre)
pg_dump -h $DB_HOST -p $DB_PORT -U $DB_USER -F c -b -f "$BACKUP_BASE_DIR/1_Base_Datos/comunidad_db_$FECHA.backup" $DB_NAME

# ==========================================
# 2. FRONTEND LOCAL (MAC)
# ==========================================
echo "-> 2/4 Copiando código fuente Frontend (Mac)..."
# Usamos rsync para excluir carpetas pesadas innecesarias como node_modules
rsync -av --exclude 'node_modules' --exclude '.git' "$MAC_FRONTEND_DIR/" "$BACKUP_BASE_DIR/2_Frontend_Mac/"

# ==========================================
# 3. BACKEND SERVIDOR
# ==========================================
echo "-> 3/4 Descargando código fuente Backend desde el servidor..."
# Excluimos entornos virtuales y caché de Python
rsync -avzhe ssh --exclude 'venv' --exclude '__pycache__' --exclude '.git' "$SERVER_USER@$SERVER_IP:$SERVER_BACKEND_DIR/" "$BACKUP_BASE_DIR/3_Backend_Servidor/"

# ==========================================
# 4. FRONTEND COMPILADO SERVIDOR
# ==========================================
echo "-> 4/4 Descargando Frontend compilado desde el servidor..."
rsync -avzhe ssh "$SERVER_USER@$SERVER_IP:$SERVER_FRONTEND_COMPILADO_DIR/" "$BACKUP_BASE_DIR/4_Frontend_Compilado/"

# ==========================================
# COMPRESIÓN FINAL
# ==========================================
echo "-> Comprimiendo todo el paquete..."
cd "$HOME/Downloads"
tar -czf "RUFE_Backup_$FECHA.tar.gz" "RUFE_Backup_$FECHA"

# Limpieza de la carpeta temporal descomprimida
rm -rf "RUFE_Backup_$FECHA"
unset PGPASSWORD

echo "=========================================="
echo "¡Copia de seguridad finalizada exitosamente!"
echo "Archivo generado: $HOME/Downloads/RUFE_Backup_$FECHA.tar.gz"
echo "=========================================="
