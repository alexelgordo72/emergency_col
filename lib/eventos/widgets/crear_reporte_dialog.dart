import 'package:flutter/material.dart';
import 'package:sgrd_final/services/api_service.dart';

class CrearReporteDialog extends StatefulWidget {
  final VoidCallback onCreado;

  const CrearReporteDialog({
    Key? key,
    required this.onCreado,
  }) : super(key: key);

  @override
  State<CrearReporteDialog> createState() => _CrearReporteDialogState();
}

class _CrearReporteDialogState extends State<CrearReporteDialog> {
  final _formKey = GlobalKey<FormState>();
  final _tituloCtrl = TextEditingController();
  final _ciudadanoCtrl = TextEditingController();
  final _cedulaCtrl = TextEditingController();
  final _telefonoCtrl = TextEditingController();
  final _direccionCtrl = TextEditingController();
  final _descripcionCtrl = TextEditingController();

  String _estadoSeleccionado = 'PENDIENTE';
  String _prioridadSeleccionada = 'MEDIA';
  String _tipoRegistro = 'RUFE';
  String? _barrioSeleccionado;
  bool _guardando = false;
  bool _cargandoBarrios = true;
  List<String> _barrios = [];

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
  ];

  final List<String> _prioridades = ['ALTA', 'MEDIA', 'BAJA'];
  final List<String> _tipos = ['RUFE', 'SOLICITUD', 'AHE'];

  @override
  void initState() {
    super.initState();
    _cargarBarrios();
  }

  Future<void> _cargarBarrios() async {
    final barrios = await ApiService.obtenerBarrios();
    if (mounted) {
      setState(() {
        _barrios = barrios;
        _cargandoBarrios = false;
      });
    }
  }

  @override
  void dispose() {
    _tituloCtrl.dispose();
    _ciudadanoCtrl.dispose();
    _cedulaCtrl.dispose();
    _telefonoCtrl.dispose();
    _direccionCtrl.dispose();
    _descripcionCtrl.dispose();
    super.dispose();
  }

  Future<void> _guardar() async {
    if (!_formKey.currentState!.validate()) return;

    if (_barrioSeleccionado == null || _barrioSeleccionado!.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Debes seleccionar un barrio'),
          backgroundColor: Colors.orange,
        ),
      );
      return;
    }

    setState(() => _guardando = true);

    try {
      int tipoRegistroId = 2;
      if (_tipoRegistro == 'SOLICITUD') tipoRegistroId = 1;
      if (_tipoRegistro == 'AHE') tipoRegistroId = 3;

      final datosNuevos = {
        'titulo': _tituloCtrl.text.trim(),
        'descripcion_detallada': _descripcionCtrl.text.trim(),
        'sector_barrio': _barrioSeleccionado,
        'direccion_referencia': _direccionCtrl.text.trim(),
        'estado_actual': _estadoSeleccionado,
        'tipo_registro_id': tipoRegistroId,
        'datos_extra': {
          'ciudadano': _ciudadanoCtrl.text.trim(),
          'telefono': _telefonoCtrl.text.trim(),
          'cedula': _cedulaCtrl.text.trim(),
          'prioridad': _prioridadSeleccionada,
          'fuente_origen': 'CREACION MANUAL',
        },
      };

      await ApiService.crearReporte(datosNuevos);

      if (mounted) {
        Navigator.pop(context);
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('Reporte creado correctamente'),
            backgroundColor: Colors.green,
          ),
        );
        widget.onCreado();
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Error al crear: $e'),
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
      title: const Text('Crear Nuevo Reporte'),
      content: SizedBox(
        width: 500,
        child: SingleChildScrollView(
          child: Form(
            key: _formKey,
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                // Tipo de Registro
                DropdownButtonFormField<String>(
                  value: _tipoRegistro,
                  isExpanded: true,
                  decoration: const InputDecoration(
                    labelText: 'Tipo de Registro',
                    border: OutlineInputBorder(),
                  ),
                  items: _tipos.map((t) {
                    return DropdownMenuItem(value: t, child: Text(t));
                  }).toList(),
                  onChanged: (v) => setState(() => _tipoRegistro = v!),
                ),
                const SizedBox(height: 12),
                // Titulo
                TextFormField(
                  controller: _tituloCtrl,
                  decoration: const InputDecoration(
                    labelText: 'Titulo',
                    border: OutlineInputBorder(),
                  ),
                  validator: (v) => v == null || v.isEmpty ? 'Requerido' : null,
                ),
                const SizedBox(height: 12),
                // Ciudadano
                TextFormField(
                  controller: _ciudadanoCtrl,
                  decoration: const InputDecoration(
                    labelText: 'Ciudadano (Jefe de Hogar)',
                    border: OutlineInputBorder(),
                  ),
                ),
                const SizedBox(height: 12),
                // Cedula
                TextFormField(
                  controller: _cedulaCtrl,
                  decoration: const InputDecoration(
                    labelText: 'Cedula',
                    border: OutlineInputBorder(),
                  ),
                ),
                const SizedBox(height: 12),
                // Telefono
                TextFormField(
                  controller: _telefonoCtrl,
                  decoration: const InputDecoration(
                    labelText: 'Telefono',
                    border: OutlineInputBorder(),
                  ),
                ),
                const SizedBox(height: 12),
                // ==========================================
                // DROPDOWN DE BARRIO (carga desde la BD)
                // ==========================================
                _cargandoBarrios
                    ? const Padding(
                        padding: EdgeInsets.all(16.0),
                        child: Center(
                          child: Column(
                            children: [
                              SizedBox(
                                width: 24,
                                height: 24,
                                child: CircularProgressIndicator(strokeWidth: 2),
                              ),
                              SizedBox(height: 8),
                              Text('Cargando barrios...', style: TextStyle(fontSize: 12)),
                            ],
                          ),
                        ),
                      )
                    : DropdownButtonFormField<String>(
                        value: _barrioSeleccionado,
                        isExpanded: true,
                        decoration: const InputDecoration(
                          labelText: 'Barrio / Sector',
                          border: OutlineInputBorder(),
                          prefixIcon: Icon(Icons.location_on),
                        ),
                        items: _barrios.map((b) {
                          return DropdownMenuItem(
                            value: b,
                            child: Text(
                              b,
                              overflow: TextOverflow.ellipsis,
                            ),
                          );
                        }).toList(),
                        onChanged: (v) =>
                            setState(() => _barrioSeleccionado = v),
                        validator: (v) =>
                            v == null || v.isEmpty ? 'Selecciona un barrio' : null,
                      ),
                const SizedBox(height: 12),
                // Direccion
                TextFormField(
                  controller: _direccionCtrl,
                  decoration: const InputDecoration(
                    labelText: 'Direccion',
                    border: OutlineInputBorder(),
                  ),
                ),
                const SizedBox(height: 12),
                // Estado
                DropdownButtonFormField<String>(
                  value: _estadoSeleccionado,
                  isExpanded: true,
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
                // Prioridad
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
                // Descripcion
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
