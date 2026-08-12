import re

ruta = 'lib/main.dart'
with open(ruta, 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Asegurar el import
if "import 'screens/gestion_barrios_dialog.dart';" not in c:
    c = "import 'screens/gestion_barrios_dialog.dart';\n" + c

boton_barrios = """
          IconButton(
            icon: const Icon(Icons.holiday_village, color: Colors.white, size: 28),
            tooltip: 'Gestión de Barrios',
            onPressed: () {
              showDialog(
                context: context,
                builder: (context) => const GestionBarriosDialog(),
              );
            },
          ),
"""

# 2. Buscar exactamente el botón de la planilla (assignment_late) e inyectar el de barrios justo antes
if 'Icons.holiday_village' not in c:
    # Usamos expresiones regulares para encontrar el inicio exacto del botón de la planilla
    pattern = r"(IconButton\s*\(\s*icon:\s*const\s*Icon\(\s*Icons\.assignment_late)"
    match = re.search(pattern, c)
    
    if match:
        idx = match.start()
        c = c[:idx] + boton_barrios + c[idx:]
        with open(ruta, 'w', encoding='utf-8') as f:
            f.write(c)
        print("✅ ¡Éxito! Botón de Barrios inyectado correctamente junto al de la planilla.")
    else:
        print("⚠️ No encontré el botón de la planilla para usarlo como referencia.")
else:
    print("✅ El código del botón ya estaba, solo faltaba recargar.")

