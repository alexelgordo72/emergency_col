class ReporteComunitario {
  final String id;
  final String titulo;
  String estado;  // Mutable para trazabilidad
  final String fecha;
  final String barrio;
  final String direccion;
  final String? ciudadano;
  final String? telefono;
  final String? descripcion;
  final double? latitud;
  final double? longitud;
  final int? comuna;
  final Map<String, dynamic>? datosExtra;

  ReporteComunitario({
    required this.id,
    required this.titulo,
    required this.estado,
    required this.fecha,
    required this.barrio,
    required this.direccion,
    this.ciudadano,
    this.telefono,
    this.descripcion,
    this.latitud,
    this.longitud,
    this.comuna,
    this.datosExtra,
  });

  factory ReporteComunitario.fromJson(Map<String, dynamic> json) {
    final datosExtra = json['datos_extra'] is Map ? json['datos_extra'] : null;
    
    return ReporteComunitario(
      id: json['id']?.toString() ?? '',
      titulo: json['titulo'] ?? 'Sin título',
      estado: json['estado'] ?? json['estado_actual'] ?? 'Pendiente',
      fecha: json['fecha'] ?? json['fecha_creacion'] ?? '',
      barrio: json['barrio'] ?? json['sector_barrio'] ?? 'Sin barrio',
      direccion: json['direccion'] ?? json['direccion_referencia'] ?? '',
      ciudadano: json['ciudadano'] ?? datosExtra?['ciudadano'],
      telefono: json['telefono'] ?? datosExtra?['telefono'],
      descripcion: json['descripcion'] ?? json['descripcion_detallada'],
      latitud: json['latitud']?.toDouble(),
      longitud: json['longitud']?.toDouble(),
      comuna: json['comuna'] ?? datosExtra?['comuna'],
      datosExtra: datosExtra,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'titulo': titulo,
      'estado': estado,
      'fecha': fecha,
      'barrio': barrio,
      'direccion': direccion,
      'ciudadano': ciudadano,
      'telefono': telefono,
      'descripcion': descripcion,
      'latitud': latitud,
      'longitud': longitud,
      'comuna': comuna,
      'datos_extra': datosExtra,
    };
  }
}
