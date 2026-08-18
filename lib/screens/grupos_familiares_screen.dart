import 'package:flutter/material.dart';
import '../services/grupo_familiar_service.dart';

class GruposFamiliaresScreen extends StatefulWidget {
  const GruposFamiliaresScreen({Key? key}) : super(key: key);

  @override
  State<GruposFamiliaresScreen> createState() => _GruposFamiliaresScreenState();
}

class _GruposFamiliaresScreenState extends State<GruposFamiliaresScreen> {
  late Future<List<Map<String, dynamic>>> _gruposFuture;
  final TextEditingController _searchController = TextEditingController();
  bool _isSearching = false;
  Map<String, dynamic>? _grupoEncontrado;

  @override
  void initState() {
    super.initState();
    _gruposFuture = GrupoFamiliarService.obtenerTodosLosGrupos();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Grupos Familiares'),
        backgroundColor: Colors.red[700],
        foregroundColor: Colors.white,
        actions: [
          IconButton(
            icon: Icon(Icons.refresh),
            onPressed: () {
              setState(() {
                _gruposFuture = GrupoFamiliarService.obtenerTodosLosGrupos();
              });
            },
          ),
        ],
      ),
      body: Column(
        children: [
          Container(
            padding: EdgeInsets.all(16),
            color: Colors.white,
            child: Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _searchController,
                    decoration: InputDecoration(
                      hintText: 'Buscar por teléfono...',
                      border: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(8),
                      ),
                      prefixIcon: Icon(Icons.search, color: Colors.red[700]),
                    ),
                    onSubmitted: (value) async {
                      if (value.isNotEmpty) {
                        setState(() {
                          _isSearching = true;
                        });
                        final resultado = await GrupoFamiliarService.buscarPorTelefono(value);
                        setState(() {
                          _grupoEncontrado = resultado;
                          _isSearching = false;
                        });
                      }
                    },
                  ),
                ),
                SizedBox(width: 8),
                ElevatedButton(
                  onPressed: () {
                    setState(() {
                      _isSearching = false;
                      _grupoEncontrado = null;
                      _searchController.clear();
                    });
                  },
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.grey[300],
                    foregroundColor: Colors.black87,
                  ),
                  child: Text('Limpiar'),
                ),
              ],
            ),
          ),
          if (_grupoEncontrado != null && _grupoEncontrado!.isNotEmpty)
            _buildGrupoCard(_grupoEncontrado!),
          if (_grupoEncontrado == null)
            Expanded(
              child: FutureBuilder<List<Map<String, dynamic>>>(
                future: _gruposFuture,
                builder: (context, snapshot) {
                  if (snapshot.connectionState == ConnectionState.waiting) {
                    return Center(child: CircularProgressIndicator());
                  }
                  if (snapshot.hasError) {
                    return Center(child: Text('Error: ${snapshot.error}'));
                  }
                  if (!snapshot.hasData || snapshot.data!.isEmpty) {
                    return Center(child: Text('No hay grupos familiares con múltiples reportes'));
                  }
                  final grupos = snapshot.data!;
                  return ListView.builder(
                    padding: EdgeInsets.all(8),
                    itemCount: grupos.length,
                    itemBuilder: (context, index) {
                      final grupo = grupos[index];
                      return _buildGrupoCard(grupo);
                    },
                  );
                },
              ),
            ),
        ],
      ),
    );
  }

  Widget _buildGrupoCard(Map<String, dynamic> grupo) {
    final reportes = grupo['reportes'] as List<dynamic>? ?? [];
    final total = grupo['total_reportes'] ?? 0;
    final telefono = grupo['telefono'] ?? 'Sin teléfono';
    final ciudadanos = grupo['ciudadanos'] ?? '';

    return Card(
      margin: EdgeInsets.all(8),
      elevation: 2,
      child: ExpansionTile(
        leading: Container(
          width: 50,
          height: 50,
          decoration: BoxDecoration(
            color: Colors.purple[100],
            borderRadius: BorderRadius.circular(25),
          ),
          child: Center(
            child: Text(
              '$total',
              style: TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.bold,
                color: Colors.purple[800],
              ),
            ),
          ),
        ),
        title: Row(
          children: [
            Icon(Icons.family_restroom, color: Colors.purple[700]),
            SizedBox(width: 8),
            Expanded(
              child: Text(
                '👨‍👩‍👧‍👦 Grupo Familiar',
                style: TextStyle(fontWeight: FontWeight.bold),
              ),
            ),
          ],
        ),
        subtitle: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('📞 $telefono'),
            if (ciudadanos.isNotEmpty)
              Text('👤 $ciudadanos', style: TextStyle(fontSize: 12)),
            Text(
              '📄 $total reportes',
              style: TextStyle(fontSize: 12, color: Colors.grey[600]),
            ),
          ],
        ),
        children: [
          ...reportes.map((reporte) => ListTile(
            leading: CircleAvatar(
              backgroundColor: _getEstadoColor(reporte['estado']),
              child: Text(
                reporte['estado']?.substring(0, 1) ?? '?',
                style: TextStyle(color: Colors.white, fontSize: 12),
              ),
            ),
            title: Text(
              reporte['titulo'] ?? 'Sin título',
              style: TextStyle(fontWeight: FontWeight.w500),
            ),
            subtitle: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text('📍 ${reporte['barrio'] ?? 'Sin barrio'} - ${reporte['direccion'] ?? ''}'),
                Text('👤 ${reporte['ciudadano'] ?? 'Anónimo'}'),
              ],
            ),
            isThreeLine: true,
            trailing: Chip(
              label: Text(reporte['estado'] ?? 'Pendiente'),
              backgroundColor: _getEstadoColor(reporte['estado']).withOpacity(0.2),
            ),
          )).toList(),
        ],
      ),
    );
  }

  Color _getEstadoColor(String? estado) {
    if (estado == null) return Colors.grey;
    switch (estado.toLowerCase()) {
      case 'pendiente': return Colors.orange;
      case 'recibido': return Colors.blue;
      case 'en proceso': return Colors.cyan;
      case 'visitado sin prioridad': return Colors.grey;
      case 'visitado-de-prioridad baja': return Colors.green;
      case 'visitado-de-prioridad media': return Colors.orange;
      case 'visitado-de-prioridad alta': return Colors.red;
      default: return Colors.grey;
    }
  }
}
