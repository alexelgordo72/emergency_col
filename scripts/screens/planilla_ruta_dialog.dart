import 'package:flutter/material.dart';
import 'package:pdf/pdf.dart';
import 'package:pdf/widgets.dart' as pw;
import 'package:printing/printing.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

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
      final url = Uri.parse('http://10.147.17.2:8001/api/reportes/agrupados?limit=100&offset=0');
      final response = await http.get(url);

      if (response.statusCode != 200) {
        throw Exception('Error del servidor: ${response.statusCode}');
      }

      final data = json.decode(response.body);
      Map<String, List<Map<String, dynamic>>> gruposAgrupados = {};

      if (data is Map) {
        data.forEach((key, value) {
          if (value is List) {
            gruposAgrupados[key.toString()] = value.map((item) => Map<String, dynamic>.from(item)).toList();
          }
        });
      } else if (data is List) {
        for (var item in data) {
          final mapItem = Map<String, dynamic>.from(item);
          final barrio = mapItem['barrio']?.toString() ?? 'GENERAL';
          gruposAgrupados.putIfAbsent(barrio, () => []).add(mapItem);
        }
      }

      final pdf = pw.Document();

      pdf.addPage(
        pw.MultiPage(
          pageFormat: PdfPageFormat.letter,
          margin: const pw.EdgeInsets.all(20),
          build: (pw.Context context) {
            List<pw.Widget> widgetsPdf = [
              pw.Header(
                level: 0,
                child: pw.Column(
                  crossAxisAlignment: pw.CrossAxisAlignment.start,
                  children: [
                    pw.Text("SGRD YUMBO - PLANILLA DE RUTA DE VISITAS", style: pw.TextStyle(fontSize: 16, fontWeight: pw.FontWeight.bold)),
                    pw.Text("Sistema de Gestión de Riesgo de Desastres - Reportes Georreferenciados", style: const pw.TextStyle(fontSize: 10, color: PdfColors.grey700)),
                  ],
                ),
              ),
              pw.SizedBox(height: 10),
            ];

            if (gruposAgrupados.isEmpty) {
              widgetsPdf.add(pw.Paragraph(text: "No se encontraron reportes registrados para agrupar."));
            } else {
              gruposAgrupados.forEach((barrioNombre, visitas) {
                widgetsPdf.add(
                  pw.Container(
                    margin: const pw.EdgeInsets.only(bottom: 15),
                    child: pw.Column(
                      crossAxisAlignment: pw.CrossAxisAlignment.start,
                      children: [
                        pw.Container(
                          padding: const pw.EdgeInsets.all(6),
                          color: PdfColors.grey300,
                          width: double.infinity,
                          child: pw.Text(
                            "ZONA / BARRIO: $barrioNombre",
                            style: pw.TextStyle(fontSize: 11, fontWeight: pw.FontWeight.bold),
                          ),
                        ),
                        pw.Table.fromTextArray(
                          headerStyle: pw.TextStyle(fontWeight: pw.FontWeight.bold, fontSize: 8),
                          cellStyle: const pw.TextStyle(fontSize: 8),
                          headers: ['#', 'Asunto / Novedad', 'Dirección / Referencia', 'Ciudadano Afectado', 'Teléfono', 'Estado'],
                          data: List<List<String>>.generate(
                            visitas.length,
                            (index) {
                              final v = visitas[index];
                              final novedad = v['titulo']?.toString() ?? 'Daño Estructural';
                              final direccion = v['direccion']?.toString() ?? 'Sin dirección';
                              
                              String ciudadano = 'No registrado';
                              String telefono = 'N/A';
                              if (v['datos_extra'] != null && v['datos_extra'] is Map) {
                                ciudadano = v['datos_extra']['ciudadano']?.toString() ?? 'No registrado';
                                telefono = v['datos_extra']['telefono']?.toString() ?? 'N/A';
                              }
                              final estado = v['estado']?.toString() ?? 'Pendiente';

                              return [
                                '${index + 1}',
                                novedad,
                                direccion,
                                ciudadano,
                                telefono,
                                estado,
                              ];
                            },
                          ),
                        ),
                        pw.Container(
                          height: 30,
                          decoration: pw.BoxDecoration(
                            border: pw.Border.all(color: PdfColors.grey400, width: 0.5),
                          ),
                          alignment: pw.Alignment.topLeft,
                          padding: const pw.EdgeInsets.all(4),
                          child: const pw.Text("OBSERVACIONES / ESPACIO DE ESCRITO EN TERRENO:", style: pw.TextStyle(fontSize: 7, color: PdfColors.grey600)),
                        ),
                        pw.SizedBox(height: 8),
                      ],
                    ),
                  ),
                );
              });
            }

            return widgetsPdf;
          },
        ),
      );

      await Printing.layoutPdf(
        onLayout: (PdfPageFormat format) async => pdf.save(),
      );
    } catch (e) {
      print('Error al generar PDF: $e');
    } finally {
      setState(() => generando = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Dialog(
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: Container(
        width: 500,
        height: 350,
        padding: const EdgeInsets.all(24),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Icon(Icons.picture_as_pdf, size: 60, color: Colors.red),
            const SizedBox(height: 20),
            const Text('Generador de Planilla de Ruta', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            const SizedBox(height: 10),
            const Text('Exporta todas las visitas agrupadas por sector con espacios de anotación.', textAlign: TextAlign.center, style: TextStyle(color: Colors.grey)),
            const SizedBox(height: 30),
            SizedBox(
              width: double.infinity,
              height: 45,
              child: ElevatedButton.icon(
                style: ElevatedButton.styleFrom(backgroundColor: Colors.red[800], foregroundColor: Colors.white),
                icon: generando 
                    ? const SizedBox(width: 20, height: 20, child: CircularProgressIndicator(color: Colors.white, strokeWidth: 2)) 
                    : const Icon(Icons.print),
                label: Text(generando ? 'Generando PDF...' : 'Generar y Exportar Planilla PDF', style: const TextStyle(fontSize: 15)),
                onPressed: generando ? null : _generarPdfPlanilla,
              ),
            ),
          ],
        ),
      ),
    );
  }
}
