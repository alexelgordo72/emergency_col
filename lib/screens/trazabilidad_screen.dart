import 'package:flutter/material.dart';
import '../services/api_service.dart';
import '../models/trazabilidad_model.dart';

class TrazabilidadScreen extends StatefulWidget {
  const TrazabilidadScreen({Key? key}) : super(key: key);

  @override
  _TrazabilidadScreenState createState() => _TrazabilidadScreenState();
}

class _TrazabilidadScreenState extends State<TrazabilidadScreen> {
  late Future<List<ReporteEvento>> futureReportes;

  @override
  void initState() {
    super.initState();
    _cargarDatos();
  }

  void _cargarDatos() {
    setState(() {
      futureReportes = ApiService.obtenerReportes();
    });
  }

  void _mostrarModalActualizacion(ReporteEvento reporte) {
    String estadoSeleccionado = reporte.estadoActual;
    final observacionController = TextEditingController();

    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: Text('Actualizar Evento #${reporte.id.substring(0, 6)}'),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            DropdownButtonFormField<String>(
              value: ['Pendiente', 'En Proceso', 'Inspeccionado', 'Cerrado'].contains(estadoSeleccionado) 
                  ? estadoSeleccionado 
                  : 'Pendiente',
              items: ['Pendiente', 'En Proceso', 'Inspeccionado', 'Cerrado']
                  .map((e) => DropdownMenuItem(value: e, child: Text(e)))
                  .toList(),
              onChanged: (val) => setState(() => estadoSeleccionado = val!),
              decoration: const InputDecoration(labelText: 'Nuevo Estado'),
            ),
            const SizedBox(height: 12),
            TextField(
              controller: observacionController,
              decoration: const InputDecoration(
                labelText: 'Observación / Qué se hizo',
                border: OutlineInputBorder(),
              ),
              maxLines: 3,
            ),
          ],
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('Cancelar'),
          ),
          ElevatedButton(
            style: ElevatedButton.styleFrom(backgroundColor: Colors.red[800]),
            onPressed: () async {
              if (observacionController.text.isEmpty) return;
              bool exito = await ApiService.actualizarEstado(
                reporte.id, 
                estadoSeleccionado, 
                observacionController.text,
              );
              Navigator.pop(context);
              if (exito) {
                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(content: Text('Trazabilidad actualizada con éxito')),
                );
                _cargarDatos();
              }
            },
            child: const Text('Guardar'),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Trazabilidad y Ciclo de Vida'),
        backgroundColor: Colors.red[900],
      ),
      body: FutureBuilder<List<ReporteEvento>>(
        future: futureReportes,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          } else if (snapshot.hasError) {
            return Center(child: Text('Error: ${snapshot.error}'));
          } else if (!snapshot.hasData || snapshot.data!.isEmpty) {
            return const Center(child: Text('No hay eventos registrados.'));
          }

          final reportes = snapshot.data!;
          return ListView.builder(
            itemCount: reportes.length,
            padding: const EdgeInsets.all(12),
            itemBuilder: (context, index) {
              final rep = reportes[index];
              return Card(
                elevation: 3,
                margin: const EdgeInsets.only(bottom: 12),
                child: ExpansionTile(
                  title: Text(
                    '${rep.sectorBarrio.toUpperCase()} - ${rep.titulo}',
                    style: const TextStyle(fontWeight: FontWeight.bold),
                  ),
                  subtitle: Text('Estado: ${rep.estadoActual} | Creado: ${rep.fechaCreacion}'),
                  trailing: IconButton(
                    icon: const Icon(Icons.edit_note, color: Colors.red),
                    onPressed: () => _mostrarModalActualizacion(rep),
                    tooltip: 'Actualizar Estado',
                  ),
                  children: [
                    FutureBuilder<List<TrazabilidadItem>>(
                      future: ApiService.obtenerHistorial(rep.id),
                      builder: (context, histSnapshot) {
                        if (histSnapshot.connectionState == ConnectionState.waiting) {
                          return const Padding(
                            padding: EdgeInsets.all(8.0),
                            child: CircularProgressIndicator(strokeWidth: 2),
                          );
                        }
                        final historial = histSnapshot.data ?? [];
                        if (historial.isEmpty) {
                          return const Padding(
                            padding: EdgeInsets.all(8.0),
                            child: Text('Sin historial de cambios aún.'),
                          );
                        }
                        return ListView.builder(
                          shrinkWrap: true,
                          physics: const NeverScrollableScrollPhysics(),
                          itemCount: historial.length,
                          itemBuilder: (context, hIndex) {
                            final h = historial[hIndex];
                            return ListTile(
                              dense: true,
                              leading: const Icon(Icons.history, size: 20, color: Colors.grey),
                              title: Text('${h.estadoAnterior} ➔ ${h.estadoNuevo}'),
                              subtitle: Text('${h.observacion}\nResponsable: ${h.usuario}'),
                              trailing: Text(h.fechaCambio.substring(0, 10), style: const TextStyle(fontSize: 11)),
                            );
                          },
                        );
                      },
                    ),
                  ],
                ),
              );
            },
          );
        },
      ),
    );
  }
}
