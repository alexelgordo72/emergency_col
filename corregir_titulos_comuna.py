import os

archivo = "lib/screens/planilla_ruta_dialog.dart"

if os.path.exists(archivo):
    with open(archivo, "r", encoding="utf-8") as f:
        lineas = f.readlines()

    # Reemplazamos la lógica del prefijo en las líneas 49 y 162
    for i in range(len(lineas)):
        if "String prefijoId =" in lineas[i]:
            lineas[i] = lineas[i].replace(
                "String prefijoId = idBarrio > 0 ? 'ID $idBarrio - ' : 'OTRO - '",
                "String prefijoId = 'COMUNA ${agrupados[barrio]?.first.comuna ?? 0} - '"
            )

    with open(archivo, "w", encoding="utf-8") as f:
        f.writelines(lineas)
    print("¡Títulos actualizados para mostrar COMUNA en lugar de ID!")
else:
    print("No se encontró el archivo.")
