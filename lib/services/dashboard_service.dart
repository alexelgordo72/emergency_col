import 'dart:convert';
import 'package:http/http.dart' as http;
import '../config.dart';

class DashboardService {
  static const String baseUrl = AppConfig.apiUrl;

  static Future<Map<String, dynamic>> getDashboardData({
    String? prioridad,
    String? comuna,
  }) async {
    try {
      final queryParams = <String, String>{};
      if (prioridad != null && prioridad != 'TODAS') {
        queryParams['prioridad'] = prioridad;
      }
      if (comuna != null && comuna != 'TODAS') {
        queryParams['comuna'] = comuna;
      }

      final uri = Uri.parse('$baseUrl/api/dashboard/detallado')
          .replace(queryParameters: queryParams);

      final response = await http.get(
        uri,
        headers: {'Content-Type': 'application/json'},
      );

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        return _transformDashboardData(data);
      }
      return {};
    } catch (e) {
      print('❌ Error obteniendo dashboard: $e');
      return {};
    }
  }

  static Map<String, dynamic> _transformDashboardData(Map<String, dynamic> data) {
    final reportes = data['reportes'] as List<dynamic>? ?? [];
    
    final prioridadStats = <String, int>{};
    for (var r in reportes) {
      final p = r['prioridad']?.toString().toUpperCase() ?? 'BAJA';
      prioridadStats[p] = (prioridadStats[p] ?? 0) + 1;
    }

    final comunaStats = <String, int>{};
    for (var r in reportes) {
      final c = r['comuna_o_sector'] ?? 'Sin Asignar';
      comunaStats[c] = (comunaStats[c] ?? 0) + 1;
    }

    final tipoStats = <String, int>{};
    for (var r in reportes) {
      final t = r['tipo_formulario'] ?? 'Sin Tipo';
      tipoStats[t] = (tipoStats[t] ?? 0) + 1;
    }

    return {
      'total_reportes': data['total_reportes_alta_prioridad'] ?? 0,
      'total_comunas': data['total_comunas'] ?? 0,
      'total_barrios': data['total_barrios'] ?? 0,
      'total_tipos': data['total_tipos'] ?? 0,
      'prioridad_stats': prioridadStats,
      'comuna_stats': comunaStats,
      'tipo_stats': tipoStats,
      'comunas': data['comunas'] ?? [],
      'barrios': data['barrios'] ?? [],
      'tipos': data['tipos_formulario'] ?? [],
      'reportes': reportes.take(20).toList(),
    };
  }

  static Future<Map<String, dynamic>> getResumenRapido() async {
    try {
      final data = await getDashboardData();
      return {
        'total': data['total_reportes'] ?? 0,
        'alta': data['prioridad_stats']?['ALTA'] ?? 0,
        'media': data['prioridad_stats']?['MEDIA'] ?? 0,
        'baja': data['prioridad_stats']?['BAJA'] ?? 0,
        'comunas': data['total_comunas'] ?? 0,
        'barrios': data['total_barrios'] ?? 0,
      };
    } catch (e) {
      return {};
    }
  }
}
