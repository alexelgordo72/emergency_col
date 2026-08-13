import 'package:flutter/material.dart';
import '../services/api_service.dart';
import '../models/reporte_comunitario.dart';

class DashboardAlcaldia extends StatefulWidget {
  const DashboardAlcaldia({Key? key}) : super(key: key);
  @override
  _DashboardAlcaldiaState createState() => _DashboardAlcaldiaState();
}

class _DashboardAlcaldiaState extends State<DashboardAlcaldia> {
  late Future<List<ReporteComunitario>> futureReportes;

  @override
  void initState() {
    super.initState();
    futureReportes = ApiService.obtenerReportes();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Gráficas de Impacto - Alcaldía'),
        backgroundColor: Colors.red[900],
        foregroundColor: Colors.white,
      ),
      body: FutureBuilder<List<ReporteComunitario>>(
        future: futureReportes,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) return const Center(child: CircularProgressIndicator());
          if (snapshot.hasError) return Center(child: Text('Error: ${snapshot.error}'));

          var reportes = snapshot.data ?? [];
          Map<String, int> conteo = {};
          int maxEventos = 0;
          
          for (var r in reportes) {
            String barrio = r.barrio.toUpperCase();
            conteo[barrio] = (conteo[barrio] ?? 0) + 1;
            if (conteo[barrio]! > maxEventos) maxEventos = conteo[barrio]!;
          }

          var ordenados = conteo.entries.toList()..sort((a, b) => b.value.compareTo(a.value));

          return Padding(
            padding: const EdgeInsets.all(32.0),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text('Total de Reportes: ${reportes.length}', style: TextStyle(fontSize: 28, fontWeight: FontWeight.bold, color: Colors.blueGrey[800])),
                const SizedBox(height: 30),
                Expanded(
                  child: ListView.builder(
                    itemCount: ordenados.length,
                    itemBuilder: (context, index) {
                      var item = ordenados[index];
                      double porcentaje = maxEventos == 0 ? 0 : item.value / maxEventos;
                      return Padding(
                        padding: const EdgeInsets.symmetric(vertical: 12.0),
                        child: Row(
                          children: [
                            SizedBox(width: 180, child: Text(item.key, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16))),
                            Expanded(
                              child: Stack(
                                children: [
                                  Container(height: 35, decoration: BoxDecoration(color: Colors.grey[200], borderRadius: BorderRadius.circular(8))),
                                  FractionallySizedBox(
                                    widthFactor: porcentaje,
                                    child: Container(
                                      height: 35,
                                      decoration: BoxDecoration(
                                        color: Colors.red[800],
                                        borderRadius: BorderRadius.circular(8),
                                      ),
                                    ),
                                  ),
                                ],
                              ),
                            ),
                            const SizedBox(width: 16),
                            SizedBox(width: 50, child: Text('${item.value}', style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 18, color: Colors.black87))),
                          ],
                        ),
                      );
                    },
                  ),
                ),
              ],
            ),
          );
        },
      ),
    );
  }
}
