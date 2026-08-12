import os

ruta = 'lib/main.dart'
with open(ruta, 'r', encoding='utf-8') as f:
    lineas = f.readlines()

# 1. Asegurar el import en la primera línea
import_line = "import 'screens/gestion_barrios_dialog.dart';\n"
if import_line not in lineas and not any('gestion_barrios_dialog.dart' in l for l in lineas):
    lineas.insert(0, import_line)

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

# 2. Buscar la línea exacta del portapapeles (assignment_late)
idx_target = -1
for i, linea in enumerate(lineas):
    if 'Icons.assignment_late' in linea:
        idx_target = i
        break

if idx_target != -1:
    # 3. Retroceder hasta encontrar el inicio de ese IconButton e inyectar el nuestro
    for j in range(idx_target, -1, -1):
        if 'IconButton' in lineas[j]:
            # Verificar que no lo hayamos inyectado ya en intentos anteriores
            if not any('Icons.holiday_village' in l for l in lineas[max(0, j-15):j]):
                lineas.insert(j, boton_barrios)
                with open(ruta, 'w', encoding='utf-8') as f:
                    f.writelines(lineas)
                print("✅ ¡Éxito! Botón inyectado de forma precisa junto a la planilla.")
            else:
                print("✅ El botón ya parece estar cerca de esa línea. Verifica si hay un error en Flutter.")
            break
else:
    print("⚠️ No encontré el botón de assignment_late en el código.")
