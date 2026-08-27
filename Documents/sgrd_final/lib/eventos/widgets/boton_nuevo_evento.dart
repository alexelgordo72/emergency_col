import 'package:flutter/material.dart';
import 'package:sgrd_final/eventos/screens/crear_evento_screen.dart';

class BotonNuevoEvento extends StatelessWidget {
  final VoidCallback? onEventoCreado;

  const BotonNuevoEvento({Key? key, this.onEventoCreado}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return FloatingActionButton(
      onPressed: () async {
        final result = await showDialog<bool>(
          context: context,
          barrierDismissible: false,
          builder: (context) => const CrearEventoScreen(),
        );
        if (result == true && onEventoCreado != null) {
          onEventoCreado!();
        }
      },
      backgroundColor: Colors.red[700],
      child: const Icon(Icons.add, color: Colors.white),
      tooltip: 'Nuevo Evento',
      mini: true,
    );
  }
}
