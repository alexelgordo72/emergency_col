import os

ruta = 'lib/main.dart'
with open(ruta, 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Asegurar que el servicio correcto esté importado
if "import 'services/barrio_service.dart';" not in c:
    c = "import 'services/barrio_service.dart';\n" + c

# 2. Reemplazar la línea problemática que trae la cadena sucia por la limpia
linea_vieja = "List<String> listaBarrios = await ApiService.obtenerBarrios();"
linea_nueva = """var listaBarriosObj = await BarrioService.getBarrios();
    List<String> listaBarrios = listaBarriosObj.map((b) => b.nombre).toList();"""

if linea_vieja in c:
    c = c.replace(linea_vieja, linea_nueva)
    with open(ruta, 'w', encoding='utf-8') as f:
        f.write(c)
    print("✅ Menú desplegable arreglado. Ahora mostrará y guardará solo el nombre.")
else:
    print("⚠️ No encontré la línea exacta. Avisame si el problema persiste.")

