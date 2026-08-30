import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/evento_model.dart';
import '../../config.dart';

class EventoService {
  static String get baseUrl => AppConfig.apiUrl;

  static Future<bool> crearEvento(EventoModel evento) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/reportes'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode(evento.toJson()),
      );
      return response.statusCode == 200 || response.statusCode == 201;
    } catch (e) {
      print('❌ Error al crear evento: $e');
      return false;
    }
  }

  static Future<bool> actualizarEvento(String id, EventoModel evento) async {
    try {
      final payload = <String, dynamic>{};
      if (evento.titulo.isNotEmpty) payload['titulo'] = evento.titulo;
      if (evento.descripcion.isNotEmpty) payload['descripcion_detallada'] = evento.descripcion;
      if (evento.barrio.isNotEmpty) payload['sector_barrio'] = evento.barrio;
      if (evento.direccion.isNotEmpty) payload['direccion_referencia'] = evento.direccion;
      if (evento.ciudadano.isNotEmpty || evento.cedula.isNotEmpty || evento.telefono.isNotEmpty) {
        payload['datos_extra'] = {};
        if (evento.ciudadano.isNotEmpty) payload['datos_extra']['ciudadano'] = evento.ciudadano;
        if (evento.cedula.isNotEmpty) payload['datos_extra']['cedula'] = evento.cedula;
        if (evento.telefono.isNotEmpty) payload['datos_extra']['telefono'] = evento.telefono;
        if (evento.prioridad.isNotEmpty) payload['datos_extra']['prioridad'] = evento.prioridad;
      }
      final response = await http.put(
        Uri.parse('$baseUrl/reportes/$id'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode(payload),
      );
      return response.statusCode == 200 || response.statusCode == 201;
    } catch (e) {
      print('❌ Error al actualizar evento: $e');
      return false;
    }
  }

  static Future<bool> eliminarEvento(String id) async {
    try {
      final response = await http.delete(
        Uri.parse('$baseUrl/reportes/$id'),
        headers: {'Content-Type': 'application/json'},
      );
      return response.statusCode == 200 || response.statusCode == 204;
    } catch (e) {
      print('❌ Error al eliminar evento: $e');
      return false;
    }
  }

  static Future<Map<String, String?>?> obtenerDatosRufe(String numeroRufe) async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/reportes?limit=10000'),
        headers: {'Content-Type': 'application/json'},
      );
      if (response.statusCode != 200) return null;
      final data = json.decode(response.body);
      final List list = data['data'] ?? [];
      Map<String, dynamic>? reporteData;
      for (var item in list) {
        final titulo = item['titulo'] ?? '';
        if (titulo.contains('RUFE #$numeroRufe') || titulo.contains('RUFE $numeroRufe')) {
          reporteData = item;
          break;
        }
      }
      if (reporteData == null) return null;
      final datosExtra = reporteData['datos_extra'] ?? {};
      final jefeHogar = datosExtra['jefe_hogar'] ?? {};
      String? ciudadano;
      String? cedula;
      String? barrio;
      String? descripcion;
      String? telefono;
      if (jefeHogar is Map) {
        final nombre = jefeHogar['nombre'] ?? '';
        final apellido = jefeHogar['apellido'] ?? '';
        if (nombre.isNotEmpty) ciudadano = nombre + (apellido.isNotEmpty ? ' $apellido' : '');
        if (jefeHogar['cedula'] != null) cedula = jefeHogar['cedula'].toString();
      }
      if (datosExtra['telefono'] != null) telefono = datosExtra['telefono'].toString();
      if (datosExtra['barrio'] != null) barrio = datosExtra['barrio'].toString();
      final evaluacionDanos = datosExtra['evaluacion_danos_edan'] ?? {};
      if (evaluacionDanos is Map) {
        final descTecnica = evaluacionDanos['descripcion_tecnica'] ?? '';
        if (descTecnica.toString().isNotEmpty) descripcion = descTecnica.toString();
      }
      if (descripcion == null || descripcion.isEmpty) {
        if (datosExtra['descripcion'] != null) descripcion = datosExtra['descripcion'].toString();
      }
      return {
        'ciudadano': ciudadano,
        'cedula': cedula,
        'barrio': barrio,
        'telefono': telefono,
        'descripcion': descripcion,
      };
    } catch (e) {
      print('❌ Error al obtener datos del RUFE: $e');
      return null;
    }
  }
}
