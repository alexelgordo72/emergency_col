import 'dart:convert';
import 'package:http/http.dart' as http;
import '../config.dart';

class EventoService {
  static const String baseUrl = AppConfig.apiUrl;

  static Future<bool> crearEvento(Map<String, dynamic> data) async {
    try {
      final url = '$baseUrl/reportes';
      
      print('📤 Creando evento en: $url');
      print('📤 Payload: $data');
      
      final response = await http.post(
        Uri.parse(url),
        headers: {'Content-Type': 'application/json'},
        body: json.encode(data),
      );
      
      print('📥 Status: ${response.statusCode}');
      print('📥 Response: ${response.body}');
      
      return response.statusCode == 200 || response.statusCode == 201;
    } catch (e) {
      print('❌ Error al crear evento: $e');
      return false;
    }
  }
}
