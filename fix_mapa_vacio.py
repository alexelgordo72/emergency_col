import os

ruta = 'lib/main.dart'
with open(ruta, 'r', encoding='utf-8') as f:
    c = f.read()

# Buscar la capa de la polilínea y envolverla en un condicional
bloque_viejo = """                        PolylineLayer(
                          polylines: [
                            Polyline(
                              points: rutaOrdenada,
                              strokeWidth: 4.0,
                              color: Colors.blueAccent.withOpacity(0.7),
                            ),
                          ],
                        ),"""

bloque_nuevo = """                        if (rutaOrdenada.isNotEmpty)
                          PolylineLayer(
                            polylines: [
                              Polyline(
                                points: rutaOrdenada,
                                strokeWidth: 4.0,
                                color: Colors.blueAccent.withOpacity(0.7),
                              ),
                            ],
                          ),"""

if bloque_viejo in c:
    c = c.replace(bloque_viejo, bloque_nuevo)
    with open(ruta, 'w', encoding='utf-8') as f:
        f.write(c)
    print("✅ Seguro anti-colapso aplicado al mapa.")
else:
    print("⚠️ No se encontró el bloque exacto. Es posible que ya esté corregido.")
