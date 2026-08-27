import 'dart:convert';
import 'package:http/http.dart' as http;
import '../config.dart';

class ApiService {
  static const String baseUrl = AppConfig.apiUrl;

  static Future<Map<String, dynamic>> obtenerReportes({
    int limit = 10000,
    int offset = 0,
    String? barrio,
    String? nombre,
    String? telefono,
  }) async {
    try {
      final queryParams = <String, String>{
        'limit': limit.toString(),
        'offset': offset.toString(),
      };
      
      if (barrio != null && barrio.isNotEmpty) queryParams['barrio'] = barrio;
      if (nombre != null && nombre.isNotEmpty) queryParams['nombre'] = nombre;
      if (telefono != null && telefono.isNotEmpty) queryParams['telefono'] = telefono;

      final uri = Uri.parse('$baseUrl/reportes').replace(queryParameters: queryParams);
      final response = await http.get(
        uri,
        headers: {'Content-Type': 'application/json'},
      );

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        return {
          'data': data['data'] ?? [],
          'total': data['total'] ?? 0,
        };
      }
      return {'data': [], 'total': 0};
    } catch (e) {
      print('❌ Error: $e');
      return {'data': [], 'total': 0};
    }
  }
}
