import 'package:flutter/material.dart';
import 'package:emergency_col/services/api_service.dart';
import 'package:emergency_col/services/barrio_service.dart';
import 'package:emergency_col/models/barrio.dart';

class NuevoEventoDialog extends StatefulWidget {
  const NuevoEventoDialog({super.key});

  @override
  State<NuevoEventoDialog> createState() => _NuevoEventoDialogState();
}

class _NuevoEventoDialogState extends State<NuevoEventoDialog> {
  final _formKey = GlobalKey<FormState>();
  final _tituloController = TextEditingController();
  final _direccionController = TextEditingController();
  final _ciudadanoController = TextEditingController();
  final _cedulaController = TextEditingController();
  final _telefonoController = TextEditingController();
  final _descripcionController = TextEditingController();
  
  List<Barrio> _barrios = [];
  String? _barrioSeleccionado;
  String _prioridadSeleccionada = 'PRIORIDAD MEDIA';
  bool _cargandoBarrios = true;
  bool _cargando = false;

  @override
  void initState() {
    super.initState();
    _cargarBarrios();
  }

  Future<void> _cargarBarrios() async {
    try {
      final barrios = await BarrioService.getBarrios();
      setState(() {
        _barrios = barrios;
        _cargandoBarrios = false;
        if (_barrios.isNotEmpty) {
          _barrioSeleccionado = _barrios.first.nombre;
        }
      });
      print('✅ Barrios cargados: ${barrios.length}');
    } catch (e) {
      print('❌ Error cargando barrios: $e');
      setState(() {
        _cargandoBarrios = false;
      });
    }
  }

  @override
  void dispose() {
    _tituloController.dispose();
    _direccionController.dispose();
    _ciudadanoController.dispose();
    _cedulaController.dispose();
    _telefonoController.dispose();
    _descripcionController.dispose();
    super.dispose();
  }

  Future<void> _crearReporte() async {
    if (!_formKey.currentState!.validate()) return;

    setState(() => _cargando = true);

    try {
      final data = {
        'titulo': _tituloController.text.trim(),
        'descripcion_detallada': _descripcionController.text.trim(),
        'sector_barrio': _barrioSeleccionado ?? '',
        'direccion_referencia': _direccionController.text.trim(),
        'estado': 'PENDIENTE',
        'datos_extra': {
          'ciudadano': _ciudadanoController.text.trim(),
          'cedula': _cedulaController.text.trim(),
          'telefono': _telefonoController.text.trim(),
          'prioridad': _prioridadSeleccionada,
          'fuente_origen': 'Nuevo Evento SGRD',
        },
      };

      print('📤 Creando reporte: $data');
      final exito = await ApiService.crearReporte(data);

      setState(() => _cargando = false);

      if (exito) {
        if (mounted) {
          Navigator.pop(context, true);
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(content: Text('✅ Reporte creado exitosamente'), backgroundColor: Colors.green),
          );
        }
      } else {
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(content: Text('❌ Error al crear el reporte'), backgroundColor: Colors.red),
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
      title: const Text('Nuevo Evento', style: TextStyle(fontWeight: FontWeight.bold)),
      content: SizedBox(
        width: 400,
        child: Form(
          key: _formKey,
          child: SingleChildScrollView(
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                TextFormField(
                  controller: _tituloController,
                  decoration: const InputDecoration(
                    labelText: 'Título *',
                    border: OutlineInputBorder(),
                  ),
                  validator: (value) => value?.isEmpty ?? true ? 'Campo requerido' : null,
                ),
                const SizedBox(height: 12),
                TextFormField(
                  controller: _direccionController,
                  decoration: const InputDecoration(
                    labelText: 'Dirección *',
                    border: OutlineInputBorder(),
                  ),
                  validator: (value) => value?.isEmpty ?? true ? 'Campo requerido' : null,
                ),
                const SizedBox(height: 12),
                if (_cargandoBarrios)
                  const Padding(
                    padding: EdgeInsets.symmetric(vertical: 16),
                    child: CircularProgressIndicator(),
                  )
                else
                  DropdownButtonFormField<String>(
                    decoration: const InputDecoration(
                      labelText: 'Barrio',
                      border: OutlineInputBorder(),
                    ),
                    value: _barrioSeleccionado,
                    items: _barrios.map((barrio) {
                      return DropdownMenuItem(
                        value: barrio.nombre,
                        child: Text(barrio.nombre),
                      );
                    }).toList(),
                    onChanged: (value) {
                      setState(() => _barrioSeleccionado = value);
                    },
                  ),
                const SizedBox(height: 12),
                TextFormField(
                  controller: _ciudadanoController,
                  decoration: const InputDecoration(
                    labelText: 'Ciudadano Afectado',
                    border: OutlineInputBorder(),
                  ),
                ),
                const SizedBox(height: 12),
                TextFormField(
                  controller: _cedulaController,
                  decoration: const InputDecoration(
                    labelText: 'Cédula',
                    border: OutlineInputBorder(),
                  ),
                  keyboardType: TextInputType.number,
                ),
                const SizedBox(height: 12),
                TextFormField(
                  controller: _telefonoController,
                  decoration: const InputDecoration(
                    labelText: 'Teléfono',
                    border: OutlineInputBorder(),
                  ),
                  keyboardType: TextInputType.phone,
                ),
                const SizedBox(height: 12),
                TextFormField(
                  controller: _descripcionController,
                  decoration: const InputDecoration(
                    labelText: 'Descripción',
                    border: OutlineInputBorder(),
                  ),
                  maxLines: 3,
                ),
                const SizedBox(height: 12),
                DropdownButtonFormField<String>(
                  decoration: const InputDecoration(
                    labelText: 'Prioridad',
                    border: OutlineInputBorder(),
                  ),
                  value: _prioridadSeleccionada,
                  items: const [
                    DropdownMenuItem(value: 'PRIORIDAD ALTA', child: Text('🔴 Alta')),
                    DropdownMenuItem(value: 'PRIORIDAD MEDIA', child: Text('🟡 Media')),
                    DropdownMenuItem(value: 'PRIORIDAD BAJA', child: Text('🟢 Baja')),
                  ],
                  onChanged: (value) {
                    if (value != null) {
                      setState(() => _prioridadSeleccionada = value);
                    }
                  },
                ),
              ],
            ),
          ),
        ),
      ),
      actions: [
        TextButton(
          onPressed: _cargando ? null : () => Navigator.pop(context),
          child: const Text('Cancelar'),
        ),
        ElevatedButton(
          onPressed: _cargando ? null : _crearReporte,
          style: ElevatedButton.styleFrom(
            backgroundColor: Colors.red[700],
            foregroundColor: Colors.white,
          ),
          child: _cargando
              ? const SizedBox(
                  width: 20,
                  height: 20,
                  child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white),
                )
              : const Text('Crear Evento'),
        ),
      ],
    );
  }
}
