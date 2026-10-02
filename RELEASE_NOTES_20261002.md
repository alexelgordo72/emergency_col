# Release SGRD Yumbo - 2026-10-02
# Release SGRD Yumbo - 2026-10-02

## Componentes

### Frontend (Flutter)
- Build de produccion: gs://sgrd-uploads/frontend/build/sgrd_frontend_v3_20261002_125323.tar.gz
- Codigo fuente: gs://sgrd-uploads/frontend/source/sgrd_frontend_release_20261002_60b8914.tar.gz
- Commit Git: b3790ed (rama feature/inventario-observaciones)
- Repo: https://github.com/alexelgordo72/emergency_col
- Cambio principal: URL de API cambiada a relativa (/api) para funcionar con tunel Cloudflare.

### Backend (FastAPI)
- Archivo: gs://sgrd-uploads/backend/sgrd_backend_release_20261002_181117.tar.gz
- Usuario BD: app_sgrd_write
- Tablas nuevas: solicitudes, rufes, ahe
- Endpoint: Puerto 8001

### Base de Datos (PostgreSQL)
- Archivo: gs://sgrd-uploads/database/sgrd_db_release_20261002_181131.sql.gz
- Usuario: admin_comunidad
- Base de datos: comunidad_db
- Contenido:
  - solicitudes: 1732 registros
  - rufes: 1516 registros (incluye 13 RDE)
  - ahe: 2 registros
  - reportes_comunitarios: 3250 registros (historico)

## Infraestructura

- Servidor: sgrd-yumbo-vm (GCP)
- IP ZeroTier: 10.147.17.24
- Backend: http://10.147.17.24:8001 (Docker: api_sgrd)
- Frontend: http://10.147.17.24:8081 (Nginx -> /var/www/emergency_col)
- Tunel Cloudflare: https://balance-accessories-extras-moms.trycloudflare.com
- Base de Datos: 10.147.17.24:5432 (Docker: db_sgrd)

## Como restaurar

### Backend
tar -xzvf sgrd_backend_release_20261002_181117.tar.gz -C /home/alexelgordo/backend_sgrd/
cd /home/alexelgordo/backend_sgrd
docker-compose down
docker-compose up -d --build

### Base de Datos
docker cp sgrd_db_release_20261002_181131.sql.gz db_sgrd:/tmp/
docker exec db_sgrd gunzip -c /tmp/sgrd_db_release_20261002_181131.sql.gz | psql -U admin_comunidad -d comunidad_db

### Frontend
tar -xzvf sgrd_frontend_v3_20261002_125323.tar.gz -C /var/www/emergency_col/
sudo chown -R www-data:www-data /var/www/emergency_col/
sudo systemctl reload nginx
