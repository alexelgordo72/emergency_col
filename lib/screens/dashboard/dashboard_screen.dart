import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import '../../services/dashboard_service.dart';

class DashboardScreen extends StatefulWidget {
  const DashboardScreen({Key? key}) : super(key: key);

  @override
  State<DashboardScreen> createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen> {
  late Future<Map<String, dynamic>> _dashboardFuture;
  String _filtroPrioridad = 'TODAS';
  String _filtroComuna = 'TODAS';
  bool _isLoading = false;

  @override
  void initState() {
    super.initState();
    _cargarDashboard();
  }

  void _cargarDashboard() {
    setState(() {
      _isLoading = true;
      _dashboardFuture = DashboardService.getDashboardData(
        prioridad: _filtroPrioridad,
        comuna: _filtroComuna,
      ).then((data) {
        setState(() => _isLoading = false);
        return data;
      }).catchError((e) {
        setState(() => _isLoading = false);
        return {};
      });
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.grey[50],
      appBar: _buildAppBar(),
      body: FutureBuilder<Map<String, dynamic>>(
        future: _dashboardFuture,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return _buildLoadingState();
          }
          if (snapshot.hasError || !snapshot.hasData || snapshot.data!.isEmpty) {
            return _buildErrorState();
          }
          final data = snapshot.data!;
          return _buildDashboardContent(data);
        },
      ),
    );
  }

  PreferredSizeWidget _buildAppBar() {
    return AppBar(
      elevation: 0,
      backgroundColor: Colors.transparent,
      foregroundColor: Colors.red[700],
      title: Row(
        children: [
          Container(
            padding: EdgeInsets.all(8),
            decoration: BoxDecoration(
              color: Colors.red[700],
              borderRadius: BorderRadius.circular(12),
            ),
            child: Icon(Icons.dashboard, color: Colors.white, size: 24),
          ),
          SizedBox(width: 12),
          Text(
            'Dashboard SGRD',
            style: TextStyle(
              fontSize: 20,
              fontWeight: FontWeight.bold,
              color: Colors.grey[800],
            ),
          ),
        ],
      ),
      actions: [
        IconButton(
          icon: Icon(Icons.refresh, color: Colors.grey[600]),
          onPressed: _cargarDashboard,
          tooltip: 'Actualizar',
        ),
      ],
    );
  }

  Widget _buildLoadingState() {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Container(
            width: 60,
            height: 60,
            child: CircularProgressIndicator(
              strokeWidth: 3,
              color: Colors.red[700],
            ),
          ),
          SizedBox(height: 24),
          Text(
            'Cargando dashboard...',
            style: TextStyle(color: Colors.grey[600], fontSize: 14),
          ),
        ],
      ),
    );
  }

  Widget _buildErrorState() {
    return Center(
      child: Container(
        padding: EdgeInsets.all(32),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(Icons.error_outline, size: 64, color: Colors.red[300]),
            SizedBox(height: 16),
            Text(
              'Error al cargar el dashboard',
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Colors.grey[700]),
            ),
            SizedBox(height: 8),
            Text(
              'Verifica la conexión con el servidor',
              style: TextStyle(color: Colors.grey[500]),
            ),
            SizedBox(height: 24),
            ElevatedButton.icon(
              onPressed: _cargarDashboard,
              icon: Icon(Icons.refresh),
              label: Text('Reintentar'),
              style: ElevatedButton.styleFrom(
                backgroundColor: Colors.red[700],
                foregroundColor: Colors.white,
                padding: EdgeInsets.symmetric(horizontal: 32, vertical: 12),
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildDashboardContent(Map<String, dynamic> data) {
    return SingleChildScrollView(
      padding: EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          _buildFilters(),
          SizedBox(height: 16),
          _buildStatCards(data),
          SizedBox(height: 16),
          _buildCharts(data),
          SizedBox(height: 16),
          _buildReportList(data),
        ],
      ),
    );
  }

  Widget _buildFilters() {
    return Container(
      padding: EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(16),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.04),
            blurRadius: 8,
            offset: Offset(0, 2),
          ),
        ],
      ),
      child: Row(
        children: [
          Expanded(
            child: _buildFilterDropdown(
              value: _filtroPrioridad,
              items: ['TODAS', 'ALTA', 'MEDIA', 'BAJA'],
              label: 'Prioridad',
              onChanged: (value) {
                setState(() {
                  _filtroPrioridad = value!;
                  _cargarDashboard();
                });
              },
            ),
          ),
          SizedBox(width: 12),
          Expanded(
            child: FutureBuilder<Map<String, dynamic>>(
              future: _dashboardFuture,
              builder: (context, snapshot) {
                if (snapshot.hasData && snapshot.data!['comunas'] != null) {
                  final comunas = ['TODAS', ...?snapshot.data!['comunas']];
                  return _buildFilterDropdown(
                    value: _filtroComuna,
                    items: comunas,
                    label: 'Comuna',
                    onChanged: (value) {
                      setState(() {
                        _filtroComuna = value!;
                        _cargarDashboard();
                      });
                    },
                  );
                }
                return _buildFilterDropdown(
                  value: 'TODAS',
                  items: ['TODAS'],
                  label: 'Comuna',
                  onChanged: null,
                );
              },
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildFilterDropdown({
    required String value,
    required List<String> items,
    required String label,
    Function(String?)? onChanged,
  }) {
    return DropdownButtonFormField<String>(
      value: items.contains(value) ? value : items.first,
      decoration: InputDecoration(
        labelText: label,
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(10),
          borderSide: BorderSide(color: Colors.grey[300]!),
        ),
        enabledBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(10),
          borderSide: BorderSide(color: Colors.grey[300]!),
        ),
        focusedBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(10),
          borderSide: BorderSide(color: Colors.red[700]!, width: 2),
        ),
        contentPadding: EdgeInsets.symmetric(horizontal: 12, vertical: 4),
        isDense: true,
      ),
      items: items.map((item) {
        return DropdownMenuItem(
          value: item,
          child: Text(
            item,
            style: TextStyle(
              fontWeight: item == 'TODAS' ? FontWeight.bold : FontWeight.normal,
            ),
          ),
        );
      }).toList(),
      onChanged: onChanged,
      isDense: true,
    );
  }

  Widget _buildStatCards(Map<String, dynamic> data) {
    final stats = [
      {
        'title': 'Total Reportes',
        'value': '${data['total_reportes']}',
        'icon': Icons.assignment,
        'color': Colors.blue[700]!,
        'bgColor': Colors.blue[50]!,
      },
      {
        'title': 'Alta Prioridad',
        'value': '${data['prioridad_stats']?['ALTA'] ?? 0}',
        'icon': Icons.warning_amber_rounded,
        'color': Colors.red[700]!,
        'bgColor': Colors.red[50]!,
      },
      {
        'title': 'Comunas',
        'value': '${data['total_comunas']}',
        'icon': Icons.location_city,
        'color': Colors.green[700]!,
        'bgColor': Colors.green[50]!,
      },
      {
        'title': 'Tipos',
        'value': '${data['total_tipos']}',
        'icon': Icons.category,
        'color': Colors.purple[700]!,
        'bgColor': Colors.purple[50]!,
      },
    ];

    return GridView.builder(
      shrinkWrap: true,
      physics: NeverScrollableScrollPhysics(),
      gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
        crossAxisCount: 4,
        crossAxisSpacing: 12,
        mainAxisSpacing: 12,
        childAspectRatio: 1.2,
      ),
      itemCount: stats.length,
      itemBuilder: (context, index) {
        final stat = stats[index];
        return _buildStatCard(
          title: stat['title'] as String,
          value: stat['value'] as String,
          icon: stat['icon'] as IconData,
          color: stat['color'] as Color,
          bgColor: stat['bgColor'] as Color,
        );
      },
    );
  }

  Widget _buildStatCard({
    required String title,
    required String value,
    required IconData icon,
    required Color color,
    required Color bgColor,
  }) {
    return Container(
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(16),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.04),
            blurRadius: 8,
            offset: Offset(0, 2),
          ),
        ],
      ),
      padding: EdgeInsets.all(12),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Container(
            padding: EdgeInsets.all(8),
            decoration: BoxDecoration(
              color: bgColor,
              borderRadius: BorderRadius.circular(10),
            ),
            child: Icon(icon, color: color, size: 20),
          ),
          Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                value,
                style: TextStyle(
                  fontSize: 22,
                  fontWeight: FontWeight.bold,
                  color: Colors.grey[800],
                ),
              ),
              Text(
                title,
                style: TextStyle(
                  fontSize: 11,
                  color: Colors.grey[500],
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildCharts(Map<String, dynamic> data) {
    return Row(
      children: [
        Expanded(
          child: _buildPriorityChart(data),
        ),
        SizedBox(width: 12),
        Expanded(
          child: _buildComunaChart(data),
        ),
      ],
    );
  }

  Widget _buildPriorityChart(Map<String, dynamic> data) {
    final stats = data['prioridad_stats'] as Map<String, int>? ?? {};
    final total = stats.values.fold(0, (sum, val) => sum + val);
    
    final priorities = ['ALTA', 'MEDIA', 'BAJA'];
    final colors = [Colors.red, Colors.orange, Colors.green];
    final icons = [Icons.warning, Icons.info, Icons.check_circle];

    return Container(
      padding: EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(16),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.04),
            blurRadius: 8,
            offset: Offset(0, 2),
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Icon(Icons.pie_chart, size: 18, color: Colors.grey[600]),
              SizedBox(width: 8),
              Text(
                'Prioridad',
                style: TextStyle(
                  fontSize: 14,
                  fontWeight: FontWeight.bold,
                  color: Colors.grey[700],
                ),
              ),
            ],
          ),
          SizedBox(height: 12),
          ...priorities.asMap().entries.map((entry) {
            final index = entry.key;
            final prioridad = entry.value;
            final count = stats[prioridad] ?? 0;
            final percentage = total > 0 ? (count / total * 100) : 0;

            return Padding(
              padding: const EdgeInsets.only(bottom: 8),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      Icon(icons[index], size: 14, color: colors[index]),
                      SizedBox(width: 6),
                      Text(
                        prioridad,
                        style: TextStyle(
                          fontSize: 12,
                          fontWeight: FontWeight.w600,
                          color: Colors.grey[700],
                        ),
                      ),
                      Spacer(),
                      Text(
                        '$count',
                        style: TextStyle(
                          fontSize: 12,
                          fontWeight: FontWeight.bold,
                          color: Colors.grey[800],
                        ),
                      ),
                    ],
                  ),
                  SizedBox(height: 4),
                  ClipRRect(
                    borderRadius: BorderRadius.circular(6),
                    child: LinearProgressIndicator(
                      value: percentage / 100,
                      backgroundColor: Colors.grey[100],
                      color: colors[index],
                      minHeight: 6,
                    ),
                  ),
                ],
              ),
            );
          }).toList(),
        ],
      ),
    );
  }

  Widget _buildComunaChart(Map<String, dynamic> data) {
    final stats = data['comuna_stats'] as Map<String, int>? ?? {};
    final sorted = stats.entries.toList()
      ..sort((a, b) => b.value.compareTo(a.value));
    
    final topCommunes = sorted.take(5).toList();

    return Container(
      padding: EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(16),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.04),
            blurRadius: 8,
            offset: Offset(0, 2),
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Icon(Icons.location_on, size: 18, color: Colors.grey[600]),
              SizedBox(width: 8),
              Text(
                'Top Comunas',
                style: TextStyle(
                  fontSize: 14,
                  fontWeight: FontWeight.bold,
                  color: Colors.grey[700],
                ),
              ),
            ],
          ),
          SizedBox(height: 12),
          ...topCommunes.map((entry) {
            final total = stats.values.fold(0, (sum, val) => sum + val);
            final percentage = total > 0 ? (entry.value / total * 100) : 0;

            return Padding(
              padding: const EdgeInsets.only(bottom: 8),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      Text(
                        entry.key.length > 12 ? '${entry.key.substring(0, 12)}...' : entry.key,
                        style: TextStyle(
                          fontSize: 12,
                          fontWeight: FontWeight.w500,
                          color: Colors.grey[700],
                        ),
                      ),
                      Spacer(),
                      Text(
                        '${entry.value}',
                        style: TextStyle(
                          fontSize: 12,
                          fontWeight: FontWeight.bold,
                          color: Colors.grey[800],
                        ),
                      ),
                    ],
                  ),
                  SizedBox(height: 4),
                  ClipRRect(
                    borderRadius: BorderRadius.circular(6),
                    child: LinearProgressIndicator(
                      value: percentage / 100,
                      backgroundColor: Colors.grey[100],
                      color: Colors.blue[700],
                      minHeight: 6,
                    ),
                  ),
                ],
              ),
            );
          }).toList(),
        ],
      ),
    );
  }

  Widget _buildReportList(Map<String, dynamic> data) {
    final reportes = data['reportes'] as List<dynamic>? ?? [];

    if (reportes.isEmpty) {
      return Container(
        padding: EdgeInsets.all(32),
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(16),
        ),
        child: Center(
          child: Column(
            children: [
              Icon(Icons.inbox, size: 48, color: Colors.grey[300]),
              SizedBox(height: 8),
              Text(
                'No hay reportes con estos filtros',
                style: TextStyle(color: Colors.grey[500]),
              ),
            ],
          ),
        ),
      );
    }

    return Container(
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(16),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.04),
            blurRadius: 8,
            offset: Offset(0, 2),
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Padding(
            padding: EdgeInsets.all(16),
            child: Row(
              children: [
                Icon(Icons.list_alt, size: 18, color: Colors.grey[600]),
                SizedBox(width: 8),
                Text(
                  'Reportes Recientes',
                  style: TextStyle(
                    fontSize: 14,
                    fontWeight: FontWeight.bold,
                    color: Colors.grey[700],
                  ),
                ),
                Spacer(),
                Text(
                  '${reportes.length} reportes',
                  style: TextStyle(
                    fontSize: 12,
                    color: Colors.grey[500],
                  ),
                ),
              ],
            ),
          ),
          ListView.separated(
            shrinkWrap: true,
            physics: NeverScrollableScrollPhysics(),
            itemCount: reportes.length > 10 ? 10 : reportes.length,
            separatorBuilder: (context, index) => Divider(height: 1, color: Colors.grey[100]),
            itemBuilder: (context, index) {
              final r = reportes[index];
              return _buildReportItem(r);
            },
          ),
        ],
      ),
    );
  }

  Widget _buildReportItem(Map<String, dynamic> reporte) {
    final prioridad = reporte['prioridad']?.toString().toUpperCase() ?? 'BAJA';
    final color = _getPriorityColor(prioridad);
    
    return ListTile(
      contentPadding: EdgeInsets.symmetric(horizontal: 16, vertical: 4),
      leading: Container(
        width: 40,
        height: 40,
        decoration: BoxDecoration(
          color: color.withOpacity(0.1),
          borderRadius: BorderRadius.circular(10),
        ),
        child: Center(
          child: Text(
            prioridad.substring(0, 1),
            style: TextStyle(
              color: color,
              fontWeight: FontWeight.bold,
              fontSize: 14,
            ),
          ),
        ),
      ),
      title: Text(
        reporte['tipo_formulario'] ?? 'Sin título',
        style: TextStyle(
          fontWeight: FontWeight.w600,
          fontSize: 14,
          color: Colors.grey[800],
        ),
      ),
      subtitle: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            '${reporte['comuna_o_sector'] ?? 'Sin comuna'} • ${reporte['barrio_o_corregimiento'] ?? 'Sin barrio'}',
            style: TextStyle(fontSize: 12, color: Colors.grey[500]),
          ),
          Row(
            children: [
              Icon(Icons.person, size: 12, color: Colors.grey[400]),
              SizedBox(width: 4),
              Text(
                reporte['jefe_de_hogar'] ?? 'No registra',
                style: TextStyle(fontSize: 11, color: Colors.grey[500]),
              ),
              SizedBox(width: 12),
              Icon(Icons.phone, size: 12, color: Colors.grey[400]),
              SizedBox(width: 4),
              Text(
                reporte['telefono_contacto'] ?? 'N/A',
                style: TextStyle(fontSize: 11, color: Colors.grey[500]),
              ),
            ],
          ),
        ],
      ),
      trailing: Container(
        padding: EdgeInsets.symmetric(horizontal: 8, vertical: 4),
        decoration: BoxDecoration(
          color: color.withOpacity(0.1),
          borderRadius: BorderRadius.circular(8),
        ),
        child: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(
              Icons.person,
              size: 14,
              color: Colors.grey[500],
            ),
            SizedBox(width: 4),
            Text(
              '${reporte['total_personas_hogar'] ?? 0}',
              style: TextStyle(
                fontSize: 12,
                fontWeight: FontWeight.w600,
                color: Colors.grey[700],
              ),
            ),
          ],
        ),
      ),
      onTap: () {
        _showReportDetail(reporte);
      },
    );
  }

  Color _getPriorityColor(String prioridad) {
    switch (prioridad) {
      case 'ALTA':
        return Colors.red;
      case 'MEDIA':
        return Colors.orange;
      case 'BAJA':
        return Colors.green;
      default:
        return Colors.grey;
    }
  }

  void _showReportDetail(Map<String, dynamic> reporte) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: Text(
          reporte['tipo_formulario'] ?? 'Detalle del Reporte',
          style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
        ),
        content: SingleChildScrollView(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            mainAxisSize: MainAxisSize.min,
            children: [
              _buildDetailRow('Comuna', reporte['comuna_o_sector']),
              _buildDetailRow('Barrio', reporte['barrio_o_corregimiento']),
              _buildDetailRow('Prioridad', reporte['prioridad'], color: _getPriorityColor(reporte['prioridad'] ?? 'BAJA')),
              _buildDetailRow('Jefe de Hogar', reporte['jefe_de_hogar']),
              _buildDetailRow('Teléfono', reporte['telefono_contacto']),
              _buildDetailRow('Personas en Hogar', '${reporte['total_personas_hogar'] ?? 0}'),
              Divider(height: 24),
              if (reporte['observaciones_evaluador'] != null) ...[
                Text('Observaciones:', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 13)),
                SizedBox(height: 4),
                Text(reporte['observaciones_evaluador'], style: TextStyle(fontSize: 13)),
              ],
            ],
          ),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: Text('Cerrar', style: TextStyle(color: Colors.red[700])),
          ),
        ],
      ),
    );
  }

  Widget _buildDetailRow(String label, dynamic value, {Color? color}) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 4),
      child: Row(
        children: [
          Text(
            '$label: ',
            style: TextStyle(fontWeight: FontWeight.w600, fontSize: 13, color: Colors.grey[700]),
          ),
          Expanded(
            child: Text(
              value?.toString() ?? 'N/A',
              style: TextStyle(
                fontSize: 13,
                color: color ?? Colors.grey[800],
                fontWeight: color != null ? FontWeight.bold : FontWeight.normal,
              ),
            ),
          ),
        ],
      ),
    );
  }
}
