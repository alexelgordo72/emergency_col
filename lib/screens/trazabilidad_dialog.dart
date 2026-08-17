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

  // ✅ ESTADOS EXACTOS DE LA BASE DE DATOS
  final List<String> estadosPosibles = [
    'Pendiente',
    'En Proceso',
    'Visitado sin prioridad',
    'Visitado-DE-Prioridad Baja',
    'Visitado-DE-Prioridad Media',
    'Visitado-DE-Prioridad Alta',
  ];

  @override
  void initState() {
    super.initState();
    String estadoActual = widget.reporte.estado.trim();
    estadoSeleccionado = estadosPosibles.contains(estadoActual) 
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
        setState(() {
          widget.reporte.estado = estadoSeleccionado;
        });
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('✅ Registro guardado exitosamente'), backgroundColor: Colors.green),
        );
        Navigator.pop(context, true);
      } else {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('❌ Error al guardar el registro'), backgroundColor: Colors.red),
        );
      }
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('❌ Error: $e'), backgroundColor: Colors.red),
      );
    } finally {
      setState(() => guardando = false);
    }
  }

  Color _getEstadoColor(String estado) {
    switch (estado.toLowerCase().trim()) {
      case 'pendiente': return Colors.orange;
      case 'en proceso': return Colors.cyan;
      case 'visitado sin prioridad': return Colors.grey;
      case 'visitado-de-prioridad baja': return Colors.green;
      case 'visitado-de-prioridad media': return Colors.orange;
      case 'visitado-de-prioridad alta': return Colors.red;
      default: return Colors.grey;
    }
  }

  @override
  Widget build(BuildContext context) {
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
                  Row(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      const Text('Estado Actual: ', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 14)),
                      Container(
                        padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                        decoration: BoxDecoration(
                          color: _getEstadoColor(widget.reporte.estado),
                          borderRadius: BorderRadius.circular(8),
                        ),
                        child: Text(
                          widget.reporte.estado,
                          style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 14),
                        ),
                      ),
                    ],
                  ),
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
                                                    color: _getEstadoColor(h.estadoNuevo).withOpacity(0.2),
                                                    borderRadius: BorderRadius.circular(4),
                                                    border: Border.all(color: _getEstadoColor(h.estadoNuevo)),
                                                  ),
                                                  child: Text(
                                                    '${h.estadoAnterior} → ${h.estadoNuevo}',
                                                    style: TextStyle(fontWeight: FontWeight.bold, color: _getEstadoColor(h.estadoNuevo), fontSize: 12),
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
                          items: estadosPosibles
                              .where((e) => e != widget.reporte.estado.trim())
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
                              backgroundColor: Colors.green[700],
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
