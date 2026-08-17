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
