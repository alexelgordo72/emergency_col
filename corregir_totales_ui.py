import os

archivo = "lib/screens/planilla_ruta_dialog.dart"

if not os.path.exists(archivo):
    print(f"Error: No se encontró el archivo {archivo}.")
    exit(1)

with open(archivo, "r", encoding="utf-8") as f:
    codigo = f.read()

# Reemplazamos la variable incorrecta por la estándar del FutureBuilder
codigo = codigo.replace("${reportes.length}", "${snapshot.data?.length ?? 0}")

with open(archivo, "w", encoding="utf-8") as f:
    f.write(codigo)

print("¡Código corregido! Se reemplazó 'reportes' por 'snapshot.data'.")
