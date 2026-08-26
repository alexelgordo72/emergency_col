import 'package:flutter/material.dart';
import 'package:emergency_col/services/api_service.dart';
import 'package:emergency_col/screens/crear_evento_screen.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({Key? key}) : super(key: key);

  @override
  _HomeScreenState createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  List<dynamic> reportes = [];
  bool cargando = true;
  String? error;

  @override
  void initState() {
    super.initState();
    cargarReportes();
  }

  Future<void> cargarReportes() async {
    setState(() => cargando = true);
    try {
      final result = await ApiService.obtenerReportes();
      
      List<dynamic> lista = [];
      if (result is Map<String, dynamic>) {
        final data = result['data'];
        if (data is List) {
          lista = data;
        }
      } else if (result is List) {
        lista = result;
      }
      
      setState(() {
        reportes = lista;
        cargando = false;
      });
    } catch (e) {
      setState(() {
        error = e.toString();
        cargando = false;
      });
      print('❌ Error: $e');
    }
  }

  void _nuevoEvento() {
    Navigator.push(
      context,
      MaterialPageRoute(builder: (context) => const CrearEventoScreen()),
    ).then((_) => cargarReportes());
  }

  Future<void> _eliminarReporte(String id, String titulo) async {
    final confirm = await showDialog<bool>(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Confirmar eliminación'),
        content: Text('¿Estás seguro de eliminar el reporte "$titulo"?'),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context, false),
            child: const Text('Cancelar'),
          ),
          TextButton(
            onPressed: () => Navigator.pop(context, true),
            style: TextButton.styleFrom(foregroundColor: Colors.red),
            child: const Text('Eliminar'),
          ),
        ],
      ),
    );

    if (confirm == true) {
      try {
        final exito = await ApiService.eliminarReporte(id);
        if (exito) {
          if (mounted) {
            ScaffoldMessenger.of(context).showSnackBar(
              const SnackBar(content: Text('✅ Reporte eliminado'), backgroundColor: Colors.green),
            );
            cargarReportes();
          }
        } else {
          if (mounted) {
            ScaffoldMessenger.of(context).showSnackBar(
              const SnackBar(content: Text('❌ Error al eliminar'), backgroundColor: Colors.red),
            );
          }
        }
      } catch (e) {
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text('❌ Error: $e'), backgroundColor: Colors.red),
          );
        }
      }
    }
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
            icon: const Icon(Icons.refresh),
            onPressed: cargarReportes,
            tooltip: 'Recargar',
          ),
        ],
      ),
      body: cargando
          ? const Center(child: CircularProgressIndicator())
          : error != null
              ? Center(child: Text('Error: $error'))
              : Column(
                  children: [
                    Container(
                      padding: const EdgeInsets.all(16),
                      color: Colors.grey[200],
                      child: Row(
                        mainAxisAlignment: MainAxisAlignment.spaceAround,
                        children: [
                          _buildStatCard('Total', reportes.length.toString(), Colors.blue),
                          _buildStatCard('Pendientes', '0', Colors.orange),
                          _buildStatCard('Visitados', '0', Colors.green),
                        ],
                      ),
                    ),
                    Expanded(
                      child: reportes.isEmpty
                          ? const Center(child: Text('No hay reportes'))
                          : ListView.builder(
                              itemCount: reportes.length,
                              itemBuilder: (context, index) {
                                final r = reportes[index];
                                final estado = r['estado'] ?? 'PENDIENTE';
                                Color color = Colors.orange;
                                if (estado.toUpperCase().contains('VISITADO')) {
                                  color = Colors.green;
                                } else if (estado.toUpperCase().contains('VERIFICADO')) {
                                  color = Colors.blue;
                                }
                                return Card(
                                  margin: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                                  child: ListTile(
                                    title: Text(
                                      r['titulo'] ?? 'Sin título',
                                      style: const TextStyle(fontWeight: FontWeight.bold),
                                    ),
                                    subtitle: Column(
                                      crossAxisAlignment: CrossAxisAlignment.start,
                                      children: [
                                        Text('${r['barrio'] ?? r['sector_barrio'] ?? 'Sin barrio'} - ${r['direccion'] ?? r['direccion_referencia'] ?? 'Sin dirección'}'),
                                        Text(
                                          '${r['ciudadano'] ?? 'Anónimo'} | ${r['telefono'] ?? 'N/A'}',
                                          style: const TextStyle(fontSize: 12),
                                        ),
                                      ],
                                    ),
                                    trailing: Row(
                                      mainAxisSize: MainAxisSize.min,
                                      children: [
                                        Container(
                                          padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                                          decoration: BoxDecoration(
                                            color: color,
                                            borderRadius: BorderRadius.circular(8),
                                          ),
                                          child: Text(
                                            estado,
                                            style: const TextStyle(
                                              color: Colors.white,
                                              fontWeight: FontWeight.bold,
                                              fontSize: 10,
                                            ),
                                          ),
                                        ),
                                        IconButton(
                                          icon: const Icon(Icons.delete, color: Colors.red, size: 20),
                                          onPressed: () => _eliminarReporte(
                                            r['id'] ?? '',
                                            r['titulo'] ?? '',
                                          ),
                                          tooltip: 'Eliminar',
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
      floatingActionButton: FloatingActionButton(
        onPressed: _nuevoEvento,
        backgroundColor: Colors.red[700],
        child: const Icon(Icons.add, color: Colors.white),
        tooltip: 'Nuevo Evento',
      ),
    );
  }

  Widget _buildStatCard(String label, String value, Color color) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      decoration: BoxDecoration(
        color: color,
        borderRadius: BorderRadius.circular(8),
      ),
      child: Column(
        children: [
          Text(
            value,
            style: const TextStyle(
              fontSize: 20,
              fontWeight: FontWeight.bold,
              color: Colors.white,
            ),
          ),
          Text(
            label,
            style: const TextStyle(
              fontSize: 12,
              color: Colors.white70,
            ),
          ),
        ],
      ),
    );
  }
}
