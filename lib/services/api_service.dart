import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/reporte_comunitario.dart';
import '../models/trazabilidad_model.dart';

class ApiService {
  static const String baseUrl = 'http://10.147.17.2:8000/api';

  static Future<List<ReporteComunitario>> obtenerReportes({String? barrio, String? nombre, String? telefono}) async {
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
    try {
      print('📤 PUT reporte ID: $id');
      print('📤 PUT datos: $datos');
      final response = await http.put(
        Uri.parse('$baseUrl/reportes/$id'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode(datos),
      );
      print('📡 PUT response: ${response.statusCode}');
      print('📡 PUT body: ${response.body}');
      return response.statusCode == 200;
    } catch (e) {
      print('❌ Error al actualizar: $e');
      return false;
    }
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
    try {
      final response = await http.get(Uri.parse('$baseUrl/trazabilidad/$reporteId'));
      print('📡 GET trazabilidad - Status: ${response.statusCode}');
      print('📡 GET trazabilidad - Body: ${response.body}');
      
      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        // La respuesta es un array directamente, no tiene propiedad 'historial'
        List list = data is List ? data : [];
        return list.map((item) => TrazabilidadItem.fromJson(item)).toList();
      } else {
        print('❌ Error: ${response.statusCode} - ${response.body}');
        return [];
      }
    } catch (e) {
      print('❌ Error al cargar historial: $e');
      return [];
    }
  }

  static Future<bool> actualizarEstadoTrazabilidad(String reporteId, String nuevoEstado, String observacion) async {
    try {
      print('📤 Actualizando estado: reporte=$reporteId, estado=$nuevoEstado');
      final response = await http.put(
        Uri.parse('$baseUrl/reportes/$reporteId/estado'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode({
          'estado': nuevoEstado,
          'observacion': observacion,
        }),
      );
      print('📡 PUT estado - Status: ${response.statusCode}');
      print('📡 PUT estado - Body: ${response.body}');
      return response.statusCode == 200;
    } catch (e) {
      print('❌ Error al actualizar estado: $e');
      return false;
    }
  }

  // NUEVO: Método para descargar el detalle RUFE
  static Future<Map<String, dynamic>?> obtenerDetalleRufe(String reporteId) async {
    try {
      final response = await http.get(Uri.parse('$baseUrl/reportes/$reporteId/rufe'));
      if (response.statusCode == 200) {
        return json.decode(response.body);
      }
    } catch (e) {
      print('Error obteniendo RUFE: $e');
    }
    return null;
  }
}
