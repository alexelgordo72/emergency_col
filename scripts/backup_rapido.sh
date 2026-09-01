#!/bin/bash

cd /Users/admin/Documents

FECHA=$(date +%Y%m%d_%H%M%S)
SEMANA=$(date +%Y-W%U)
BACKUP_FILE="backups/semanas/${SEMANA}/sgrd_backup_${FECHA}.tar.gz"
BACKUP_DIR="/tmp/sgrd_backup_${FECHA}"

mkdir -p "$(dirname $BACKUP_FILE)" "$BACKUP_DIR"

echo "🗄️ Base de datos..."
ssh -t almofa@10.147.17.2 "echo 'almofa' | sudo -S docker exec db_sgrd pg_dump -U postgres -d sgrd" > "$BACKUP_DIR/database.sql" 2>/dev/null

echo "🔧 Backend..."
ssh almofa@10.147.17.2 "tar -czf /tmp/backend_backup.tar.gz -C ~ backend_sgrd 2>/dev/null"
scp almofa@10.147.17.2:/tmp/backend_backup.tar.gz "$BACKUP_DIR/backend.tar.gz" 2>/dev/null

echo "📱 sgrd_final..."
tar -czf "$BACKUP_DIR/sgrd_final_source.tar.gz" --exclude="sgrd_final/build" --exclude="sgrd_final/.dart_tool" --exclude="sgrd_final/pubspec.lock" sgrd_final/

echo "📱 emergency_col..."
tar -czf "$BACKUP_DIR/emergency_col_source.tar.gz" --exclude="emergency_col/build" --exclude="emergency_col/.dart_tool" --exclude="emergency_col/pubspec.lock" emergency_col/ 2>/dev/null

echo "🌐 Frontend desplegado..."
ssh -t almofa@10.147.17.2 "echo 'almofa' | sudo -S tar -czf /tmp/frontend_deployed.tar.gz -C /var/www emergency_col/ 2>/dev/null"
scp almofa@10.147.17.2:/tmp/frontend_deployed.tar.gz "$BACKUP_DIR/frontend_deployed.tar.gz" 2>/dev/null

echo "📁 Scripts..."
mkdir -p "$BACKUP_DIR/scripts"
cp -r ~/scripts/* "$BACKUP_DIR/scripts/" 2>/dev/null

echo "📦 Comprimiendo..."
cd /tmp
tar -czf "/Users/admin/Documents/$BACKUP_FILE" "sgrd_backup_${FECHA}/"
rm -rf "$BACKUP_DIR"

cd /Users/admin/Documents
cp "$BACKUP_FILE" ~/Desktop/

echo ""
echo "✅ Backup completado!"
echo "📦 Archivo: $BACKUP_FILE"
echo "📏 Tamaño: $(du -h $BACKUP_FILE | cut -f1)"

echo "📤 Subiendo a GitHub..."
gh release upload v1.0.3 "$BACKUP_FILE" --repo alexelgordo72/emergency_col --clobber

echo ""
echo "✅ ¡Completado! 🔗 https://github.com/alexelgordo72/emergency_col/releases/tag/v1.0.3"
