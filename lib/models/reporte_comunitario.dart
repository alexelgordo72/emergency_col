class ReporteComunitario {
  final String id;
  final String titulo;
  final String descripcion;
  final String barrio;
  final String direccion;
  final int gravedad;
  final String estado;
  final double? latitud;
  final double? longitud;
  final Map<String, dynamic>? datosExtra;

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
  });

  factory ReporteComunitario.fromJson(Map<String, dynamic> json) {
    return ReporteComunitario(
      id: json['id'] ?? '',
      titulo: json['titulo'] ?? 'Sin título',
      descripcion: json['descripcion_detallada'] ?? '',
      barrio: json['sector_barrio'] ?? 'No especificado',
      direccion: json['direccion_referencia'] ?? '',
      gravedad: json['gravedad'] ?? 3,
      estado: json['estado'] ?? 'recibido',
      latitud: json['latitud'] != null ? double.tryParse(json['latitud'].toString()) : null,
      longitud: json['longitud'] != null ? double.tryParse(json['longitud'].toString()) : null,
      datosExtra: json['datos_extra'], 
    );
  }
}
