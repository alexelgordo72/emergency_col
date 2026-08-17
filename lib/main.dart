import 'services/barrio_service.dart';
import 'screens/gestion_barrios_dialog.dart';
import 'screens/planilla_ruta_dialog.dart';
import 'screens/dashboard/dashboard_screen.dart';
import 'screens/trazabilidad_dialog.dart';
import 'package:flutter/material.dart';
import 'package:flutter_map/flutter_map.dart';
import 'package:latlong2/latlong.dart';
import 'services/api_service.dart';
import 'models/reporte_comunitario.dart';

void main() => runApp(MaterialApp(home: HomeScreen(), debugShowCheckedModeBanner: false));

class HomeScreen extends StatefulWidget {
  @override
  _HomeScreenState createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  // Variables para paginación
  List<ReporteComunitario> reportes = [];
  int totalReportes = 0;
  int currentOffset = 0;
  final int limit = 50;
  bool cargando = false;
  bool cargandoMas = false;
  bool tieneMas = true;
  final ScrollController _scrollController = ScrollController();
  
  // Variables de búsqueda
  final TextEditingController _searchController = TextEditingController();
  String _tipoFiltro = 'barrio';
  
  // Variables del mapa
  final MapController _mapController = MapController();
  final LatLng _centroYumbo = const LatLng(3.5833, -76.4953);
  double _currentZoom = 14.0;

  @override
  void initState() {
    super.initState();
    _cargarReportes();
    _scrollController.addListener(() {
      if (_scrollController.position.pixels >= _scrollController.position.maxScrollExtent - 200) {
        _cargarMas();
      }
    });
  }

  @override
  void dispose() {
    _scrollController.dispose();
    super.dispose();
  }

  void _cargarReportes({bool reiniciar = true}) async {
    if (cargando) return;
    
    setState(() {
      cargando = true;
      if (reiniciar) {
        reportes = [];
        currentOffset = 0;
        tieneMas = true;
      }
    });

    try {
      String? barrio = _tipoFiltro == 'barrio' ? _searchController.text : null;
      String? nombre = _tipoFiltro == 'nombre' ? _searchController.text : null;
      String? telefono = _tipoFiltro == 'telefono' ? _searchController.text : null;
      
      final result = await ApiService.obtenerReportes(
        barrio: barrio,
        nombre: nombre,
        telefono: telefono,
        limit: limit,
        offset: currentOffset,
      );
      
      setState(() {
        if (reiniciar) {
          reportes = result['data'] ?? [];
        } else {
          reportes.addAll(result['data'] ?? []);
        }
        totalReportes = result['total'] ?? 0;
        currentOffset += (result['data'] as List?)?.length ?? 0;
        tieneMas = currentOffset < totalReportes;
        cargando = false;
      });
    } catch (e) {
      print('❌ Error al cargar reportes: $e');
      setState(() => cargando = false);
    }
  }

  void _cargarMas() {
    if (!cargandoMas && tieneMas && !cargando && reportes.isNotEmpty) {
      setState(() => cargandoMas = true);
      _cargarReportes(reiniciar: false);
      setState(() => cargandoMas = false);
    }
  }

  void _zoomIn() {
    setState(() {
      _currentZoom++;
      _mapController.move(_mapController.camera.center, _currentZoom);
    });
  }

  void _zoomOut() {
    setState(() {
      _currentZoom--;
      _mapController.move(_mapController.camera.center, _currentZoom);
    });
  }

  void _mostrarDetalleRufe(ReporteComunitario reporte) async {
    bool esRufe = reporte.datosExtra?['es_rufe'] == true;
    
    if (!esRufe) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Este evento no tiene ficha RUFE.'), backgroundColor: Colors.orange)
      );
      return;
    }

    showDialog(
      context: context,
      barrierDismissible: false,
      builder: (context) => AlertDialog(
        content: Row(
          children: [
            CircularProgressIndicator(color: Colors.red[700]),
            SizedBox(width: 20),
            Text("Cargando núcleo familiar..."),
          ],
        ),
      ),
    );

    final rufeData = await ApiService.obtenerDetalleRufe(reporte.id);
    Navigator.pop(context);

    if (rufeData == null || rufeData['status'] != 'success') {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('No se pudo cargar la ficha RUFE.'), backgroundColor: Colors.red)
      );
      return;
    }

    final form = rufeData['formulario'];
    final nucleo = rufeData['nucleo_familiar'] as List<dynamic>;

    showDialog(
      context: context,
      builder: (context) {
        return AlertDialog(
          title: Text('Ficha RUFE #${form['numero_formulario']} - ${reporte.barrio}'),
          content: SingleChildScrollView(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              mainAxisSize: MainAxisSize.min,
              children: [
                Row(
                  children: [
                    Text('Prioridad: ', style: TextStyle(fontWeight: FontWeight.bold)),
                    Chip(
                      label: Text('${form['prioridad']}'),
                      backgroundColor: form['prioridad'] == 'ALTA' ? Colors.red[100] : (form['prioridad'] == 'MEDIA' ? Colors.orange[100] : Colors.green[100]),
                    )
                  ],
                ),
                SizedBox(height: 8),
                Text('Evaluación Técnica:', style: TextStyle(fontWeight: FontWeight.bold, color: Colors.blueGrey)),
                Text('${form['observaciones_evaluador']}'),
                SizedBox(height: 12),
                Text('Mascotas en riesgo:', style: TextStyle(fontWeight: FontWeight.bold, color: Colors.blueGrey)),
                Text('${form['observaciones_animales']}'),
                Divider(height: 30, thickness: 2),
                Text('Núcleo Familiar:', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
                SizedBox(height: 8),
                ...nucleo.map((p) => Card(
                  elevation: 1,
                  margin: EdgeInsets.only(bottom: 6),
                  child: ListTile(
                    leading: CircleAvatar(
                      backgroundColor: p['es_jefe_hogar'] ? Colors.red[100] : Colors.grey[200],
                      child: Icon(p['es_jefe_hogar'] ? Icons.star : Icons.person, color: p['es_jefe_hogar'] ? Colors.red[700] : Colors.grey[600]),
                    ),
                    title: Text(p['nombre_completo'], style: TextStyle(fontWeight: FontWeight.bold, fontSize: 14)),
                    subtitle: Text('Doc: ${p['documento_identidad']} | Tel: ${p['telefono']}'),
                  ),
                )).toList(),
              ],
            ),
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.pop(context), 
              child: Text('Cerrar', style: TextStyle(color: Colors.red[700]))
            )
          ],
        );
      }
    );
  }

  void _mostrarDialogoEdicion(ReporteComunitario reporte) async {
    final tituloCtrl = TextEditingController(text: reporte.titulo);
    final direccionCtrl = TextEditingController(text: reporte.direccion);
    final ciudadanoCtrl = TextEditingController(text: reporte.datosExtra?['ciudadano'] ?? '');
    final telefonoCtrl = TextEditingController(text: reporte.datosExtra?['telefono'] ?? '');
    
    var listaBarriosObj = await BarrioService.getBarrios();
    List<String> listaBarrios = listaBarriosObj.map((b) => b.nombre).toList();
    listaBarrios.sort((a, b) => a.compareTo(b));
    String barrioSeleccionado = listaBarrios.contains(reporte.barrio) ? reporte.barrio : (listaBarrios.isNotEmpty ? listaBarrios.first : reporte.barrio);

    showDialog(
      context: context,
      builder: (dialogContext) {
        return StatefulBuilder(
          builder: (context, setStateModal) {
            return AlertDialog(
              title: Text('Editar Registro'),
              content: SingleChildScrollView(
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    TextField(controller: tituloCtrl, decoration: InputDecoration(labelText: 'Título / Asunto')),
                    SizedBox(height: 12),
                    DropdownButtonFormField<String>(
                      value: listaBarrios.contains(barrioSeleccionado) ? barrioSeleccionado : null,
                      decoration: InputDecoration(labelText: 'Barrio', border: OutlineInputBorder()),
                      items: listaBarrios.map((b) => DropdownMenuItem(value: b, child: Text(b))).toList(),
                      onChanged: (val) => setStateModal(() => barrioSeleccionado = val!),
                    ),
                    SizedBox(height: 12),
                    TextField(controller: direccionCtrl, decoration: InputDecoration(labelText: 'Dirección')),
                    TextField(controller: ciudadanoCtrl, decoration: InputDecoration(labelText: 'Ciudadano Afectado')),
                    TextField(controller: telefonoCtrl, decoration: InputDecoration(labelText: 'Teléfono')),
                  ],
                ),
              ),
              actions: [
                TextButton(
                  onPressed: () => Navigator.pop(dialogContext),
                  child: Text('Cancelar', style: TextStyle(color: Colors.grey)),
                ),
                ElevatedButton(
                  style: ElevatedButton.styleFrom(backgroundColor: Colors.red[700]),
                  onPressed: () async {
                    final datosActualizados = {
                      'categoria_id': 2,
                      'titulo': tituloCtrl.text.trim(),
                      'descripcion_detallada': reporte.descripcion ?? 'Reporte actualizado desde la app',
                      'sector_barrio': barrioSeleccionado.toUpperCase().trim(),
                      'direccion_referencia': direccionCtrl.text.trim(),
                      'latitud': reporte.latitud ?? 3.59,
                      'longitud': reporte.longitud ?? -76.49,
                      'datos_extra': {
                        'ciudadano': ciudadanoCtrl.text.isNotEmpty ? ciudadanoCtrl.text.trim() : (reporte.datosExtra?['ciudadano'] ?? 'Anónimo'),
                        'telefono': telefonoCtrl.text.isNotEmpty ? telefonoCtrl.text.trim() : (reporte.datosExtra?['telefono'] ?? 'No registrado'),
                      }
                    };
                    
                    print('📤 Enviando datos: $datosActualizados');
                    bool exito = await ApiService.actualizarReporte(reporte.id, datosActualizados);
                    print('📡 PUT response: $exito');
                    Navigator.pop(dialogContext);
                    if (exito) {
                      _cargarReportes(reiniciar: true);
                      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Registro actualizado', style: TextStyle(color: Colors.white)), backgroundColor: Colors.green));
                    } else {
                      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Error al actualizar', style: TextStyle(color: Colors.white)), backgroundColor: Colors.red));
                    }
                  },
                  child: Text('Guardar', style: TextStyle(color: Colors.white)),
                ),
              ],
            );
          },
        );
      }
    );
  }

  void _mostrarDialogoCreacion() async {
    final tituloCtrl = TextEditingController();
    final direccionCtrl = TextEditingController();
    final ciudadanoCtrl = TextEditingController();
    final telefonoCtrl = TextEditingController();

    var listaBarriosObj = await BarrioService.getBarrios();
    List<String> listaBarrios = listaBarriosObj.map((b) => b.nombre).toList();
    listaBarrios.sort((a, b) => a.compareTo(b));
    String? barrioSeleccionado = listaBarrios.isNotEmpty ? listaBarrios.first : null;

    showDialog(
      context: context,
      builder: (dialogContext) {
        return StatefulBuilder(
          builder: (context, setStateModal) {
            return AlertDialog(
              title: Text('Nuevo Evento de Emergencia'),
              content: SingleChildScrollView(
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    TextField(controller: tituloCtrl, decoration: InputDecoration(labelText: 'Título (Ej. Daño Estructural)')),
                    SizedBox(height: 12),
                    DropdownButtonFormField<String>(
                      value: barrioSeleccionado,
                      decoration: InputDecoration(labelText: 'Seleccione el Barrio', border: OutlineInputBorder()),
                      items: listaBarrios.map((b) => DropdownMenuItem(value: b, child: Text(b))).toList(),
                      onChanged: (val) => setStateModal(() => barrioSeleccionado = val),
                    ),
                    SizedBox(height: 12),
                    TextField(controller: direccionCtrl, decoration: InputDecoration(labelText: 'Dirección')),
                    TextField(controller: ciudadanoCtrl, decoration: InputDecoration(labelText: 'Ciudadano Afectado')),
                    TextField(controller: telefonoCtrl, decoration: InputDecoration(labelText: 'Teléfono')),
                  ],
                ),
              ),
              actions: [
                TextButton(
                  onPressed: () => Navigator.pop(dialogContext),
                  child: Text('Cancelar', style: TextStyle(color: Colors.grey)),
                ),
                ElevatedButton(
                  style: ElevatedButton.styleFrom(backgroundColor: Colors.red[700]),
                  onPressed: () async {
                    if (tituloCtrl.text.isEmpty || barrioSeleccionado == null) {
                      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Complete los campos obligatorios', style: TextStyle(color: Colors.white)), backgroundColor: Colors.red));
                      return;
                    }

                    final nuevoDato = {
                      'categoria_id': 2,
                      'titulo': tituloCtrl.text,
                      'descripcion_detallada': 'Reporte desde la app',
                      'sector_barrio': barrioSeleccionado!.toUpperCase(),
                      'direccion_referencia': direccionCtrl.text,
                      'latitud': 3.59,
                      'longitud': -76.49,
                      'datos_extra': {
                        'ciudadano': ciudadanoCtrl.text.isNotEmpty ? ciudadanoCtrl.text : 'Anónimo',
                        'telefono': telefonoCtrl.text.isNotEmpty ? telefonoCtrl.text : 'No registrado',
                      }
                    };

                    bool exito = await ApiService.crearReporte(nuevoDato);
                    Navigator.pop(dialogContext);
                    if (exito) {
                      _cargarReportes(reiniciar: true);
                      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Evento registrado con éxito', style: TextStyle(color: Colors.white)), backgroundColor: Colors.green));
                    }
                  },
                  child: Text('Registrar', style: TextStyle(color: Colors.white)),
                ),
              ],
            );
          },
        );
      }
    );
  }

  Color _getEstadoColor(String estado) {
    switch (estado.toLowerCase()) {
      case 'pendiente': return Colors.orange;
      case 'recibido': return Colors.blue;
      case 'en proceso': return Colors.cyan;
      case 'visitado-de-prioridad baja': return Colors.green;
      case 'visitado-de-prioridad media': return Colors.orange;
      case 'visitado-de-prioridad alta': return Colors.red;
      case 'inspeccionado': return Colors.indigo;
      case 'cerrado': return Colors.green;
      default: return Colors.grey;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('SGRD Yumbo', style: TextStyle(fontSize: 16)),
        backgroundColor: Colors.red[700],
        foregroundColor: Colors.white,
        actions: [
          IconButton(
            icon: const Icon(Icons.dashboard, color: Colors.white, size: 22),
            tooltip: 'Dashboard',
            onPressed: () {
              Navigator.push(
                context,
                MaterialPageRoute(builder: (context) => const DashboardScreen()),
              );
            },
          ),
          IconButton(
            icon: const Icon(Icons.holiday_village, color: Colors.white, size: 22),
            tooltip: 'Gestión de Barrios',
            onPressed: () {
              showDialog(
                context: context,
                builder: (context) => const GestionBarriosDialog(),
              );
            },
          ),
          IconButton(
            icon: const Icon(Icons.assignment_late, color: Colors.white, size: 22),
            tooltip: 'Generar Planilla de Ruta',
            onPressed: () {
              showDialog(
                context: context,
                builder: (context) => const PlanillaRutaDialog(),
              );
            },
          ),
          IconButton(
            icon: Icon(Icons.refresh),
            onPressed: () {
              _searchController.clear();
              _cargarReportes(reiniciar: true);
            },
          )
        ],
      ),
      body: Row(
        children: [
          Expanded(
            flex: 1,
            child: Scaffold(
              floatingActionButton: FloatingActionButton.extended(
                onPressed: _mostrarDialogoCreacion,
                backgroundColor: Colors.red[700],
                icon: const Icon(Icons.add, color: Colors.white),
                label: const Text('Nuevo Evento', style: TextStyle(color: Colors.white)),
              ),
              body: Column(
                children: [
                  Container(
                    color: Colors.white,
                    padding: EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                    child: Row(
                      children: [
                        Expanded(
                          flex: 2,
                          child: DropdownButtonFormField<String>(
                            value: _tipoFiltro,
                            decoration: InputDecoration(
                              contentPadding: EdgeInsets.symmetric(horizontal: 10),
                              border: OutlineInputBorder(borderRadius: BorderRadius.circular(8)),
                            ),
                            items: [
                              DropdownMenuItem(value: 'barrio', child: Text('Barrio')),
                              DropdownMenuItem(value: 'nombre', child: Text('Nombre')),
                              DropdownMenuItem(value: 'telefono', child: Text('Teléfono')),
                              DropdownMenuItem(value: 'rufe', child: Text('🔖 RUFE')),
                            ],
                            onChanged: (val) => setState(() => _tipoFiltro = val!),
                          ),
                        ),
                        SizedBox(width: 8),
                        Expanded(
                          flex: 3,
                          child: TextField(
                            controller: _searchController,
                            decoration: InputDecoration(
                              hintText: 'Buscar...',
                              suffixIcon: IconButton(
                                icon: Icon(Icons.search, color: Colors.red[700]),
                                onPressed: () => _cargarReportes(reiniciar: true),
                              ),
                              border: OutlineInputBorder(borderRadius: BorderRadius.circular(8)),
                              contentPadding: EdgeInsets.symmetric(horizontal: 10),
                            ),
                            onSubmitted: (_) => _cargarReportes(reiniciar: true),
                          ),
                        ),
                      ],
                    ),
                  ),
                  Expanded(
                    child: reportes.isEmpty && cargando
                        ? const Center(child: CircularProgressIndicator())
                        : reportes.isEmpty && !cargando
                            ? const Center(child: Text('No se encontraron resultados'))
                            : ListView.builder(
                                controller: _scrollController,
                                padding: EdgeInsets.all(8),
                                itemCount: reportes.length + (tieneMas ? 1 : 0),
                                itemBuilder: (context, index) {
                                  if (index == reportes.length) {
                                    return Container(
                                      padding: EdgeInsets.all(16),
                                      child: Center(
                                        child: cargandoMas
                                            ? const CircularProgressIndicator()
                                            : const Text('No hay más reportes'),
                                      ),
                                    );
                                  }
                                  final reporte = reportes[index];
                                  final ciudadano = reporte.datosExtra?['ciudadano'] ?? 'Anónimo';
                                  final telefono = reporte.datosExtra?['telefono'] ?? 'N/A';
                                  final bool esRufe = reporte.datosExtra?['es_rufe'] == true;

                                  return Card(
                                    elevation: 2,
                                    margin: EdgeInsets.symmetric(vertical: 6),
                                    child: ListTile(
                                      leading: CircleAvatar(
                                        backgroundColor: esRufe ? Colors.purple[50] : Colors.red[50],
                                        child: Icon(esRufe ? Icons.assignment_ind : Icons.warning_amber_rounded, color: esRufe ? Colors.purple[700] : Colors.red[700]),
                                      ),
                                      title: Text(reporte.titulo, style: TextStyle(fontWeight: FontWeight.bold)),
                                      subtitle: Column(
                                        crossAxisAlignment: CrossAxisAlignment.start,
                                        children: [
                                          SizedBox(height: 4),
                                          Text('📍 ${reporte.barrio} - ${reporte.direccion}'),
                                          Text('👤 $ciudadano | 📱 $telefono'),
                                          Row(
                                            children: [
                                              const Text('📊 Estado: ', style: TextStyle(fontSize: 12)),
                                              Container(
                                                padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                                                decoration: BoxDecoration(
                                                  color: _getEstadoColor(reporte.estado),
                                                  borderRadius: BorderRadius.circular(8),
                                                ),
                                                child: Text(
                                                  reporte.estado,
                                                  style: const TextStyle(fontSize: 12, color: Colors.white, fontWeight: FontWeight.bold),
                                                ),
                                              ),
                                            ],
                                          ),
                                        ],
                                      ),
                                      isThreeLine: true,
                                      trailing: Row(
                                        mainAxisSize: MainAxisSize.min,
                                        children: [
                                          IconButton(
                                            icon: const Icon(Icons.history_edu, color: Colors.blue),
                                            tooltip: 'Trazabilidad y Ciclo de Vida',
                                            onPressed: () {
                                              showDialog(
                                                context: context,
                                                barrierDismissible: false,
                                                builder: (context) => TrazabilidadDialog(reporte: reporte),
                                              );
                                            },
                                          ),
                                          IconButton(
                                            icon: Icon(Icons.edit_outlined, color: Colors.blueGrey),
                                            onPressed: () => _mostrarDialogoEdicion(reporte),
                                          )
                                        ],
                                      ),
                                    ),
                                  );
                                },
                              ),
                  ),
                ],
              ),
            ),
          ),
          Expanded(
            flex: 1,
            child: Stack(
              children: [
                FlutterMap(
                  mapController: _mapController,
                  options: MapOptions(
                    initialCenter: _centroYumbo,
                    initialZoom: _currentZoom,
                  ),
                  children: [
                    TileLayer(
                      urlTemplate: 'https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png',
                      subdomains: ['a', 'b', 'c'],
                      userAgentPackageName: 'com.emergency_col.app',
                    ),
                    if (reportes.isNotEmpty)
                      PolylineLayer(
                        polylines: [
                          Polyline(
                            points: reportes
                                .where((r) => r.latitud != null && r.longitud != null)
                                .map((r) => LatLng(r.latitud!, r.longitud!))
                                .toList(),
                            strokeWidth: 4.0,
                            color: Colors.blueAccent.withOpacity(0.7),
                          ),
                        ],
                      ),
                    MarkerLayer(
                      markers: reportes
                          .where((r) => r.latitud != null && r.longitud != null)
                          .map((reporte) {
                        bool esRufe = reporte.datosExtra?['es_rufe'] == true;
                        final punto = LatLng(reporte.latitud!, reporte.longitud!);
                        return Marker(
                          point: punto,
                          width: 50,
                          height: 50,
                          child: Tooltip(
                            message: '${reporte.titulo}\n${reporte.barrio}',
                            child: GestureDetector(
                              onTap: () => _mostrarDetalleRufe(reporte),
                              child: Icon(
                                Icons.location_on,
                                color: esRufe ? Colors.purple[800] : Colors.red[900],
                                size: 45,
                              ),
                            ),
                          ),
                        );
                      }).toList(),
                    ),
                  ],
                ),
                Positioned(
                  bottom: 20,
                  right: 20,
                  child: Column(
                    children: [
                      FloatingActionButton(
                        heroTag: "btn1",
                        mini: true,
                        backgroundColor: Colors.white,
                        onPressed: _zoomIn,
                        child: Icon(Icons.add, color: Colors.black87),
                      ),
                      SizedBox(height: 8),
                      FloatingActionButton(
                        heroTag: "btn2",
                        mini: true,
                        backgroundColor: Colors.white,
                        onPressed: _zoomOut,
                        child: Icon(Icons.remove, color: Colors.black87),
                      ),
                    ],
                  ),
                )
              ],
            ),
          ),
        ],
      ),
    );
  }
}
