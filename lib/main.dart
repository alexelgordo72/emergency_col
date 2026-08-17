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
  List<ReporteComunitario> reportes = [];
  int totalReportes = 0;
  int currentOffset = 0;
  final int limit = 50;
  bool cargando = false;
  bool cargandoMas = false;
  bool tieneMas = true;
  final ScrollController _scrollController = ScrollController();
  
  final TextEditingController _searchController = TextEditingController();
  String _tipoFiltro = 'barrio';
  
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

  Future<void> _cargarReportes({bool reiniciar = true}) async {
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
      final String filtro = _searchController.text;
      String? barrioFiltro;
      String? nombreFiltro;
      String? telefonoFiltro;
      
      if (filtro.isNotEmpty) {
        switch (_tipoFiltro) {
          case 'barrio':
            barrioFiltro = filtro;
            break;
          case 'nombre':
            nombreFiltro = filtro;
            break;
          case 'telefono':
            telefonoFiltro = filtro;
            break;
          case 'rufe':
            // RUFE es un filtro especial que se maneja en el backend
            barrioFiltro = filtro;
            break;
        }
      }
      
      final result = await ApiService.obtenerReportes(
        barrio: barrioFiltro,
        nombre: nombreFiltro,
        telefono: telefonoFiltro,
        limit: limit,
        offset: currentOffset,
      );
      
      setState(() {
        final nuevosReportes = result['data'] as List<ReporteComunitario>? ?? [];
        
        if (reiniciar) {
          reportes = nuevosReportes;
        } else {
          reportes.addAll(nuevosReportes);
        }
        
        totalReportes = result['total'] ?? 0;
        currentOffset += nuevosReportes.length;
        
        // Verificar si hay más resultados
        tieneMas = currentOffset < totalReportes;
        
        cargando = false;
        cargandoMas = false;
      });
    } catch (e) {
      print('❌ Error al cargar reportes: $e');
      setState(() {
        cargando = false;
        cargandoMas = false;
      });
    }
  }

  void _cargarMas() {
    if (!cargandoMas && tieneMas && !cargando) {
      setState(() => cargandoMas = true);
      _cargarReportes(reiniciar: false);
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

  void _mostrarDialogoEdicion(ReporteComunitario reporte) async {
    final tituloCtrl = TextEditingController(text: reporte.titulo);
    final direccionCtrl = TextEditingController(text: reporte.direccion);
    final ciudadanoCtrl = TextEditingController(text: reporte.ciudadano ?? '');
    final telefonoCtrl = TextEditingController(text: reporte.telefono ?? '');
    
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
                        'ciudadano': ciudadanoCtrl.text.isNotEmpty ? ciudadanoCtrl.text.trim() : (reporte.ciudadano ?? 'Anónimo'),
                        'telefono': telefonoCtrl.text.isNotEmpty ? telefonoCtrl.text.trim() : (reporte.telefono ?? 'No registrado'),
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

  @override
  Widget build(BuildContext context) {
    final reportesConCoordenadas = reportes.where((r) => r.latitud != null && r.longitud != null).toList();

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
                onPressed: () {
                  // TODO: Implementar creación de reporte
                },
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
                  // Mostrar total de resultados
                  if (reportes.isNotEmpty || totalReportes > 0)
                    Padding(
                      padding: EdgeInsets.symmetric(horizontal: 12, vertical: 4),
                      child: Text(
                        'Mostrando ${reportes.length} de $totalReportes resultados',
                        style: TextStyle(fontSize: 12, color: Colors.grey[600]),
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
                                  final ciudadano = reporte.ciudadano ?? 'Anónimo';
                                  final telefono = reporte.telefono ?? 'N/A';

                                  return Card(
                                    elevation: 2,
                                    margin: EdgeInsets.symmetric(vertical: 6),
                                    child: ListTile(
                                      leading: CircleAvatar(
                                        backgroundColor: Colors.red[50],
                                        child: Icon(Icons.warning_amber_rounded, color: Colors.red[700]),
                                      ),
                                      title: Text(reporte.titulo, style: TextStyle(fontWeight: FontWeight.bold)),
                                      subtitle: Column(
                                        crossAxisAlignment: CrossAxisAlignment.start,
                                        children: [
                                          SizedBox(height: 4),
                                          Text('📍 ${reporte.barrio} - ${reporte.direccion}'),
                                          Text('👤 $ciudadano | 📱 $telefono'),
                                          if (reporte.latitud != null && reporte.longitud != null)
                                            Text('📍 ${reporte.latitud!.toStringAsFixed(6)}, ${reporte.longitud!.toStringAsFixed(6)}',
                                                style: TextStyle(fontSize: 10, color: Colors.grey[500])),
                                        ],
                                      ),
                                      isThreeLine: true,
                                      trailing: Row(
                                        mainAxisSize: MainAxisSize.min,
                                        children: [
                                          IconButton(
                                            icon: Icon(Icons.history_edu, color: Colors.blue),
                                            tooltip: 'Trazabilidad',
                                            onPressed: () {
                                              showDialog(
                                                context: context,
                                                builder: (context) => TrazabilidadDialog(reporte: reporte),
                                              );
                                            },
                                          ),
                                          IconButton(
                                            icon: Icon(Icons.edit_outlined, color: Colors.blueGrey),
                                            tooltip: 'Editar',
                                            onPressed: () => _mostrarDialogoEdicion(reporte),
                                          ),
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
                    if (reportesConCoordenadas.isNotEmpty)
                      PolylineLayer(
                        polylines: [
                          Polyline(
                            points: reportesConCoordenadas
                                .map((r) => LatLng(r.latitud!, r.longitud!))
                                .toList(),
                            strokeWidth: 4.0,
                            color: Colors.blueAccent.withOpacity(0.7),
                          ),
                        ],
                      ),
                    MarkerLayer(
                      markers: reportesConCoordenadas.map((reporte) {
                        final punto = LatLng(reporte.latitud!, reporte.longitud!);
                        return Marker(
                          point: punto,
                          width: 50,
                          height: 50,
                          child: Tooltip(
                            message: '${reporte.titulo}\n${reporte.barrio}',
                            child: GestureDetector(
                              onTap: () {
                                showDialog(
                                  context: context,
                                  builder: (context) => AlertDialog(
                                    title: Text(reporte.titulo),
                                    content: Column(
                                      mainAxisSize: MainAxisSize.min,
                                      crossAxisAlignment: CrossAxisAlignment.start,
                                      children: [
                                        Text('📍 ${reporte.barrio}'),
                                        Text('📌 ${reporte.direccion}'),
                                        Text('👤 ${reporte.ciudadano ?? 'Anónimo'}'),
                                        Text('📱 ${reporte.telefono ?? 'N/A'}'),
                                        Text('📊 ${reporte.estado}'),
                                      ],
                                    ),
                                    actions: [
                                      TextButton(
                                        onPressed: () => Navigator.pop(context),
                                        child: Text('Cerrar'),
                                      ),
                                    ],
                                  ),
                                );
                              },
                              child: Icon(
                                Icons.location_on,
                                color: Colors.red[900],
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
