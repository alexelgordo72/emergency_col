import os
import re

archivo = "lib/screens/planilla_ruta_dialog.dart"

if not os.path.exists(archivo):
    print(f"Error: No se encontró el archivo {archivo}.")
    exit(1)

with open(archivo, "r", encoding="utf-8") as f:
    codigo = f.read()

# 1. Agregar el Total General en el título principal
# Asume que la variable de la lista completa se llama 'reportes' o similar.
if "Total general" not in codigo:
    codigo = re.sub(
        r"(Text\(\s*['\"]SGRD YUMBO - PLANILLA DE RUTA DE VISITAS['\"])",
        r"Text('SGRD YUMBO - PLANILLA DE RUTA DE VISITAS\\nTotal general de registros en este reporte: ${reportes.length}'",
        codigo
    )

# 2. Agregar el Total por Barrio en el encabezado oscuro
# Busca la interpolación de texto que empieza con 'ID...' y le suma el conteo.
# Asume que iteras sobre un mapa y la lista agrupada está en 'entry.value'.
if "(Total:" not in codigo:
    codigo = re.sub(
        r"(Text\(\s*['\"]ID [^'\"]+['\"])",
        r"\1 + ' (Total: ${entry.value.length} registros)'",
        codigo
    )

with open(archivo, "w", encoding="utf-8") as f:
    f.write(codigo)

print("¡Textos inyectados correctamente! Revisa planilla_ruta_dialog.dart si usas nombres de variables distintos a 'reportes' o 'entry.value'.")
