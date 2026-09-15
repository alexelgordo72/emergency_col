import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:sgrd_final/config.dart';

class ApiService {
  static const String baseUrl = AppConfig.apiUrl;

  static Future<Map<String, dynamic>> obtenerReportes({
    int limit = 10000,
    int offset = 0,
  }) async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/reportes?limit=$limit&offset=$offset'),
        headers: {'Content-Type': 'application/json'},
      );
      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        return {
          'data': data['data'] ?? [],
          'total': data['total'] ?? 0,
        };
      }
      return {'data': [], 'total': 0};
    } catch (e) {
      print('❌ Error en obtenerReportes: $e');
      return {'data': [], 'total': 0};
    }
  }

  static Future<Map<String, dynamic>> obtenerDashboardCompleto() async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/dashboard/completo'),
        headers: {'Content-Type': 'application/json'},
      );
      if (response.statusCode == 200) {
        return json.decode(response.body);
      } else {
        throw Exception('Error al obtener dashboard: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error: $e');
    }
  }

  static Future<Map<String, dynamic>> obtenerReportePorId(String id) async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/reportes/$id'),
        headers: {'Content-Type': 'application/json'},
      );
      if (response.statusCode == 200) {
        return json.decode(response.body);
      } else {
        throw Exception('Error al obtener reporte: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error: $e');
    }
  }

  static Future<Map<String, dynamic>> actualizarReporte(String id, Map<String, dynamic> data) async {
    try {
      final response = await http.put(
        Uri.parse('$baseUrl/reportes/$id'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode(data),
      );
      if (response.statusCode == 200) {
        return json.decode(response.body);
      } else {
        throw Exception('Error al actualizar reporte: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error: $e');
    }
  }
}
