import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:uuid/uuid.dart';
import '../config.dart';

class ApiService {
  static const String baseUrl = AppConfig.apiUrl;

  // ============================================================
  // REPORTES
  // ============================================================

  static Future<bool> crearReporte(Map<String, dynamic> data) async {
    try {
      final id = const Uuid().v4();
      final url = '$baseUrl/api/reportes?reporte_id=$id';
      
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

      final uri = Uri.parse('$baseUrl/api/reportes').replace(queryParameters: queryParams);
      final response = await http.get(
        uri,
        headers: {'Content-Type': 'application/json'},
      );

      if (response.statusCode == 200) {
        return json.decode(response.body);
      }
      return {'data': [], 'total': 0};
    } catch (e) {
      print('❌ Error en obtenerReportes: $e');
      return {'data': [], 'total': 0};
    }
  }

  static Future<Map<String, dynamic>> obtenerReporte(String id) async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/api/reportes/$id'),
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

  static Future<bool> actualizarReporte(String id, Map<String, dynamic> data) async {
    try {
      final response = await http.put(
        Uri.parse('$baseUrl/api/reportes/$id'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode(data),
      );
      return response.statusCode == 200 || response.statusCode == 201;
    } catch (e) {
      print('❌ Error en actualizarReporte: $e');
      return false;
    }
  }

  static Future<bool> eliminarReporte(String id) async {
    try {
      final response = await http.delete(
        Uri.parse('$baseUrl/api/reportes/$id'),
        headers: {'Content-Type': 'application/json'},
      );
      return response.statusCode == 200 || response.statusCode == 204;
    } catch (e) {
      print('❌ Error en eliminarReporte: $e');
      return false;
    }
  }

  // ============================================================
  // RUFE
  // ============================================================

  static Future<List<dynamic>> obtenerRufes() async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/api/rufe'),
        headers: {'Content-Type': 'application/json'},
      );

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        return data['data'] ?? [];
      }
      return [];
    } catch (e) {
      print('❌ Error en obtenerRufes: $e');
      return [];
    }
  }

  static Future<Map<String, dynamic>> obtenerRufe(String id) async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/api/rufe/$id'),
        headers: {'Content-Type': 'application/json'},
      );

      if (response.statusCode == 200) {
        return json.decode(response.body);
      }
      return {};
    } catch (e) {
      print('❌ Error en obtenerRufe: $e');
      return {};
    }
  }

  // ============================================================
  // BARRIOS
  // ============================================================

  static Future<List<dynamic>> obtenerBarrios() async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/api/barrios'),
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
  // TRAZABILIDAD (NUEVO)
  // ============================================================

  static Future<List<dynamic>> obtenerHistorial(String reporteId) async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/api/trazabilidad?reporte_id=$reporteId'),
        headers: {'Content-Type': 'application/json'},
      );

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        return data['data'] ?? [];
      }
      return [];
    } catch (e) {
      print('❌ Error en obtenerHistorial: $e');
      return [];
    }
  }

  static Future<bool> actualizarEstadoTrazabilidad({
    required String reporteId,
    required String estadoAnterior,
    required String estadoNuevo,
    required String observacion,
    String usuario = 'Operador SGRD',
  }) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/api/trazabilidad'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode({
          'reporte_id': reporteId,
          'estado_anterior': estadoAnterior,
          'estado_nuevo': estadoNuevo,
          'observacion': observacion,
          'usuario': usuario,
        }),
      );
      return response.statusCode == 200 || response.statusCode == 201;
    } catch (e) {
      print('❌ Error en actualizarEstadoTrazabilidad: $e');
      return false;
    }
  }
}
