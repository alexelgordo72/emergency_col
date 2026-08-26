import 'package:flutter/material.dart';
import 'package:emergency_col/services/evento_service.dart';
import 'package:emergency_col/services/barrio_service.dart';
import 'package:emergency_col/models/barrio.dart';

class CrearEventoScreen extends StatefulWidget {
  const CrearEventoScreen({Key? key}) : super(key: key);

  @override
  _CrearEventoScreenState createState() => _CrearEventoScreenState();
}

class _CrearEventoScreenState extends State<CrearEventoScreen> {
  final _formKey = GlobalKey<FormState>();
  final _tituloController = TextEditingController();
  final _direccionController = TextEditingController();
  final _ciudadanoController = TextEditingController();
  final _cedulaController = TextEditingController();
  final _telefonoController = TextEditingController();
  final _descripcionController = TextEditingController();
  
  List<Barrio> _barrios = [];
  String? _barrioSeleccionado;
  String _prioridadSeleccionada = 'BAJA';
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

  Future<void> _crearEvento() async {
    if (!_formKey.currentState!.validate()) return;

    setState(() => _cargando = true);

    try {
      // Construir el payload EXACTAMENTE como lo acepta el backend
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

      print('📤 Creando evento: $data');
      final exito = await EventoService.crearEvento(data);

      setState(() => _cargando = false);

      if (exito) {
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(content: Text('✅ Evento creado exitosamente'), backgroundColor: Colors.green),
          );
          Navigator.pop(context, true);
        }
      } else {
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(content: Text('❌ Error al crear el evento'), backgroundColor: Colors.red),
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
    return Scaffold(
      appBar: AppBar(
        title: const Text('Nuevo Evento de Emergencia'),
        backgroundColor: Colors.red[700],
        foregroundColor: Colors.white,
        leading: IconButton(
          icon: const Icon(Icons.arrow_back),
          onPressed: () => Navigator.pop(context),
        ),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Form(
          key: _formKey,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              TextFormField(
                controller: _tituloController,
                decoration: const InputDecoration(
                  labelText: 'Título / Asunto *',
                  border: OutlineInputBorder(),
                  prefixIcon: Icon(Icons.title),
                ),
                validator: (value) => value?.isEmpty ?? true ? 'Campo requerido' : null,
              ),
              const SizedBox(height: 16),
              if (_cargandoBarrios)
                const Center(child: CircularProgressIndicator())
              else
                DropdownButtonFormField<String>(
                  decoration: const InputDecoration(
                    labelText: 'Barrio *',
                    border: OutlineInputBorder(),
                    prefixIcon: Icon(Icons.location_city),
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
                  validator: (value) => value == null ? 'Seleccione un barrio' : null,
                ),
              const SizedBox(height: 16),
              TextFormField(
                controller: _direccionController,
                decoration: const InputDecoration(
                  labelText: 'Dirección / Referencia *',
                  border: OutlineInputBorder(),
                  prefixIcon: Icon(Icons.location_on),
                ),
                validator: (value) => value?.isEmpty ?? true ? 'Campo requerido' : null,
              ),
              const SizedBox(height: 16),
              TextFormField(
                controller: _ciudadanoController,
                decoration: const InputDecoration(
                  labelText: 'Ciudadano Afectado',
                  border: OutlineInputBorder(),
                  prefixIcon: Icon(Icons.person),
                ),
              ),
              const SizedBox(height: 16),
              TextFormField(
                controller: _cedulaController,
                decoration: const InputDecoration(
                  labelText: 'Cédula',
                  border: OutlineInputBorder(),
                  prefixIcon: Icon(Icons.badge),
                ),
                keyboardType: TextInputType.number,
              ),
              const SizedBox(height: 16),
              TextFormField(
                controller: _telefonoController,
                decoration: const InputDecoration(
                  labelText: 'Teléfono de Contacto',
                  border: OutlineInputBorder(),
                  prefixIcon: Icon(Icons.phone),
                ),
                keyboardType: TextInputType.phone,
              ),
              const SizedBox(height: 16),
              TextFormField(
                controller: _descripcionController,
                decoration: const InputDecoration(
                  labelText: 'Descripción *',
                  border: OutlineInputBorder(),
                  prefixIcon: Icon(Icons.description),
                ),
                maxLines: 3,
                validator: (value) => value?.isEmpty ?? true ? 'Campo requerido' : null,
              ),
              const SizedBox(height: 16),
              DropdownButtonFormField<String>(
                decoration: const InputDecoration(
                  labelText: 'Prioridad',
                  border: OutlineInputBorder(),
                  prefixIcon: Icon(Icons.priority_high),
                ),
                value: _prioridadSeleccionada,
                items: const [
                  DropdownMenuItem(value: 'ALTA', child: Text('🔴 Alta')),
                  DropdownMenuItem(value: 'MEDIA', child: Text('🟡 Media')),
                  DropdownMenuItem(value: 'BAJA', child: Text('🟢 Baja')),
                ],
                onChanged: (value) {
                  if (value != null) {
                    setState(() => _prioridadSeleccionada = value);
                  }
                },
              ),
              const SizedBox(height: 24),
              Row(
                children: [
                  Expanded(
                    child: OutlinedButton(
                      onPressed: _cargando ? null : () => Navigator.pop(context),
                      style: OutlinedButton.styleFrom(
                        padding: const EdgeInsets.symmetric(vertical: 16),
                      ),
                      child: const Text('Cancelar'),
                    ),
                  ),
                  const SizedBox(width: 16),
                  Expanded(
                    flex: 2,
                    child: ElevatedButton(
                      onPressed: _cargando ? null : _crearEvento,
                      style: ElevatedButton.styleFrom(
                        backgroundColor: Colors.red[700],
                        foregroundColor: Colors.white,
                        padding: const EdgeInsets.symmetric(vertical: 16),
                      ),
                      child: _cargando
                          ? const Row(
                              mainAxisAlignment: MainAxisAlignment.center,
                              children: [
                                SizedBox(
                                  width: 20,
                                  height: 20,
                                  child: CircularProgressIndicator(
                                    strokeWidth: 2,
                                    color: Colors.white,
                                  ),
                                ),
                                SizedBox(width: 8),
                                Text('Guardando...'),
                              ],
                            )
                          : const Text('Registrar Evento'),
                    ),
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }
}
