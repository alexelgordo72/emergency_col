import 'dart:convert';
import 'package:http/http.dart' as http;
import '../config.dart';

class DashboardAgrupadoService {
  static String get baseUrl => AppConfig.apiUrl;

  static Future<List<Map<String, dynamic>>> obtenerDashboardAgrupado() async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/dashboard/agrupado'),
        headers: {'Content-Type': 'application/json'},
      );

      print('📡 GET dashboard_agrupado - Status: ${response.statusCode}');

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        if (data is List) {
          return List<Map<String, dynamic>>.from(data);
        }
        return [];
      } else {
        print('❌ Error: ${response.statusCode} - ${response.body}');
        return [];
      }
    } catch (e) {
      print('❌ Error al obtener dashboard agrupado: $e');
      return [];
    }
  }

  static Future<Map<String, dynamic>> obtenerResumenDashboard() async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/dashboard/resumen'),
        headers: {'Content-Type': 'application/json'},
      );

      if (response.statusCode == 200) {
        return json.decode(response.body);
      } else {
        return {};
      }
    } catch (e) {
      print('❌ Error al obtener resumen: $e');
      return {};
    }
  }
}
