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
      print('Error en obtenerReportes: $e');
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

  static Future<Map<String, dynamic>> actualizarReporte(
      String id, Map<String, dynamic> data) async {
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

  static Future<Map<String, dynamic>> crearReporte(
      Map<String, dynamic> data) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/reportes'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode(data),
      );
      if (response.statusCode == 200 || response.statusCode == 201) {
        return json.decode(response.body);
      } else {
        throw Exception(
            'Error al crear reporte: ${response.statusCode} - ${response.body}');
      }
    } catch (e) {
      throw Exception('Error: $e');
    }
  }

  static Future<Map<String, dynamic>> eliminarReporte(String id) async {
    try {
      final response = await http.delete(
        Uri.parse('$baseUrl/reportes/$id'),
        headers: {'Content-Type': 'application/json'},
      );
      // Aceptar 200 (OK), 204 (No Content) y también 404 (ya no existe)
      if (response.statusCode == 200 ||
          response.statusCode == 204 ||
          response.statusCode == 404) {
        return {'success': true, 'message': 'Reporte eliminado'};
      } else {
        throw Exception(
            'Error al eliminar reporte: ${response.statusCode} - ${response.body}');
      }
    } catch (e) {
      throw Exception('Error: $e');
    }
  }

  static Future<List<String>> obtenerBarrios() async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/barrios'),
        headers: {'Content-Type': 'application/json'},
      );
      if (response.statusCode == 200) {
        final List<dynamic> data = json.decode(response.body);
        return data
            .map((b) => (b['nombre'] ?? b['barrio'] ?? '').toString())
            .where((s) => s.isNotEmpty)
            .toList();
      }
      return [];
    } catch (e) {
      print('Error en obtenerBarrios: $e');
      return [];
    }
  }
}
