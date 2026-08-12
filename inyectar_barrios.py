import os

ruta = 'lib/main.dart'
with open(ruta, 'r', encoding='utf-8') as f:
    c = f.read()

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

if 'PlanillaRutaDialog' in c and 'GestionBarriosDialog(' not in c:
    # Insertar justo antes del botón de la planilla para que queden juntos
    idx = c.find("tooltip: 'Generar Planilla de Ruta'")
    idx_start = c.rfind("IconButton", 0, idx)
    c = c[:idx_start] + boton_barrios + c[idx_start:]
    with open(ruta, 'w', encoding='utf-8') as f:
        f.write(c)
    print("✅ Botón de Gestión de Barrios inyectado en el AppBar.")
