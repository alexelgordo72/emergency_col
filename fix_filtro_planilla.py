import os

ruta = 'lib/screens/planilla_ruta_dialog.dart'
with open(ruta, 'r', encoding='utf-8') as f:
    c = f.read()

viejo_filtro = "r.estado.toLowerCase() == 'pendiente'"
nuevo_filtro = "r.estado.toLowerCase().trim() == 'pendiente' || r.estado.toLowerCase().trim() == 'recibido'"

if viejo_filtro in c:
    c = c.replace(viejo_filtro, nuevo_filtro)
    with open(ruta, 'w', encoding='utf-8') as f:
        f.write(c)
    print("✅ Filtro actualizado correctamente para incluir 'recibido' y 'pendiente'.")
else:
    print("⚠️ No se encontró la línea a reemplazar. Avisame si el problema persiste.")
