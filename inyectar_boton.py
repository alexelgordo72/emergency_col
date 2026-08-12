import os

ruta = 'lib/main.dart'
with open(ruta, 'r', encoding='utf-8') as f:
    contenido = f.read()

# 1. Inyectar el import si no existe
if "import 'screens/trazabilidad_dialog.dart';" not in contenido:
    contenido = "import 'screens/trazabilidad_dialog.dart';\n" + contenido

# 2. Buscar el botón de edición e insertar el nuestro antes
if 'Icon(Icons.edit' in contenido:
    idx_lapis = contenido.find('Icon(Icons.edit')
    idx_boton = contenido.rfind('IconButton', 0, idx_lapis)
    
    if idx_boton != -1:
        nuevo_boton = """IconButton(
                                icon: const Icon(Icons.history_edu, color: Colors.blue),
                                tooltip: 'Trazabilidad y Ciclo de Vida',
                                onPressed: () {
                                  showDialog(
                                    context: context,
                                    barrierDismissible: false,
                                    builder: (context) => TrazabilidadDialog(reporte: reporte),
                                  );
                                },
                              ),
                              """
        contenido = contenido[:idx_boton] + nuevo_boton + contenido[idx_boton:]
        
        with open(ruta, 'w', encoding='utf-8') as f:
            f.write(contenido)
        print("✅ Botón de trazabilidad inyectado correctamente en main.dart")
    else:
        print("⚠️ No se encontró la estructura del botón. Avísame y lo ajustamos.")
else:
    print("⚠️ No se encontró el icono de edición (Icons.edit) en main.dart.")
