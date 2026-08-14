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
  late Future<List<ReporteComunitario>> futureReportes;

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

  // Calcular total por comuna
  int calcularTotalComuna(Map<String, List<ReporteComunitario>> agrupados, int comuna) {
    int total = 0;
    for (var entry in agrupados.entries) {
      if ((entry.value.first.comuna ?? 0) == comuna) {
        total += entry.value.length;
      }
    }
    return total;
  }

  // Obtener todas las comunas presentes en el reporte
  List<int> obtenerComunasPresentes(Map<String, List<ReporteComunitario>> agrupados) {
    Set<int> comunas = {};
    for (var entry in agrupados.entries) {
      comunas.add(entry.value.first.comuna ?? 0);
    }
    return comunas.toList()..sort();
  }

  Future<void> _generarYDescargarPDF(Map<String, List<ReporteComunitario>> agrupados, List<String> barriosPresentes) async {
    final pdf = pw.Document();

    pdf.addPage(
      pw.MultiPage(
        pageFormat: PdfPageFormat.a4,
        margin: const pw.EdgeInsets.all(32),
        build: (pw.Context context) {
          List<pw.Widget> elementos = [
            pw.Header(
              level: 0,
              child: pw.Text('SGRD YUMBO - PLANILLA DE RUTA DE VISITAS\nTotal general de registros en este reporte: ${agrupados.values.fold<int>(0, (p, c) => p + c.length)}', style: pw.TextStyle(fontSize: 18, fontWeight: pw.FontWeight.bold, color: PdfColors.red900)),
            ),
          ];

          // Agrupar por comuna para mostrar totales
          Map<int, List<String>> barriosPorComuna = {};
          for (String barrio in barriosPresentes) {
            int comuna = agrupados[barrio]?.first.comuna ?? 0;
            if (!barriosPorComuna.containsKey(comuna)) {
              barriosPorComuna[comuna] = [];
            }
            barriosPorComuna[comuna]!.add(barrio);
          }

          // Recorrer comunas en orden
          List<int> comunasOrdenadas = barriosPorComuna.keys.toList()..sort();
          
          for (int comuna in comunasOrdenadas) {
            int totalComuna = 0;
            for (String barrio in barriosPorComuna[comuna]!) {
              totalComuna += agrupados[barrio]!.length;
            }

            // Título de comuna con total
            elementos.add(
              pw.Container(
                margin: const pw.EdgeInsets.only(top: 16, bottom: 8),
                padding: const pw.EdgeInsets.all(8),
                color: PdfColors.green100,
                child: pw.Text(
                  '📊 TOTAL COMUNA $comuna: $totalComuna solicitudes',
                  style: pw.TextStyle(fontWeight: pw.FontWeight.bold, fontSize: 14, color: PdfColors.green800),
                ),
              )
            );

            // Barrios de esta comuna
            for (String barrio in barriosPorComuna[comuna]!) {
              List<ReporteComunitario> lista = agrupados[barrio]!;
              String prefijoId = 'COMUNA $comuna - ';

              elementos.add(
                pw.Container(
                  margin: const pw.EdgeInsets.only(top: 12, bottom: 8),
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
        child: FutureBuilder<List<ReporteComunitario>>(
          future: futureReportes,
          builder: (context, snapshot) {
            if (snapshot.connectionState == ConnectionState.waiting) {
              return const Center(child: CircularProgressIndicator());
            }
            if (snapshot.hasError) return Center(child: Text('Error: ${snapshot.error}'));

            var reportesPendientes = (snapshot.data ?? []).where((r) => 
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
              int comunaA = agrupados[a]?.first.comuna ?? 0;
              int comunaB = agrupados[b]?.first.comuna ?? 0;
              if (comunaA != comunaB) return comunaA.compareTo(comunaB);
              return a.compareTo(b);
            });

            // Obtener comunas presentes
            List<int> comunasPresentes = obtenerComunasPresentes(agrupados);

            return Column(
              children: [
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Text('SGRD YUMBO - PLANILLA DE RUTA DE VISITAS\nTotal general de registros en este reporte: ${snapshot.data?.length ?? 0}',
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
                          onPressed: reportesPendientes.isEmpty ? null : () => _generarYDescargarPDF(agrupados, barriosPresentes),
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

                          // Verificar si es el primer barrio de esta comuna
                          bool esPrimeroDeComuna = index == 0 || (agrupados[barriosPresentes[index-1]]?.first.comuna ?? 0) != comuna;
                          int totalComuna = calcularTotalComuna(agrupados, comuna);

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
                                        columnSpacing: 20,
                                        columns: const [
                                          DataColumn(label: Text('Asunto/Novedad', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 11))),
                                          DataColumn(label: Text('Dirección / Referencia', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 11))),
                                          DataColumn(label: Text('Ciudadano Afectado', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 11))),
                                          DataColumn(label: Text('Teléfono', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 11))),
                                          DataColumn(label: Text('Estado', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 11))),
                                        ],
                                        rows: lista.map((r) {
                                          String telefono = r.datosExtra?['telefono'] ?? 'N/A';
                                          String afectado = r.datosExtra?['ciudadano'] ?? 'Anónimo';
                                          if (telefono.isEmpty) telefono = 'N/A';
                                          if (afectado.isEmpty) afectado = 'Anónimo';

                                          return DataRow(cells: [
                                            DataCell(Text(r.titulo, style: const TextStyle(fontSize: 10))),
                                            DataCell(Text(r.direccion, style: const TextStyle(fontSize: 10))),
                                            DataCell(Text(afectado, style: const TextStyle(fontSize: 10))),
                                            DataCell(Text(telefono, style: const TextStyle(fontSize: 10))),
                                            DataCell(
                                              Row(
                                                mainAxisSize: MainAxisSize.min,
                                                children: [
                                                  const Icon(Icons.square, color: Colors.black, size: 10),
                                                  const SizedBox(width: 4),
                                                  Text(r.estado, style: const TextStyle(fontSize: 10, fontWeight: FontWeight.bold)),
                                                ],
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
                // Resumen final
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
                        ...comunasPresentes.map((comuna) {
                          int total = calcularTotalComuna(agrupados, comuna);
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
                                '${snapshot.data?.length ?? 0}',
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
}
