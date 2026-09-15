import 'package:flutter/material.dart';

class BotonNuevoEvento extends StatelessWidget {
  final VoidCallback onEventoCreado;

  const BotonNuevoEvento({
    Key? key,
    required this.onEventoCreado,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return FloatingActionButton(
      onPressed: () {
        // TODO: Implementar creación de evento
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('📝 Crear nuevo evento')),
        );
      },
      backgroundColor: Colors.red[700],
      child: const Icon(Icons.add, color: Colors.white),
    );
  }
}
