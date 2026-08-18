import 'package:flutter/material.dart';
import '../services/dashboard_generator.dart';

class GenerarDashboardScreen extends StatefulWidget {
  const GenerarDashboardScreen({Key? key}) : super(key: key);

  @override
  State<GenerarDashboardScreen> createState() => _GenerarDashboardScreenState();
}

class _GenerarDashboardScreenState extends State<GenerarDashboardScreen> {
  bool _generando = false;
  bool _guardado = false;
  int _totalReportes = 0;
  String _mensaje = '';
  Map<String, dynamic>? _dashboardData;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Generar Dashboard'),
        backgroundColor: Colors.red[700],
        foregroundColor: Colors.white,
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            const SizedBox(height: 20),
            Icon(
              Icons.dashboard,
              size: 80,
              color: Colors.red[700],
            ),
            const SizedBox(height: 16),
            Text(
              'Dashboard Agrupado',
              style: TextStyle(
                fontSize: 24,
                fontWeight: FontWeight.bold,
                color: Colors.grey[800],
              ),
            ),
            const SizedBox(height: 8),
            Text(
              'Genera el dashboard agrupando reportes por teléfono',
              style: TextStyle(fontSize: 14, color: Colors.grey[600]),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 32),
            SizedBox(
              width: double.infinity,
              height: 56,
              child: ElevatedButton(
                onPressed: _generando ? null : _generarDashboard,
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.red[700],
                  foregroundColor: Colors.white,
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(12),
                  ),
                ),
                child: _generando
                    ? Row(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          SizedBox(
                            width: 24,
                            height: 24,
                            child: CircularProgressIndicator(
                              color: Colors.white,
                              strokeWidth: 2,
                            ),
                          ),
                          SizedBox(width: 12),
                          Text('Generando dashboard...'),
                        ],
                      )
                    : Row(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Icon(Icons.refresh),
                          SizedBox(width: 8),
                          Text(_guardado ? 'Actualizar Dashboard' : 'Generar Dashboard'),
                        ],
                      ),
              ),
            ),
            const SizedBox(height: 16),
            SizedBox(
              width: double.infinity,
              height: 56,
              child: ElevatedButton.icon(
                onPressed: _dashboardData != null ? _verDashboard : null,
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.blue[700],
                  foregroundColor: Colors.white,
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(12),
                  ),
                ),
                icon: Icon(Icons.visibility),
                label: Text('Ver Dashboard Generado'),
              ),
            ),
            const SizedBox(height: 32),
            if (_mensaje.isNotEmpty)
              Container(
                padding: EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: _guardado ? Colors.green[50] : Colors.red[50],
                  borderRadius: BorderRadius.circular(12),
                  border: Border.all(
                    color: _guardado ? Colors.green : Colors.red,
                  ),
                ),
                child: Column(
                  children: [
                    Text(
                      _mensaje,
                      style: TextStyle(
                        color: _guardado ? Colors.green[800] : Colors.red[800],
                      ),
                    ),
                    if (_totalReportes > 0)
                      Text(
                        'Total reportes agrupados: $_totalReportes',
                        style: TextStyle(
                          fontWeight: FontWeight.bold,
                          fontSize: 18,
                          color: _guardado ? Colors.green[800] : Colors.red[800],
                        ),
                      ),
                  ],
                ),
              ),
          ],
        ),
      ),
    );
  }

  Future<void> _generarDashboard() async {
    setState(() {
      _generando = true;
      _mensaje = '';
      _guardado = false;
    });

    final resultado = await DashboardGenerator.generarDashboard();

    setState(() {
      _generando = false;
      if (resultado['success'] == true) {
        _guardado = true;
        _totalReportes = resultado['total_reportes'] ?? 0;
        _mensaje = '✅ Dashboard generado exitosamente';
        _dashboardData = resultado;
      } else {
        _guardado = false;
        _mensaje = '❌ Error: ${resultado['error'] ?? 'Desconocido'}';
        _totalReportes = 0;
      }
    });
  }

  void _verDashboard() {
    if (_dashboardData == null) return;
    
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: Text('Dashboard Agrupado'),
        content: Container(
          width: 500,
          height: 400,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                'Total reportes: ${_dashboardData!['total_reportes']}',
                style: TextStyle(fontWeight: FontWeight.bold),
              ),
              SizedBox(height: 8),
              Text(
                'Última actualización: ${_dashboardData!['fecha_actualizacion'] ?? 'N/A'}',
                style: TextStyle(fontSize: 12, color: Colors.grey),
              ),
              SizedBox(height: 16),
              Expanded(
                child: ListView.builder(
                  itemCount: (_dashboardData!['reportes'] as List?)?.length ?? 0,
                  itemBuilder: (context, index) {
                    final r = (_dashboardData!['reportes'] as List)[index];
                    return Card(
                      margin: EdgeInsets.only(bottom: 8),
                      child: ListTile(
                        leading: CircleAvatar(
                          backgroundColor: r['total_reportes_grupo'] > 1 
                              ? Colors.purple[100] 
                              : Colors.grey[200],
                          child: Text(
                            '${r['total_reportes_grupo']}',
                            style: TextStyle(
                              fontWeight: FontWeight.bold,
                              color: r['total_reportes_grupo'] > 1 
                                  ? Colors.purple[700] 
                                  : Colors.grey[600],
                            ),
                          ),
                        ),
                        title: Text(
                          r['titulo'] ?? 'Sin título',
                          style: TextStyle(fontWeight: FontWeight.w500),
                          maxLines: 1,
                          overflow: TextOverflow.ellipsis,
                        ),
                        subtitle: Text(
                          '📞 ${r['telefono'] ?? 'Sin teléfono'} | 📍 ${r['barrio'] ?? 'Sin barrio'}',
                          style: TextStyle(fontSize: 12),
                        ),
                        trailing: Chip(
                          label: Text(r['estado'] ?? 'Pendiente'),
                          backgroundColor: _getEstadoColor(r['estado']).withOpacity(0.2),
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
            child: Text('Cerrar'),
          ),
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
