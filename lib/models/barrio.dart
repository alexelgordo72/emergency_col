class Barrio {
  final int id;
  final String nombre;

  Barrio({required this.id, required this.nombre});

  factory Barrio.fromJson(Map<String, dynamic> json) {
    return Barrio(
      id: json['id'],
      nombre: json['nombre'] ?? '',
    );
  }
}
