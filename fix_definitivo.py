import os
import re

ruta = 'lib/main.dart'
with open(ruta, 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Limpiar CUALQUIER intento fallido previo para que no haya errores
patron = re.compile(r'IconButton\(\s*icon:\s*const\s*Icon\(Icons\.holiday_village.*?,\s*\n\s*\),?', re.DOTALL)
c = patron.sub('', c)

# 2. Asegurar el import
if "import 'screens/gestion_barrios_dialog.dart';" not in c:
    c = "import 'screens/gestion_barrios_dialog.dart';\n" + c

nuevo_boton = """
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

# 3. Inyección quirúrgica usando el botón de la planilla como ancla
idx_assignment = c.find('Icons.assignment_late')
if idx_assignment != -1:
    idx_actions = c.rfind('actions:', 0, idx_assignment)
    if idx_actions != -1:
        idx_bracket = c.find('[', idx_actions)
        if idx_bracket != -1:
            c = c[:idx_bracket+1] + nuevo_boton + c[idx_bracket+1:]
            with open(ruta, 'w', encoding='utf-8') as f:
                f.write(c)
            print("✅ ¡Éxito total! El botón se inyectó correctamente junto al portapapeles.")
        else:
            print("❌ Fallo: No encontré '[' después de actions.")
    else:
        print("❌ Fallo: No encontré 'actions:' antes del botón de planilla.")
else:
    print("❌ Fallo: No encontré 'assignment_late' en el archivo.")
