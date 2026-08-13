import os

archivo = "lib/screens/planilla_ruta_dialog.dart"

if not os.path.exists(archivo):
    print(f"Error: No se encontró el archivo {archivo}.")
    exit(1)

with open(archivo, "r", encoding="utf-8") as f:
    lineas = f.readlines()

for i in range(len(lineas)):
    # Buscamos específicamente la línea del PDF donde usamos pw.Text
    if "pw.Text('SGRD YUMBO - PLANILLA DE RUTA DE VISITAS" in lineas[i]:
        lineas[i] = lineas[i].replace(
            "${snapshot.data?.length ?? 0}", 
            "${agrupados.values.fold<int>(0, (p, c) => p + c.length)}"
        )
        break # Solo lo cambiamos aquí, dejamos la UI intacta

with open(archivo, "w", encoding="utf-8") as f:
    f.writelines(lineas)

print("¡Alcance de variable corregido para el PDF!")
