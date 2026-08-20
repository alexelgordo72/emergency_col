import 'package:emergency_col/services/dashboard_service.dart';

void main() async {
  print('🔄 Regenerando dashboard...');
  print('⏳ Esto puede tomar unos segundos...');
  
  final exito = await DashboardService.regenerarDashboard();
  
  if (exito) {
    print('✅ Dashboard regenerado exitosamente');
    print('📊 Verifica en la base de datos');
  } else {
    print('❌ Error al regenerar dashboard. Revisa los logs.');
  }
}
