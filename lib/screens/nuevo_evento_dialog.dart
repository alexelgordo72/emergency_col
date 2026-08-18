import 'package:flutter/material.dart';
import '../services/api_service.dart';
import '../services/barrio_service.dart';

class NuevoEventoDialog extends StatefulWidget {
  const NuevoEventoDialog({Key? key}) : super(key: key);

  @override
  State<NuevoEventoDialog> createState() => _NuevoEventoDialogState();
}

class _NuevoEventoDialogState extends State<NuevoEventoDialog> {
  final _formKey = GlobalKey<FormState>();
  final TextEditingController _tituloController = TextEditingController();
  final TextEditingController _direccionController = TextEditingController();
  final TextEditingController _ciudadanoController = TextEditingController();
  final TextEditingController _telefonoController = TextEditingController();
  
  String? _barrioSeleccionado;
  List<String> _barrios = [];
  bool _cargando = true;
  bool _guardando = false;

  @override
  void initState() {
    super.initState();
    _cargarBarrios();
  }

  Future<void> _cargarBarrios() async {
    try {
      final barrios = await BarrioService.getBarrios();
      setState(() {
        _barrios = barrios.map((b) => b.nombre).toList();
        _barrios.sort();
        _cargando = false;
      });
    } catch (e) {
      setState(() => _cargando = false);
    }
  }

  Future<void> _guardarEvento() async {
    if (!_formKey.currentState!.validate()) return;
    
    setState(() => _guardando = true);
    
    try {
      final datos = {
        'categoria_id': 2,
        'titulo': _tituloController.text.trim(),
        'descripcion_detallada': 'Reporte desde la app',
        'sector_barrio': _barrioSeleccionado?.toUpperCase() ?? '',
        'direccion_referencia': _direccionController.text.trim(),
        'latitud': 3.59,
        'longitud': -76.49,
        'datos_extra': {
          'ciudadano': _ciudadanoController.text.isNotEmpty ? _ciudadanoController.text.trim() : 'Anónimo',
          'telefono': _telefonoController.text.isNotEmpty ? _telefonoController.text.trim() : 'No registrado',
        }
      };
      
      final exito = await ApiService.crearReporte(datos);
      
      if (exito) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('✅ Evento registrado con éxito'), backgroundColor: Colors.green),
        );
        Navigator.pop(context, true);
      } else {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('❌ Error al registrar el evento'), backgroundColor: Colors.red),
        );
      }
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('❌ Error: $e'), backgroundColor: Colors.red),
      );
    } finally {
      setState(() => _guardando = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return AlertDialog(
      title: Row(
        children: [
          Icon(Icons.add_circle, color: Colors.red[700]),
          SizedBox(width: 8),
          Text('Nuevo Evento de Emergencia', style: TextStyle(fontSize: 18)),
        ],
      ),
      content: Container(
        width: 450,
        child: _cargando
            ? Center(child: CircularProgressIndicator())
            : Form(
                key: _formKey,
                child: SingleChildScrollView(
                  child: Column(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      TextFormField(
                        controller: _tituloController,
                        decoration: const InputDecoration(
                          labelText: 'Título / Asunto',
                          border: OutlineInputBorder(),
                          prefixIcon: Icon(Icons.title),
                        ),
                        validator: (value) {
                          if (value == null || value.isEmpty) {
                            return 'Ingrese un título';
                          }
                          return null;
                        },
                      ),
                      const SizedBox(height: 12),
                      DropdownButtonFormField<String>(
                        value: _barrioSeleccionado,
                        decoration: const InputDecoration(
                          labelText: 'Barrio',
                          border: OutlineInputBorder(),
                          prefixIcon: Icon(Icons.location_city),
                        ),
                        items: _barrios.map((barrio) {
                          return DropdownMenuItem(
                            value: barrio,
                            child: Text(barrio),
                          );
                        }).toList(),
                        onChanged: (value) {
                          setState(() => _barrioSeleccionado = value);
                        },
                        validator: (value) {
                          if (value == null || value.isEmpty) {
                            return 'Seleccione un barrio';
                          }
                          return null;
                        },
                      ),
                      const SizedBox(height: 12),
                      TextFormField(
                        controller: _direccionController,
                        decoration: const InputDecoration(
                          labelText: 'Dirección / Referencia',
                          border: OutlineInputBorder(),
                          prefixIcon: Icon(Icons.location_on),
                        ),
                      ),
                      const SizedBox(height: 12),
                      TextFormField(
                        controller: _ciudadanoController,
                        decoration: const InputDecoration(
                          labelText: 'Ciudadano Afectado',
                          border: OutlineInputBorder(),
                          prefixIcon: Icon(Icons.person),
                        ),
                      ),
                      const SizedBox(height: 12),
                      TextFormField(
                        controller: _telefonoController,
                        decoration: const InputDecoration(
                          labelText: 'Teléfono de Contacto',
                          border: OutlineInputBorder(),
                          prefixIcon: Icon(Icons.phone),
                        ),
                        keyboardType: TextInputType.phone,
                      ),
                    ],
                  ),
                ),
              ),
      ),
      actions: [
        TextButton(
          onPressed: () => Navigator.pop(context),
          child: Text('Cancelar', style: TextStyle(color: Colors.grey)),
        ),
        ElevatedButton(
          onPressed: _guardando ? null : _guardarEvento,
          style: ElevatedButton.styleFrom(
            backgroundColor: Colors.red[700],
            foregroundColor: Colors.white,
          ),
          child: _guardando
              ? Row(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    SizedBox(
                      width: 20,
                      height: 20,
                      child: CircularProgressIndicator(
                        color: Colors.white,
                        strokeWidth: 2,
                      ),
                    ),
                    SizedBox(width: 8),
                    Text('Guardando...'),
                  ],
                )
              : Text('Registrar Evento'),
        ),
      ],
    );
  }
}
