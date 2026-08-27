import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/barrio.dart';
import '../config.dart';

class BarrioService {
  static String get baseUrl => AppConfig.apiUrl;

  static Future<List<Barrio>> getBarrios() async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/barrios'),
        headers: {'Content-Type': 'application/json'},
      );

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        final List list = data is List ? data : (data['data'] ?? []);
        
        // Eliminar duplicados por nombre
        final Map<String, Barrio> barriosUnicos = {};
        for (var item in list) {
          final barrio = Barrio.fromJson(item);
          barriosUnicos[barrio.nombre] = barrio;
        }
        
        return barriosUnicos.values.toList();
      }
      return [];
    } catch (e) {
      print('❌ Error al obtener barrios: $e');
      return [];
    }
  }
}
