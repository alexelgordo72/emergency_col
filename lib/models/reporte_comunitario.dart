class ReporteComunitario {
  final String id;
  final String titulo;
  final String descripcion;
  final String barrio;
  final String direccion;
  final int gravedad;
  String estado;  // ← CAMBIADO de 'final' a 'String' (mutable)
  final double? latitud;
  final double? longitud;
  final Map<String, dynamic>? datosExtra;
  final int? comuna;

  ReporteComunitario({
    required this.id,
    required this.titulo,
    required this.descripcion,
    required this.barrio,
    required this.direccion,
    required this.gravedad,
    required this.estado,
    this.latitud,
    this.longitud,
    this.datosExtra,
    this.comuna,
  });

  factory ReporteComunitario.fromJson(Map<String, dynamic> json) {
    return ReporteComunitario(
      id: json['id'] ?? '',
      titulo: json['titulo'] ?? 'Sin título',
      descripcion: json['descripcion_detallada'] ?? '',
      barrio: json['sector_barrio'] ?? 'No especificado',
      direccion: json['direccion_referencia'] ?? '',
      gravedad: json['gravedad'] ?? 3,
      estado: json['estado_actual'] ?? json['estado'] ?? 'recibido',
      latitud: json['latitud'] != null ? double.tryParse(json['latitud'].toString()) : null,
      longitud: json['longitud'] != null ? double.tryParse(json['longitud'].toString()) : null,
      comuna: json['comuna'] is int ? json['comuna'] : int.tryParse(json['comuna']?.toString() ?? '0'),
      datosExtra: json['datos_extra'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'titulo': titulo,
      'descripcion_detallada': descripcion,
      'sector_barrio': barrio,
      'direccion_referencia': direccion,
      'gravedad': gravedad,
      'estado_actual': estado,
      'latitud': latitud,
      'longitud': longitud,
      'comuna': comuna,
      'datos_extra': datosExtra,
    };
  }
}
