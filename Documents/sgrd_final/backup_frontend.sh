#!/bin/bash
# ============================================================
# BACKUP DEL FRONTEND - SGRD Yumbo
# ============================================================

FECHA=$(date +%Y%m%d_%H%M%S)
FECHA_DIR=$(date +%Y%m%d)
BACKUP_DIR="/tmp/frontend_backups"
BUCKET="gs://sgrd-uploads/backups/${FECHA_DIR}"

mkdir -p ${BACKUP_DIR}

echo "========================================"
echo "BACKUP FRONTEND - ${FECHA}"
echo "========================================"

# Backup del código fuente
echo "📦 Empaquetando frontend..."
cd /Users/admin/Documents/sgrd_final
tar -czf ${BACKUP_DIR}/frontend_${FECHA}.tar.gz \
  --exclude=build \
  --exclude=.dart_tool \
  --exclude=pubspec.lock \
  .

echo "✅ Frontend empaquetado: $(ls -lh ${BACKUP_DIR}/frontend_${FECHA}.tar.gz | awk '{print $5}')"

# Subir al bucket
echo "📤 Subiendo al bucket..."
/Users/admin/Downloads/google-cloud-sdk/bin/gsutil cp ${BACKUP_DIR}/frontend_${FECHA}.tar.gz ${BUCKET}/

echo "✅ Frontend subido al bucket"
echo "📦 Archivo: ${BUCKET}/frontend_${FECHA}.tar.gz"
