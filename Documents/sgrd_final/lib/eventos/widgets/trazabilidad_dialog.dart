import 'package:flutter/material.dart';
import 'package:sgrd_final/services/api_service.dart';
import 'package:sgrd_final/services/auth_service.dart';

class TrazabilidadDialog extends StatefulWidget {
  final String reporteId;

  const TrazabilidadDialog({Key? key, required this.reporteId}) : super(key: key);

  @override
  _TrazabilidadDialogState createState() => _TrazabilidadDialogState();
}

class _TrazabilidadDialogState extends State<TrazabilidadDialog> {
  Map<String, dynamic>? data;
  List<Map<String, dynamic>> estados = [];
  List<Map<String, dynamic>> visitas = [];
  bool _cargando = true;
  String? _error;
  String? _estadoSeleccionado;
  final TextEditingController _observacionController = TextEditingController();
  bool _cambiandoEstado = false;

  @override
  void initState() {
    super.initState();
    _cargarDatos();
  }

  @override
  void dispose() {
    _observacionController.dispose();
    super.dispose();
  }

  Future<void> _cargarDatos() async {
    setState(() {
      _cargando = true;
      _error = null;
    });

    try {
      print('🔍 Cargando trazabilidad para: ${widget.reporteId}');
      
      final trazabilidad = await ApiService.obtenerTrazabilidad(widget.reporteId);
      final estadosList = await ApiService.obtenerEstados();
      final visitasList = await ApiService.obtenerVisitas(widget.reporteId);

      print('📊 Visitas encontradas: ${visitasList.length}');

      setState(() {
        data = trazabilidad as Map<String, dynamic>?;
        estados = estadosList;
        visitas = visitasList;
        _cargando = false;
      });
    } catch (e) {
      print('❌ Error: $e');
      setState(() {
        _error = 'Error al cargar datos: $e';
        _cargando = false;
      });
    }
  }

  Future<void> _cambiarEstado() async {
    if (_estadoSeleccionado == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Selecciona un estado'), backgroundColor: Colors.orange),
      );
      return;
    }

    setState(() => _cambiandoEstado = true);

    try {
      final response = await ApiService.cambiarEstado(
        widget.reporteId,
        _estadoSeleccionado!,
        _observacionController.text,
      );

      if (response['message'] != null) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('✅ ${response['message']}'),
            backgroundColor: Colors.green,
          ),
        );
        await _cargarDatos();
        setState(() {
          _estadoSeleccionado = null;
          _observacionController.clear();
        });
      }
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('❌ Error: $e'), backgroundColor: Colors.red),
      );
    }

    setState(() => _cambiandoEstado = false);
  }

  @override
  Widget build(BuildContext context) {
    final width = MediaQuery.of(context).size.width * 0.85;
    final height = MediaQuery.of(context).size.height * 0.8;

    return Dialog(
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: Container(
        width: width > 900 ? 900 : width,
        height: height > 650 ? 650 : height,
        padding: const EdgeInsets.all(16),
        child: _cargando
            ? const Center(child: CircularProgressIndicator())
            : _error != null
                ? Center(child: Text(_error!))
                : Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        children: [
                          const Icon(Icons.timeline, size: 24, color: Colors.purple),
                          const SizedBox(width: 8),
                          const Text(
                            'Trazabilidad del Evento',
                            style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                          ),
                          const Spacer(),
                          IconButton(
                            icon: const Icon(Icons.close, size: 20),
                            padding: EdgeInsets.zero,
                            constraints: const BoxConstraints(),
                            onPressed: () => Navigator.pop(context),
                          ),
                        ],
                      ),
                      const Divider(height: 16),
                      Expanded(
                        child: Row(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Expanded(
                              flex: 3,
                              child: _buildInfoReporte(),
                            ),
                            const SizedBox(width: 12),
                            Expanded(
                              flex: 7,
                              child: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  _buildSelectorEstado(),
                                  const SizedBox(height: 8),
                                  Expanded(
                                    child: Row(
                                      children: [
                                        Expanded(
                                          flex: 5,
                                          child: _buildHistorial(),
                                        ),
                                        const SizedBox(width: 8),
                                        Expanded(
                                          flex: 5,
                                          child: _buildVisitas(),
                                        ),
                                      ],
                                    ),
                                  ),
                                ],
                              ),
                            ),
                          ],
                        ),
                      ),
                    ],
                  ),
      ),
    );
  }

  Widget _buildInfoReporte() {
    final reporte = data?['reporte'];
    if (reporte == null) return const SizedBox();

    return Container(
      padding: const EdgeInsets.all(8),
      decoration: BoxDecoration(
        color: Colors.grey[50],
        borderRadius: BorderRadius.circular(8),
        border: Border.all(color: Colors.grey[300]!),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            '📌 ${reporte['titulo'] ?? 'Sin título'}',
            style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 13),
            overflow: TextOverflow.ellipsis,
            maxLines: 2,
          ),
          const SizedBox(height: 8),
          _buildInfoRow('Estado', _getEstadoChip(reporte['estado_actual'] ?? 'PENDIENTE')),
          _buildInfoRow('Barrio', Text(reporte['barrio'] ?? 'N/A', style: const TextStyle(fontSize: 11))),
          _buildInfoRow('Dirección', Text(_truncate(reporte['direccion'] ?? 'N/A', 25), style: const TextStyle(fontSize: 11))),
          _buildInfoRow('Ciudadano', Text(reporte['datos_extra']?['ciudadano'] ?? 'Anónimo', style: const TextStyle(fontSize: 11))),
          _buildInfoRow('Teléfono', Text(reporte['datos_extra']?['telefono'] ?? 'No registra', style: const TextStyle(fontSize: 11))),
          if (reporte['descripcion'] != null && reporte['descripcion'].isNotEmpty)
            Padding(
              padding: const EdgeInsets.only(top: 4),
              child: Text(
                '📝 ${_truncate(reporte['descripcion'], 50)}',
                style: const TextStyle(fontSize: 10, color: Colors.grey),
              ),
            ),
        ],
      ),
    );
  }

  Widget _buildInfoRow(String label, Widget value) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 2),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          SizedBox(
            width: 55,
            child: Text(
              '$label:',
              style: const TextStyle(fontWeight: FontWeight.w500, fontSize: 11),
            ),
          ),
          Expanded(child: value),
        ],
      ),
    );
  }

  Widget _buildSelectorEstado() {
    final estadoActual = data?['reporte']?['estado_actual'] ?? '';

    return Container(
      padding: const EdgeInsets.all(8),
      decoration: BoxDecoration(
        color: Colors.grey[50],
        borderRadius: BorderRadius.circular(8),
        border: Border.all(color: Colors.grey[300]!),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text('🔄 Cambiar Estado', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 12)),
          const SizedBox(height: 6),
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 8),
            decoration: BoxDecoration(
              border: Border.all(color: Colors.grey[400]!),
              borderRadius: BorderRadius.circular(6),
            ),
            child: DropdownButtonHideUnderline(
              child: DropdownButton<String>(
                value: _estadoSeleccionado,
                hint: Text(
                  estadoActual,
                  style: TextStyle(
                    fontSize: 12,
                    color: _getColorForEstado(estadoActual),
                    fontWeight: FontWeight.w500,
                  ),
                ),
                isExpanded: true,
                icon: const Icon(Icons.arrow_drop_down, color: Colors.grey),
                items: estados.where((e) => e['nombre'] != estadoActual).map((estado) {
                  String nombre = estado['nombre'] ?? '';
                  String color = estado['color'] ?? '#FF9800';
                  return DropdownMenuItem<String>(
                    value: nombre,
                    child: Row(
                      children: [
                        Container(
                          width: 12,
                          height: 12,
                          decoration: BoxDecoration(
                            color: _hexToColor(color),
                            shape: BoxShape.circle,
                          ),
                        ),
                        const SizedBox(width: 8),
                        Text(nombre, style: const TextStyle(fontSize: 12)),
                      ],
                    ),
                  );
                }).toList(),
                onChanged: (value) {
                  setState(() {
                    _estadoSeleccionado = value;
                  });
                },
              ),
            ),
          ),
          const SizedBox(height: 6),
          Row(
            children: [
              Expanded(
                flex: 3,
                child: TextField(
                  controller: _observacionController,
                  decoration: const InputDecoration(
                    hintText: 'Observación...',
                    border: OutlineInputBorder(),
                    contentPadding: EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                    isDense: true,
                  ),
                  style: const TextStyle(fontSize: 11),
                  maxLines: 2,
                ),
              ),
              const SizedBox(width: 8),
              Expanded(
                flex: 1,
                child: ElevatedButton(
                  onPressed: _cambiandoEstado || _estadoSeleccionado == null ? null : _cambiarEstado,
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.blue,
                    foregroundColor: Colors.white,
                    padding: const EdgeInsets.symmetric(vertical: 8),
                    minimumSize: const Size(0, 32),
                  ),
                  child: _cambiandoEstado
                      ? const SizedBox(width: 16, height: 16, child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white))
                      : const Text('Aplicar', style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold)),
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildHistorial() {
    final historial = data?['historial'] ?? [];
    if (historial.isEmpty) {
      return Container(
        padding: const EdgeInsets.all(8),
        decoration: BoxDecoration(
          color: Colors.grey[50],
          borderRadius: BorderRadius.circular(8),
          border: Border.all(color: Colors.grey[300]!),
        ),
        child: const Center(
          child: Text('No hay cambios', style: TextStyle(fontSize: 11, color: Colors.grey)),
        ),
      );
    }

    return Container(
      padding: const EdgeInsets.all(8),
      decoration: BoxDecoration(
        color: Colors.grey[50],
        borderRadius: BorderRadius.circular(8),
        border: Border.all(color: Colors.grey[300]!),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text('📜 Historial', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 11)),
          const SizedBox(height: 4),
          Expanded(
            child: ListView.builder(
              itemCount: historial.length,
              itemBuilder: (context, index) {
                final item = historial[index];
                return _buildHistorialItem(item);
              },
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildHistorialItem(Map<String, dynamic> item) {
    return Container(
      margin: const EdgeInsets.only(bottom: 4),
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(4),
        border: Border.all(color: Colors.grey[200]!),
      ),
      child: Row(
        children: [
          Icon(Icons.timeline, size: 14, color: Colors.grey[600]),
          const SizedBox(width: 6),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  '${item['estado_anterior'] ?? 'Inicio'} → ${item['estado_nuevo']}',
                  style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 11),
                ),
                if (item['observacion'] != null && item['observacion'].isNotEmpty)
                  Text(
                    '💬 ${item['observacion']}',
                    style: TextStyle(fontSize: 10, color: Colors.grey[600]),
                  ),
                Text(
                  '👤 ${item['usuario'] ?? 'Sistema'} • ${_formatFecha(item['fecha_cambio'])}',
                  style: TextStyle(fontSize: 9, color: Colors.grey[500]),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildVisitas() {
    if (visitas.isEmpty) {
      return Container(
        padding: const EdgeInsets.all(8),
        decoration: BoxDecoration(
          color: Colors.grey[50],
          borderRadius: BorderRadius.circular(8),
          border: Border.all(color: Colors.grey[300]!),
        ),
        child: const Center(
          child: Text('🚶 Sin visitas de campo', style: TextStyle(fontSize: 11, color: Colors.grey)),
        ),
      );
    }

    return Container(
      padding: const EdgeInsets.all(8),
      decoration: BoxDecoration(
        color: Colors.grey[50],
        borderRadius: BorderRadius.circular(8),
        border: Border.all(color: Colors.grey[300]!),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              const Icon(Icons.person_pin_circle, size: 16, color: Colors.green),
              const SizedBox(width: 4),
              const Text('🚶 Visitas de Campo', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 11)),
              const Spacer(),
              Text(
                '${visitas.length} visita${visitas.length > 1 ? 's' : ''}',
                style: const TextStyle(fontSize: 10, color: Colors.grey),
              ),
            ],
          ),
          const SizedBox(height: 4),
          Expanded(
            child: ListView.builder(
              itemCount: visitas.length,
              itemBuilder: (context, index) {
                final visita = visitas[index];
                return _buildVisitaItem(visita);
              },
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildVisitaItem(Map<String, dynamic> visita) {
    Color estadoColor = Colors.grey;
    IconData estadoIcon = Icons.help_outline;

    switch (visita['codigo']?.toString().toUpperCase()) {
      case 'OK':
        estadoColor = Colors.green;
        estadoIcon = Icons.check_circle;
        break;
      case 'N.A':
      case 'N.C':
        estadoColor = Colors.orange;
        estadoIcon = Icons.warning_amber;
        break;
      case 'D.M':
        estadoColor = Colors.red;
        estadoIcon = Icons.error_outline;
        break;
      default:
        estadoColor = Colors.blue;
        estadoIcon = Icons.info_outline;
    }

    return Container(
      margin: const EdgeInsets.only(bottom: 4),
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(4),
        border: Border.all(color: Colors.grey[200]!),
      ),
      child: Row(
        children: [
          Icon(estadoIcon, size: 14, color: estadoColor),
          const SizedBox(width: 6),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  children: [
                    Text(
                      visita['ciudadano'] ?? 'Sin nombre',
                      style: const TextStyle(fontWeight: FontWeight.w500, fontSize: 10),
                    ),
                    const Spacer(),
                    Text(
                      _formatFecha(visita['fecha']),
                      style: const TextStyle(fontSize: 8, color: Colors.grey),
                    ),
                  ],
                ),
                if (visita['observaciones'] != null && visita['observaciones'].isNotEmpty)
                  Text(
                    '💬 ${visita['observaciones']}',
                    style: TextStyle(fontSize: 9, color: Colors.grey[600]),
                    overflow: TextOverflow.ellipsis,
                    maxLines: 1,
                  ),
                Row(
                  children: [
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 4, vertical: 1),
                      decoration: BoxDecoration(
                        color: estadoColor.withOpacity(0.2),
                        borderRadius: BorderRadius.circular(4),
                      ),
                      child: Text(
                        visita['codigo'] ?? 'N/A',
                        style: TextStyle(fontSize: 8, color: estadoColor, fontWeight: FontWeight.w500),
                      ),
                    ),
                    const SizedBox(width: 4),
                    if (visita['barrio'] != null && visita['barrio'].isNotEmpty)
                      Text(
                        '📍 ${visita['barrio']}',
                        style: const TextStyle(fontSize: 8, color: Colors.grey),
                      ),
                  ],
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  String _formatFecha(String? fecha) {
    if (fecha == null) return '';
    try {
      final date = DateTime.parse(fecha);
      return '${date.day}/${date.month} ${date.hour}:${date.minute.toString().padLeft(2, '0')}';
    } catch (e) {
      return fecha;
    }
  }

  String _truncate(String text, int maxLength) {
    if (text.length <= maxLength) return text;
    return '${text.substring(0, maxLength)}...';
  }

  Widget _getEstadoChip(String estado) {
    Color color = _getColorForEstado(estado);
    return Chip(
      label: Text(estado, style: const TextStyle(fontSize: 10, color: Colors.white)),
      backgroundColor: color,
      padding: EdgeInsets.zero,
      materialTapTargetSize: MaterialTapTargetSize.shrinkWrap,
      labelPadding: const EdgeInsets.symmetric(horizontal: 6),
    );
  }

  Color _getColorForEstado(String estado) {
    for (var e in estados) {
      if (e['nombre'] == estado) {
        return _hexToColor(e['color'] ?? '#FF9800');
      }
    }
    return Colors.grey;
  }

  Color _hexToColor(String hex) {
    hex = hex.replaceAll('#', '');
    if (hex.length == 6) {
      hex = 'FF$hex';
    }
    return Color(int.parse('0x$hex'));
  }
}
