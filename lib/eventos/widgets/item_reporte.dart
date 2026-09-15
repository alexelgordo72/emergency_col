import 'package:flutter/material.dart';
import 'package:sgrd_final/services/api_service.dart';

class ItemReporte extends StatefulWidget {
  final dynamic reporte;
  final VoidCallback onActualizar;

  const ItemReporte({
    Key? key,
    required this.reporte,
    required this.onActualizar,
  }) : super(key: key);

  @override
  State<ItemReporte> createState() => _ItemReporteState();
}

class _ItemReporteState extends State<ItemReporte> {
  bool _eliminando = false;

  Future<void> _eliminarReporte() async {
    final confirmar = await showDialog<bool>(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Eliminar Reporte'),
        content: const Text('¿Estás seguro de que deseas eliminar este reporte?'),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context, false),
            child: const Text('Cancelar'),
          ),
          TextButton(
            onPressed: () => Navigator.pop(context, true),
            child: const Text('Eliminar', style: TextStyle(color: Colors.red)),
          ),
        ],
      ),
    );

    if (confirmar == true && mounted) {
      setState(() => _eliminando = true);
      try {
        final id = widget.reporte['id'];
        // TODO: Implementar eliminar
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('🗑️ Reporte eliminado')),
        );
        widget.onActualizar();
      } catch (e) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Error: $e')),
        );
      } finally {
        if (mounted) setState(() => _eliminando = false);
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    final reporte = widget.reporte;
    final titulo = reporte['titulo'] ?? 'Sin título';
    final ciudadano = reporte['ciudadano'] ?? 'Anónimo';
    final telefono = reporte['telefono'] ?? 'N/A';
    final estado = reporte['estado'] ?? 'PENDIENTE';
    final barrio = reporte['sector_barrio'] ?? reporte['barrio'] ?? 'Sin barrio';
    final id = reporte['id'] ?? '';

    Color estadoColor = Colors.orange;
    if (estado.toUpperCase().contains('VISITADO')) {
      estadoColor = Colors.green;
    } else if (estado.toUpperCase().contains('VERIFICADO')) {
      estadoColor = Colors.blue;
    } else if (estado.toUpperCase().contains('CERRADO')) {
      estadoColor = Colors.grey;
    }

    return Card(
      margin: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
      child: Column(
        children: [
          ListTile(
            title: Text(
              titulo,
              style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 13),
              maxLines: 2,
              overflow: TextOverflow.ellipsis,
            ),
            subtitle: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text('👤 $ciudadano'),
                Text('📞 $telefono'),
                Text('📍 $barrio'),
              ],
            ),
            trailing: Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                // Botón Trazabilidad
                IconButton(
                  icon: const Icon(Icons.timeline, color: Colors.purple, size: 20),
                  onPressed: () {
                    ScaffoldMessenger.of(context).showSnackBar(
                      SnackBar(content: Text('📊 Trazabilidad de: $titulo')),
                    );
                  },
                  tooltip: 'Trazabilidad',
                ),
                // Botón Editar
                IconButton(
                  icon: const Icon(Icons.edit, color: Colors.blue, size: 20),
                  onPressed: () {
                    ScaffoldMessenger.of(context).showSnackBar(
                      SnackBar(content: Text('✏️ Editar: $titulo')),
                    );
                  },
                  tooltip: 'Editar',
                ),
                // Botón Eliminar
                IconButton(
                  icon: _eliminando
                      ? const SizedBox(
                          width: 20,
                          height: 20,
                          child: CircularProgressIndicator(strokeWidth: 2),
                        )
                      : const Icon(Icons.delete, color: Colors.red, size: 20),
                  onPressed: _eliminando ? null : _eliminarReporte,
                  tooltip: 'Eliminar',
                ),
                // Estado
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                  decoration: BoxDecoration(
                    color: estadoColor,
                    borderRadius: BorderRadius.circular(4),
                  ),
                  child: Text(
                    estado,
                    style: const TextStyle(
                      color: Colors.white,
                      fontSize: 10,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
