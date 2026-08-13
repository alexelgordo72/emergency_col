#!/bin/bash
echo "🚀 Construyendo Emergency Col para producción..."
flutter clean
flutter pub get
flutter build web --release --dart-define=API_URL=http://10.147.17.2:8000
echo "✅ Construcción completada!"
