import 'package:flutter/material.dart';
import 'package:emergency_col/models/barrio.dart';
import 'package:emergency_col/services/barrio_service.dart';

class GestionBarriosDialog extends StatefulWidget {
  const GestionBarriosDialog({Key? key}) : super(key: key);

  @override
  _GestionBarriosDialogState createState() => _GestionBarriosDialogState();
}

class _GestionBarriosDialogState extends State<GestionBarriosDialog> {
  final _formKey = GlobalKey<FormState>();
  final _nombreController = TextEditingController();
  final _comunaController = TextEditingController();
  List<Barrio> _barrios = [];
  bool _cargando = true;

  @override
  void initState() {
    super.initState();
    _cargarBarrios();
  }

  Future<void> _cargarBarrios() async {
    setState(() => _cargando = true);
    try {
      final barrios = await BarrioService.getBarrios();
      setState(() {
        _barrios = barrios;
        _cargando = false;
      });
    } catch (e) {
      setState(() => _cargando = false);
      print('❌ Error cargando barrios: $e');
    }
  }

  Future<void> _crearBarrio() async {
    if (!_formKey.currentState!.validate()) return;

    final nombre = _nombreController.text.trim();
    final comuna = int.tryParse(_comunaController.text.trim()) ?? 0;

    try {
      final exito = await BarrioService.createBarrio(nombre, comuna);
      if (exito) {
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(content: Text('✅ Barrio creado exitosamente'), backgroundColor: Colors.green),
          );
          _nombreController.clear();
          _comunaController.clear();
          _cargarBarrios();
        }
      } else {
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(content: Text('❌ Error al crear el barrio'), backgroundColor: Colors.red),
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
  }

  Future<void> _eliminarBarrio(int id) async {
    final confirm = await showDialog<bool>(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Confirmar eliminación'),
        content: const Text('¿Estás seguro de eliminar este barrio?'),
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
      try {
        final exito = await BarrioService.deleteBarrio(id);
        if (exito) {
          if (mounted) {
            ScaffoldMessenger.of(context).showSnackBar(
              const SnackBar(content: Text('✅ Barrio eliminado'), backgroundColor: Colors.green),
            );
            _cargarBarrios();
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
    }
  }

  @override
  void dispose() {
    _nombreController.dispose();
    _comunaController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return AlertDialog(
      title: const Text('Gestionar Barrios'),
      content: SizedBox(
        width: 400,
        height: 400,
        child: Column(
          children: [
            Form(
              key: _formKey,
              child: Row(
                children: [
                  Expanded(
                    flex: 2,
                    child: TextFormField(
                      controller: _nombreController,
                      decoration: const InputDecoration(
                        labelText: 'Nombre *',
                        border: OutlineInputBorder(),
                      ),
                      validator: (value) => value?.isEmpty ?? true ? 'Campo requerido' : null,
                    ),
                  ),
                  const SizedBox(width: 8),
                  Expanded(
                    flex: 1,
                    child: TextFormField(
                      controller: _comunaController,
                      decoration: const InputDecoration(
                        labelText: 'Comuna *',
                        border: OutlineInputBorder(),
                      ),
                      keyboardType: TextInputType.number,
                      validator: (value) => value?.isEmpty ?? true ? 'Campo requerido' : null,
                    ),
                  ),
                  const SizedBox(width: 8),
                  ElevatedButton(
                    onPressed: _crearBarrio,
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.green,
                      foregroundColor: Colors.white,
                    ),
                    child: const Text('Agregar'),
                  ),
                ],
              ),
            ),
            const Divider(),
            const SizedBox(height: 8),
            Expanded(
              child: _cargando
                  ? const Center(child: CircularProgressIndicator())
                  : _barrios.isEmpty
                      ? const Center(child: Text('No hay barrios'))
                      : ListView.builder(
                          itemCount: _barrios.length,
                          itemBuilder: (context, index) {
                            final barrio = _barrios[index];
                            return ListTile(
                              title: Text(barrio.nombre),
                              subtitle: Text('Comuna: ${barrio.comuna ?? "Sin comuna"}'),
                              trailing: IconButton(
                                icon: const Icon(Icons.delete, color: Colors.red),
                                onPressed: () => _eliminarBarrio(barrio.id ?? 0),
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
          child: const Text('Cerrar'),
        ),
      ],
    );
  }
}
