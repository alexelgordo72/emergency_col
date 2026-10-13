import 'package:flutter/material.dart';
import 'package:sgrd_final/services/api_service.dart';

class EditarReporteDialog extends StatefulWidget {
  final Map<String, dynamic> reporte;
  final VoidCallback onActualizado;

  const EditarReporteDialog({
    Key? key,
    required this.reporte,
    required this.onActualizado,
  }) : super(key: key);

  @override
  State<EditarReporteDialog> createState() => _EditarReporteDialogState();
}

class _EditarReporteDialogState extends State<EditarReporteDialog> {
  final _formKey = GlobalKey<FormState>();
  late TextEditingController _tituloCtrl;
  late TextEditingController _ciudadanoCtrl;
  late TextEditingController _telefonoCtrl;
  late TextEditingController _barrioCtrl;
  late TextEditingController _direccionCtrl;
  late TextEditingController _descripcionCtrl;
  late TextEditingController _cedulaCtrl;

  String _estadoSeleccionado = 'PENDIENTE';
  String _prioridadSeleccionada = 'MEDIA';
  bool _guardando = false;

  final List<String> _estados = [
    'PENDIENTE',
    'PENDIENTE con FORMATO',
    'RECIBIDO',
    'Visitado-DE-Prioridad Alta',
    'Visitado-DE-Prioridad Media',
    'Visitado-DE-Prioridad Baja',
    'Visitado Sin RUFE',
    'Verificado-EDHAS',
    'Verificado-AHE',
    'CERRADO',
    'Visita Fallida - No Estaban',
    'Visita Fallida - Direccion Mala',
    'Visita Fallida - No Contestan',
  ];

  final List<String> _prioridades = ['ALTA', 'MEDIA', 'BAJA'];

  @override
  void initState() {
    super.initState();
    final r = widget.reporte;
    _tituloCtrl = TextEditingController(text: r['titulo'] ?? '');
    _ciudadanoCtrl = TextEditingController(text: r['ciudadano'] ?? '');
    _telefonoCtrl = TextEditingController(text: r['telefono'] ?? '');
    _barrioCtrl = TextEditingController(text: r['sector_barrio'] ?? r['barrio'] ?? '');
    _direccionCtrl = TextEditingController(text: r['direccion_referencia'] ?? r['direccion'] ?? '');
    _descripcionCtrl = TextEditingController(text: r['descripcion'] ?? r['descripcion_detallada'] ?? '');
    _cedulaCtrl = TextEditingController(text: r['cedula'] ?? '');

    final estadoActual = r['estado'] ?? r['estado_actual'] ?? 'PENDIENTE';
    if (_estados.contains(estadoActual)) {
      _estadoSeleccionado = estadoActual;
    } else {
      _estados.add(estadoActual);
      _estadoSeleccionado = estadoActual;
    }

    final prioridadActual = r['prioridad'] ?? 'MEDIA';
    if (_prioridades.contains(prioridadActual)) {
      _prioridadSeleccionada = prioridadActual;
    }
  }

  @override
  void dispose() {
    _tituloCtrl.dispose();
    _ciudadanoCtrl.dispose();
    _telefonoCtrl.dispose();
    _barrioCtrl.dispose();
    _direccionCtrl.dispose();
    _descripcionCtrl.dispose();
    _cedulaCtrl.dispose();
    super.dispose();
  }

  Future<void> _guardar() async {
    if (!_formKey.currentState!.validate()) return;

    setState(() => _guardando = true);

    try {
      final id = widget.reporte['id'];
      final datosActualizados = {
        'titulo': _tituloCtrl.text.trim(),
        'descripcion_detallada': _descripcionCtrl.text.trim(),
        'sector_barrio': _barrioCtrl.text.trim(),
        'direccion_referencia': _direccionCtrl.text.trim(),
        'estado_actual': _estadoSeleccionado,
        'datos_extra': {
          'ciudadano': _ciudadanoCtrl.text.trim(),
          'telefono': _telefonoCtrl.text.trim(),
          'cedula': _cedulaCtrl.text.trim(),
          'prioridad': _prioridadSeleccionada,
        },
      };

      await ApiService.actualizarReporte(id, datosActualizados);

      if (mounted) {
        Navigator.pop(context);
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('Reporte actualizado correctamente'),
            backgroundColor: Colors.green,
          ),
        );
        widget.onActualizado();
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Error al guardar: $e'),
            backgroundColor: Colors.red,
          ),
        );
      }
    } finally {
      if (mounted) setState(() => _guardando = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return AlertDialog(
      title: const Text('Editar Reporte'),
      content: SizedBox(
        width: 500,
        child: SingleChildScrollView(
          child: Form(
            key: _formKey,
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                TextFormField(
                  controller: _tituloCtrl,
                  decoration: const InputDecoration(
                    labelText: 'Titulo',
                    border: OutlineInputBorder(),
                  ),
                  validator: (v) => v == null || v.isEmpty ? 'Requerido' : null,
                ),
                const SizedBox(height: 12),
                TextFormField(
                  controller: _ciudadanoCtrl,
                  decoration: const InputDecoration(
                    labelText: 'Ciudadano (Jefe de Hogar)',
                    border: OutlineInputBorder(),
                  ),
                ),
                const SizedBox(height: 12),
                TextFormField(
                  controller: _cedulaCtrl,
                  decoration: const InputDecoration(
                    labelText: 'Cedula',
                    border: OutlineInputBorder(),
                  ),
                ),
                const SizedBox(height: 12),
                TextFormField(
                  controller: _telefonoCtrl,
                  decoration: const InputDecoration(
                    labelText: 'Telefono',
                    border: OutlineInputBorder(),
                  ),
                ),
                const SizedBox(height: 12),
                TextFormField(
                  controller: _barrioCtrl,
                  decoration: const InputDecoration(
                    labelText: 'Barrio / Sector',
                    border: OutlineInputBorder(),
                  ),
                ),
                const SizedBox(height: 12),
                TextFormField(
                  controller: _direccionCtrl,
                  decoration: const InputDecoration(
                    labelText: 'Direccion',
                    border: OutlineInputBorder(),
                  ),
                ),
                const SizedBox(height: 12),
                DropdownButtonFormField<String>(
                  value: _estadoSeleccionado,
                  decoration: const InputDecoration(
                    labelText: 'Estado',
                    border: OutlineInputBorder(),
                  ),
                  items: _estados.map((e) {
                    return DropdownMenuItem(
                      value: e,
                      child: Text(e, style: const TextStyle(fontSize: 12)),
                    );
                  }).toList(),
                  onChanged: (v) => setState(() => _estadoSeleccionado = v!),
                ),
                const SizedBox(height: 12),
                DropdownButtonFormField<String>(
                  value: _prioridadSeleccionada,
                  decoration: const InputDecoration(
                    labelText: 'Prioridad',
                    border: OutlineInputBorder(),
                  ),
                  items: _prioridades.map((p) {
                    return DropdownMenuItem(value: p, child: Text(p));
                  }).toList(),
                  onChanged: (v) => setState(() => _prioridadSeleccionada = v!),
                ),
                const SizedBox(height: 12),
                TextFormField(
                  controller: _descripcionCtrl,
                  decoration: const InputDecoration(
                    labelText: 'Descripcion / Observaciones',
                    border: OutlineInputBorder(),
                  ),
                  maxLines: 4,
                ),
              ],
            ),
          ),
        ),
      ),
      actions: [
        TextButton(
          onPressed: _guardando ? null : () => Navigator.pop(context),
          child: const Text('Cancelar'),
        ),
        ElevatedButton.icon(
          onPressed: _guardando ? null : _guardar,
          icon: _guardando
              ? const SizedBox(
                  width: 16,
                  height: 16,
                  child: CircularProgressIndicator(
                    strokeWidth: 2,
                    color: Colors.white,
                  ),
                )
              : const Icon(Icons.save),
          label: Text(_guardando ? 'Guardando...' : 'Guardar'),
          style: ElevatedButton.styleFrom(
            backgroundColor: Colors.green[700],
            foregroundColor: Colors.white,
          ),
        ),
      ],
    );
  }
}
