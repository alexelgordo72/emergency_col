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

# 2. Inyectar a la fuerza justo después de abrir la lista de "actions:"
if 'Icons.holiday_village' not in c:
    # Esta expresión regular atrapa "actions: [" o "actions: <Widget>[" sin importar los espacios
    c = re.sub(r'(actions:\s*(?:<Widget>)?\s*\[)', r'\1\n' + boton_barrios, c, count=1)
    
    with open(ruta, 'w', encoding='utf-8') as f:
        f.write(c)
    print("✅ Botón de Barrios inyectado a la fuerza en el menú superior.")
else:
    print("⚠️ El código ya estaba en el archivo. Forzando un guardado por si acaso...")
    with open(ruta, 'w', encoding='utf-8') as f:
        f.write(c)
