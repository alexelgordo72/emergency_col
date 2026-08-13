class Barrio {
  final int id;
  final String nombre;
  final int comuna;

  Barrio({required this.id, required this.nombre, this.comuna = 0});

  factory Barrio.fromJson(Map<String, dynamic> json) {
    return Barrio(
      id: json['id'],
      nombre: json['nombre'],
      comuna: json['comuna'] ?? 0,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'nombre': nombre,
      'comuna': comuna,
    };
  }
}
