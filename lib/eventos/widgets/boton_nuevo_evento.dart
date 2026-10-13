import 'package:flutter/material.dart';
import 'package:sgrd_final/eventos/widgets/crear_reporte_dialog.dart';

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
        showDialog(
          context: context,
          barrierDismissible: false,
          builder: (context) => CrearReporteDialog(
            onCreado: onEventoCreado,
          ),
        );
      },
      backgroundColor: Colors.red[700],
      child: const Icon(Icons.add, color: Colors.white),
    );
  }
}
