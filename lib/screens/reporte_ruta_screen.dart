import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import '../services/reporte_ruta_service.dart';
import '../models/reporte_ruta.dart';

class ReporteRutaScreen extends StatefulWidget {
  const ReporteRutaScreen({super.key});

  @override
  State<ReporteRutaScreen> createState() => _ReporteRutaScreenState();
}

class _ReporteRutaScreenState extends State<ReporteRutaScreen> {
  late Future<List<ReporteRuta>> _reporteFuture;
  String _filtroComuna = 'TODAS';
  String _filtroPrioridad = 'TODAS';
  final List<String> _comunas = ['TODAS', '0', '1', '2', '3', '4'];
  final List<String> _prioridades = ['TODAS', 'ALTA', 'MEDIA', 'BAJA'];

  @override
  void initState() {
    super.initState();
    _cargarReporte();
  }

  void _cargarReporte() {
    setState(() {
      _reporteFuture = ReporteRutaService.generarReporteRuta(
        comuna: _filtroComuna,
        prioridad: _filtroPrioridad,
      );
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.grey[50],
      appBar: AppBar(
        title: const Text(
          '📋 Planilla de Ruta de Visitas',
          style: TextStyle(fontWeight: FontWeight.bold),
        ),
        backgroundColor: Colors.red[700],
        foregroundColor: Colors.white,
        elevation: 0,
        actions: [
          IconButton(
            icon: const Icon(Icons.picture_as_pdf),
            onPressed: () {
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(content: Text('Generando PDF...')),
              );
            },
            tooltip: 'Exportar a PDF',
          ),
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: _cargarReporte,
            tooltip: 'Recargar',
          ),
        ],
      ),
      body: Column(
        children: [
          _buildFiltros(),
          Expanded(
            child: FutureBuilder<List<ReporteRuta>>(
              future: _reporteFuture,
              builder: (context, snapshot) {
                if (snapshot.connectionState == ConnectionState.waiting) {
                  return const Center(child: CircularProgressIndicator());
                }

                if (snapshot.hasError || !snapshot.hasData || snapshot.data!.isEmpty) {
                  return Center(
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Icon(Icons.error_outline, size: 60, color: Colors.red[300]),
                        const SizedBox(height: 16),
                        const Text(
                          'No se pudo generar el reporte',
                          style: TextStyle(fontSize: 16),
                        ),
                        const SizedBox(height: 8),
                        Text(
                          snapshot.error?.toString() ?? 'Sin datos disponibles',
                          style: TextStyle(color: Colors.grey[600]),
                          textAlign: TextAlign.center,
                        ),
                        const SizedBox(height: 16),
                        ElevatedButton.icon(
                          onPressed: _cargarReporte,
                          icon: const Icon(Icons.refresh),
                          label: const Text('Reintentar'),
                        ),
                      ],
                    ),
                  );
                }

                final reportes = snapshot.data!;
                return _buildReporteContent(reportes);
              },
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildFiltros() {
    return Container(
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: Colors.white,
        boxShadow: [
          BoxShadow(
            color: Colors.grey.withOpacity(0.1),
            spreadRadius: 1,
            blurRadius: 4,
            offset: const Offset(0, 2),
          ),
        ],
      ),
      child: Row(
        children: [
          Expanded(
            child: DropdownButtonFormField<String>(
              value: _filtroComuna,
              decoration: const InputDecoration(
                labelText: 'Comuna',
                border: OutlineInputBorder(),
                isDense: true,
                contentPadding: EdgeInsets.symmetric(horizontal: 12, vertical: 8),
              ),
              items: _comunas.map((c) {
                return DropdownMenuItem(
                  value: c,
                  child: Text(c == 'TODAS' ? 'Todas' : 'Comuna $c'),
                );
              }).toList(),
              onChanged: (value) {
                setState(() {
                  _filtroComuna = value!;
                });
                _cargarReporte();
              },
            ),
          ),
          const SizedBox(width: 12),
          Expanded(
            child: DropdownButtonFormField<String>(
              value: _filtroPrioridad,
              decoration: const InputDecoration(
                labelText: 'Prioridad',
                border: OutlineInputBorder(),
                isDense: true,
                contentPadding: EdgeInsets.symmetric(horizontal: 12, vertical: 8),
              ),
              items: _prioridades.map((p) {
                return DropdownMenuItem(
                  value: p,
                  child: Text(p == 'TODAS' ? 'Todas' : p),
                );
              }).toList(),
              onChanged: (value) {
                setState(() {
                  _filtroPrioridad = value!;
                });
                _cargarReporte();
              },
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildReporteContent(List<ReporteRuta> reportes) {
    final Map<String, List<ReporteRuta>> agrupado = {};
    for (var r in reportes) {
      agrupado.putIfAbsent(r.comuna, () => []).add(r);
    }

    final fechaFormateada = DateFormat('yyyy-MM-dd').format(DateTime.now());
    int totalGeneral = 0;
    for (var r in reportes) {
      totalGeneral += r.totalVisitas;
    }

    return ListView(
      padding: const EdgeInsets.all(16),
      children: [
        Container(
          padding: const EdgeInsets.all(16),
          decoration: BoxDecoration(
            color: Colors.white,
            borderRadius: BorderRadius.circular(12),
            boxShadow: [
              BoxShadow(
                color: Colors.grey.withOpacity(0.1),
                spreadRadius: 1,
                blurRadius: 4,
                offset: const Offset(0, 2),
              ),
            ],
          ),
          child: Column(
            children: [
              const Text(
                'SGRD YUMBO - PLANILLA DE RUTA DE VISITAS',
                style: TextStyle(
                  fontSize: 18,
                  fontWeight: FontWeight.bold,
                  color: Colors.red,
                ),
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: 4),
              const Text(
                'Sistema de Gestión de Riesgo de Desastres - Reportes Georreferenciados',
                style: TextStyle(fontSize: 12, color: Colors.grey),
                textAlign: TextAlign.center,
              ),
              const Divider(),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Text(
                    'Total de visitas pendientes: $totalGeneral',
                    style: const TextStyle(fontWeight: FontWeight.bold),
                  ),
                  Text('Fecha: $fechaFormateada'),
                ],
              ),
            ],
          ),
        ),
        const SizedBox(height: 16),
        ...agrupado.entries.map((entry) {
          final comuna = entry.key;
          final barrios = entry.value;
          return Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const SizedBox(height: 12),
              ...barrios.map((barrio) {
                return _buildBarrioCard(barrio);
              }),
            ],
          );
        }),
      ],
    );
  }

  Widget _buildBarrioCard(ReporteRuta barrio) {
    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: Padding(
        padding: const EdgeInsets.all(12),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(
                  'Comuna ${barrio.comuna} - Barrio ${barrio.barrio.toUpperCase()}',
                  style: const TextStyle(
                    fontWeight: FontWeight.bold,
                    fontSize: 16,
                  ),
                ),
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
                  decoration: BoxDecoration(
                    color: Colors.blue[50],
                    borderRadius: BorderRadius.circular(12),
                  ),
                  child: Text(
                    'Total Visitas: ${barrio.totalVisitas}',
                    style: TextStyle(
                      color: Colors.blue[800],
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ),
              ],
            ),
            const Divider(),
            if (barrio.visitas.isNotEmpty) ...[
              Container(
                decoration: BoxDecoration(
                  border: Border.all(color: Colors.grey[300]!),
                  borderRadius: BorderRadius.circular(8),
                ),
                child: Column(
                  children: [
                    Container(
                      padding: const EdgeInsets.all(8),
                      decoration: BoxDecoration(
                        color: Colors.grey[100],
                        borderRadius: const BorderRadius.vertical(top: Radius.circular(8)),
                      ),
                      child: const Row(
                        children: [
                          SizedBox(width: 30, child: Text('#', style: TextStyle(fontWeight: FontWeight.bold))),
                          Expanded(flex: 2, child: Text('Asunto / Novedad', style: TextStyle(fontWeight: FontWeight.bold))),
                          Expanded(flex: 2, child: Text('Dirección / Referencia', style: TextStyle(fontWeight: FontWeight.bold))),
                          Expanded(flex: 2, child: Text('Ciudadano Afectado', style: TextStyle(fontWeight: FontWeight.bold))),
                          Expanded(flex: 1, child: Text('Teléfono', style: TextStyle(fontWeight: FontWeight.bold))),
                        ],
                      ),
                    ),
                    ...barrio.visitas.map((visita) {
                      return Container(
                        padding: const EdgeInsets.all(8),
                        decoration: BoxDecoration(
                          border: Border(
                            bottom: BorderSide(color: Colors.grey[200]!),
                          ),
                        ),
                        child: Row(
                          children: [
                            SizedBox(width: 30, child: Text(visita.numero)),
                            Expanded(flex: 2, child: Text(visita.asunto, style: const TextStyle(fontSize: 12))),
                            Expanded(flex: 2, child: Text(visita.direccion, style: const TextStyle(fontSize: 12))),
                            Expanded(flex: 2, child: Text(visita.ciudadano, style: const TextStyle(fontSize: 12))),
                            Expanded(flex: 1, child: Text(visita.telefono, style: const TextStyle(fontSize: 12))),
                          ],
                        ),
                      );
                    }),
                  ],
                ),
              ),
              const SizedBox(height: 8),
            ],
            const Text(
              'OBSERVACIONES',
              style: TextStyle(fontWeight: FontWeight.bold, fontSize: 14),
            ),
            const SizedBox(height: 4),
            ...List.generate(barrio.totalVisitas, (index) {
              return Padding(
                padding: const EdgeInsets.symmetric(vertical: 2),
                child: Text(
                  'Visita ${index + 1}: ${barrio.observaciones.length > index ? barrio.observaciones[index] : ''}'
                ),
              );
            }),
            const SizedBox(height: 8),
            if (barrio.totalVisitas > 0) ...[
              Text(
                'Total de visitas pendientes: ${barrio.totalVisitas}',
                style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 12),
              ),
            ],
          ],
        ),
      ),
    );
  }
}
