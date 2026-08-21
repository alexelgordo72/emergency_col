import 'dart:convert';
import 'package:http/http.dart' as http;
import '../config.dart';
import '../models/reporte_comunitario.dart';

class ReporteRutaService {
  static String get baseUrl => AppConfig.apiUrl;

  static Future<List<ReporteComunitario>> obtenerReportesPendientes() async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/reportes?limit=10000&offset=0'),
        headers: {'Content-Type': 'application/json'},
      );

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        final List<dynamic> dataList = data['data'] ?? [];
        final reportes = dataList
            .map((e) => ReporteComunitario.fromJson(e))
            .where((r) => r.estado.toLowerCase().contains('pendiente'))
            .toList();
        return reportes;
      } else {
        return [];
      }
    } catch (e) {
      print('❌ Error al obtener reportes pendientes: $e');
      return [];
    }
  }

  static Future<Map<String, Map<String, List<ReporteComunitario>>>> agruparPorComunaYBarrio(
      List<ReporteComunitario> reportes) async {
    final Map<String, Map<String, List<ReporteComunitario>>> resultado = {};

    // Obtener barrios con comuna
    final barriosResponse = await http.get(
      Uri.parse('$baseUrl/barrios'),
      headers: {'Content-Type': 'application/json'},
    );

    Map<String, int> barrioComuna = {};
    if (barriosResponse.statusCode == 200) {
      final List data = json.decode(barriosResponse.body);
      for (var item in data) {
        final nombre = (item['nombre'] ?? '').toString().toUpperCase().trim();
        final comuna = item['comuna'] ?? 0;
        barrioComuna[nombre] = comuna;
      }
    }

    for (var reporte in reportes) {
      final barrioNombre = reporte.barrio.toUpperCase().trim();
      final comuna = barrioComuna[barrioNombre] ?? 0;
      final comunaKey = comuna.toString();

      if (!resultado.containsKey(comunaKey)) {
        resultado[comunaKey] = {};
      }

      if (!resultado[comunaKey]!.containsKey(barrioNombre)) {
        resultado[comunaKey]![barrioNombre] = [];
      }

      resultado[comunaKey]![barrioNombre]!.add(reporte);
    }

    return resultado;
  }
}
