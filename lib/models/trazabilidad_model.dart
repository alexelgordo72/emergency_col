class TrazabilidadItem {
  final String estadoAnterior;
  final String estadoNuevo;
  final String observacion;
  final String fechaCambio;
  final String usuario;

  TrazabilidadItem({
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
        // Asegurarnos de que Flutter sepa que es UTC agregando la 'Z'
        if (!fechaRaw.endsWith('Z')) fechaRaw += 'Z';
        DateTime utcDate = DateTime.parse(fechaRaw);
        DateTime localDate = utcDate.toLocal(); // Convierte a la zona horaria del dispositivo
        // Cortar para mostrar solo YYYY-MM-DD HH:MM
        fechaLocal = localDate.toString().substring(0, 16);
      } catch (e) {
        fechaLocal = fechaRaw; // Si hay error de formato, muestra la original
      }
    }

    return TrazabilidadItem(
      estadoAnterior: json['estado_anterior'] ?? 'Inicial',
      estadoNuevo: json['estado_nuevo'] ?? '',
      observacion: json['observacion'] ?? '',
      fechaCambio: fechaLocal,
      usuario: json['usuario'] ?? 'Operador SGRD',
    );
  }
}
