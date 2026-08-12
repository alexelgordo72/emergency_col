import 'package:flutter/material.dart';
import '../models/barrio.dart';
import '../services/barrio_service.dart';

class GestionBarriosDialog extends StatefulWidget {
  const GestionBarriosDialog({Key? key}) : super(key: key);

  @override
  _GestionBarriosDialogState createState() => _GestionBarriosDialogState();
}

class _GestionBarriosDialogState extends State<GestionBarriosDialog> {
  List<Barrio> barrios = [];
  bool cargando = true;
  final TextEditingController _idController = TextEditingController();
  final TextEditingController _nombreController = TextEditingController();

  @override
  void initState() {
    super.initState();
    _cargarBarrios();
  }

  Future<void> _cargarBarrios() async {
    setState(() => cargando = true);
    barrios = await BarrioService.getBarrios();
    setState(() => cargando = false);
  }

  Future<void> _guardarBarrio([Barrio? barrioExistente]) async {
    if (barrioExistente != null) {
      _idController.text = barrioExistente.id.toString();
      _nombreController.text = barrioExistente.nombre;
    } else {
      _idController.clear();
      _nombreController.clear();
    }

    await showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: Text(barrioExistente == null ? 'Nuevo Barrio' : 'Editar Barrio'),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            TextField(
              controller: _idController,
              decoration: const InputDecoration(labelText: 'ID del Barrio (Ej: 1, 2, 3)'),
              keyboardType: TextInputType.number,
              // Si estamos editando, no permitimos cambiar el ID para no dañar la BD
              enabled: barrioExistente == null, 
            ),
            const SizedBox(height: 10),
            TextField(
              controller: _nombreController,
              decoration: const InputDecoration(labelText: 'Nombre del Barrio'),
              autofocus: barrioExistente == null ? false : true,
            ),
          ],
        ),
        actions: [
          TextButton(onPressed: () => Navigator.pop(context), child: const Text('Cancelar', style: TextStyle(color: Colors.grey))),
          ElevatedButton(
            style: ElevatedButton.styleFrom(backgroundColor: Colors.blue[800]),
            onPressed: () async {
              int? idParseado = int.tryParse(_idController.text);
              if (idParseado == null || _nombreController.text.isEmpty) {
                ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('ID inválido o nombre vacío'), backgroundColor: Colors.red));
                return;
              }
              
              bool exito = await BarrioService.createBarrio(idParseado, _nombreController.text);
              if (exito) {
                Navigator.pop(context);
                _cargarBarrios();
              }
            },
            child: const Text('Guardar', style: TextStyle(color: Colors.white)),
          )
        ],
      ),
    );
  }

  Future<void> _eliminarBarrio(int id) async {
    bool confirmar = await showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Confirmar'),
        content: const Text('¿Eliminar este barrio definitivamente?'),
        actions: [
          TextButton(onPressed: () => Navigator.pop(context, false), child: const Text('Cancelar', style: TextStyle(color: Colors.grey))),
          ElevatedButton(
            style: ElevatedButton.styleFrom(backgroundColor: Colors.red),
            onPressed: () => Navigator.pop(context, true), 
            child: const Text('Eliminar', style: TextStyle(color: Colors.white)),
          )
        ],
      ),
    );

    if (confirmar) {
      await BarrioService.deleteBarrio(id);
      _cargarBarrios();
    }
  }

  @override
  Widget build(BuildContext context) {
    return Dialog(
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: Container(
        width: 600,
        height: 700,
        padding: const EdgeInsets.all(24),
        child: Column(
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                const Text('Gestión de Barrios', style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold)),
                IconButton(icon: const Icon(Icons.close), onPressed: () => Navigator.pop(context)),
              ],
            ),
            const Divider(thickness: 2),
            Row(
              children: [
                Expanded(
                  child: ElevatedButton.icon(
                    style: ElevatedButton.styleFrom(backgroundColor: Colors.blue[800], foregroundColor: Colors.white),
                    icon: const Icon(Icons.add_location_alt),
                    label: const Text('Agregar Nuevo Barrio'),
                    onPressed: () => _guardarBarrio(),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 15),
            Expanded(
              child: cargando
                  ? const Center(child: CircularProgressIndicator())
                  : (barrios.isEmpty 
                      ? const Center(child: Text('No hay barrios registrados. Agrega el primero.'))
                      : ListView.builder(
                          itemCount: barrios.length,
                          itemBuilder: (context, index) {
                            final b = barrios[index];
                            return Card(
                              child: ListTile(
                                leading: CircleAvatar(
                                  backgroundColor: Colors.blue[100],
                                  child: Text(b.id.toString(), style: TextStyle(fontWeight: FontWeight.bold, color: Colors.blue[900])),
                                ),
                                title: Text(b.nombre, style: const TextStyle(fontWeight: FontWeight.bold)),
                                trailing: Row(
                                  mainAxisSize: MainAxisSize.min,
                                  children: [
                                    IconButton(icon: const Icon(Icons.edit, color: Colors.blue), onPressed: () => _guardarBarrio(b)),
                                    IconButton(icon: const Icon(Icons.delete, color: Colors.red), onPressed: () => _eliminarBarrio(b.id)),
                                  ],
                                ),
                              ),
                            );
                          },
                        )),
            ),
          ],
        ),
      ),
    );
  }
}
