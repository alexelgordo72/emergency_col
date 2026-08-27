import 'package:flutter/material.dart';
import 'package:sgrd_final/eventos/models/evento_model.dart';
import 'package:sgrd_final/eventos/services/evento_service.dart';
import 'package:sgrd_final/services/barrio_service.dart';
import 'package:sgrd_final/models/barrio.dart';

class CrearEventoScreen extends StatefulWidget {
  final EventoModel? eventoEditar;
  const CrearEventoScreen({Key? key, this.eventoEditar}) : super(key: key);

  @override
  _CrearEventoScreenState createState() => _CrearEventoScreenState();
}

class _CrearEventoScreenState extends State<CrearEventoScreen> {
  final _formKey = GlobalKey<FormState>();
  
  final _tituloController = TextEditingController();
  final _descripcionController = TextEditingController();
  final _direccionController = TextEditingController();
  final _ciudadanoController = TextEditingController();
  final _cedulaController = TextEditingController();
  final _telefonoController = TextEditingController();
  
  List<String> _barrios = [];
  String? _barrioSeleccionado;
  String _prioridadSeleccionada = 'BAJA';
  bool _cargandoBarrios = true;
  bool _cargando = false;
  bool _editando = false;
  bool _cargandoDatos = false;
  String? _mensajeDatos;

  @override
  void initState() {
    super.initState();
    _editando = widget.eventoEditar != null;
    if (_editando) {
      _cargarDatosEvento();
      _cargarDatosRufe();
    }
    _cargarBarrios();
  }

  void _cargarDatosEvento() {
    final e = widget.eventoEditar!;
    _tituloController.text = e.titulo;
    _descripcionController.text = e.descripcion;
    _direccionController.text = e.direccion;
    _ciudadanoController.text = e.ciudadano;
    _cedulaController.text = e.cedula;
    _telefonoController.text = e.telefono;
    _prioridadSeleccionada = e.prioridad;
    _barrioSeleccionado = e.barrio;
  }

  Future<void> _cargarDatosRufe() async {
    final titulo = widget.eventoEditar!.titulo;
    print('🔍 Título completo: $titulo');
    
    String? numeroRufe;
    List<RegExp> patrones = [
      RegExp(r'RUFE\s*#?\s*(\d+)', caseSensitive: false),
      RegExp(r'Rufe\s*#?\s*(\d+)', caseSensitive: false),
      RegExp(r'rufe\s*#?\s*(\d+)', caseSensitive: false),
    ];
    
    for (var regex in patrones) {
      final match = regex.firstMatch(titulo);
      if (match != null) {
        numeroRufe = match.group(1);
        if (numeroRufe != null && numeroRufe.isNotEmpty) {
          print('🔍 Número de RUFE encontrado: $numeroRufe');
          break;
        }
      }
    }
    
    if (numeroRufe == null || numeroRufe.isEmpty) {
      print('⚠️ No se pudo extraer el número de RUFE');
      setState(() {
        _mensajeDatos = '⚠️ No se encontró número de RUFE en el título';
      });
      return;
    }
    
    setState(() {
      _cargandoDatos = true;
      _mensajeDatos = '🔄 Cargando datos del RUFE #$numeroRufe...';
    });
    
    try {
      final datos = await EventoService.obtenerDatosRufe(numeroRufe);
      
      if (datos != null) {
        bool datosCargados = false;
        
        if (datos['ciudadano'] != null && datos['ciudadano']!.isNotEmpty) {
          _ciudadanoController.text = datos['ciudadano']!;
          print('✅ Ciudadano cargado: ${datos['ciudadano']}');
          datosCargados = true;
        }
        
        if (datos['cedula'] != null && datos['cedula']!.isNotEmpty) {
          _cedulaController.text = datos['cedula']!;
          print('✅ Cédula cargada: ${datos['cedula']}');
          datosCargados = true;
        }
        
        if (datos['barrio'] != null && datos['barrio']!.isNotEmpty) {
          if (_barrios.contains(datos['barrio'])) {
            _barrioSeleccionado = datos['barrio'];
            print('✅ Barrio cargado: ${datos['barrio']}');
            datosCargados = true;
          } else {
            print('⚠️ Barrio "${datos['barrio']}" no está en la lista disponible');
          }
        }
        
        if (datos['telefono'] != null && datos['telefono']!.isNotEmpty) {
          _telefonoController.text = datos['telefono']!;
          print('✅ Teléfono cargado: ${datos['telefono']}');
          datosCargados = true;
        }
        
        if (_descripcionController.text.isEmpty && 
            datos['descripcion'] != null && datos['descripcion']!.isNotEmpty) {
          _descripcionController.text = datos['descripcion']!;
          print('✅ Descripción cargada');
          datosCargados = true;
        }
        
        if (datosCargados) {
          setState(() {
            _mensajeDatos = '✅ Datos cargados desde RUFE #$numeroRufe';
          });
        } else {
          setState(() {
            _mensajeDatos = '⚠️ No se encontraron datos adicionales en RUFE #$numeroRufe';
          });
        }
      } else {
        setState(() {
          _mensajeDatos = '⚠️ No se encontró información para RUFE #$numeroRufe';
        });
      }
    } catch (e) {
      print('❌ Error cargando datos del RUFE: $e');
      setState(() {
        _mensajeDatos = '❌ Error al cargar datos: $e';
      });
    }
    setState(() => _cargandoDatos = false);
  }

  Future<void> _cargarBarrios() async {
    try {
      final barrios = await BarrioService.getBarrios();
      
      final Set<String> barriosSet = {};
      for (var barrio in barrios) {
        if (barrio.nombre.isNotEmpty) {
          barriosSet.add(barrio.nombre);
        }
      }
      
      final listaUnica = barriosSet.toList()..sort();
      
      setState(() {
        _barrios = listaUnica;
        _cargandoBarrios = false;
        if (_barrioSeleccionado != null && !_barrios.contains(_barrioSeleccionado)) {
          _barrioSeleccionado = _barrios.isNotEmpty ? _barrios.first : null;
        }
        if (_barrioSeleccionado == null && _barrios.isNotEmpty) {
          _barrioSeleccionado = _barrios.first;
        }
      });
    } catch (e) {
      print('❌ Error cargando barrios: $e');
      setState(() => _cargandoBarrios = false);
    }
  }

  Future<void> _guardarEvento() async {
    if (!_formKey.currentState!.validate()) return;
    
    setState(() => _cargando = true);
    try {
      final evento = EventoModel(
        id: _editando ? widget.eventoEditar!.id : null,
        titulo: _tituloController.text.trim(),
        descripcion: _descripcionController.text.trim(),
        barrio: _barrioSeleccionado ?? '',
        direccion: _direccionController.text.trim(),
        ciudadano: _ciudadanoController.text.trim(),
        cedula: _cedulaController.text.trim(),
        telefono: _telefonoController.text.trim(),
        prioridad: _prioridadSeleccionada,
      );
      
      bool exito;
      if (_editando) {
        exito = await EventoService.actualizarEvento(evento.id!, evento);
      } else {
        exito = await EventoService.crearEvento(evento);
      }
      
      setState(() => _cargando = false);
      if (exito) {
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              content: Text(_editando ? '✅ Evento actualizado' : '✅ Evento creado'),
              backgroundColor: Colors.green,
            ),
          );
          Navigator.pop(context, true);
        }
      } else {
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              content: Text(_editando ? '❌ Error al actualizar' : '❌ Error al crear'),
              backgroundColor: Colors.red,
            ),
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
  void dispose() {
    _tituloController.dispose();
    _descripcionController.dispose();
    _direccionController.dispose();
    _ciudadanoController.dispose();
    _cedulaController.dispose();
    _telefonoController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final screenWidth = MediaQuery.of(context).size.width;
    final isSmallScreen = screenWidth < 600;
    
    return Dialog(
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: Container(
        width: isSmallScreen ? screenWidth * 0.9 : 560,
        constraints: BoxConstraints(
          maxHeight: MediaQuery.of(context).size.height * 0.85,
        ),
        padding: const EdgeInsets.all(20),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            // Título del diálogo
            Row(
              children: [
                Icon(
                  _editando ? Icons.edit : Icons.add,
                  color: Colors.red[700],
                  size: 22,
                ),
                const SizedBox(width: 10),
                Expanded(
                  child: Text(
                    _editando ? 'Editar Evento' : 'Nuevo Evento',
                    style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                  ),
                ),
                IconButton(
                  icon: const Icon(Icons.close, size: 22),
                  onPressed: () => Navigator.pop(context),
                  padding: EdgeInsets.zero,
                  constraints: const BoxConstraints(),
                ),
              ],
            ),
            const Divider(height: 12),
            
            // Mensaje de estado
            if (_mensajeDatos != null && _editando)
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                margin: const EdgeInsets.only(bottom: 8),
                decoration: BoxDecoration(
                  color: _mensajeDatos!.contains('✅') ? Colors.green[50] :
                         _mensajeDatos!.contains('⚠️') ? Colors.orange[50] :
                         _mensajeDatos!.contains('❌') ? Colors.red[50] :
                         Colors.blue[50],
                  borderRadius: BorderRadius.circular(6),
                ),
                child: Row(
                  children: [
                    Icon(
                      _mensajeDatos!.contains('✅') ? Icons.check_circle :
                      _mensajeDatos!.contains('⚠️') ? Icons.warning :
                      _mensajeDatos!.contains('❌') ? Icons.error :
                      Icons.info,
                      size: 14,
                      color: _mensajeDatos!.contains('✅') ? Colors.green :
                             _mensajeDatos!.contains('⚠️') ? Colors.orange :
                             _mensajeDatos!.contains('❌') ? Colors.red :
                             Colors.blue,
                    ),
                    const SizedBox(width: 6),
                    Expanded(
                      child: Text(
                        _mensajeDatos!,
                        style: TextStyle(
                          fontSize: 11,
                          color: _mensajeDatos!.contains('✅') ? Colors.green[700] :
                                 _mensajeDatos!.contains('⚠️') ? Colors.orange[700] :
                                 _mensajeDatos!.contains('❌') ? Colors.red[700] :
                                 Colors.blue[700],
                        ),
                        overflow: TextOverflow.ellipsis,
                        maxLines: 1,
                      ),
                    ),
                  ],
                ),
              ),
            
            // Formulario
            Expanded(
              child: SingleChildScrollView(
                child: Form(
                  key: _formKey,
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.stretch,
                    children: [
                      // Título - EN 2 LÍNEAS
                      TextFormField(
                        controller: _tituloController,
                        decoration: const InputDecoration(
                          labelText: 'Título *',
                          border: OutlineInputBorder(),
                          prefixIcon: Icon(Icons.title, size: 18),
                          contentPadding: EdgeInsets.symmetric(horizontal: 12, vertical: 10),
                        ),
                        style: const TextStyle(fontSize: 13, height: 1.3),
                        maxLines: 2,
                        minLines: 1,
                        keyboardType: TextInputType.multiline,
                        textInputAction: TextInputAction.newline,
                        validator: (value) => value?.isEmpty ?? true ? 'Campo requerido' : null,
                      ),
                      const SizedBox(height: 10),
                      
                      // Barrio
                      if (_cargandoBarrios)
                        const Center(child: CircularProgressIndicator())
                      else
                        DropdownButtonFormField<String>(
                          decoration: const InputDecoration(
                            labelText: 'Barrio *',
                            border: OutlineInputBorder(),
                            prefixIcon: Icon(Icons.location_city, size: 18),
                            contentPadding: EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                            isDense: true,
                          ),
                          value: _barrioSeleccionado,
                          items: _barrios.map((barrio) {
                            return DropdownMenuItem<String>(
                              value: barrio,
                              child: Text(
                                barrio,
                                overflow: TextOverflow.ellipsis,
                                style: const TextStyle(fontSize: 13),
                              ),
                            );
                          }).toList(),
                          onChanged: (value) {
                            setState(() => _barrioSeleccionado = value);
                          },
                          validator: (value) => value == null ? 'Seleccione un barrio' : null,
                          style: const TextStyle(fontSize: 13),
                        ),
                      const SizedBox(height: 10),
                      
                      // Dirección
                      TextFormField(
                        controller: _direccionController,
                        decoration: const InputDecoration(
                          labelText: 'Dirección *',
                          border: OutlineInputBorder(),
                          prefixIcon: Icon(Icons.location_on, size: 18),
                          contentPadding: EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                          isDense: true,
                        ),
                        style: const TextStyle(fontSize: 13),
                        maxLines: 1,
                        validator: (value) => value?.isEmpty ?? true ? 'Campo requerido' : null,
                      ),
                      const SizedBox(height: 10),
                      
                      // Descripción
                      TextFormField(
                        controller: _descripcionController,
                        decoration: InputDecoration(
                          labelText: 'Descripción *',
                          border: OutlineInputBorder(),
                          prefixIcon: _cargandoDatos
                              ? const SizedBox(
                                  width: 18,
                                  height: 18,
                                  child: Padding(
                                    padding: EdgeInsets.all(4.0),
                                    child: CircularProgressIndicator(strokeWidth: 2),
                                  ),
                                )
                              : const Icon(Icons.description, size: 18),
                          contentPadding: EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                          isDense: true,
                        ),
                        maxLines: 2,
                        style: const TextStyle(fontSize: 13),
                        validator: (value) => value?.isEmpty ?? true ? 'Campo requerido' : null,
                      ),
                      const SizedBox(height: 10),
                      
                      // Ciudadano
                      TextFormField(
                        controller: _ciudadanoController,
                        decoration: InputDecoration(
                          labelText: 'Ciudadano',
                          border: OutlineInputBorder(),
                          prefixIcon: _cargandoDatos
                              ? const SizedBox(
                                  width: 18,
                                  height: 18,
                                  child: Padding(
                                    padding: EdgeInsets.all(4.0),
                                    child: CircularProgressIndicator(strokeWidth: 2),
                                  ),
                                )
                              : const Icon(Icons.person, size: 18),
                          contentPadding: EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                          isDense: true,
                        ),
                        style: const TextStyle(fontSize: 13),
                        maxLines: 1,
                      ),
                      const SizedBox(height: 10),
                      
                      // Cédula
                      TextFormField(
                        controller: _cedulaController,
                        decoration: InputDecoration(
                          labelText: 'Cédula',
                          border: OutlineInputBorder(),
                          prefixIcon: _cargandoDatos
                              ? const SizedBox(
                                  width: 18,
                                  height: 18,
                                  child: Padding(
                                    padding: EdgeInsets.all(4.0),
                                    child: CircularProgressIndicator(strokeWidth: 2),
                                  ),
                                )
                              : const Icon(Icons.badge, size: 18),
                          contentPadding: EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                          isDense: true,
                        ),
                        style: const TextStyle(fontSize: 13),
                        keyboardType: TextInputType.number,
                        maxLines: 1,
                      ),
                      const SizedBox(height: 10),
                      
                      // Teléfono
                      TextFormField(
                        controller: _telefonoController,
                        decoration: const InputDecoration(
                          labelText: 'Teléfono',
                          border: OutlineInputBorder(),
                          prefixIcon: Icon(Icons.phone, size: 18),
                          contentPadding: EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                          isDense: true,
                        ),
                        style: const TextStyle(fontSize: 13),
                        keyboardType: TextInputType.phone,
                        maxLines: 1,
                      ),
                      const SizedBox(height: 10),
                      
                      // Prioridad
                      if (_editando)
                        Container(
                          padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                          decoration: BoxDecoration(
                            border: Border.all(color: Colors.grey[400]!),
                            borderRadius: BorderRadius.circular(4),
                            color: Colors.grey[100],
                          ),
                          child: Row(
                            children: [
                              const Icon(Icons.priority_high, size: 18, color: Colors.grey),
                              const SizedBox(width: 8),
                              Expanded(
                                child: Column(
                                  crossAxisAlignment: CrossAxisAlignment.start,
                                  children: [
                                    Text(
                                      'Prioridad',
                                      style: TextStyle(
                                        fontSize: 10,
                                        color: Colors.grey[600],
                                      ),
                                    ),
                                    Text(
                                      _prioridadSeleccionada,
                                      style: const TextStyle(
                                        fontSize: 13,
                                        fontWeight: FontWeight.bold,
                                      ),
                                    ),
                                  ],
                                ),
                              ),
                            ],
                          ),
                        )
                      else
                        DropdownButtonFormField<String>(
                          decoration: const InputDecoration(
                            labelText: 'Prioridad',
                            border: OutlineInputBorder(),
                            prefixIcon: Icon(Icons.priority_high, size: 18),
                            contentPadding: EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                            isDense: true,
                          ),
                          value: _prioridadSeleccionada,
                          items: const [
                            DropdownMenuItem(value: 'ALTA', child: Text('🔴 Alta', style: TextStyle(fontSize: 13))),
                            DropdownMenuItem(value: 'MEDIA', child: Text('🟡 Media', style: TextStyle(fontSize: 13))),
                            DropdownMenuItem(value: 'BAJA', child: Text('🟢 Baja', style: TextStyle(fontSize: 13))),
                          ],
                          onChanged: (value) {
                            if (value != null) setState(() => _prioridadSeleccionada = value);
                          },
                          style: const TextStyle(fontSize: 13),
                        ),
                      const SizedBox(height: 16),
                      
                      // Botones
                      Row(
                        children: [
                          Expanded(
                            child: OutlinedButton(
                              onPressed: _cargando ? null : () => Navigator.pop(context),
                              style: OutlinedButton.styleFrom(
                                padding: const EdgeInsets.symmetric(vertical: 12),
                              ),
                              child: const Text('Cancelar', style: TextStyle(fontSize: 14)),
                            ),
                          ),
                          const SizedBox(width: 12),
                          Expanded(
                            flex: 2,
                            child: ElevatedButton(
                              onPressed: _cargando ? null : _guardarEvento,
                              style: ElevatedButton.styleFrom(
                                backgroundColor: Colors.red[700],
                                foregroundColor: Colors.white,
                                padding: const EdgeInsets.symmetric(vertical: 12),
                              ),
                              child: _cargando
                                  ? const SizedBox(
                                      width: 20,
                                      height: 20,
                                      child: CircularProgressIndicator(
                                        strokeWidth: 2,
                                        color: Colors.white,
                                      ),
                                    )
                                  : Text(
                                      _editando ? 'Actualizar' : 'Registrar',
                                      style: const TextStyle(fontSize: 14),
                                    ),
                            ),
                          ),
                        ],
                      ),
                    ],
                  ),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
