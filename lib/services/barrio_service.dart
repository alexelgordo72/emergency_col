import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/barrio.dart';

class BarrioService {
  static const String baseUrl = 'http://10.147.17.2:8000/api';

  static Future<List<Barrio>> getBarrios() async {
    try {
      final response = await http.get(Uri.parse('$baseUrl/barrios'));
      if (response.statusCode == 200) {
        List data = jsonDecode(utf8.decode(response.bodyBytes));
        return data.map((e) => Barrio.fromJson(e)).toList();
      }
      return [];
    } catch (e) {
      print("Error de conexion: $e");
      return [];
    }
  }

  static Future<bool> createBarrio(int id, String nombre) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/barrios'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'id': id, 'nombre': nombre}),
      );
      return response.statusCode == 200;
    } catch (e) {
      return false;
    }
  }

  static Future<bool> deleteBarrio(int id) async {
    try {
      final response = await http.delete(Uri.parse('$baseUrl/barrios/$id'));
      return response.statusCode == 200;
    } catch (e) {
      return false;
    }
  }
}
