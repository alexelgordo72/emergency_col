import 'package:flutter/material.dart';
import 'package:pdf/pdf.dart';
import 'package:pdf/widgets.dart' as pw;
import 'package:printing/printing.dart';
import '../services/api_service.dart';
import '../models/reporte_comunitario.dart';

class PlanillaRutaDialog extends StatefulWidget {
  const PlanillaRutaDialog({Key? key}) : super(key: key);

  @override
  _PlanillaRutaDialogState createState() => _PlanillaRutaDialogState();
}

class _PlanillaRutaDialogState extends State<PlanillaRutaDialog> {
  late Future<Map<String, dynamic>> futureReportes;

  final List<String> ordenBarriosOficial = [
    'LAS VEGAS', 'MADRIGAL', 'BELLAVISTA', 'FRAY PEÑA', 'LLERAS',
    'PIZARRO', 'GUADALUPE', 'BOLIVAR', 'URIBE', 'BUENOS AIRES',
    'BELALCAZAR', 'CAMPESTRE REAL', 'DIONISIO', 'FINLANDIA',
    'ESTANCIA', 'AMERICAS', 'PANORAMA'
  ];

  @override
  void initState() {
    super.initState();
    futureReportes = ApiService.obtenerReportes();
  }

  Future<void> _generarYDescargarPDF(
    Map<String, List<ReporteComunitario>> agrupados,
    List<String> barriosPresentes
  ) async {
    final pdf = pw.Document();

    pdf.addPage(
      pw.MultiPage(
        pageFormat: PdfPageFormat.a4,
        margin: const pw.EdgeInsets.all(32),
        build: (pw.Context context) {
          List<pw.Widget> elementos = [
            pw.Header(
              level: 0,
              child: pw.Text(
                'SGRD YUMBO - PLANILLA DE RUTA DE VISITAS\nTotal general de registros en este reporte: ${agrupados.values.fold<int>(0, (p, c) => p + c.length)}',
                style: pw.TextStyle(fontSize: 18, fontWeight: pw.FontWeight.bold, color: PdfColors.red900),
              ),
            ),
          ];

          for (String barrio in barriosPresentes) {
            List<ReporteComunitario> lista = agrupados[barrio]!;
            int comuna = agrupados[barrio]?.first.comuna ?? 0;
            String prefijoId = 'COMUNA $comuna - ';

            elementos.add(
              pw.Container(
                margin: const pw.EdgeInsets.only(top: 20, bottom: 8),
                padding: const pw.EdgeInsets.all(6),
                color: comuna == 0 ? PdfColors.grey600 : PdfColors.blueGrey800,
                child: pw.Row(
                  mainAxisAlignment: pw.MainAxisAlignment.spaceBetween,
                  children: [
                    pw.Text('$prefijoId$barrio', style: pw.TextStyle(color: PdfColors.white, fontWeight: pw.FontWeight.bold, fontSize: 14)),
                    pw.Container(
                      padding: const pw.EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                      decoration: pw.BoxDecoration(
                        color: comuna == 0 ? PdfColors.orange : PdfColors.blue,
                        borderRadius: pw.BorderRadius.circular(8),
                      ),
                      child: pw.Text('${lista.length}', style: pw.TextStyle(color: PdfColors.white, fontWeight: pw.FontWeight.bold, fontSize: 12)),
                    ),
                  ],
                ),
              )
            );

            elementos.add(
              pw.TableHelper.fromTextArray(
                headers: ['Asunto/Novedad', 'Dirección / Referencia', 'Ciudadano Afectado', 'Teléfono', 'Estado'],
                headerStyle: pw.TextStyle(fontWeight: pw.FontWeight.bold, fontSize: 10),
                cellStyle: const pw.TextStyle(fontSize: 10),
                headerDecoration: const pw.BoxDecoration(color: PdfColors.grey300),
                cellAlignment: pw.Alignment.centerLeft,
                data: lista.map((r) {
                  String telefono = r.datosExtra?['telefono'] ?? 'N/A';
                  String afectado = r.datosExtra?['ciudadano'] ?? 'Anónimo';
                  if (telefono.isEmpty) telefono = 'N/A';
                  if (afectado.isEmpty) afectado = 'Anónimo';
                  return [r.titulo, r.direccion, afectado, telefono, r.estado];
                }).toList(),
              )
            );
          }
          return elementos;
        }
      )
    );

    await Printing.sharePdf(bytes: await pdf.save(), filename: 'Ruta_Visitas_SGRD_Yumbo.pdf');
  }

  @override
  Widget build(BuildContext context) {
    return Dialog(
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: Container(
        width: 1200,
        height: 800,
        padding: const EdgeInsets.all(24),
        child: FutureBuilder<Map<String, dynamic>>(
          future: futureReportes,
          builder: (context, snapshot) {
            if (snapshot.connectionState == ConnectionState.waiting) {
              return const Center(child: CircularProgressIndicator());
            }
            if (snapshot.hasError) return Center(child: Text('Error: ${snapshot.error}'));

            List<ReporteComunitario> reportes = [];
            if (snapshot.data != null && snapshot.data!['data'] != null) {
              reportes = (snapshot.data!['data'] as List)
                  .map((e) => ReporteComunitario.fromJson(e))
                  .toList();
            }

            var reportesPendientes = reportes.where((r) =>
              r.estado.toLowerCase().trim() == 'pendiente' || r.estado.toLowerCase().trim() == 'recibido'
            ).toList();

            Map<String, List<ReporteComunitario>> agrupados = {};
            for (var r in reportesPendientes) {
              String barrio = r.barrio.toUpperCase();
              if (!agrupados.containsKey(barrio)) agrupados[barrio] = [];
              agrupados[barrio]!.add(r);
            }

            List<String> barriosPresentes = agrupados.keys.toList();
            barriosPresentes.sort((a, b) {
              int indexA = ordenBarriosOficial.indexOf(a);
              int indexB = ordenBarriosOficial.indexOf(b);
              if (indexA == -1 && indexB == -1) return a.compareTo(b);
              if (indexA == -1) return 1;
              if (indexB == -1) return -1;
              return indexA.compareTo(indexB);
            });

            // Calcular totales por comuna
            Map<int, int> totalesComuna = {};
            for (var entry in agrupados.entries) {
              int comuna = entry.value.first.comuna ?? 0;
              totalesComuna[comuna] = (totalesComuna[comuna] ?? 0) + entry.value.length;
            }

            return Column(
              children: [
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Text(
                      'SGRD YUMBO - PLANILLA DE RUTA DE VISITAS\nTotal general de registros en este reporte: ${reportes.length}',
                      style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold, color: Colors.red[900]),
                    ),
                    Row(
                      children: [
                        ElevatedButton.icon(
                          style: ElevatedButton.styleFrom(
                            backgroundColor: Colors.red[800],
                            foregroundColor: Colors.white,
                          ),
                          icon: const Icon(Icons.picture_as_pdf),
                          label: const Text('Exportar PDF'),
                          onPressed: reportesPendientes.isEmpty
                              ? null
                              : () => _generarYDescargarPDF(agrupados, barriosPresentes),
                        ),
                        const SizedBox(width: 16),
                        IconButton(
                          icon: const Icon(Icons.close, size: 30),
                          onPressed: () => Navigator.pop(context),
                        ),
                      ],
                    )
                  ],
                ),
                const Divider(thickness: 2),
                Expanded(
                  child: reportesPendientes.isEmpty
                      ? const Center(child: Text('No hay visitas pendientes registradas.', style: TextStyle(fontSize: 18)))
                      : ListView.builder(
                          itemCount: barriosPresentes.length,
                          itemBuilder: (context, index) {
                            String barrio = barriosPresentes[index];
                            List<ReporteComunitario> lista = agrupados[barrio]!;
                            int comuna = agrupados[barrio]?.first.comuna ?? 0;
                            String prefijoId = 'COMUNA $comuna - ';

                            bool esPrimeroDeComuna = index == 0 ||
                                (agrupados[barriosPresentes[index - 1]]?.first.comuna ?? 0) != comuna;
                            int totalComuna = totalesComuna[comuna] ?? 0;

                            return Column(
                              children: [
                                if (esPrimeroDeComuna)
                                  Container(
                                    margin: const EdgeInsets.only(top: 16, bottom: 8),
                                    padding: const EdgeInsets.all(10),
                                    decoration: BoxDecoration(
                                      color: Colors.green[50],
                                      borderRadius: BorderRadius.circular(8),
                                      border: Border.all(color: Colors.green[300]!),
                                    ),
                                    child: Row(
                                      mainAxisAlignment: MainAxisAlignment.center,
                                      children: [
                                        Icon(Icons.assessment, color: Colors.green[800]),
                                        const SizedBox(width: 10),
                                        Text(
                                          '📊 TOTAL COMUNA $comuna: $totalComuna solicitudes',
                                          style: TextStyle(
                                            fontWeight: FontWeight.bold,
                                            fontSize: 16,
                                            color: Colors.green[800],
                                          ),
                                        ),
                                      ],
                                    ),
                                  ),
                                Card(
                                  margin: const EdgeInsets.symmetric(vertical: 8),
                                  elevation: 2,
                                  child: Column(
                                    crossAxisAlignment: CrossAxisAlignment.stretch,
                                    children: [
                                      Container(
                                        padding: const EdgeInsets.all(8),
                                        color: comuna == 0 ? Colors.grey[700] : Colors.blueGrey[800],
                                        child: Row(
                                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                                          children: [
                                            Row(
                                              children: [
                                                Icon(
                                                  comuna == 0 ? Icons.warning_amber : Icons.location_city,
                                                  color: comuna == 0 ? Colors.orange : Colors.white,
                                                  size: 18,
                                                ),
                                                const SizedBox(width: 8),
                                                Text(
                                                  '$prefijoId$barrio',
                                                  style: TextStyle(
                                                    color: Colors.white,
                                                    fontWeight: FontWeight.bold,
                                                    fontSize: 16,
                                                  ),
                                                ),
                                              ],
                                            ),
                                            Container(
                                              padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
                                              decoration: BoxDecoration(
                                                color: comuna == 0 ? Colors.orange : Colors.blue,
                                                borderRadius: BorderRadius.circular(12),
                                              ),
                                              child: Text(
                                                '${lista.length}',
                                                style: const TextStyle(
                                                  color: Colors.white,
                                                  fontWeight: FontWeight.bold,
                                                  fontSize: 14,
                                                ),
                                              ),
                                            ),
                                          ],
                                        ),
                                      ),
                                      SingleChildScrollView(
                                        scrollDirection: Axis.horizontal,
                                        child: DataTable(
                                          headingRowColor: MaterialStateProperty.resolveWith((states) => Colors.grey[200]),
                                          columnSpacing: 16,
                                          columns: const [
                                            DataColumn(label: Text('Asunto/Novedad', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 10))),
                                            DataColumn(label: Text('Dirección', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 10))),
                                            DataColumn(label: Text('Ciudadano', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 10))),
                                            DataColumn(label: Text('Teléfono', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 10))),
                                            DataColumn(label: Text('Estado', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 10))),
                                          ],
                                          rows: lista.map((r) {
                                            String telefono = r.datosExtra?['telefono'] ?? 'N/A';
                                            String afectado = r.datosExtra?['ciudadano'] ?? 'Anónimo';
                                            if (telefono.isEmpty) telefono = 'N/A';
                                            if (afectado.isEmpty) afectado = 'Anónimo';

                                            return DataRow(cells: [
                                              DataCell(Text(r.titulo, style: const TextStyle(fontSize: 9))),
                                              DataCell(Text(r.direccion, style: const TextStyle(fontSize: 9))),
                                              DataCell(Text(afectado, style: const TextStyle(fontSize: 9))),
                                              DataCell(Text(telefono, style: const TextStyle(fontSize: 9))),
                                              DataCell(
                                                Container(
                                                  padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                                                  decoration: BoxDecoration(
                                                    color: _getEstadoColor(r.estado),
                                                    borderRadius: BorderRadius.circular(8),
                                                  ),
                                                  child: Text(
                                                    r.estado,
                                                    style: const TextStyle(fontSize: 8, color: Colors.white, fontWeight: FontWeight.bold),
                                                  ),
                                                ),
                                              ),
                                            ]);
                                          }).toList(),
                                        ),
                                      ),
                                    ],
                                  ),
                                ),
                              ],
                            );
                          },
                        ),
                ),
                if (reportesPendientes.isNotEmpty)
                  Container(
                    margin: const EdgeInsets.only(top: 12),
                    padding: const EdgeInsets.all(12),
                    decoration: BoxDecoration(
                      color: Colors.blue[50],
                      borderRadius: BorderRadius.circular(8),
                      border: Border.all(color: Colors.blue[300]!),
                    ),
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.spaceAround,
                      children: [
                        ...totalesComuna.keys.map((comuna) {
                          int total = totalesComuna[comuna] ?? 0;
                          return Column(
                            children: [
                              Text(
                                'COMUNA $comuna',
                                style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 12),
                              ),
                              Container(
                                padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
                                decoration: BoxDecoration(
                                  color: comuna == 0 ? Colors.orange : Colors.blue,
                                  borderRadius: BorderRadius.circular(12),
                                ),
                                child: Text(
                                  '$total',
                                  style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold),
                                ),
                              ),
                            ],
                          );
                        }).toList(),
                        Container(
                          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                          decoration: BoxDecoration(
                            color: Colors.green[700],
                            borderRadius: BorderRadius.circular(12),
                          ),
                          child: Column(
                            children: [
                              const Text('TOTAL', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 12)),
                              Text(
                                '${reportesPendientes.length}',
                                style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 16),
                              ),
                            ],
                          ),
                        ),
                      ],
                    ),
                  ),
              ],
            );
          },
        ),
      ),
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
}
