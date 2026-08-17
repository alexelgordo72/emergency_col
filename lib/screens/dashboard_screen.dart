import 'package:flutter/material.dart';
import 'package:fl_chart/fl_chart.dart';
import '../services/api_service.dart';
import '../models/reporte_comunitario.dart';

class DashboardScreen extends StatefulWidget {
  const DashboardScreen({Key? key}) : super(key: key);

  @override
  _DashboardScreenState createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen> {
  List<ReporteComunitario> reportes = [];
  bool cargando = true;
  String? error;

  // Filtros
  String? comunaSeleccionada;
  String? barrioSeleccionado;
  String zonaSeleccionada = 'Todos';

  // Datos procesados
  int totalReportes = 0;
  int pendientes = 0;
  int visitados = 0;
  Map<String, int> prioridades = {};
  Map<String, int> generos = {};
  Map<String, int> animales = {};
  Map<String, int> reportesPorComuna = {};

  List<String> comunas = ['Todas'];
  List<String> barrios = ['Todos'];

  @override
  void initState() {
    super.initState();
    _cargarDatos();
  }

  Future<void> _cargarDatos() async {
    setState(() {
      cargando = true;
      error = null;
    });

    try {
      final result = await ApiService.obtenerReportes(limit: 10000);
      reportes = result['data'] ?? [];
      _procesarDatos();
      setState(() {
        cargando = false;
      });
    } catch (e) {
      setState(() {
        error = e.toString();
        cargando = false;
      });
    }
  }

  void _procesarDatos() {
    var filtered = reportes.where((r) {
      if (zonaSeleccionada == 'Urbana') {
        return r.comuna != null && r.comuna! > 0;
      } else if (zonaSeleccionada == 'Rural') {
        return r.comuna == null || r.comuna == 0;
      }
      return true;
    }).toList();

    if (comunaSeleccionada != null && comunaSeleccionada != 'Todas') {
      int comuna = int.parse(comunaSeleccionada!);
      filtered = filtered.where((r) => r.comuna == comuna).toList();
    }

    if (barrioSeleccionado != null && barrioSeleccionado != 'Todos') {
      filtered = filtered.where((r) => r.barrio == barrioSeleccionado).toList();
    }

    totalReportes = filtered.length;
    pendientes = filtered.where((r) =>
      r.estado.toLowerCase() == 'pendiente' || r.estado.toLowerCase() == 'recibido'
    ).length;
    visitados = filtered.where((r) =>
      r.estado.toLowerCase().contains('visitado')
    ).length;

    prioridades = {};
    for (var r in filtered.where((r) => r.estado.toLowerCase().contains('visitado'))) {
      String prioridad = r.estado.replaceAll('Visitado-DE-Prioridad ', '');
      prioridades[prioridad] = (prioridades[prioridad] ?? 0) + 1;
    }

    generos = {'Hombre': 0, 'Mujer': 0, 'Niño': 0, 'Niña': 0, 'Otro': 0};
    for (var r in filtered) {
      String nombre = r.datosExtra?['ciudadano'] ?? '';
      if (nombre.toLowerCase().contains('maria') || nombre.toLowerCase().contains('rosa') ||
          nombre.toLowerCase().contains('josefa') || nombre.toLowerCase().contains('ana') ||
          nombre.toLowerCase().contains('luisa') || nombre.toLowerCase().contains('fernanda')) {
        generos['Mujer'] = (generos['Mujer'] ?? 0) + 1;
      } else if (nombre.toLowerCase().contains('jose') || nombre.toLowerCase().contains('juan') ||
                 nombre.toLowerCase().contains('carlos') || nombre.toLowerCase().contains('luis') ||
                 nombre.toLowerCase().contains('pedro') || nombre.toLowerCase().contains('andres')) {
        generos['Hombre'] = (generos['Hombre'] ?? 0) + 1;
      } else if (nombre.toLowerCase().contains('niño') || nombre.toLowerCase().contains('menor')) {
        generos['Niño'] = (generos['Niño'] ?? 0) + 1;
      } else if (nombre.toLowerCase().contains('niña')) {
        generos['Niña'] = (generos['Niña'] ?? 0) + 1;
      } else {
        generos['Otro'] = (generos['Otro'] ?? 0) + 1;
      }
    }

    animales = {'Perros': 0, 'Gatos': 0, 'Gallinas': 0, 'Otros': 0};
    for (var r in filtered) {
      String obs = r.datosExtra?['animales']?.toString() ?? '';
      if (obs.toLowerCase().contains('perro')) {
        animales['Perros'] = (animales['Perros'] ?? 0) + 1;
      }
      if (obs.toLowerCase().contains('gato')) {
        animales['Gatos'] = (animales['Gatos'] ?? 0) + 1;
      }
      if (obs.toLowerCase().contains('gallina')) {
        animales['Gallinas'] = (animales['Gallinas'] ?? 0) + 1;
      }
      if (!obs.toLowerCase().contains('perro') && !obs.toLowerCase().contains('gato') &&
          !obs.toLowerCase().contains('gallina') && obs.isNotEmpty) {
        animales['Otros'] = (animales['Otros'] ?? 0) + 1;
      }
    }

    reportesPorComuna = {};
    for (var r in filtered) {
      int c = r.comuna ?? 0;
      String key = 'Comuna $c';
      reportesPorComuna[key] = (reportesPorComuna[key] ?? 0) + 1;
    }

    comunas = ['Todas'];
    for (var r in filtered) {
      if (r.comuna != null) {
        String c = r.comuna.toString();
        if (!comunas.contains(c)) comunas.add(c);
      }
    }
    comunas.sort();

    barrios = ['Todos'];
    for (var r in filtered) {
      if (!barrios.contains(r.barrio) && r.barrio.isNotEmpty) {
        barrios.add(r.barrio);
      }
    }
    barrios.sort();
  }

  Color _getPrioridadColor(String prioridad) {
    switch (prioridad.toLowerCase()) {
      case 'alta': return Colors.red;
      case 'media': return Colors.orange;
      case 'baja': return Colors.green;
      default: return Colors.grey;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.grey[100],
      appBar: AppBar(
        title: const Text('📊 Dashboard SGRD Yumbo'),
        backgroundColor: Colors.red[800],
        foregroundColor: Colors.white,
        elevation: 0,
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: _cargarDatos,
          ),
          IconButton(
            icon: const Icon(Icons.close),
            onPressed: () => Navigator.pop(context),
          ),
        ],
      ),
      body: cargando
          ? const Center(child: CircularProgressIndicator())
          : error != null
              ? Center(child: Text('Error: $error'))
              : SingleChildScrollView(
                  padding: const EdgeInsets.all(16),
                  child: Column(
                    children: [
                      _buildFiltros(),
                      const SizedBox(height: 16),
                      _buildMetricas(),
                      const SizedBox(height: 16),
                      _buildGraficos(),
                    ],
                  ),
                ),
    );
  }

  Widget _buildFiltros() {
    return Container(
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(12),
        boxShadow: [
          BoxShadow(color: Colors.grey.withOpacity(0.1), blurRadius: 8),
        ],
      ),
      child: Wrap(
        spacing: 12,
        runSpacing: 8,
        alignment: WrapAlignment.center,
        children: [
          _buildFiltroComuna(),
          _buildFiltroBarrio(),
          _buildFiltroZona(),
        ],
      ),
    );
  }

  Widget _buildFiltroComuna() {
    return DropdownButton<String>(
      value: comunaSeleccionada ?? 'Todas',
      hint: const Text('Comuna'),
      items: comunas.map((c) {
        return DropdownMenuItem(value: c, child: Text(c));
      }).toList(),
      onChanged: (val) {
        setState(() {
          comunaSeleccionada = val;
          _procesarDatos();
        });
      },
    );
  }

  Widget _buildFiltroBarrio() {
    return DropdownButton<String>(
      value: barrioSeleccionado ?? 'Todos',
      hint: const Text('Barrio'),
      items: barrios.map((b) {
        return DropdownMenuItem(value: b, child: Text(b));
      }).toList(),
      onChanged: (val) {
        setState(() {
          barrioSeleccionado = val;
          _procesarDatos();
        });
      },
    );
  }

  Widget _buildFiltroZona() {
    return DropdownButton<String>(
      value: zonaSeleccionada,
      items: const [
        DropdownMenuItem(value: 'Todos', child: Text('🌍 Todos')),
        DropdownMenuItem(value: 'Urbana', child: Text('🏙️ Urbana')),
        DropdownMenuItem(value: 'Rural', child: Text('🌾 Rural')),
      ],
      onChanged: (val) {
        setState(() {
          zonaSeleccionada = val!;
          comunaSeleccionada = 'Todas';
          barrioSeleccionado = 'Todos';
          _procesarDatos();
        });
      },
    );
  }

  Widget _buildMetricas() {
    return Row(
      children: [
        Expanded(
          child: _buildMetricaCard(
            '📋 Total',
            totalReportes.toString(),
            Colors.blue,
            Icons.list_alt,
          ),
        ),
        const SizedBox(width: 12),
        Expanded(
          child: _buildMetricaCard(
            '⏳ Pendientes',
            pendientes.toString(),
            Colors.orange,
            Icons.pending,
          ),
        ),
        const SizedBox(width: 12),
        Expanded(
          child: _buildMetricaCard(
            '✅ Visitados',
            visitados.toString(),
            Colors.green,
            Icons.verified,
          ),
        ),
      ],
    );
  }

  Widget _buildMetricaCard(String titulo, String valor, Color color, IconData icon) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(12),
        boxShadow: [
          BoxShadow(color: Colors.grey.withOpacity(0.1), blurRadius: 4),
        ],
      ),
      child: Column(
        children: [
          Icon(icon, color: color, size: 28),
          const SizedBox(height: 8),
          Text(
            valor,
            style: TextStyle(fontSize: 28, fontWeight: FontWeight.bold, color: color),
          ),
          Text(
            titulo,
            style: const TextStyle(fontSize: 12, color: Colors.grey),
          ),
        ],
      ),
    );
  }

  Widget _buildGraficos() {
    return Column(
      children: [
        _buildCard('🎯 Prioridades de Visitados', _buildPrioridadesChart()),
        const SizedBox(height: 16),
        _buildCard('👥 Caracterización por Género', _buildGenerosChart()),
        const SizedBox(height: 16),
        _buildCard('🐾 Animales Reportados', _buildAnimalesChart()),
        const SizedBox(height: 16),
        _buildCard('📊 Reportes por Comuna', _buildComunasChart()),
      ],
    );
  }

  Widget _buildCard(String titulo, Widget child) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(12),
        boxShadow: [
          BoxShadow(color: Colors.grey.withOpacity(0.1), blurRadius: 4),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            titulo,
            style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: 12),
          SizedBox(height: 180, child: child),
        ],
      ),
    );
  }

  Widget _buildPrioridadesChart() {
    if (prioridades.isEmpty) {
      return const Center(child: Text('No hay datos de prioridades'));
    }
    return PieChart(
      PieChartData(
        sections: prioridades.entries.map((e) {
          return PieChartSectionData(
            value: e.value.toDouble(),
            title: '${e.key}\n${e.value}',
            color: _getPrioridadColor(e.key),
            radius: 50,
            titleStyle: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 12),
          );
        }).toList(),
        sectionsSpace: 4,
        centerSpaceRadius: 20,
      ),
    );
  }

  Widget _buildGenerosChart() {
    if (generos.values.every((v) => v == 0)) {
      return const Center(child: Text('No hay datos de género'));
    }
    return PieChart(
      PieChartData(
        sections: generos.entries.map((e) {
          return PieChartSectionData(
            value: e.value.toDouble(),
            title: '${e.key}\n${e.value}',
            color: [
              Colors.blue,
              Colors.pink,
              Colors.lightBlue,
              Colors.purple,
              Colors.grey,
            ][generos.keys.toList().indexOf(e.key)],
            radius: 50,
            titleStyle: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 12),
          );
        }).toList(),
        sectionsSpace: 4,
        centerSpaceRadius: 20,
      ),
    );
  }

  Widget _buildAnimalesChart() {
    if (animales.values.every((v) => v == 0)) {
      return const Center(child: Text('No hay datos de animales'));
    }
    return BarChart(
      BarChartData(
        alignment: BarChartAlignment.spaceAround,
        barGroups: animales.entries.map((e) {
          return BarChartGroupData(
            x: animales.keys.toList().indexOf(e.key),
            barRods: [
              BarChartRodData(
                toY: e.value.toDouble(),
                color: Colors.brown,
                width: 30,
                borderRadius: BorderRadius.circular(4),
                backDrawRodData: BackgroundBarChartRodData(
                  show: true,
                  toY: 5,
                  color: Colors.grey[200],
                ),
              ),
            ],
          );
        }).toList(),
        titlesData: FlTitlesData(
          bottomTitles: AxisTitles(
            sideTitles: SideTitles(
              showTitles: true,
              getTitlesWidget: (value, meta) {
                return Text(
                  animales.keys.toList()[value.toInt()],
                  style: const TextStyle(fontSize: 10, fontWeight: FontWeight.bold),
                );
              },
            ),
          ),
        ),
        gridData: const FlGridData(show: false),
        borderData: FlBorderData(show: false),
      ),
    );
  }

  Widget _buildComunasChart() {
    if (reportesPorComuna.isEmpty) {
      return const Center(child: Text('No hay datos por comuna'));
    }
    return BarChart(
      BarChartData(
        alignment: BarChartAlignment.spaceAround,
        barGroups: reportesPorComuna.entries.map((e) {
          return BarChartGroupData(
            x: reportesPorComuna.keys.toList().indexOf(e.key),
            barRods: [
              BarChartRodData(
                toY: e.value.toDouble(),
                color: Colors.blue,
                width: 30,
                borderRadius: BorderRadius.circular(4),
                backDrawRodData: BackgroundBarChartRodData(
                  show: true,
                  toY: 10,
                  color: Colors.grey[200],
                ),
              ),
            ],
          );
        }).toList(),
        titlesData: FlTitlesData(
          bottomTitles: AxisTitles(
            sideTitles: SideTitles(
              showTitles: true,
              getTitlesWidget: (value, meta) {
                return Text(
                  reportesPorComuna.keys.toList()[value.toInt()],
                  style: const TextStyle(fontSize: 10, fontWeight: FontWeight.bold),
                );
              },
            ),
          ),
        ),
        gridData: const FlGridData(show: false),
        borderData: FlBorderData(show: false),
      ),
    );
  }
}
