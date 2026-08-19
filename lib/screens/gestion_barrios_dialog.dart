import 'package:flutter/material.dart';
import '../services/barrio_service.dart';
import '../models/barrio.dart';

class GestionBarriosDialog extends StatefulWidget {
  const GestionBarriosDialog({Key? key}) : super(key: key);

  @override
  State<GestionBarriosDialog> createState() => _GestionBarriosDialogState();
}

class _GestionBarriosDialogState extends State<GestionBarriosDialog> {
  List<Barrio> barrios = [];
  bool cargando = true;
  final TextEditingController _nombreController = TextEditingController();
  final TextEditingController _comunaController = TextEditingController();

  @override
  void initState() {
    super.initState();
    _cargarBarrios();
  }

  Future<void> _cargarBarrios() async {
    setState(() => cargando = true);
    try {
      final result = await BarrioService.getBarrios();
      setState(() {
        barrios = result;
        cargando = false;
      });
    } catch (e) {
      setState(() => cargando = false);
    }
  }

  Future<void> _crearBarrio() async {
    final nombre = _nombreController.text.trim().toUpperCase();
    final comuna = int.tryParse(_comunaController.text.trim()) ?? 0;

    if (nombre.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Ingrese el nombre del barrio'), backgroundColor: Colors.red),
      );
      return;
    }

    final exito = await BarrioService.createBarrio(nombre, comuna);
    if (exito) {
      _nombreController.clear();
      _comunaController.clear();
      await _cargarBarrios();
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Barrio creado exitosamente'), backgroundColor: Colors.green),
      );
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Error al crear el barrio'), backgroundColor: Colors.red),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return AlertDialog(
      title: const Text('Gestión de Barrios'),
      content: Container(
        width: 500,
        height: 400,
        child: Column(
          children: [
            // Formulario de creación
            Row(
              children: [
                Expanded(
                  flex: 2,
                  child: TextField(
                    controller: _nombreController,
                    decoration: const InputDecoration(
                      labelText: 'Nuevo Barrio',
                      border: OutlineInputBorder(),
                    ),
                  ),
                ),
                SizedBox(width: 8),
                Expanded(
                  flex: 1,
                  child: TextField(
                    controller: _comunaController,
                    decoration: const InputDecoration(
                      labelText: 'Comuna',
                      border: OutlineInputBorder(),
                    ),
                    keyboardType: TextInputType.number,
                  ),
                ),
                SizedBox(width: 8),
                ElevatedButton(
                  onPressed: _crearBarrio,
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.green[700],
                    foregroundColor: Colors.white,
                  ),
                  child: const Text('Agregar'),
                ),
              ],
            ),
            SizedBox(height: 12),
            // Lista de barrios
            Expanded(
              child: cargando
                  ? const Center(child: CircularProgressIndicator())
                  : barrios.isEmpty
                      ? const Center(child: Text('No hay barrios registrados'))
                      : ListView.builder(
                          itemCount: barrios.length,
                          itemBuilder: (context, index) {
                            final barrio = barrios[index];
                            return Card(
                              margin: const EdgeInsets.only(bottom: 4),
                              child: ListTile(
                                title: Text(barrio.nombre),
                                subtitle: Text('Comuna ${barrio.comuna}'),
                                trailing: Row(
                                  mainAxisSize: MainAxisSize.min,
                                  children: [
                                    IconButton(
                                      icon: const Icon(Icons.delete, color: Colors.red),
                                      onPressed: () async {
                                        final confirm = await showDialog<bool>(
                                          context: context,
                                          builder: (context) => AlertDialog(
                                            title: const Text('Eliminar Barrio'),
                                            content: Text('¿Eliminar ${barrio.nombre}?'),
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
                                        if (confirm == true) {
                                          final exito = await BarrioService.deleteBarrio(barrio.id);
                                          if (exito) {
                                            await _cargarBarrios();
                                            ScaffoldMessenger.of(context).showSnackBar(
                                              const SnackBar(content: Text('Barrio eliminado'), backgroundColor: Colors.green),
                                            );
                                          }
                                        }
                                      },
                                    ),
                                  ],
                                ),
                              ),
                            );
                          },
                        ),
            ),
          ],
        ),
      ),
      actions: [
        TextButton(
          onPressed: () => Navigator.pop(context),
          child: const Text('Cerrar', style: TextStyle(color: Colors.red)),
        ),
      ],
    );
  }
}
