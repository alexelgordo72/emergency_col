import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:sgrd_final/config.dart';
import 'package:sgrd_final/services/auth_service.dart';

class ApiService {
  static const String baseUrl = AppConfig.apiUrl;

  // ============================================================
  // REPORTES
  // ============================================================
  static Future<Map<String, dynamic>> obtenerReportes({
    int limit = 10000,
    int offset = 0,
    String? barrio,
    String? nombre,
    String? telefono,
  }) async {
    try {
      final queryParams = <String, String>{
        'limit': limit.toString(),
        'offset': offset.toString(),
      };

      if (barrio != null && barrio.isNotEmpty) queryParams['barrio'] = barrio;
      if (nombre != null && nombre.isNotEmpty) queryParams['nombre'] = nombre;
      if (telefono != null && telefono.isNotEmpty) queryParams['telefono'] = telefono;

      final uri = Uri.parse('$baseUrl/reportes').replace(queryParameters: queryParams);

      final response = await http.get(
        uri,
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

  static Future<List<dynamic>> obtenerBarrios() async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/barrios'),
        headers: {'Content-Type': 'application/json'},
      );

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        return data['data'] ?? [];
      }
      return [];
    } catch (e) {
      print('❌ Error en obtenerBarrios: $e');
      return [];
    }
  }

  // ============================================================
  // ESTADOS
  // ============================================================
  static Future<List<Map<String, dynamic>>> obtenerEstados() async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/estados'),
        headers: {'Content-Type': 'application/json'},
      );

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        if (data is List) {
          return data.map((e) => Map<String, dynamic>.from(e)).toList();
        }
        return [];
      } else {
        throw Exception('Error al obtener estados: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error: $e');
    }
  }

  // ============================================================
  // TRAZABILIDAD
  // ============================================================
  static Future<Map<String, dynamic>> obtenerTrazabilidad(String reporteId) async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/trazabilidad/$reporteId'),
        headers: {'Content-Type': 'application/json'},
      );

      if (response.statusCode == 200) {
        return json.decode(response.body);
      } else {
        throw Exception('Error al obtener trazabilidad: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error: $e');
    }
  }

  static Future<Map<String, dynamic>> cambiarEstado(
    String reporteId,
    String nuevoEstado,
    String observacion,
  ) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/trazabilidad/$reporteId'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode({
          'estado_nuevo': nuevoEstado,
          'observacion': observacion,
          'usuario': AuthService.currentUser?.nombre ?? 'Sistema',
        }),
      );

      if (response.statusCode == 200) {
        return json.decode(response.body);
      } else {
        throw Exception('Error al cambiar estado: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Error: $e');
    }
  }

  // ============================================================
  // VISITAS DE CAMPO
  // ============================================================
  static Future<List<Map<String, dynamic>>> obtenerVisitas(String reporteId) async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/visitas/$reporteId'),
        headers: {'Content-Type': 'application/json'},
      );

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        if (data is List) {
          return data.map((e) => Map<String, dynamic>.from(e)).toList();
        }
        return [];
      } else {
        return [];
      }
    } catch (e) {
      print('❌ Error al obtener visitas: $e');
      return [];
    }
  }
}
