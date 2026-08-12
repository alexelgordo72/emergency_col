import os

ruta = 'lib/main.dart'
with open(ruta, 'r', encoding='utf-8') as f:
    c = f.read()

# Asegurar importaciones
if "import 'screens/planilla_ruta_dialog.dart';" not in c:
    c = "import 'screens/planilla_ruta_dialog.dart';\n" + c
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
          ),"""

boton_planilla = """
          IconButton(
            icon: const Icon(Icons.assignment_late, color: Colors.white, size: 28),
            tooltip: 'Generar Planilla de Ruta',
            onPressed: () {
              showDialog(
                context: context,
                builder: (context) => const PlanillaRutaDialog(),
              );
            },
          ),"""

ambos_botones = boton_barrios + boton_planilla

# Insertar de forma segura sin usar expresiones regulares destructivas
if 'actions: [' in c:
    if 'Icons.holiday_village' not in c:
        c = c.replace('actions: [', 'actions: [' + ambos_botones)
elif 'AppBar(' in c:
    idx_appbar = c.find('AppBar(')
    idx_title = c.find('title:', idx_appbar)
    if idx_title != -1:
        c = c[:idx_title] + f'actions: [{ambos_botones}],\n        ' + c[idx_title:]

with open(ruta, 'w', encoding='utf-8') as f:
    f.write(c)
print("✅ Código recuperado y botones inyectados con éxito.")
