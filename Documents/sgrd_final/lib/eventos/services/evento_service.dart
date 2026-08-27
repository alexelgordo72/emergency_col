import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:sgrd_final/config.dart';
import '../models/evento_model.dart';

class EventoService {
  static const String baseUrl = AppConfig.apiUrl;

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

  static Future<List<EventoModel>> obtenerEventos() async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/reportes?limit=10000'),
        headers: {'Content-Type': 'application/json'},
      );
      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        final List list = data['data'] ?? [];
        return list.map((item) => EventoModel.fromJson(item)).toList();
      }
      return [];
    } catch (e) {
      print('❌ Error al obtener eventos: $e');
      return [];
    }
  }

  static Future<bool> actualizarEvento(String id, EventoModel evento) async {
    try {
      final Map<String, dynamic> payload = {};
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

  static Future<EventoModel?> obtenerEvento(String id) async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/reportes/$id'),
        headers: {'Content-Type': 'application/json'},
      );
      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        return EventoModel.fromJson(data);
      }
      return null;
    } catch (e) {
      print('❌ Error al obtener evento: $e');
      return null;
    }
  }

  static Future<Map<String, String?>?> obtenerDatosRufe(String numeroRufe) async {
    try {
      print('🔍 Buscando datos para RUFE #$numeroRufe');
      
      // 1. Buscar el reporte que contiene el RUFE
      final response = await http.get(
        Uri.parse('$baseUrl/reportes?limit=10000'),
        headers: {'Content-Type': 'application/json'},
      );
      
      if (response.statusCode != 200) {
        print('❌ Error al obtener reportes: ${response.statusCode}');
        return null;
      }
      
      final data = json.decode(response.body);
      final List list = data['data'] ?? [];
      print('🔍 Revisando ${list.length} reportes...');
      
      Map<String, dynamic>? reporteData;
      for (var item in list) {
        final titulo = item['titulo'] ?? '';
        if (titulo.contains('RUFE #$numeroRufe') || titulo.contains('RUFE $numeroRufe')) {
          reporteData = item;
          print('✅ Encontrado reporte: $titulo');
          break;
        }
      }
      
      if (reporteData == null) {
        print('⚠️ No se encontró reporte con RUFE #$numeroRufe');
        return null;
      }
      
      // 2. Extraer datos del reporte
      final datosExtra = reporteData['datos_extra'] ?? {};
      
      String? ciudadano;
      String? cedula;
      String? barrio;
      String? descripcion;
      String? telefono;
      
      // === BUSCAR CIUDADANO Y CÉDULA en jefe_hogar ===
      final jefeHogar = datosExtra['jefe_hogar'] ?? {};
      if (jefeHogar is Map) {
        final nombre = jefeHogar['nombre'] ?? '';
        final apellido = jefeHogar['apellido'] ?? '';
        if (nombre.isNotEmpty) {
          ciudadano = nombre + (apellido.isNotEmpty ? ' $apellido' : '');
          print('✅ Ciudadano encontrado en jefe_hogar: $ciudadano');
        }
        if (jefeHogar['cedula'] != null && jefeHogar['cedula'].toString().isNotEmpty) {
          cedula = jefeHogar['cedula'].toString();
          print('✅ Cédula encontrada en jefe_hogar: $cedula');
        }
      }
      
      // === BUSCAR TELÉFONO ===
      if (datosExtra['telefono'] != null && datosExtra['telefono'].toString().isNotEmpty) {
        telefono = datosExtra['telefono'].toString();
        print('✅ Teléfono encontrado: $telefono');
      }
      
      // === BUSCAR BARRIO ===
      if (datosExtra['barrio'] != null && datosExtra['barrio'].toString().isNotEmpty) {
        barrio = datosExtra['barrio'].toString();
        print('✅ Barrio encontrado en datos_extra: $barrio');
      } else if (reporteData['sector_barrio'] != null && reporteData['sector_barrio'].toString().isNotEmpty) {
        barrio = reporteData['sector_barrio'].toString();
        print('✅ Barrio encontrado en sector_barrio: $barrio');
      }
      
      // === BUSCAR DESCRIPCIÓN ===
      // Primero en evaluacion_danos_edan
      final evaluacionDanos = datosExtra['evaluacion_danos_edan'] ?? {};
      if (evaluacionDanos is Map) {
        final descTecnica = evaluacionDanos['descripcion_tecnica'] ?? '';
        if (descTecnica.toString().isNotEmpty) {
          descripcion = descTecnica.toString();
          print('✅ Descripción encontrada en evaluacion_danos_edan');
        }
      }
      
      // Si no hay descripción, buscar en otros lugares
      if (descripcion == null || descripcion.isEmpty) {
        if (datosExtra['descripcion'] != null && datosExtra['descripcion'].toString().isNotEmpty) {
          descripcion = datosExtra['descripcion'].toString();
          print('✅ Descripción encontrada en datos_extra.descripcion');
        } else if (datosExtra['observaciones'] != null && datosExtra['observaciones'].toString().isNotEmpty) {
          descripcion = datosExtra['observaciones'].toString();
          print('✅ Descripción encontrada en datos_extra.observaciones');
        } else if (reporteData['descripcion_detallada'] != null && reporteData['descripcion_detallada'].toString().isNotEmpty) {
          descripcion = reporteData['descripcion_detallada'].toString();
          print('✅ Descripción encontrada en descripcion_detallada');
        }
      }
      
      // === Si no hay barrio, intentar extraer del título ===
      if (barrio == null || barrio.isEmpty) {
        final titulo = reporteData['titulo'] ?? '';
        final match = RegExp(r'\(([^)]+)\)$').firstMatch(titulo);
        if (match != null) {
          barrio = match.group(1)?.trim() ?? '';
          if (barrio.isNotEmpty) {
            print('✅ Barrio extraído del título: $barrio');
          }
        }
      }
      
      print('📝 Datos extraídos:');
      print('  👤 Ciudadano: $ciudadano');
      print('  🪪 Cédula: $cedula');
      print('  📍 Barrio: $barrio');
      print('  📱 Teléfono: $telefono');
      print('  📄 Descripción: ${descripcion?.substring(0, descripcion!.length > 50 ? 50 : descripcion.length)}...');
      
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

  static Future<String?> obtenerDescripcionRufe(String numeroRufe) async {
    final datos = await obtenerDatosRufe(numeroRufe);
    return datos?['descripcion'];
  }
}
