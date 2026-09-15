import 'package:flutter/material.dart';
import 'package:flutter_map/flutter_map.dart';
import 'package:latlong2/latlong.dart';
import 'package:sgrd_final/services/api_service.dart';
import 'package:sgrd_final/services/auth_service.dart';
import 'package:sgrd_final/screens/login_screen.dart';
import 'package:sgrd_final/screens/dashboard_screen.dart';
import 'package:sgrd_final/eventos/widgets/boton_nuevo_evento.dart';
import 'package:sgrd_final/eventos/widgets/item_reporte.dart';

class Principal extends StatefulWidget {
  const Principal({Key? key}) : super(key: key);

  @override
  State<Principal> createState() => _PrincipalState();
}

class _PrincipalState extends State<Principal> {
  List<dynamic> items = [];
  List<dynamic> itemsFiltrados = [];
  bool isLoading = true;
  String? errorMessage;

  String? barrioSeleccionado;
  String? nombreBusqueda;
  String? telefonoBusqueda;

  List<String> barrios = ['Todos'];
  final MapController mapController = MapController();
  double _currentZoom = 12.0;
  LatLng _currentCenter = const LatLng(3.5834, -76.4974);

  @override
  void initState() {
    super.initState();
    cargarDatos();
  }

  Future<void> cargarDatos() async {
    setState(() {
      isLoading = true;
      errorMessage = null;
    });

    try {
      final response = await ApiService.obtenerReportes(limit: 10000);

      List<dynamic> tempList = [];
      if (response is Map<String, dynamic>) {
        final data = response['data'];
        if (data is List) {
          tempList = data;
        }
      }

      List<String> listaBarrios = ['Todos'];
      for (var item in tempList) {
        final barrio = item['barrio'] ?? item['sector_barrio'];
        if (barrio != null && barrio.isNotEmpty && !listaBarrios.contains(barrio)) {
          listaBarrios.add(barrio);
        }
      }

      setState(() {
        items = tempList;
        itemsFiltrados = tempList;
        barrios = listaBarrios;
        isLoading = false;
      });
    } catch (e) {
      setState(() {
        errorMessage = 'Error: $e';
        isLoading = false;
      });
    }
  }

  void filtrarResultados() {
    setState(() {
      itemsFiltrados = items.where((item) {
        if (barrioSeleccionado != null && barrioSeleccionado != 'Todos') {
          final barrio = item['barrio'] ?? item['sector_barrio'] ?? '';
          if (barrio != barrioSeleccionado) return false;
        }

        if (nombreBusqueda != null && nombreBusqueda!.isNotEmpty) {
          final nombre = item['ciudadano'] ?? '';
          if (!nombre.toLowerCase().contains(nombreBusqueda!.toLowerCase())) return false;
        }

        if (telefonoBusqueda != null && telefonoBusqueda!.isNotEmpty) {
          final telefono = item['telefono'] ?? '';
          if (!telefono.contains(telefonoBusqueda!)) return false;
        }

        return true;
      }).toList();
    });
  }

  void _zoomIn() {
    setState(() {
      _currentZoom = (_currentZoom + 0.5).clamp(1.0, 18.0);
      mapController.move(_currentCenter, _currentZoom);
    });
  }

  void _zoomOut() {
    setState(() {
      _currentZoom = (_currentZoom - 0.5).clamp(1.0, 18.0);
      mapController.move(_currentCenter, _currentZoom);
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('SGRD Yumbo'),
        backgroundColor: Colors.red[700],
        foregroundColor: Colors.white,
        actions: [
          IconButton(
            icon: const Icon(Icons.dashboard),
            onPressed: () {
              Navigator.push(
                context,
                MaterialPageRoute(builder: (context) => const DashboardScreen()),
              );
            },
            tooltip: 'Dashboard',
          ),
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: cargarDatos,
            tooltip: 'Recargar',
          ),
          IconButton(
            icon: const Icon(Icons.logout),
            onPressed: () {
              showDialog(
                context: context,
                builder: (context) => AlertDialog(
                  title: const Text('Cerrar Sesión'),
                  content: const Text('¿Estás seguro de que deseas salir?'),
                  actions: [
                    TextButton(
                      onPressed: () => Navigator.pop(context),
                      child: const Text('Cancelar'),
                    ),
                    TextButton(
                      onPressed: () {
                        AuthService.logout();
                        Navigator.pushReplacement(
                          context,
                          MaterialPageRoute(builder: (context) => const LoginScreen()),
                        );
                      },
                      child: const Text('Salir', style: TextStyle(color: Colors.red)),
                    ),
                  ],
                ),
              );
            },
            tooltip: 'Cerrar Sesión',
          ),
        ],
      ),
      body: isLoading
          ? const Center(child: CircularProgressIndicator())
          : errorMessage != null
              ? Center(child: Text('Error: $errorMessage'))
              : LayoutBuilder(
                  builder: (context, constraints) {
                    if (constraints.maxWidth > 800) {
                      return Row(
                        children: [
                          Expanded(
                            flex: 2,
                            child: Column(
                              children: [
                                _buildFiltros(),
                                Expanded(child: _buildListaReportes()),
                              ],
                            ),
                          ),
                          Expanded(
                            flex: 3,
                            child: Stack(
                              children: [
                                _buildMapa(),
                                Positioned(
                                  bottom: 16,
                                  right: 16,
                                  child: Column(
                                    children: [
                                      FloatingActionButton(
                                        heroTag: 'zoomIn',
                                        onPressed: _zoomIn,
                                        mini: true,
                                        backgroundColor: Colors.white,
                                        foregroundColor: Colors.black,
                                        child: const Icon(Icons.add, size: 18),
                                      ),
                                      const SizedBox(height: 6),
                                      FloatingActionButton(
                                        heroTag: 'zoomOut',
                                        onPressed: _zoomOut,
                                        mini: true,
                                        backgroundColor: Colors.white,
                                        foregroundColor: Colors.black,
                                        child: const Icon(Icons.remove, size: 18),
                                      ),
                                    ],
                                  ),
                                ),
                              ],
                            ),
                          ),
                        ],
                      );
                    } else {
                      return Column(
                        children: [
                          _buildFiltros(),
                          Expanded(
                            flex: 2,
                            child: Stack(
                              children: [
                                _buildMapa(),
                                Positioned(
                                  bottom: 16,
                                  right: 16,
                                  child: Column(
                                    children: [
                                      FloatingActionButton(
                                        heroTag: 'zoomIn',
                                        onPressed: _zoomIn,
                                        mini: true,
                                        backgroundColor: Colors.white,
                                        foregroundColor: Colors.black,
                                        child: const Icon(Icons.add, size: 18),
                                      ),
                                      const SizedBox(height: 6),
                                      FloatingActionButton(
                                        heroTag: 'zoomOut',
                                        onPressed: _zoomOut,
                                        mini: true,
                                        backgroundColor: Colors.white,
                                        foregroundColor: Colors.black,
                                        child: const Icon(Icons.remove, size: 18),
                                      ),
                                    ],
                                  ),
                                ),
                              ],
                            ),
                          ),
                          Expanded(
                            flex: 3,
                            child: _buildListaReportes(),
                          ),
                        ],
                      );
                    }
                  },
                ),
      floatingActionButton: BotonNuevoEvento(
        onEventoCreado: cargarDatos,
      ),
      floatingActionButtonLocation: FloatingActionButtonLocation.startFloat,
    );
  }

  Widget _buildFiltros() {
    return Container(
      padding: const EdgeInsets.all(8),
      color: Colors.grey[100],
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          Row(
            children: [
              Expanded(
                child: DropdownButtonFormField<String>(
                  decoration: const InputDecoration(
                    labelText: 'Barrio',
                    border: OutlineInputBorder(),
                    prefixIcon: Icon(Icons.location_city, size: 16),
                    contentPadding: EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                    isDense: true,
                  ),
                  value: barrioSeleccionado ?? 'Todos',
                  items: barrios.map((barrio) {
                    return DropdownMenuItem(
                      value: barrio,
                      child: Text(
                        barrio,
                        overflow: TextOverflow.ellipsis,
                        style: const TextStyle(fontSize: 12),
                      ),
                    );
                  }).toList(),
                  onChanged: (value) {
                    barrioSeleccionado = value;
                    filtrarResultados();
                  },
                ),
              ),
            ],
          ),
          const SizedBox(height: 4),
          Row(
            children: [
              Expanded(
                child: TextField(
                  decoration: const InputDecoration(
                    labelText: 'Nombre',
                    border: OutlineInputBorder(),
                    prefixIcon: Icon(Icons.person, size: 16),
                    contentPadding: EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                    isDense: true,
                  ),
                  onChanged: (value) {
                    nombreBusqueda = value;
                    filtrarResultados();
                  },
                ),
              ),
              const SizedBox(width: 4),
              Expanded(
                child: TextField(
                  decoration: const InputDecoration(
                    labelText: 'Teléfono',
                    border: OutlineInputBorder(),
                    prefixIcon: Icon(Icons.phone, size: 16),
                    contentPadding: EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                    isDense: true,
                  ),
                  keyboardType: TextInputType.phone,
                  onChanged: (value) {
                    telefonoBusqueda = value;
                    filtrarResultados();
                  },
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildMapa() {
    return Container(
      color: Colors.grey[200],
      child: FlutterMap(
        mapController: mapController,
        options: MapOptions(
          initialCenter: _currentCenter,
          initialZoom: _currentZoom,
          maxZoom: 18,
        ),
        children: [
          TileLayer(
            urlTemplate: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
            subdomains: ['a', 'b', 'c'],
            userAgentPackageName: 'com.example.app',
          ),
          MarkerLayer(
            markers: itemsFiltrados.where((item) {
              final lat = item['latitud'];
              final lng = item['longitud'];
              return lat != null && lng != null && lat != 0 && lng != 0;
            }).map((item) {
              final estado = item['estado'] ?? 'PENDIENTE';
              Color color = Colors.orange;
              if (estado.toUpperCase().contains('VISITADO')) {
                color = Colors.green;
              } else if (estado.toUpperCase().contains('VERIFICADO')) {
                color = Colors.blue;
              }
              return Marker(
                point: LatLng(
                  (item['latitud'] as num).toDouble(),
                  (item['longitud'] as num).toDouble(),
                ),
                width: 24,
                height: 24,
                child: Container(
                  decoration: BoxDecoration(
                    color: color,
                    shape: BoxShape.circle,
                    border: Border.all(color: Colors.white, width: 2),
                    boxShadow: [
                      BoxShadow(
                        color: Colors.black.withOpacity(0.3),
                        blurRadius: 3,
                      ),
                    ],
                  ),
                  child: const Icon(
                    Icons.location_on,
                    color: Colors.white,
                    size: 14,
                  ),
                ),
              );
            }).toList(),
          ),
        ],
      ),
    );
  }

  Widget _buildListaReportes() {
    if (itemsFiltrados.isEmpty) {
      return const Center(child: Text('No hay reportes'));
    }
    return ListView.builder(
      itemCount: itemsFiltrados.length,
      itemBuilder: (context, index) {
        final item = itemsFiltrados[index];
        return ItemReporte(
          reporte: item,
          onActualizar: cargarDatos,
        );
      },
    );
  }
}
