import os

archivo = "lib/models/reporte_comunitario.dart"

if not os.path.exists(archivo):
    print("No se encontró el archivo.")
    exit(1)

with open(archivo, "r", encoding="utf-8") as f:
    codigo = f.read()

# 1. Añadir la propiedad comuna si no existe
if "final int? comuna;" not in codigo:
    codigo = codigo.replace(
        "final Map<String, dynamic>? datosExtra;",
        "final Map<String, dynamic>? datosExtra;\n  final int? comuna;"
    )

# 2. Añadir comuna al constructor si no existe
if "this.comuna," not in codigo:
    codigo = codigo.replace(
        "this.datosExtra,",
        "this.datosExtra,\n    this.comuna,"
    )

# 3. Añadir el mapeo desde JSON (buscando el método fromJson o creando un parche seguro)
if "comuna:" not in codigo and "factory ReporteComunitario.fromJson" in codigo:
    codigo = codigo.replace(
        "datosExtra:",
        "comuna: json['comuna'] is int ? json['comuna'] : int.tryParse(json['comuna']?.toString() ?? '0'),\n      datosExtra:"
    )

with open(archivo, "w", encoding="utf-8") as f:
    f.write(codigo)

print("¡Modelo ReporteComunitario actualizado con éxito!")
