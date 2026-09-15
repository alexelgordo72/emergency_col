import 'package:flutter/material.dart';
import 'package:sgrd_final/services/api_service.dart';

class DashboardScreen extends StatefulWidget {
  const DashboardScreen({Key? key}) : super(key: key);

  @override
  State<DashboardScreen> createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen> {
  Map<String, dynamic>? dashboardData;
  bool isLoading = true;
  String? error;

  @override
  void initState() {
    super.initState();
    _cargarDashboard();
  }

  Future<void> _cargarDashboard() async {
    setState(() {
      isLoading = true;
      error = null;
    });

    try {
      final response = await ApiService.obtenerDashboardCompleto();
      if (response['status'] == 'success') {
        setState(() {
          dashboardData = response['data'];
          isLoading = false;
        });
      } else {
        setState(() {
          error = 'Error al cargar datos';
          isLoading = false;
        });
      }
    } catch (e) {
      setState(() {
        error = 'Error al cargar dashboard: $e';
        isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('📊 Tablero de Control'),
        backgroundColor: Colors.red[700],
        foregroundColor: Colors.white,
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: _cargarDashboard,
            tooltip: 'Recargar',
          ),
        ],
      ),
      body: isLoading
          ? const Center(child: CircularProgressIndicator())
          : error != null
              ? Center(child: Text(error!))
              : dashboardData == null
                  ? const Center(child: Text('Sin datos'))
                  : _buildDashboard(),
    );
  }

  Widget _buildDashboard() {
    final data = dashboardData!;
    final total = data['total'] ?? 0;
    final estados = data['estados'] as List<dynamic>? ?? [];
    final generos = data['generos'] as List<dynamic>? ?? [];
    final animales = data['animales'] as Map<String, dynamic>? ?? {};

    return SingleChildScrollView(
      padding: const EdgeInsets.all(12),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          _buildTotalCard(total),
          const SizedBox(height: 16),
          _buildSeccion('🐾 Animales Sintientes', [
            _buildAnimalCard('🐔 Aves', animales['aves'] ?? 0, Colors.green),
            _buildAnimalCard('🐱 Gatos', animales['gatos'] ?? 0, Colors.orange),
            _buildAnimalCard('🐶 Perros', animales['perros'] ?? 0, Colors.blue),
          ]),
          const SizedBox(height: 16),
          _buildSeccion('📋 Solicitudes Recibidas',
            estados.map((e) => _buildEstadoRow(e['estado'], e['total'])).toList(),
          ),
          const SizedBox(height: 16),
          _buildSeccion('👤 Distribución por Género',
            generos.map((g) => _buildGeneroRow(g['genero'], g['total'])).toList(),
          ),
        ],
      ),
    );
  }

  Widget _buildSeccion(String titulo, List<Widget> children) {
    return Container(
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(12),
        boxShadow: [
          BoxShadow(
            color: Colors.grey.withOpacity(0.1),
            blurRadius: 8,
            offset: const Offset(0, 2),
          ),
        ],
      ),
      child: Padding(
        padding: const EdgeInsets.all(12),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              titulo,
              style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 8),
            ...children,
          ],
        ),
      ),
    );
  }

  Widget _buildAnimalCard(String label, int count, Color color) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      decoration: BoxDecoration(
        color: color.withOpacity(0.1),
        borderRadius: BorderRadius.circular(8),
        border: Border.all(color: color.withOpacity(0.3)),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Text(
            '$count',
            style: TextStyle(
              fontWeight: FontWeight.bold,
              fontSize: 18,
              color: color,
            ),
          ),
          const SizedBox(width: 8),
          Text(
            label,
            style: const TextStyle(fontSize: 13, fontWeight: FontWeight.w500),
          ),
        ],
      ),
    );
  }

  Widget _buildEstadoRow(String estado, int total) {
    Color color = Colors.orange;
    if (estado.contains('PENDIENTE')) color = Colors.orange;
    else if (estado.contains('VISITADO')) color = Colors.green;
    else if (estado.contains('VERIFICADO')) color = Colors.blue;
    else if (estado.contains('CERRADO')) color = Colors.grey;
    else if (estado.contains('RECIBIDO')) color = Colors.purple;

    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 2),
      child: Row(
        children: [
          Container(
            width: 10,
            height: 10,
            decoration: BoxDecoration(
              color: color,
              shape: BoxShape.circle,
            ),
          ),
          const SizedBox(width: 8),
          Expanded(
            child: Text(
              estado,
              style: const TextStyle(fontSize: 12),
              overflow: TextOverflow.ellipsis,
            ),
          ),
          Text(
            '$total',
            style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 13),
          ),
        ],
      ),
    );
  }

  Widget _buildGeneroRow(String genero, int total) {
    Color color = Colors.blue;
    if (genero.contains('Femenino') || genero == 'FEMENINO') color = Colors.pink;
    else if (genero.contains('Masculino') || genero == 'MASCULINO') color = Colors.blue;
    else if (genero.contains('Biro') || genero == 'OTRO') color = Colors.purple;
    else color = Colors.grey;

    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 2),
      child: Row(
        children: [
          Container(
            width: 10,
            height: 10,
            decoration: BoxDecoration(
              color: color,
              shape: BoxShape.circle,
            ),
          ),
          const SizedBox(width: 8),
          Expanded(
            child: Text(
              genero,
              style: const TextStyle(fontSize: 12),
            ),
          ),
          Text(
            '$total',
            style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 13),
          ),
        ],
      ),
    );
  }

  Widget _buildTotalCard(int total) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        gradient: LinearGradient(
          colors: [Colors.red[700]!, Colors.red[500]!],
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
        ),
        borderRadius: BorderRadius.circular(12),
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          const Icon(Icons.assignment, color: Colors.white, size: 28),
          const SizedBox(width: 12),
          Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Text(
                'Total Solicitudes',
                style: TextStyle(color: Colors.white70, fontSize: 12),
              ),
              Text(
                '$total',
                style: const TextStyle(
                  color: Colors.white,
                  fontSize: 28,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }
}
