class ReporteRuta {
  final String comuna;
  final String barrio;
  final int totalVisitas;
  final List<Visita> visitas;
  final List<String> observaciones;
  final DateTime fecha;

  ReporteRuta({
    required this.comuna,
    required this.barrio,
    required this.totalVisitas,
    required this.visitas,
    this.observaciones = const [],
    required this.fecha,
  });

  factory ReporteRuta.fromJson(Map<String, dynamic> json) {
    return ReporteRuta(
      comuna: json['comuna'] ?? 'Sin Comuna',
      barrio: json['barrio'] ?? 'Sin Barrio',
      totalVisitas: json['total_visitas'] ?? 0,
      visitas: (json['visitas'] as List?)
              ?.map((v) => Visita.fromJson(v))
              .toList() ??
          [],
      observaciones: List<String>.from(json['observaciones'] ?? []),
      fecha: DateTime.parse(json['fecha'] ?? DateTime.now().toIso8601String()),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'comuna': comuna,
      'barrio': barrio,
      'total_visitas': totalVisitas,
      'visitas': visitas.map((v) => v.toJson()).toList(),
      'observaciones': observaciones,
      'fecha': fecha.toIso8601String(),
    };
  }
}

class Visita {
  final String numero;
  final String asunto;
  final String direccion;
  final String ciudadano;
  final String telefono;

  Visita({
    required this.numero,
    required this.asunto,
    required this.direccion,
    required this.ciudadano,
    required this.telefono,
  });

  factory Visita.fromJson(Map<String, dynamic> json) {
    return Visita(
      numero: json['numero'] ?? '',
      asunto: json['asunto'] ?? '',
      direccion: json['direccion'] ?? '',
      ciudadano: json['ciudadano'] ?? '',
      telefono: json['telefono'] ?? '',
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'numero': numero,
      'asunto': asunto,
      'direccion': direccion,
      'ciudadano': ciudadano,
      'telefono': telefono,
    };
  }
}
