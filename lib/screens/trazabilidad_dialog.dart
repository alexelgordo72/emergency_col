import 'package:flutter/material.dart';
import '../services/api_service.dart';
import '../models/reporte_comunitario.dart';
import '../models/trazabilidad_model.dart';

class TrazabilidadDialog extends StatefulWidget {
  final ReporteComunitario reporte;

  const TrazabilidadDialog({Key? key, required this.reporte}) : super(key: key);

  @override
  _TrazabilidadDialogState createState() => _TrazabilidadDialogState();
}

class _TrazabilidadDialogState extends State<TrazabilidadDialog> {
  late Future<List<TrazabilidadItem>> futureHistorial;
  String estadoSeleccionado = 'Pendiente';
  final observacionController = TextEditingController();
  bool guardando = false;

  @override
  void initState() {
    super.initState();
    // Ajustar al nombre correcto de la variable: estado
    String estadoActual = widget.reporte.estado;
    estadoSeleccionado = ['Pendiente', 'En Proceso', 'Inspeccionado', 'Cerrado'].contains(estadoActual) 
        ? estadoActual 
        : 'Pendiente';
    _cargarHistorial();
  }

  void _cargarHistorial() {
    setState(() {
      futureHistorial = ApiService.obtenerHistorial(widget.reporte.id);
    });
  }

  Future<void> _guardarTrazabilidad() async {
    if (observacionController.text.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Por favor, ingresa el detalle de la accion.', style: TextStyle(color: Colors.white)), backgroundColor: Colors.red),
      );
      return;
    }
    setState(() => guardando = true);
    try {
      bool exito = await ApiService.actualizarEstadoTrazabilidad(
        widget.reporte.id,
        estadoSeleccionado,
        observacionController.text,
      );
      if (exito) {
        observacionController.clear();
        _cargarHistorial();
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Registro guardado exitosamente'), backgroundColor: Colors.green),
        );
      }
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Error: $e'), backgroundColor: Colors.red),
      );
    } finally {
      setState(() => guardando = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    // Extraer el nombre del ciudadano si existe
    String nombreAfectado = widget.reporte.datosExtra?['ciudadano'] ?? 'No registrado';

    return Dialog(
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: Container(
        width: 1000,
        height: 650,
        padding: const EdgeInsets.all(24),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(
                  'Trazabilidad: ${widget.reporte.titulo}',
                  style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold, color: Colors.red[900]),
                ),
                IconButton(
                  icon: const Icon(Icons.close),
                  onPressed: () => Navigator.pop(context),
                )
              ],
            ),
            const SizedBox(height: 10),
            
            // --- NUEVO PANEL CON LOS DATOS CORRECTOS ---
            Container(
              width: double.infinity,
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: Colors.blueGrey[50],
                borderRadius: BorderRadius.circular(8),
                border: Border.all(color: Colors.blueGrey[200]!),
              ),
              child: Wrap(
                spacing: 20,
                runSpacing: 10,
                children: [
                  Text('Afectado: $nombreAfectado', style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 14)),
                  Text('Barrio: ${widget.reporte.barrio}', style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 14)),
                  Text('Direccion: ${widget.reporte.direccion}', style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 14)),
                  Text('Estado Actual: ${widget.reporte.estado}', style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 14, color: Colors.blue)),
                ],
              ),
            ),
            const SizedBox(height: 10),
            const Divider(thickness: 2),
            const SizedBox(height: 10),

            Expanded(
              child: Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Expanded(
                    flex: 5,
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const Text('Historial del Evento', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18)),
                        const SizedBox(height: 15),
                        Expanded(
                          child: Container(
                            decoration: BoxDecoration(
                              color: Colors.grey[100],
                              borderRadius: BorderRadius.circular(8),
                              border: Border.all(color: Colors.grey[300]!),
                            ),
                            child: FutureBuilder<List<TrazabilidadItem>>(
                              future: futureHistorial,
                              builder: (context, snapshot) {
                                if (snapshot.connectionState == ConnectionState.waiting) {
                                  return const Center(child: CircularProgressIndicator());
                                }
                                if (snapshot.hasError) return Center(child: Text('${snapshot.error}', textAlign: TextAlign.center));
                                
                                final historial = snapshot.data ?? [];
                                if (historial.isEmpty) {
                                  return const Center(child: Text('No hay registros previos.', style: TextStyle(color: Colors.grey)));
                                }

                                return ListView.builder(
                                  padding: const EdgeInsets.all(12),
                                  itemCount: historial.length,
                                  itemBuilder: (context, index) {
                                    final h = historial[index];
                                    return Card(
                                      elevation: 2,
                                      margin: const EdgeInsets.only(bottom: 12),
                                      child: Padding(
                                        padding: const EdgeInsets.all(12),
                                        child: Column(
                                          crossAxisAlignment: CrossAxisAlignment.start,
                                          children: [
                                            Row(
                                              mainAxisAlignment: MainAxisAlignment.spaceBetween,
                                              children: [
                                                Container(
                                                  padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                                                  decoration: BoxDecoration(
                                                    color: Colors.red[50],
                                                    borderRadius: BorderRadius.circular(4),
                                                    border: Border.all(color: Colors.red[200]!),
                                                  ),
                                                  child: Text(
                                                    '${h.estadoAnterior} -> ${h.estadoNuevo}',
                                                    style: TextStyle(fontWeight: FontWeight.bold, color: Colors.red[800], fontSize: 12),
                                                  ),
                                                ),
                                                Text(h.fechaCambio.length > 16 ? h.fechaCambio.substring(0, 16) : h.fechaCambio, style: const TextStyle(fontSize: 12, color: Colors.grey)),
                                              ],
                                            ),
                                            const SizedBox(height: 8),
                                            Text(h.observacion, style: const TextStyle(fontSize: 14)),
                                            const SizedBox(height: 8),
                                            Text('Operador: ${h.usuario}', style: const TextStyle(fontSize: 12, fontStyle: FontStyle.italic, color: Colors.blueGrey)),
                                          ],
                                        ),
                                      ),
                                    );
                                  },
                                );
                              },
                            ),
                          ),
                        ),
                      ],
                    ),
                  ),
                  
                  const VerticalDivider(width: 40, thickness: 1),

                  Expanded(
                    flex: 4,
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const Text('Registrar Nueva Accion', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18)),
                        const SizedBox(height: 15),
                        DropdownButtonFormField<String>(
                          value: estadoSeleccionado,
                          items: ['Pendiente', 'En Proceso', 'Inspeccionado', 'Cerrado']
                              .map((e) => DropdownMenuItem(value: e, child: Text(e)))
                              .toList(),
                          onChanged: (val) => setState(() => estadoSeleccionado = val!),
                          decoration: const InputDecoration(
                            labelText: 'Actualizar Estado a...',
                            border: OutlineInputBorder(),
                            filled: true,
                            fillColor: Colors.white,
                          ),
                        ),
                        const SizedBox(height: 20),
                        TextField(
                          controller: observacionController,
                          maxLines: 10,
                          decoration: const InputDecoration(
                            labelText: 'Detalle de la accion realizada o visita',
                            alignLabelWithHint: true,
                            border: OutlineInputBorder(),
                            filled: true,
                            fillColor: Colors.white,
                          ),
                        ),
                        const Spacer(),
                        SizedBox(
                          width: double.infinity,
                          height: 50,
                          child: ElevatedButton.icon(
                            style: ElevatedButton.styleFrom(
                              backgroundColor: Colors.red[800],
                              foregroundColor: Colors.white,
                              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
                            ),
                            icon: guardando 
                              ? const SizedBox(width: 20, height: 20, child: CircularProgressIndicator(color: Colors.white, strokeWidth: 2)) 
                              : const Icon(Icons.add_task),
                            label: Text(guardando ? 'Guardando Registro...' : 'Guardar y Actualizar Trazabilidad', style: const TextStyle(fontSize: 16)),
                            onPressed: guardando ? null : _guardarTrazabilidad,
                          ),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
