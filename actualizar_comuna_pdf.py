import os

# 1. Actualizar el modelo ReporteComunitario para incluir 'comuna'
modelo_path = "lib/models/reporte_comunitario.dart"
if os.path.exists(modelo_path):
    with open(modelo_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    if "final int? comuna;" not in content:
        # Insertamos el campo comuna en la clase
        content = content.replace("final String? sectorBarrio;", "final String? sectorBarrio;\n  final int? comuna;")
        # Lo agregamos al constructor
        content = content.replace("this.sectorBarrio,", "this.sectorBarrio,\n    this.comuna,")
        # Lo agregamos al fromJson si existe
        content = content.replace("sectorBarrio: json['sector_barrio']", "sectorBarrio: json['sector_barrio'],\n      comuna: json['comuna']")
        
        with open(modelo_path, "w", encoding="utf-8") as f:
            f.write(content)
        print("-> Modelo ReporteComunitario actualizado con 'comuna'.")
    else:
        print("-> El modelo ya tiene la comuna incluida.")

# 2. Actualizar el PDF en planilla_ruta_dialog.dart para pintarla en el título
dialog_path = "lib/screens/planilla_ruta_dialog.dart"
if os.path.exists(dialog_path):
    with open(dialog_path, "r", encoding="utf-8") as f:
        d_content = f.read()
    
    # Cambiamos el texto del encabezado del PDF para incluir la comuna
    viejo_header = "child: pw.Text('ID 1 - $barrio'"
    # O un reemplazo genérico para el título del barrio en el PDF
    d_content = d_content.replace(
        "child: pw.Text('$barrio',", 
        "child: pw.Text('COMUNA ${agrupados[barrio]?.first.comuna ?? 0} - $barrio',"
    )
    
    with open(dialog_path, "w", encoding="utf-8") as f:
        f.write(d_content)
    print("-> Vista del PDF en planilla_ruta_dialog.dart actualizada.")

