class TrazabilidadItem {
  final int id;  // ← AGREGADO
  final String estadoAnterior;
  final String estadoNuevo;
  final String observacion;
  final String fechaCambio;
  final String usuario;

  TrazabilidadItem({
    required this.id,  // ← AGREGADO
    required this.estadoAnterior,
    required this.estadoNuevo,
    required this.observacion,
    required this.fechaCambio,
    required this.usuario,
  });

  factory TrazabilidadItem.fromJson(Map<String, dynamic> json) {
    String fechaRaw = json['fecha_cambio'] ?? '';
    String fechaLocal = fechaRaw;

    // Convertir de UTC (servidor) a hora local de Colombia
    if (fechaRaw.isNotEmpty) {
      try {
        if (!fechaRaw.endsWith('Z')) fechaRaw += 'Z';
        DateTime utcDate = DateTime.parse(fechaRaw);
        DateTime localDate = utcDate.toLocal();
        fechaLocal = localDate.toString().substring(0, 16);
      } catch (e) {
        fechaLocal = fechaRaw;
      }
    }

    return TrazabilidadItem(
      id: json['id'] ?? 0,  // ← AGREGADO
      estadoAnterior: json['estado_anterior'] ?? 'Inicial',
      estadoNuevo: json['estado_nuevo'] ?? '',
      observacion: json['observacion'] ?? '',
      fechaCambio: fechaLocal,
      usuario: json['usuario'] ?? 'Operador SGRD',
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,  // ← AGREGADO
      'estado_anterior': estadoAnterior,
      'estado_nuevo': estadoNuevo,
      'observacion': observacion,
      'fecha_cambio': fechaCambio,
      'usuario': usuario,
    };
  }
}
