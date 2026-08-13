#!/bin/bash
echo "🚀 Desplegando a desarrollo (10.147.17.2)..."

# Compilar
flutter clean
flutter pub get
flutter build web --release --dart-define=API_URL=http://10.147.17.2:8000

# Copiar al servidor
scp -r build/web/* almofa@10.147.17.2:/tmp/frontend_sgrd/

# Mover a la carpeta final y dar permisos
ssh almofa@10.147.17.2 "sudo rm -rf /var/www/emergency_col/* && \
                         sudo cp -r /tmp/frontend_sgrd/* /var/www/emergency_col/ && \
                         sudo chown -R www-data:www-data /var/www/emergency_col && \
                         sudo chmod -R 755 /var/www/emergency_col && \
                         rm -rf /tmp/frontend_sgrd"

echo "✅ Despliegue completado!"
echo "🌐 Accede en: http://10.147.17.2:8080"
