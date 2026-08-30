#!/bin/bash

cd /Users/admin/Documents/sgrd_final

echo "========================================"
echo "  SGRD Yumbo - Build y Deploy Producción"
echo "========================================"

# 1. Configurar para producción
echo "📝 Configurando para producción..."
cat > lib/config.dart << 'CONFIG'
class AppConfig {
  static const String apiUrl = 'https://192.168.194.1:8001/api';
}
CONFIG

echo "✅ Config creada"

# 2. Compilar
echo "🔨 Compilando..."
flutter clean
rm -rf build/ .dart_tool/ pubspec.lock
flutter pub get
flutter build web --release

if [ ! -f "build/web/main.dart.js" ]; then
    echo "❌ Compilación falló"
    exit 1
fi
echo "✅ Compilación exitosa"

# 3. Empaquetar
echo "📦 Empaquetando..."
cd build/web
tar -czf /tmp/sgrd_frontend_prod.tar.gz *

# 4. Subir al servidor
echo "📤 Subiendo a producción..."
scp /tmp/sgrd_frontend_prod.tar.gz sgrd@192.168.194.1:/tmp/

# 5. Instalar en el servidor (conectando y ejecutando manualmente)
echo "📥 Instalando en producción..."
ssh sgrd@192.168.194.1 << 'INSTALL'
echo "🔄 Extrayendo archivos..."
sudo rm -rf /home/sgrd/frontend_sgrd/*
sudo tar -xzf /tmp/sgrd_frontend_prod.tar.gz -C /home/sgrd/frontend_sgrd/
sudo chown -R sgrd:sgrd /home/sgrd/frontend_sgrd/
sudo chmod -R 755 /home/sgrd/frontend_sgrd/
sudo systemctl reload nginx
echo "✅ Frontend instalado"
INSTALL

# 6. Limpiar
rm -f /tmp/sgrd_frontend_prod.tar.gz

echo ""
echo "✅ ¡Frontend desplegado en PRODUCCIÓN!"
echo "📱 https://baseball-voluntary-cassette-removed.trycloudflare.com"
echo "🌐 http://192.168.194.1:8081"
echo "========================================"
