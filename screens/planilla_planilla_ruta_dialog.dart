import 'package:flutter/material.dart';
import 'package:pdf/pdf.dart';
import 'package:pdf/widgets.dart' as pw;
import 'package:printing/printing.dart';

class PlanillaRutaDialog extends StatefulWidget {
  const PlanillaRutaDialog({Key? key}) : super(key: key);

  @override
  _PlanillaRutaDialogState createState() => _PlanillaRutaDialogState();
}

class _PlanillaRutaDialogState extends State<PlanillaRutaDialog> {
  bool generando = false;

  Future<void> _generarPdfPlanilla() async {
    setState(() => generando = true);
    try {
      final pdf = pw.Document();

      final List<Map<String, dynamic>> datosRuta = [
        {
          "comuna": "Comuna 1",
          "id_barrio": "ID 21 - PANORAMA",
          "visitas": [
            {"novedad": "Daño Estructural", "direccion": "Calle 6B #17C-24", "afectado": "Nelvis Beltrán", "telefono": "3135607120"},
            {"novedad": "Daño Estructural", "direccion": "Carrera 16 #16A-8", "afectado": "Anonimo", "telefono": "N/A"},
            {"novedad": "Daño Estructural", "direccion": "Calle 6B #17-74", "afectado": "Isidro Lopez", "telefono": "3226767725"}
          ]
        },
        {
          "comuna": "Comuna 2",
          "id_barrio": "ID 8 - BOLIVAR",
          "visitas": [
            {"novedad": "Visita Pendiente", "direccion": "Calle 14 #2-25", "afectado": "Mayirlin Fernandez", "telefono": "3207649103"},
            {"novedad": "Daño Estructural", "direccion": "Calle 11 #4-53", "afectado": "Cristian Pacitajoa", "telefono": "3026665931"}
          ]
        }
      ];

      pdf.addPage(
        pw.MultiPage(
          pageFormat: PdfPageFormat.letter,
          margin: const pw.EdgeInsets.all(20),
          build: (pw.Context context) {
            return [
              pw.Header(
                level: 0,
                child: pw.Row(
                  mainAxisAlignment: pw.MainAxisAlignment.spaceBetween,
                  children: [
                    pw.Column(
                      crossAxisAlignment: pw.CrossAxisAlignment.start,
                      children: [
                        pw.Text("SGRD YUMBO - PLANILLA DE RUTA DE VISITAS", style: pw.TextStyle(fontSize: 16, fontWeight: pw.FontWeight.bold)),
                        pw.Text("Sistema de Gestión de Riesgo de Desastres - Reportes Georreferenciados", style: const pw.TextStyle(fontSize: 10, color: PdfColors.grey700)),
                      ],
                    ),
                  ],
                ),
              ),
              pw.SizedBox(height: 10),
              ...datosRuta.map((grupo) {
                return pw.Container(
                  margin: const pw.EdgeInsets.only(bottom: 15),
                  child: pw.Column(
                    crossAxisAlignment: pw.CrossAxisAlignment.start,
                    children: [
                      pw.Container(
                        padding: const pw.EdgeInsets.all(6),
                        color: PdfColors.grey300,
                        width: double.infinity,
                        child: pw.Text(
                          "${grupo['comuna']} - ${grupo['id_barrio']}",
                          style: pw.TextStyle(fontSize: 12, fontWeight: pw.FontWeight.bold),
                        ),
                      ),
                      pw.Table.fromTextArray(
                        headerStyle: pw.TextStyle(fontWeight: pw.FontWeight.bold, fontSize: 9),
                        cellStyle: const pw.TextStyle(fontSize: 9),
                        headers: ['#', 'Asunto / Novedad', 'Dirección / Referencia', 'Ciudadano Afectado', 'Teléfono'],
                        data: List<List<String>>.generate(
                          grupo['visitas'].length,
                          (index) {
                            final v = grupo['visitas'][index];
                            return [
                              '${index + 1}',
                              v['novedad'],
                              v['direccion'],
                              v['afectado'],
                              v['telefono'],
                            ];
                          },
                        ),
                      ),
                      pw.Container(
                        height: 35,
                        decoration: pw.BoxDecoration(
                          border: pw.Border.all(color: PdfColors.grey400, width: 0.5),
                        ),
                        alignment: pw.Alignment.topLeft,
                        padding: const pw.EdgeInsets.all(4),
                        child: const pw.Text("OBSERVACIONES / ESPACIO DE ESCRITO EN TERRENO:", style: pw.TextStyle(fontSize: 8, color: PdfColors.grey600)),
                      ),
                      pw.SizedBox(height: 10),
                    ],
                  ),
                );
              }).toList(),
            ];
          },
        ),
      );

      await Printing.layoutPdf(
        onLayout: (PdfPageFormat format) async => pdf.save(),
      );
    } catch (e) {
      print('Error: $e');
    } finally {
      setState(() => generando = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Dialog(
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: Container(
        width: 600,
        height: 400,
        padding: const EdgeInsets.all(24),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Icon(Icons.picture_as_pdf, size: 64, color: Colors.red),
            const SizedBox(height: 20),
            const Text('Generador Oficial de Planilla de Ruta', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
            const SizedBox(height: 10),
            const Text('Agrupado por Comuna y Barrio, con espacios de escritura para visitas.', textAlign: TextAlign.center, style: TextStyle(color: Colors.grey)),
            const SizedBox(height: 30),
            SizedBox(
              width: double.infinity,
              height: 50,
              child: ElevatedButton.icon(
                style: ElevatedButton.styleFrom(backgroundColor: Colors.red[800], foregroundColor: Colors.white),
                icon: generando 
                    ? const SizedBox(width: 20, height: 20, child: CircularProgressIndicator(color: Colors.white, strokeWidth: 2)) 
                    : const Icon(Icons.print),
                label: Text(generando ? 'Generando Documento...' : 'Generar y Exportar Planilla PDF', style: const TextStyle(fontSize: 16)),
                onPressed: generando ? null : _generarPdfPlanilla,
              ),
            ),
          ],
        ),
      ),
    );
  }
}
