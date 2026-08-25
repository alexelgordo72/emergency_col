import 'package:flutter/material.dart';
import '../models/reporte_comunitario.dart';
import '../models/trazabilidad_model.dart';
import '../services/api_service.dart';

class TrazabilidadDialog extends StatefulWidget {
  final ReporteComunitario reporte;

  const TrazabilidadDialog({super.key, required this.reporte});

  @override
  State<TrazabilidadDialog> createState() => _TrazabilidadDialogState();
}

class _TrazabilidadDialogState extends State<TrazabilidadDialog> {
  late Future<List<TrazabilidadItem>> futureHistorial;
  final _observacionController = TextEditingController();
  String _nuevoEstado = 'PENDIENTE';
  bool _cargando = false;

  @override
  void initState() {
    super.initState();
    _cargarHistorial();
  }

  void _cargarHistorial() {
    futureHistorial = ApiService.obtenerHistorial(widget.reporte.id!)
        .then((data) => data.map((e) => TrazabilidadItem.fromJson(e)).toList());
  }

  @override
  void dispose() {
    _observacionController.dispose();
    super.dispose();
  }

  Future<void> _actualizarEstado() async {
    if (_observacionController.text.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('⚠️ Ingresa una observación'), backgroundColor: Colors.orange),
      );
      return;
    }

    setState(() => _cargando = true);

    try {
      final exito = await ApiService.actualizarEstadoTrazabilidad(
        reporteId: widget.reporte.id!,
        estadoAnterior: widget.reporte.estado ?? 'PENDIENTE',
        estadoNuevo: _nuevoEstado,
        observacion: _observacionController.text.trim(),
      );

      setState(() => _cargando = false);

      if (exito) {
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(content: Text('✅ Estado actualizado correctamente'), backgroundColor: Colors.green),
          );
          Navigator.pop(context, true);
        }
      } else {
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(content: Text('❌ Error al actualizar el estado'), backgroundColor: Colors.red),
          );
        }
      }
    } catch (e) {
      setState(() => _cargando = false);
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('❌ Error: $e'), backgroundColor: Colors.red),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return AlertDialog(
      title: const Text('Historial de Trazabilidad'),
      content: SizedBox(
        width: 400,
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            // Estado actual
            Container(
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: Colors.blue[50],
                borderRadius: BorderRadius.circular(8),
              ),
              child: Row(
                children: [
                  const Icon(Icons.info, color: Colors.blue),
                  const SizedBox(width: 8),
                  Expanded(
                    child: Text(
                      'Estado actual: ${widget.reporte.estado ?? "PENDIENTE"}',
                      style: const TextStyle(fontWeight: FontWeight.bold),
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 16),
            // Nuevo estado
            DropdownButtonFormField<String>(
              decoration: const InputDecoration(
                labelText: 'Nuevo estado *',
                border: OutlineInputBorder(),
              ),
              value: _nuevoEstado,
              items: const [
                DropdownMenuItem(value: 'PENDIENTE', child: Text('PENDIENTE')),
                DropdownMenuItem(value: 'EN PROCESO', child: Text('EN PROCESO')),
                DropdownMenuItem(value: 'VISITADO', child: Text('VISITADO')),
                DropdownMenuItem(value: 'VERIFICADO', child: Text('VERIFICADO')),
                DropdownMenuItem(value: 'CERRADO', child: Text('CERRADO')),
              ],
              onChanged: (value) {
                if (value != null) setState(() => _nuevoEstado = value);
              },
            ),
            const SizedBox(height: 12),
            // Observación
            TextFormField(
              controller: _observacionController,
              decoration: const InputDecoration(
                labelText: 'Observación *',
                border: OutlineInputBorder(),
              ),
              maxLines: 3,
            ),
            const SizedBox(height: 16),
            // Historial
            const Divider(),
            const Text(
              'Historial',
              style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16),
            ),
            const SizedBox(height: 8),
            Expanded(
              child: FutureBuilder<List<TrazabilidadItem>>(
                future: futureHistorial,
                builder: (context, snapshot) {
                  if (snapshot.connectionState == ConnectionState.waiting) {
                    return const Center(child: CircularProgressIndicator());
                  }
                  if (snapshot.hasError) {
                    return Center(child: Text('Error: ${snapshot.error}'));
                  }
                  if (!snapshot.hasData || snapshot.data!.isEmpty) {
                    return const Center(child: Text('No hay historial'));
                  }
                  return ListView.builder(
                    shrinkWrap: true,
                    itemCount: snapshot.data!.length,
                    itemBuilder: (context, index) {
                      final item = snapshot.data![index];
                      return ListTile(
                        dense: true,
                        leading: const Icon(Icons.history, size: 16),
                        title: Text('${item.estadoAnterior} → ${item.estadoNuevo}'),
                        subtitle: Text(item.observacion),
                        trailing: Text(
                          item.fechaCambio,
                          style: const TextStyle(fontSize: 10, color: Colors.grey),
                        ),
                      );
                    },
                  );
                },
              ),
            ),
          ],
        ),
      ),
      actions: [
        TextButton(
          onPressed: _cargando ? null : () => Navigator.pop(context),
          child: const Text('Cerrar'),
        ),
        ElevatedButton(
          onPressed: _cargando ? null : _actualizarEstado,
          style: ElevatedButton.styleFrom(
            backgroundColor: Colors.blue[700],
            foregroundColor: Colors.white,
          ),
          child: _cargando
              ? const SizedBox(
                  width: 20,
                  height: 20,
                  child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white),
                )
              : const Text('Actualizar Estado'),
        ),
      ],
    );
  }
}
