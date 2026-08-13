import os

archivo_modelo = "lib/models/reporte_comunitario.dart"

if not os.path.exists(archivo_modelo):
    print(f"Error: No se encontró el archivo {archivo_modelo}")
    exit(1)

with open(archivo_modelo, "r", encoding="utf-8") as f:
    contenido = f.read()

# Verificamos si ya tiene el campo comuna para no duplicarlo
if "final int? comuna;" not in contenido and "final int comuna;" not in contenido:
    # Insertamos la propiedad justo antes del cierre de la clase o después de sectorBarrio
    if "final String? sectorBarrio;" in contenido:
        contenido = contenido.replace(
            "final String? sectorBarrio;", 
            "final String? sectorBarrio;\n  final int? comuna;"
        )
    
    # Insertamos en el constructor si existe
    if "this.sectorBarrio," in contenido:
        contenido = contenido.replace(
            "this.sectorBarrio,", 
            "this.sectorBarrio,\n    this.comuna,"
        )

    # Insertamos en el fromJson
    if "sectorBarrio:" in contenido:
        contenido = contenido.replace(
            "sectorBarrio: json['sector_barrio']", 
            "sectorBarrio: json['sector_barrio'],\n      comuna: json['comuna'] is int ? json['comuna'] : int.tryParse(json['comuna']?.toString() ?? '0')"
        )

    with open(archivo_modelo, "w", encoding="utf-8") as f:
        f.write(contenido)
    print("¡Modelo actualizado con éxito con el campo comuna!")
else:
    print("El modelo ya cuenta con el campo comuna.")
