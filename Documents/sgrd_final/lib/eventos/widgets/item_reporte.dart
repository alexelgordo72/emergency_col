import 'package:flutter/material.dart';
import 'package:sgrd_final/eventos/models/evento_model.dart';
import 'package:sgrd_final/eventos/screens/crear_evento_screen.dart';
import 'package:sgrd_final/eventos/services/evento_service.dart';

class ItemReporte extends StatefulWidget {
  final dynamic reporte;
  final VoidCallback onActualizar;

  const ItemReporte({Key? key, required this.reporte, required this.onActualizar})
      : super(key: key);

  @override
  _ItemReporteState createState() => _ItemReporteState();
}

class _ItemReporteState extends State<ItemReporte> {
  bool _eliminando = false;

  Future<void> _editar() async {
    final evento = EventoModel(
      id: widget.reporte['id'],
      titulo: widget.reporte['titulo'] ?? '',
      descripcion: widget.reporte['descripcion_detallada'] ?? '',
      barrio: widget.reporte['barrio'] ?? widget.reporte['sector_barrio'] ?? '',
      direccion: widget.reporte['direccion'] ?? widget.reporte['direccion_referencia'] ?? '',
      ciudadano: widget.reporte['ciudadano'] ?? '',
      cedula: widget.reporte['cedula'] ?? '',
      telefono: widget.reporte['telefono'] ?? '',
      prioridad: widget.reporte['prioridad'] ?? 'BAJA',
      estado: widget.reporte['estado'] ?? 'PENDIENTE',
    );

    final result = await showDialog<bool>(
      context: context,
      barrierDismissible: false,
      builder: (context) => CrearEventoScreen(eventoEditar: evento),
    );

    if (result == true) {
      widget.onActualizar();
    }
  }

  Future<void> _eliminar() async {
    final confirm = await showDialog<bool>(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Confirmar eliminación'),
        content: Text('¿Eliminar "${widget.reporte['titulo'] ?? 'este reporte'}"?'),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context, false),
            child: const Text('Cancelar'),
          ),
          TextButton(
            onPressed: () => Navigator.pop(context, true),
            style: TextButton.styleFrom(foregroundColor: Colors.red),
            child: const Text('Eliminar'),
          ),
        ],
      ),
    );

    if (confirm == true) {
      setState(() => _eliminando = true);
      try {
        final exito = await EventoService.eliminarEvento(widget.reporte['id']);
        if (exito) {
          if (mounted) {
            ScaffoldMessenger.of(context).showSnackBar(
              const SnackBar(content: Text('✅ Eliminado'), backgroundColor: Colors.green),
            );
            widget.onActualizar();
          }
        } else {
          if (mounted) {
            ScaffoldMessenger.of(context).showSnackBar(
              const SnackBar(content: Text('❌ Error al eliminar'), backgroundColor: Colors.red),
            );
          }
        }
      } catch (e) {
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text('❌ Error: $e'), backgroundColor: Colors.red),
          );
        }
      }
      setState(() => _eliminando = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    final estado = widget.reporte['estado'] ?? 'PENDIENTE';
    Color color = Colors.orange;
    if (estado.toUpperCase().contains('VISITADO')) {
      color = Colors.green;
    } else if (estado.toUpperCase().contains('VERIFICADO')) {
      color = Colors.blue;
    }

    return Card(
      margin: const EdgeInsets.symmetric(horizontal: 4, vertical: 2),
      child: ListTile(
        dense: true,
        contentPadding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
        title: Text(
          widget.reporte['titulo'] ?? 'Sin título',
          style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 12),
          overflow: TextOverflow.ellipsis,
          maxLines: 1,
        ),
        subtitle: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              widget.reporte['barrio'] ?? widget.reporte['sector_barrio'] ?? 'Sin barrio',
              style: const TextStyle(fontSize: 10),
              overflow: TextOverflow.ellipsis,
              maxLines: 1,
            ),
            Text(
              widget.reporte['ciudadano'] ?? 'Anónimo',
              style: const TextStyle(fontSize: 9),
              overflow: TextOverflow.ellipsis,
              maxLines: 1,
            ),
          ],
        ),
        trailing: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            // Estado
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
              decoration: BoxDecoration(
                color: color,
                borderRadius: BorderRadius.circular(6),
              ),
              child: Text(
                estado,
                style: const TextStyle(
                  color: Colors.white,
                  fontWeight: FontWeight.bold,
                  fontSize: 8,
                ),
              ),
            ),
            // Botón Editar
            IconButton(
              icon: const Icon(Icons.edit, size: 16, color: Colors.blue),
              onPressed: _eliminando ? null : _editar,
              tooltip: 'Editar',
              padding: EdgeInsets.zero,
              constraints: const BoxConstraints(),
            ),
            // Botón Eliminar
            IconButton(
              icon: _eliminando
                  ? const SizedBox(width: 16, height: 16, child: CircularProgressIndicator(strokeWidth: 2))
                  : const Icon(Icons.delete, size: 16, color: Colors.red),
              onPressed: _eliminando ? null : _eliminar,
              tooltip: 'Eliminar',
              padding: EdgeInsets.zero,
              constraints: const BoxConstraints(),
            ),
          ],
        ),
      ),
    );
  }
}
