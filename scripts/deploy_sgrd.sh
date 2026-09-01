#!/bin/bash

echo "========================================"
echo "  SGRD Yumbo - Despliegue"
echo "========================================"
echo ""
echo "Selecciona el ambiente:"
echo "  1) Desarrollo (10.147.17.2)"
echo "  2) Producción (192.168.194.1)"
echo ""
read -p "Opción [1-2]: " AMBIENTE

case $AMBIENTE in
  1)
    USUARIO="almofa"
    IP="10.147.17.2"
    echo "📱 Desplegando a DESARROLLO..."
    ;;
  2)
    USUARIO="sgrd"
    IP="192.168.194.1"
    echo "📱 Desplegando a PRODUCCIÓN..."
    ;;
  *)
    echo "❌ Opción inválida"
    exit 1
    ;;
esac

cd /Users/admin/Documents/sgrd_final

echo "🧹 Limpiando..."
flutter clean
rm -rf build/ .dart_tool/ pubspec.lock

echo "📦 Obteniendo dependencias..."
flutter pub get

echo "🔨 Compilando..."
flutter build web --release

if [ ! -f "build/web/main.dart.js" ]; then
    echo "❌ Compilación falló"
    exit 1
fi

echo "✅ Compilación exitosa!"

cd build/web
echo "📦 Comprimiendo..."
tar -czf /tmp/sgrd_frontend.tar.gz *

echo "📤 Subiendo a $IP..."
scp /tmp/sgrd_frontend.tar.gz $USUARIO@$IP:/tmp/

ssh $USUARIO@$IP "sudo rm -rf /var/www/emergency_col/* && sudo tar -xzf /tmp/sgrd_frontend.tar.gz -C /var/www/emergency_col/ && sudo chown -R $USUARIO:$USUARIO /var/www/emergency_col/ && sudo systemctl reload nginx"

rm -f /tmp/sgrd_frontend.tar.gz

echo ""
echo "✅ ¡Despliegue completado!"
echo "📱 Frontend: http://$IP:8081"
echo "🔗 Backend API: http://$IP:8001"
echo ""
echo "🌐 Abriendo en el navegador..."
open http://$IP:8081
