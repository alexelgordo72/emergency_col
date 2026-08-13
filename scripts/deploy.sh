#!/bin/bash
echo "🚀 Desplegando al servidor..."
./scripts/build_prod.sh
scp -r build/web/* almofa@10.147.17.2:/home/almofa/frontend_sgrd/
echo "✅ Despliegue completado!"
echo "🌐 Accede en: http://10.147.17.2"
