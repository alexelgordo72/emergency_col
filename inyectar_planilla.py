import os

ruta = 'lib/main.dart'
with open(ruta, 'r', encoding='utf-8') as f:
    c = f.read()

# Inyectar el import de la planilla si no existe
if "import 'screens/planilla_ruta_dialog.dart';" not in c:
    c = "import 'screens/planilla_ruta_dialog.dart';\n" + c

# Buscar el AppBar para inyectar la acción del botón de reporte
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
          ),
"""

if 'actions: [' in c and 'PlanillaRutaDialog' not in c:
    c = c.replace('actions: [', 'actions: [' + boton_planilla)
    with open(ruta, 'w', encoding='utf-8') as f:
        f.write(c)
    print("✅ Botón de Planilla de Ruta inyectado en el AppBar de main.dart")
elif 'AppBar(' in c and 'PlanillaRutaDialog' not in c:
    # Si no tiene un arreglo de actions creado en el AppBar, se lo creamos
    idx = c.find('AppBar(')
    idx_title = c.find('title:', idx)
    c = c[:idx_title] + f'actions: [{boton_planilla}],\n        ' + c[idx_title:]
    with open(ruta, 'w', encoding='utf-8') as f:
        f.write(c)
    print("✅ Actions y Botón de Planilla inyectados en el AppBar de main.dart")
else:
    print("⚠️ El botón parece ya estar inyectado o no se encontró el AppBar.")

