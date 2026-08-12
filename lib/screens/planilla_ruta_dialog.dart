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
              child: pw.Text('SGRD YUMBO - PLANILLA DE RUTA DE VISITAS', style: pw.TextStyle(fontSize: 18, fontWeight: pw.FontWeight.bold, color: PdfColors.red900)),
            ),
          ];

          for (String barrio in barriosPresentes) {
            List<ReporteComunitario> lista = agrupados[barrio]!;
            int idBarrio = ordenBarriosOficial.indexOf(barrio) + 1;
            String prefijoId = idBarrio > 0 ? 'ID $idBarrio - ' : 'OTRO - ';

            elementos.add(
              pw.Container(
                margin: const pw.EdgeInsets.only(top: 20, bottom: 8),
                padding: const pw.EdgeInsets.all(6),
                color: PdfColors.blueGrey800,
                child: pw.Text('$prefijoId$barrio', style: pw.TextStyle(color: PdfColors.white, fontWeight: pw.FontWeight.bold, fontSize: 14)),
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

    // Esto descarga el archivo en Web o abre el menú de compartir en móviles
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
              int indexA = ordenBarriosOficial.indexOf(a);
              int indexB = ordenBarriosOficial.indexOf(b);
              if (indexA == -1 && indexB == -1) return a.compareTo(b);
              if (indexA == -1) return 1;
              if (indexB == -1) return -1;
              return indexA.compareTo(indexB);
            });

            return Column(
              children: [
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Text(
                      'SGRD YUMBO - PLANILLA DE RUTA DE VISITAS',
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
                          int idBarrio = ordenBarriosOficial.indexOf(barrio) + 1;
                          String prefijoId = idBarrio > 0 ? 'ID $idBarrio - ' : 'OTRO - ';

                          return Card(
                            margin: const EdgeInsets.symmetric(vertical: 10),
                            elevation: 3,
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.stretch,
                              children: [
                                Container(
                                  padding: const EdgeInsets.all(8),
                                  color: Colors.blueGrey[800],
                                  child: Text(
                                    '$prefijoId$barrio',
                                    style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 16),
                                  ),
                                ),
                                DataTable(
                                  headingRowColor: MaterialStateProperty.resolveWith((states) => Colors.grey[200]),
                                  columns: const [
                                    DataColumn(label: Text('Asunto/Novedad', style: TextStyle(fontWeight: FontWeight.bold))),
                                    DataColumn(label: Text('Dirección / Referencia', style: TextStyle(fontWeight: FontWeight.bold))),
                                    DataColumn(label: Text('Ciudadano Afectado', style: TextStyle(fontWeight: FontWeight.bold))),
                                    DataColumn(label: Text('Teléfono', style: TextStyle(fontWeight: FontWeight.bold))),
                                    DataColumn(label: Text('Estado', style: TextStyle(fontWeight: FontWeight.bold))),
                                  ],
                                  rows: lista.map((r) {
                                    String telefono = r.datosExtra?['telefono'] ?? 'N/A';
                                    String afectado = r.datosExtra?['ciudadano'] ?? 'Anónimo';
                                    if (telefono.isEmpty) telefono = 'N/A';
                                    if (afectado.isEmpty) afectado = 'Anónimo';

                                    return DataRow(cells: [
                                      DataCell(Text(r.titulo)),
                                      DataCell(Text(r.direccion)),
                                      DataCell(Text(afectado)),
                                      DataCell(Text(telefono)),
                                      DataCell(
                                        Row(
                                          mainAxisSize: MainAxisSize.min,
                                          children: [
                                            const Icon(Icons.square, color: Colors.black, size: 12),
                                            const SizedBox(width: 4),
                                            Text(r.estado, style: const TextStyle(fontWeight: FontWeight.bold)),
                                          ],
                                        ),
                                      ),
                                    ]);
                                  }).toList(),
                                ),
                              ],
                            ),
                          );
                        },
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
