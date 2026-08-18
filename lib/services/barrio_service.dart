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
      ).timeout(Duration(seconds: 10));

      print('📡 GET barrios - Status: ${response.statusCode}');
      
      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        print('📡 Barrios recibidos: ${data.length}');
        
        if (data is List) {
          return data.map((e) => Barrio.fromJson(e)).toList();
        }
        return [];
      }
      return [];
    } catch (e) {
      print('❌ Error al obtener barrios: $e');
      return [];
    }
  }

  static Future<bool> createBarrio(String nombre, int comuna) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/barrios'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode({
          'nombre': nombre,
          'comuna': comuna,
        }),
      );
      print("Respuesta createBarrio: ${response.statusCode} - ${response.body}");
      return response.statusCode == 200 || response.statusCode == 201;
    } catch (e) {
      print("Error al crear barrio: $e");
      return false;
    }
  }

  static Future<bool> updateBarrio(int id, String nombre, int comuna) async {
    try {
      final response = await http.put(
        Uri.parse('$baseUrl/barrios/$id'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode({
          'nombre': nombre,
          'comuna': comuna,
        }),
      );
      print("Respuesta updateBarrio: ${response.statusCode} - ${response.body}");
      return response.statusCode == 200;
    } catch (e) {
      print("Error al actualizar barrio: $e");
      return false;
    }
  }

  static Future<bool> deleteBarrio(int id) async {
    try {
      final response = await http.delete(
        Uri.parse('$baseUrl/barrios/$id'),
      );
      print("Respuesta deleteBarrio: ${response.statusCode} - ${response.body}");
      return response.statusCode == 200;
    } catch (e) {
      print("Error al eliminar barrio: $e");
      return false;
    }
  }
}
