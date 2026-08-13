import os

archivo = "lib/screens/planilla_ruta_dialog.dart"

if os.path.exists(archivo):
    with open(archivo, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Reemplazamos la forma en cómo se pinta el título de la sección para incluir la comuna real del reporte
    # Buscamos donde imprime el nombre del barrio y anteponemos la comuna
    viejo_texto = "Text('ID ' +"
    # O si usa interpolación directa con el barrio:
    # Vamos a buscar la línea del encabezado de la tarjeta en la UI
    
    # Reemplazo seguro buscando el texto que muestra el título del grupo
    if "Barrio:" in content or "$barrio" in content:
        # Actualizamos la línea del Text que muestra el encabezado del grupo en la UI
        content = content.replace(
            "Text('$barrio'", 
            "Text('COMUNA ${agrupados[barrio]?.first.comuna ?? 0} - $barrio'"
        )

    with open(archivo, "w", encoding="utf-8") as f:
        f.write(content)
    print("¡Encabezado de la UI actualizado para mostrar la comuna!")
else:
    print("No se encontró el archivo planilla_ruta_dialog.dart")
