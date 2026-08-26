import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:uuid/uuid.dart';
import '../config.dart';

class ApiService {
  static const String baseUrl = AppConfig.apiUrl;

  // ============================================================
  // REPORTES - CRUD COMPLETO
  // ============================================================

  // CREATE
  static Future<bool> crearReporte(Map<String, dynamic> data) async {
    try {
      final id = const Uuid().v4();
      final url = '$baseUrl/reportes?reporte_id=$id';
      
      print('📤 Creando reporte en: $url');
      print('📤 Payload: $data');
      
      final response = await http.post(
        Uri.parse(url),
        headers: {'Content-Type': 'application/json'},
        body: json.encode(data),
      );
      
      print('📥 Status: ${response.statusCode}');
      print('📥 Response: ${response.body}');
      
      return response.statusCode == 200 || response.statusCode == 201;
    } catch (e) {
      print('❌ Error en crearReporte: $e');
      return false;
    }
  }

  // READ (Listar)
  static Future<Map<String, dynamic>> obtenerReportes({
    int limit = 50,
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

  // READ (Uno)
  static Future<Map<String, dynamic>> obtenerReporte(String id) async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/reportes/$id'),
        headers: {'Content-Type': 'application/json'},
      );

      if (response.statusCode == 200) {
        return json.decode(response.body);
      }
      return {};
    } catch (e) {
      print('❌ Error en obtenerReporte: $e');
      return {};
    }
  }

  // UPDATE
  static Future<bool> actualizarReporte(String id, Map<String, dynamic> data) async {
    try {
      final response = await http.put(
        Uri.parse('$baseUrl/reportes/$id'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode(data),
      );
      return response.statusCode == 200 || response.statusCode == 201;
    } catch (e) {
      print('❌ Error en actualizarReporte: $e');
      return false;
    }
  }

  // DELETE
  static Future<bool> eliminarReporte(String id) async {
    try {
      final response = await http.delete(
        Uri.parse('$baseUrl/reportes/$id'),
        headers: {'Content-Type': 'application/json'},
      );
      print('📥 DELETE Status: ${response.statusCode}');
      print('📥 DELETE Response: ${response.body}');
      return response.statusCode == 200 || response.statusCode == 204;
    } catch (e) {
      print('❌ Error en eliminarReporte: $e');
      return false;
    }
  }

  // ============================================================
  // BARRIOS
  // ============================================================

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
}
