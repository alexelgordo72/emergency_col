import 'dart:convert';
import 'package:http/http.dart' as http;
import '../config.dart';

class DashboardGenerator {
  static String get baseUrl => AppConfig.apiUrl;

  static Future<Map<String, dynamic>> generarDashboard() async {
    try {
      print('📊 Obteniendo todos los reportes...');
      
      final response = await http.get(
        Uri.parse('$baseUrl/reportes?limit=3000'),
      ).timeout(Duration(seconds: 30));

      if (response.statusCode != 200) {
        return {'success': false, 'error': 'Error al obtener reportes: ${response.statusCode}'};
      }

      final data = json.decode(response.body);
      final reportes = data['data'] as List<dynamic>? ?? [];
      print('📊 Reportes obtenidos: ${reportes.length}');

      final Map<String, Map<String, dynamic>> grupos = {};

      for (var r in reportes) {
        final telefono = r['telefono'] ?? 'Sin teléfono';
        final telefonoLimpio = telefono.replaceAll(RegExp(r'[^0-9]'), '');
        
        if (telefonoLimpio.length < 7 || telefono == 'Sin teléfono') {
          final key = '${r['id']}_$telefono';
          if (!grupos.containsKey(key)) {
            grupos[key] = {
              'id': r['id'],
              'titulo': r['titulo'] ?? 'Sin título',
              'estado': r['estado'] ?? 'Pendiente',
              'fecha': r['fecha'] ?? '',
              'barrio': r['barrio'] ?? 'Sin barrio',
              'direccion': r['direccion'] ?? '',
              'latitud': r['latitud'],
              'longitud': r['longitud'],
              'descripcion': r['descripcion'] ?? '',
              'ciudadano': r['ciudadano'] ?? 'Anónimo',
              'telefono': telefono,
              'total_reportes_grupo': 1,
            };
          }
        } else {
          if (!grupos.containsKey(telefonoLimpio)) {
            grupos[telefonoLimpio] = {
              'id': r['id'],
              'titulo': r['titulo'] ?? 'Sin título',
              'estado': r['estado'] ?? 'Pendiente',
              'fecha': r['fecha'] ?? '',
              'barrio': r['barrio'] ?? 'Sin barrio',
              'direccion': r['direccion'] ?? '',
              'latitud': r['latitud'],
              'longitud': r['longitud'],
              'descripcion': r['descripcion'] ?? '',
              'ciudadano': r['ciudadano'] ?? 'Anónimo',
              'telefono': telefono,
              'total_reportes_grupo': 0,
            };
          }
          
          final grupo = grupos[telefonoLimpio]!;
          grupo['total_reportes_grupo'] = (grupo['total_reportes_grupo'] as int) + 1;
          
          final fechaActual = DateTime.tryParse(r['fecha'] ?? '');
          final fechaExistente = DateTime.tryParse(grupo['fecha'] ?? '');
          if (fechaActual != null && (fechaExistente == null || fechaActual.isAfter(fechaExistente))) {
            grupo['id'] = r['id'];
            grupo['titulo'] = r['titulo'];
            grupo['estado'] = r['estado'];
            grupo['fecha'] = r['fecha'];
            grupo['barrio'] = r['barrio'];
            grupo['direccion'] = r['direccion'];
            grupo['latitud'] = r['latitud'];
            grupo['longitud'] = r['longitud'];
            grupo['descripcion'] = r['descripcion'];
            grupo['ciudadano'] = r['ciudadano'];
          }
        }
      }

      final reportesAgrupados = grupos.values.map((g) {
        return {
          'id': g['id'],
          'titulo': g['titulo'] ?? 'Sin título',
          'estado': g['estado'] ?? 'Pendiente',
          'fecha': g['fecha'] ?? '',
          'barrio': g['barrio'] ?? 'Sin barrio',
          'direccion': g['direccion'] ?? '',
          'latitud': g['latitud'],
          'longitud': g['longitud'],
          'descripcion': g['descripcion'] ?? '',
          'ciudadano': g['ciudadano'] ?? 'Anónimo',
          'telefono': g['telefono'] ?? 'Sin teléfono',
          'total_reportes_grupo': g['total_reportes_grupo'] ?? 1,
        };
      }).toList();

      print('📊 Total grupos: ${reportesAgrupados.length}');

      // Guardar en el backend
      print('📤 Guardando dashboard...');
      final saveResponse = await http.post(
        Uri.parse('$baseUrl/dashboard/guardar'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode({'reportes': reportesAgrupados}),
      ).timeout(Duration(seconds: 30));

      if (saveResponse.statusCode == 200) {
        final result = json.decode(saveResponse.body);
        print('✅ Dashboard guardado: ${result['total_reportes']} reportes');
        return {
          'success': true,
          'total_reportes': result['total_reportes'],
          'reportes': reportesAgrupados,
          'fecha_actualizacion': DateTime.now().toIso8601String(),
        };
      } else {
        print('❌ Error al guardar: ${saveResponse.statusCode}');
        return {'success': false, 'error': 'Error al guardar dashboard'};
      }
    } catch (e) {
      print('❌ Error: $e');
      return {'success': false, 'error': e.toString()};
    }
  }
}
