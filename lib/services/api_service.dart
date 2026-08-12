import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/reporte_comunitario.dart';
import '../models/trazabilidad_model.dart';

class ApiService {
  static const String baseUrl = 'http://10.147.17.2:8000/api';

  static Future<List<ReporteComunitario>> obtenerReportes({String? barrio, String? nombre, String? telefono}) async {
    // Construir los parámetros de consulta de forma dinámica
    final Map<String, String> queryParams = {};
    if (barrio != null && barrio.isNotEmpty && barrio != 'Barrio') {
      queryParams['barrio'] = barrio;
    }
    if (nombre != null && nombre.isNotEmpty) {
      queryParams['nombre'] = nombre;
    }
    if (telefono != null && telefono.isNotEmpty) {
      queryParams['telefono'] = telefono;
    }

    final uri = Uri.parse('$baseUrl/reportes').replace(queryParameters: queryParams.isNotEmpty ? queryParams : null);
    
    final response = await http.get(uri);
    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      List list = data is List ? data : data['reportes'] ?? [];
      return list.map((item) => ReporteComunitario.fromJson(item)).toList();
    } else {
      throw Exception('Error al cargar reportes');
    }
  }

  static Future<List<String>> obtenerBarrios() async {
    try {
      final response = await http.get(Uri.parse('$baseUrl/barrios'));
      if (response.statusCode == 200) {
        List data = json.decode(response.body);
        return data.map((e) => e.toString()).toList();
      }
    } catch (_) {}
    return [];
  }

  static Future<bool> actualizarReporte(String id, Map<String, dynamic> datos) async {
    final response = await http.put(
      Uri.parse('$baseUrl/reportes/$id'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode(datos),
    );
    return response.statusCode == 200;
  }

  static Future<bool> crearReporte(Map<String, dynamic> datos) async {
    final response = await http.post(
      Uri.parse('$baseUrl/reportes'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode(datos),
    );
    return response.statusCode == 200;
  }

  static Future<List<TrazabilidadItem>> obtenerHistorial(String reporteId) async {
    final response = await http.get(Uri.parse('$baseUrl/reportes/$reporteId/trazabilidad'));
    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      List list = data['historial'] ?? [];
      return list.map((item) => TrazabilidadItem.fromJson(item)).toList();
    } else {
      throw Exception('Error al cargar historial');
    }
  }

  static Future<bool> actualizarEstadoTrazabilidad(String reporteId, String nuevoEstado, String observacion) async {
    final response = await http.put(
      Uri.parse('$baseUrl/reportes/$reporteId/trazabilidad'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode({
        'nuevo_estado': nuevoEstado,
        'observacion': observacion,
      }),
    );
    return response.statusCode == 200;
  }
}
