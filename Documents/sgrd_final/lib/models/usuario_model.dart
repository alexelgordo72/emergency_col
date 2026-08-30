class Usuario {
  final int id;
  final String usuario;
  final String rol;
  final String nombre;
  final String? email;

  Usuario({
    required this.id,
    required this.usuario,
    required this.rol,
    required this.nombre,
    this.email,
  });

  factory Usuario.fromJson(Map<String, dynamic> json) {
    return Usuario(
      id: json['id'] ?? 0,
      usuario: json['usuario'] ?? '',
      rol: json['rol'] ?? 'consulta',
      nombre: json['nombre'] ?? '',
      email: json['email'],
    );
  }

  bool get isAdmin => rol == 'administrador';
  bool get isConsulta => rol == 'consulta';
}
