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
    final comunas = data['comunas'] as List<dynamic>? ?? [];
    final barrios = data['barrios'] as List<dynamic>? ?? [];

    return SingleChildScrollView(
      padding: const EdgeInsets.all(12),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // ZONA
          _buildSeccion('📍 Zona',
            Wrap(
              spacing: 4,
              runSpacing: 4,
              children: [
                _buildChipFilter('All', true),
                ...comunas.map((c) => _buildChipFilter('Comuna ${c['comuna']}', false)),
                ...barrios.take(5).map((b) => _buildChipFilter(b['barrio'], false)),
              ],
            ),
          ),

          const SizedBox(height: 12),

          // ANIMALES SINTIENTES
          _buildSeccion('🐾 Animales Sintientes',
            Wrap(
              spacing: 8,
              runSpacing: 8,
              children: [
                _buildAnimalCard('🐔 Aves', animales['aves'] ?? 0, Colors.green),
                _buildAnimalCard('🐱 Gatos', animales['gatos'] ?? 0, Colors.orange),
                _buildAnimalCard('🐶 Perros', animales['perros'] ?? 0, Colors.blue),
              ],
            ),
          ),

          const SizedBox(height: 12),

          // SOLICITUDES RECIBIDAS
          _buildSeccion('📋 Solicitudes Recibidas',
            Column(
              children: estados.map((e) => _buildEstadoRow(e['estado'], e['total'])).toList(),
            ),
          ),

          const SizedBox(height: 12),

          // DISTRIBUCIÓN POR GÉNERO
          _buildSeccion('👤 Distribución por Género',
            Column(
              children: generos.map((g) => _buildGeneroRow(g['genero'], g['total'])).toList(),
            ),
          ),

          const SizedBox(height: 12),

          // TOTAL
          _buildTotalCard(total),

          const SizedBox(height: 12),

          // GRÁFICO
          _buildSeccion('📈 Cantidad de Solicitudes',
            _buildBarChart(estados.take(10).toList()),
          ),
        ],
      ),
    );
  }

  Widget _buildSeccion(String titulo, Widget child) {
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
              style: const TextStyle(fontSize: 15, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 8),
            child,
          ],
        ),
      ),
    );
  }

  Widget _buildChipFilter(String label, bool selected) {
    return Chip(
      label: Text(
        label,
        style: TextStyle(
          fontSize: 11,
          color: selected ? Colors.white : Colors.black87,
        ),
      ),
      backgroundColor: selected ? Colors.red[700] : Colors.grey[200],
      padding: EdgeInsets.zero,
      materialTapTargetSize: MaterialTapTargetSize.shrinkWrap,
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

  Widget _buildBarChart(List<dynamic> items) {
    if (items.isEmpty) {
      return const Center(child: Text('Sin datos para gráfico'));
    }

    final maxValue = items.fold(0, (max, e) => e['total'] > max ? e['total'] : max);

    return Column(
      children: items.map((item) {
        final double percent = maxValue > 0 ? (item['total'] / maxValue) : 0;
        final String estado = item['estado'] ?? 'Sin estado';
        final int total = item['total'] ?? 0;

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
              SizedBox(
                width: 80,
                child: Text(
                  _truncate(estado, 12),
                  style: const TextStyle(fontSize: 9),
                  overflow: TextOverflow.ellipsis,
                ),
              ),
              const SizedBox(width: 4),
              Expanded(
                child: Container(
                  height: 14,
                  decoration: BoxDecoration(
                    color: Colors.grey[200],
                    borderRadius: BorderRadius.circular(6),
                  ),
                  child: FractionallySizedBox(
                    widthFactor: percent.clamp(0.0, 1.0),
                    child: Container(
                      decoration: BoxDecoration(
                        color: color,
                        borderRadius: BorderRadius.circular(6),
                      ),
                    ),
                  ),
                ),
              ),
              const SizedBox(width: 4),
              SizedBox(
                width: 30,
                child: Text(
                  '$total',
                  style: const TextStyle(fontSize: 9, fontWeight: FontWeight.bold),
                  textAlign: TextAlign.right,
                ),
              ),
            ],
          ),
        );
      }).toList(),
    );
  }

  String _truncate(String text, int maxLength) {
    if (text.length <= maxLength) return text;
    return '${text.substring(0, maxLength)}...';
  }
}
