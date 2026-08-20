import 'dart:convert';
import 'package:http/http.dart' as http;
import '../config.dart';

class DashboardService {
  static const String baseUrl = AppConfig.apiUrl;

  static Future<Map<String, dynamic>> getResumenGeneral() async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/dashboard/resumen'),
        headers: {'Content-Type': 'application/json'},
      );
      if (response.statusCode == 200) {
        return json.decode(response.body);
      }
      return {};
    } catch (e) {
      print('Error obteniendo resumen general: $e');
      return {};
    }
  }

  static Future<Map<String, dynamic>> getEstadisticasAHE() async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/dashboard/ahe'),
        headers: {'Content-Type': 'application/json'},
      );
      if (response.statusCode == 200) {
        return json.decode(response.body);
      }
      return {};
    } catch (e) {
      print('Error obteniendo estadísticas AHE: $e');
      return {};
    }
  }

  static Future<Map<String, dynamic>> getEstadisticasEDHAS() async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/dashboard/edhas'),
        headers: {'Content-Type': 'application/json'},
      );
      if (response.statusCode == 200) {
        return json.decode(response.body);
      }
      return {};
    } catch (e) {
      print('Error obteniendo estadísticas EDHAS: $e');
      return {};
    }
  }

  static Future<Map<String, dynamic>> getEstadisticasGenero() async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/dashboard/genero'),
        headers: {'Content-Type': 'application/json'},
      );
      if (response.statusCode == 200) {
        return json.decode(response.body);
      }
      return {};
    } catch (e) {
      print('Error obteniendo estadísticas de género: $e');
      return {};
    }
  }
}

  static Future<bool> guardarDashboard(Map<String, dynamic> data) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/dashboard/guardar'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode(data),
      );
      print('📡 POST dashboard - Status: ${response.statusCode}');
      print('📡 POST dashboard - Body: ${response.body}');
      return response.statusCode == 200 || response.statusCode == 201;
    } catch (e) {
      print('❌ Error en guardarDashboard: $e');
      return false;
    }
  }

  static Future<List<Map<String, dynamic>>> obtenerDashboardAgrupado() async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/dashboard/agrupado'),
        headers: {'Content-Type': 'application/json'},
      );
      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        if (data is List) {
          return List<Map<String, dynamic>>.from(data);
        }
        return [];
      }
      return [];
    } catch (e) {
      print('❌ Error en obtenerDashboardAgrupado: $e');
      return [];
    }
  }

  static Future<bool> regenerarDashboard() async {
    try {
      // Primero, obtener todos los reportes
      final reportesResponse = await http.get(
        Uri.parse('$baseUrl/reportes?limit=10000&offset=0'),
        headers: {'Content-Type': 'application/json'},
      );
      
      if (reportesResponse.statusCode != 200) {
        print('❌ Error al obtener reportes para dashboard');
        return false;
      }

      final data = json.decode(reportesResponse.body);
      final reportes = data['data'] as List? ?? [];
      
      print('📊 Regenerando dashboard con ${reportes.length} reportes...');

      // Limpiar dashboard existente (opcional - requiere endpoint DELETE)
      // Por ahora, solo agregamos nuevos

      int guardados = 0;
      int errores = 0;
      for (var reporte in reportes) {
        try {
          final dashboardData = {
            'reporte_id': reporte['id'],
            'titulo': reporte['titulo'] ?? 'Sin título',
            'estado': reporte['estado'] ?? reporte['estado_actual'] ?? 'Pendiente',
            'fecha': reporte['fecha'] ?? reporte['fecha_creacion'] ?? DateTime.now().toIso8601String(),
            'barrio': reporte['barrio'] ?? reporte['sector_barrio'] ?? 'Sin barrio',
            'direccion': reporte['direccion'] ?? reporte['direccion_referencia'] ?? '',
            'latitud': reporte['latitud'] ?? 0,
            'longitud': reporte['longitud'] ?? 0,
            'descripcion': reporte['descripcion'] ?? reporte['descripcion_detallada'] ?? '',
            'ciudadano': reporte['ciudadano'] ?? reporte['datos_extra']?['ciudadano'] ?? 'Anónimo',
            'telefono': reporte['telefono'] ?? reporte['datos_extra']?['telefono'] ?? 'No registra',
            'total_reportes_grupo': 1,
          };

          final exito = await guardarDashboard(dashboardData);
          if (exito) {
            guardados++;
          } else {
            errores++;
          }
        } catch (e) {
          print('❌ Error guardando reporte ${reporte['id']}: $e');
          errores++;
        }
      }

      print('✅ Dashboard regenerado: $guardados guardados, $errores errores');
      return errores == 0;
    } catch (e) {
      print('❌ Error en regenerarDashboard: $e');
      return false;
    }
  }
