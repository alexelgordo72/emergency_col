#!/usr/bin/env python3
"""
Script de backup completo de la base de datos comunidad_db
- Estructura + Datos
- Backup local (Mac)
- Backup en GCS
- Backup en Google Drive (rclone)
"""

import subprocess
import os
from datetime import datetime
import sys

# =====================================================
# CONFIGURACIÓN
# =====================================================

VM_NAME = "sgrd-yumbo-vm"
ZONE = "us-central1-a"
USER = "alexelgordo"
SSH_KEY = os.path.expanduser("~/.ssh/id_rsa")

DB_CONTAINER = "db_sgrd"
DB_NAME = "comunidad_db"
DB_USER = "admin_comunidad"

LOCAL_BACKUP_DIR = os.path.expanduser("~/Documents/sgrd_final_backups")
GCS_BUCKET = "gs://sgrd-uploads/backups/completo"

FECHA = datetime.now().strftime("%Y%m%d_%H%M%S")

# =====================================================
# FUNCIONES
# =====================================================

def run_command(cmd, description, check=True):
    print(f"\n{'='*60}")
    print(f"🔄 {description}")
    print(f"{'='*60}")
    print(f"$ {cmd}\n")
    
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr)
    
    if check and result.returncode != 0:
        print(f"❌ ERROR: {description}")
        sys.exit(1)
    
    return result

def ssh_command(remote_cmd, description):
    cmd = f'gcloud compute ssh {USER}@{VM_NAME} --zone={ZONE} --ssh-key-file={SSH_KEY} --command="{remote_cmd}"'
    return run_command(cmd, description)

def main():
    print("="*60)
    print(f"🚀 BACKUP COMPLETO DE comunidad_db")
    print(f"📅 Fecha: {FECHA}")
    print("="*60)
    
    local_backup_path = os.path.join(LOCAL_BACKUP_DIR, f"completo_{FECHA}")
    os.makedirs(local_backup_path, exist_ok=True)
    print(f"\n📁 Carpeta local: {local_backup_path}")
    
    # PASO 1: Verificar conexión SSH
    ssh_command("hostname && whoami", "Verificando conexión SSH")
    
    # PASO 2: Verificar contenedor
    ssh_command(f"sudo docker ps | grep {DB_CONTAINER}", "Verificando contenedor Docker")
    
    # PASO 3: Crear backup custom
    remote_backup_dir = f"~/backups/completo_{FECHA}"
    
    ssh_command(
        f"mkdir -p {remote_backup_dir} && cd {remote_backup_dir} && "
        f"sudo docker exec {DB_CONTAINER} pg_dump -U {DB_USER} -d {DB_NAME} "
        f"--format=custom --verbose > db_completo_{FECHA}.backup 2> backup_log_{FECHA}.txt && "
        f"ls -lh",
        "Creando backup custom en la VM"
    )
    
    # PASO 4: Crear backup SQL
    ssh_command(
        f"cd {remote_backup_dir} && "
        f"sudo docker exec {DB_CONTAINER} pg_dump -U {DB_USER} -d {DB_NAME} "
        f"--clean --if-exists --inserts | gzip > db_completo_{FECHA}.sql.gz && "
        f"ls -lh",
        "Creando backup SQL en la VM"
    )
    
    # PASO 5: Verificar backup
    ssh_command(
        f"cd {remote_backup_dir} && "
        f"echo '--- Tablas en el backup ---' && "
        f"sudo docker exec {DB_CONTAINER} pg_restore -l db_completo_{FECHA}.backup | grep 'TABLE DATA' | wc -l && "
        f"ls -lh",
        "Verificando backup"
    )
    
    # PASO 6: Subir a GCS
    ssh_command(
        f"gsutil cp {remote_backup_dir}/*.backup {remote_backup_dir}/*.sql.gz "
        f"{GCS_BUCKET}/{FECHA}/ && "
        f"gsutil ls {GCS_BUCKET}/{FECHA}/",
        "Subiendo backup a GCS"
    )
    
    # PASO 7: Descargar a Mac
    run_command(
        f'gcloud compute scp {USER}@{VM_NAME}:{remote_backup_dir}/*.backup '
        f'{local_backup_path}/ --zone={ZONE} --ssh-key-file={SSH_KEY}',
        "Descargando backup custom a la Mac"
    )
    
    run_command(
        f'gcloud compute scp {USER}@{VM_NAME}:{remote_backup_dir}/*.sql.gz '
        f'{local_backup_path}/ --zone={ZONE} --ssh-key-file={SSH_KEY}',
        "Descargando backup SQL a la Mac"
    )
    
    # PASO 8: Subir a Google Drive
    result = subprocess.run("which rclone", shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        run_command(
            f'rclone copy {local_backup_path}/ gdrive:backups_sgrd_completo_{FECHA}/',
            "Subiendo backup a Google Drive"
        )
        run_command(
            f'rclone ls gdrive:backups_sgrd_completo_{FECHA}/',
            "Verificando backup en Google Drive"
        )
    else:
        print("\n⚠️ rclone no está instalado. Saltando subida a Google Drive.")
        print("   Puedes subir manualmente desde: " + local_backup_path)
    
    # RESUMEN
    print("\n" + "="*60)
    print("✅ BACKUP COMPLETO FINALIZADO")
    print("="*60)
    print(f"\n📁 Local (Mac): {local_backup_path}/")
    print(f"☁️ GCS: {GCS_BUCKET}/{FECHA}/")
    if result.returncode == 0:
        print(f"📁 Google Drive: gdrive:backups_sgrd_completo_{FECHA}/")
    print(f"🖥️ VM: {remote_backup_dir}/")
    print("\n🎉 ¡Backup completado exitosamente!")

if __name__ == "__main__":
    main()
