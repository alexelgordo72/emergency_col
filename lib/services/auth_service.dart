import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:sgrd_final/config.dart';

class AuthService {
  static const String baseUrl = AppConfig.apiUrl;
  static Map<String, dynamic>? currentUser;

  static Future<Map<String, dynamic>> login(String usuario, String contrasena) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/login'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode({
          'usuario': usuario,
          'contrasena': contrasena,
        }),
      );
      final data = json.decode(response.body);
      if (response.statusCode == 200 && data['success'] == true) {
        currentUser = data['data'];
        return {
          'success': true,
          'message': data['message'] ?? 'Login exitoso',
          'data': data['data'],
        };
      } else {
        return {
          'success': false,
          'message': data['message'] ?? 'Error al iniciar sesión',
        };
      }
    } catch (e) {
      return {
        'success': false,
        'message': 'Error de conexión: $e',
      };
    }
  }

  static void logout() {
    currentUser = null;
  }

  static bool isAuthenticated() {
    return currentUser != null;
  }

  static String getRole() {
    return currentUser?['rol'] ?? 'consulta';
  }

  static bool isAdmin() {
    return currentUser?['rol'] == 'administrador';
  }
}
