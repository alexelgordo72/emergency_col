#!/bin/bash

cd /Users/admin/Documents/sgrd_final

echo "========================================"
echo "  SGRD Yumbo - Build y Deploy Desarrollo"
echo "========================================"

# 1. Configurar para desarrollo
echo "📝 Configurando para desarrollo..."
cat > lib/config.dart << 'CONFIG'
class AppConfig {
  static const String apiUrl = 'http://10.147.17.2:8001/api';
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
tar -czf /tmp/sgrd_frontend_dev.tar.gz *

# 4. Subir al servidor
echo "📤 Subiendo a desarrollo..."
scp /tmp/sgrd_frontend_dev.tar.gz almofa@10.147.17.2:/tmp/

# 5. Instalar en el servidor
echo "📥 Instalando en desarrollo..."
ssh almofa@10.147.17.2 << 'INSTALL'
echo "🔄 Extrayendo archivos..."
sudo rm -rf /home/almofa/frontend_sgrd/*
sudo tar -xzf /tmp/sgrd_frontend_dev.tar.gz -C /home/almofa/frontend_sgrd/
sudo chown -R almofa:almofa /home/almofa/frontend_sgrd/
sudo chmod -R 755 /home/almofa/frontend_sgrd/
sudo systemctl reload nginx
echo "✅ Frontend instalado"
INSTALL

# 6. Limpiar
rm -f /tmp/sgrd_frontend_dev.tar.gz

echo ""
echo "✅ ¡Frontend desplegado en DESARROLLO!"
echo "📱 http://10.147.17.2:8081"
echo "========================================"
