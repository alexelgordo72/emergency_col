#!/bin/bash

cd /Users/admin/Documents/sgrd_final

echo "========================================"
echo "  SGRD Yumbo - Build y Deploy por Entorno"
echo "========================================"
echo ""
echo "Selecciona el entorno:"
echo "  1) Desarrollo (10.147.17.2)"
echo "  2) Producción (192.168.194.1)"
echo ""
read -p "Opción [1-2]: " ENV_OPCION

case $ENV_OPCION in
  1)
    ENTORNO="desarrollo"
    API_URL="http://10.147.17.2:8001/api"
    USUARIO="almofa"
    IP="10.147.17.2"
    ;;
  2)
    ENTORNO="produccion"
    API_URL="https://192.168.194.1:8001/api"
    USUARIO="sgrd"
    IP="192.168.194.1"
    ;;
  *)
    echo "❌ Opción inválida"
    exit 1
    ;;
esac

echo ""
echo "📝 Configurando para $ENTORNO..."
cat > lib/config.dart << CONFIG
class AppConfig {
  static const String apiUrl = '$API_URL';
}
CONFIG

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

echo "📦 Empaquetando..."
cd build/web
tar -czf /tmp/sgrd_frontend_${ENTORNO}.tar.gz *

echo "📤 Subiendo a $ENTORNO ($IP)..."
scp /tmp/sgrd_frontend_${ENTORNO}.tar.gz $USUARIO@$IP:/tmp/

echo "📥 Instalando..."
ssh $USUARIO@$IP << INSTALL
sudo rm -rf /home/$USUARIO/frontend_sgrd/*
sudo tar -xzf /tmp/sgrd_frontend_${ENTORNO}.tar.gz -C /home/$USUARIO/frontend_sgrd/
sudo chown -R $USUARIO:$USUARIO /home/$USUARIO/frontend_sgrd/
sudo chmod -R 755 /home/$USUARIO/frontend_sgrd/
sudo systemctl reload nginx
INSTALL

rm -f /tmp/sgrd_frontend_${ENTORNO}.tar.gz

echo ""
echo "✅ ¡Frontend desplegado en $ENTORNO!"
echo "📱 http://$IP:8081"
if [ "$ENTORNO" = "produccion" ]; then
    echo "🔗 https://baseball-voluntary-cassette-removed.trycloudflare.com"
fi
echo "========================================"
