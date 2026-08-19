import 'dart:convert';
import 'package:http/http.dart' as http;
import '../config.dart';
import '../models/reporte_ruta.dart';

class ReporteRutaService {
  static const String baseUrl = AppConfig.apiUrl;

  static Future<List<ReporteRuta>> generarReporteRuta({
    String? comuna,
    String? prioridad,
  }) async {
    try {
      final uri = Uri.parse('$baseUrl/reporte/ruta').replace(queryParameters: {
        if (comuna != null && comuna != 'TODAS') 'comuna': comuna,
        if (prioridad != null && prioridad != 'TODAS') 'prioridad': prioridad,
      });

      print('📡 Generando reporte de ruta: $uri');

      final response = await http.get(
        uri,
        headers: {'Content-Type': 'application/json'},
      );

      if (response.statusCode == 200) {
        final List<dynamic> data = json.decode(response.body);
        return data.map((e) => ReporteRuta.fromJson(e)).toList();
      } else {
        throw Exception('Error al generar el reporte: ${response.statusCode}');
      }
    } catch (e) {
      print('❌ Error en ReporteRutaService: $e');
      rethrow;
    }
  }
}
