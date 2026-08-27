class EventoModel {
  final String? id;
  final String titulo;
  final String descripcion;
  final String barrio;
  final String direccion;
  final String ciudadano;
  final String cedula;
  final String telefono;
  final String prioridad;
  final String estado;
  final String fechaCreacion;

  EventoModel({
    this.id,
    required this.titulo,
    required this.descripcion,
    required this.barrio,
    required this.direccion,
    required this.ciudadano,
    required this.cedula,
    required this.telefono,
    required this.prioridad,
    this.estado = 'PENDIENTE',
    this.fechaCreacion = '',
  });

  Map<String, dynamic> toJson() {
    return {
      'titulo': titulo,
      'descripcion_detallada': descripcion,
      'sector_barrio': barrio,
      'direccion_referencia': direccion,
      'estado': estado,
      'datos_extra': {
        'ciudadano': ciudadano,
        'cedula': cedula,
        'telefono': telefono,
        'prioridad': prioridad,
        'fuente_origen': 'Nuevo Evento SGRD',
      },
    };
  }

  factory EventoModel.fromJson(Map<String, dynamic> json) {
    final datosExtra = json['datos_extra'] ?? {};
    return EventoModel(
      id: json['id'],
      titulo: json['titulo'] ?? '',
      descripcion: json['descripcion_detallada'] ?? '',
      barrio: json['sector_barrio'] ?? '',
      direccion: json['direccion_referencia'] ?? '',
      ciudadano: datosExtra['ciudadano'] ?? '',
      cedula: datosExtra['cedula'] ?? '',
      telefono: datosExtra['telefono'] ?? '',
      prioridad: datosExtra['prioridad'] ?? 'SIN PRIORIDAD',
      estado: json['estado'] ?? 'PENDIENTE',
      fechaCreacion: json['fecha_creacion'] ?? '',
    );
  }
}
