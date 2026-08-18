import 'dart:convert';
import 'package:http/http.dart' as http;
import '../config.dart';

class GrupoFamiliarService {
  static String get baseUrl => AppConfig.apiUrl;

  static Future<List<Map<String, dynamic>>> obtenerTodosLosGrupos() async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/reportes?limit=2000'),
      ).timeout(Duration(seconds: 10));

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        final reportes = data['data'] as List<dynamic>? ?? [];
        
        final Map<String, List<dynamic>> grupos = {};
        
        for (var reporte in reportes) {
          final telefono = reporte['telefono'] ?? 'Sin teléfono';
          if (!grupos.containsKey(telefono)) {
            grupos[telefono] = [];
          }
          grupos[telefono]!.add(reporte);
        }
        
        final List<Map<String, dynamic>> resultado = [];
        for (var entry in grupos.entries) {
          if (entry.value.length > 1) {
            resultado.add({
              'telefono': entry.key,
              'total_reportes': entry.value.length,
              'reportes': entry.value,
              'ciudadanos': entry.value.map((r) => r['ciudadano'] ?? 'Anónimo').toSet().join(' | '),
            });
          }
        }
        
        resultado.sort((a, b) => b['total_reportes'].compareTo(a['total_reportes']));
        return resultado;
      }
      return [];
    } catch (e) {
      print('❌ Error al obtener grupos: $e');
      return [];
    }
  }

  static Future<Map<String, dynamic>> buscarPorTelefono(String telefono) async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/grupos-por-telefono/$telefono'),
      ).timeout(Duration(seconds: 10));

      if (response.statusCode == 200) {
        return json.decode(response.body);
      }
      return {};
    } catch (e) {
      print('❌ Error al buscar grupo: $e');
      return {};
    }
  }
}
