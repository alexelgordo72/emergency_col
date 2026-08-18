class BarrioNormalizer {
  // Mapa de normalización (alias -> nombre canónico)
  static const Map<String, String> normalizacion = {
    'LA ESTANCIA': 'LA ESTANCIA',
    'ESTANCIA': 'LA ESTANCIA',
    'ESTANCIA VIEJA': 'LA ESTANCIA',
    'NUEVA ESTANCIA': 'LA ESTANCIA',
    'LA NUEVA ESTANCIA': 'LA ESTANCIA',
    'NUEVO HORIZONTE': 'NUEVO HORIZONTE',
    'NUEVO ORIZONTE': 'NUEVO HORIZONTE',
    'BELLAVISTA': 'BELLAVISTA',
    'BELLA VISTA': 'BELLAVISTA',
    'LAS VEGAS': 'LAS VEGAS',
    'VEGAS': 'LAS VEGAS',
    'BUENOS AIRES': 'BUENOS AIRES',
    'BUENOS AIRE': 'BUENOS AIRES',
    'PANORAMA': 'PANORAMA',
    'PANORAMAS': 'PANORAMA',
    'GUABINAS': 'GUABINAS',
    'GUABINA': 'GUABINAS',
    'BRISAS DEL CAMPESTRE': 'BRISAS DEL CAMPESTRE',
    'BRISAS CAMPESTRE': 'BRISAS DEL CAMPESTRE',
    'MONTAÑITAS': 'MONTAÑITAS',
    'MONTANITAS': 'MONTAÑITAS',
    'PEÑAS NEGRAS': 'PEÑAS NEGRAS',
    'PENAS NEGRAS': 'PEÑAS NEGRAS',
    'YUMBO GENERAL': 'YUMBO GENERAL',
    'YUMBO': 'YUMBO GENERAL',
    'BELALCAZAR': 'BELALCAZAR',
    'BOLIVAR': 'BOLIVAR',
    'BOLÍVAR': 'BOLIVAR',
    'URIBE': 'URIBE',
    'URIBE ALTA': 'URIBE',
    'GUACANDA': 'GUACANDA',
    'GUACANDAS': 'GUACANDA',
    'ARROYOHONDO': 'ARROYOHONDO',
    'ARROYO HONDO': 'ARROYOHONDO',
    'SANTA INES': 'SANTA INES',
    'SANTA INÉS': 'SANTA INES',
    'SAN FERNANDO': 'SAN FERNANDO',
    'VILLA INES': 'VILLA INES',
    'VILLA INÉS': 'VILLA INES',
    'CRUCES': 'CRUCES',
    'LAS CRUCES': 'CRUCES',
    'NO ESPECIFICADO': 'NO ESPECIFICADO',
    'SIN BARRIO': 'NO ESPECIFICADO',
    'NINGUNO': 'NO ESPECIFICADO',
    'CACIQUE JACINTO': 'CACIQUE JACINTO',
    'JACINTO': 'CACIQUE JACINTO',
    'EL CHOCHO': 'EL CHOCHO',
    'VEREDA EL PLACER': 'VEREDA EL PLACER',
    'LOS CHARCOS': 'LOS CHARCOS',
    'EL CORTIJO': 'EL CORTIJO',
    'EL FLORAL': 'EL FLORAL',
    'HACIENDA VERDE': 'HACIENDA VERDE',
    'JUAN PABLO': 'JUAN PABLO',
    'LA BALASTRERA': 'LA BALASTRERA',
    'LA COLINA': 'LA COLINA',
    'MIRADA': 'MIRADA',
    'MIRADOR PANORAMA': 'MIRADOR PANORAMA',
    'PORTALES DE COMFANDI': 'PORTALES DE COMFANDI',
    'RINCÓN DE DAPA': 'RINCÓN DE DAPA',
    'CORVIVALLE': 'CORVIVALLE',
    'SALAZAR': 'SALAZAR',
    'PASO DE LA TORRE': 'PASO DE LA TORRE',
    'CABECERA': 'CABECERA',
    'LA ARBOLEDA': 'LA ARBOLEDA',
    'LA PAZ': 'LA PAZ',
    'PUERTO ISAACS': 'PUERTO ISAACS',
    'YUMBILLO': 'YUMBILLO',
    'MENGA': 'MENGA',
    'FLOR DE MONTENEGRO': 'FLOR DE MONTENEGRO',
    'BRISAS DE LA SULTANA': 'BRISAS DE LA SULTANA',
    'VEREDA PILES': 'VEREDA PILES',
    'RURAL': 'RURAL',
    'SAN MARCOS': 'SAN MARCOS',
    'DAPA': 'DAPA',
    'MULALO': 'MULALO',
    'BUITRERA': 'BUITRERA',
  };

  // Mapa de comunas por barrio canónico
  static const Map<String, int> comunaPorBarrio = {
    'LAS VEGAS': 4,
    'MADRIGAL': 4,
    'BELLAVISTA': 1,
    'FRAY PEÑA': 2,
    'LLERAS': 4,
    'PIZARRO': 4,
    'GUADALUPE': 4,
    'BOLIVAR': 2,
    'URIBE': 2,
    'BUENOS AIRES': 3,
    'BELALCAZAR': 2,
    'NUEVO HORIZONTE': 3,
    'PEDREGAL': 3,
    'TRINIDAD': 3,
    'CAMPESTRE REAL': 4,
    'DIONISIO': 4,
    'AMERICAS': 1,
    'GUABINAS': 1,
    'PANORAMA': 1,
    'MULALO': 0,
    'BUITRERA': 0,
    'SAN MARCOS': 0,
    'DAPA': 0,
    'SANTA INES': 0,
    'PORTAL DE YUMBO': 1,
    'FLOR DE MONTENEGRO': 4,
    'SAN JORGE': 1,
    'VEREDA PILES': 0,
    'BRISAS DEL CAMPESTRE': 1,
    'ZONA INDUSTRIAL': 4,
    'SAN FERNANDO': 2,
    'GUACANDA': 3,
    'MONTAÑITAS': 0,
    'EL CHOCHO': 0,
    'CENCAR': 1,
    'MIRAVALLE': 0,
    'VEREDA EL PLACER': 0,
    'ARROYOHONDO': 3,
    'AY RIO': 3,
    'PEÑAS NEGRAS': 0,
    'BARICHARA': 1,
    'LOS CHARCOS': 0,
    'BRISAS DE LA SULTANA': 4,
    'CAS AMERICAS': 4,
    'CHOCHO': 2,
    'CRUCES': 2,
    'EL CORTIJO': 4,
    'EL FLORAL': 1,
    'ESTADIO': 2,
    'FINLANDIA': 4,
    'FLORIDA': 4,
    'HACIENDA VERDE': 3,
    'JUAN PABLO': 3,
    'LA BALASTRERA': 3,
    'LA COLINA': 1,
    'LA ESTANCIA': 1,
    'LAS CRUCES': 2,
    'MANGA VIEJA': 0,
    'MIRADA': 1,
    'MIRADOR PANORAMA': 1,
    'NO ESPECIFICADO': 0,
    'PORTALES DE COMFANDI': 2,
    'RINCÓN DE DAPA': 0,
    'RURAL': 0,
    'CORVIVALLE': 3,
    'YUMBO GENERAL': 0,
    'SALAZAR': 1,
    'PASO DE LA TORRE': 1,
    'CABECERA': 1,
    'LA ARBOLEDA': 1,
    'LA PAZ': 1,
    'PUERTO ISAACS': 1,
    'YUMBILLO': 0,
    'MENGA': 0,
    'CACIQUE JACINTO': 4,
    'VILLA INES': 4,
    'ESTANCIA VIEJA': 1,
    'VEREDA PEÑAS NEGRAS': 0,
  };

  static String normalizar(String barrio) {
    if (barrio.isEmpty) return 'NO ESPECIFICADO';
    
    final barrioUpper = barrio.toUpperCase().trim();
    
    for (var entry in normalizacion.entries) {
      if (barrioUpper == entry.key || barrioUpper.contains(entry.key)) {
        return entry.value;
      }
    }
    
    if (comunaPorBarrio.containsKey(barrioUpper)) {
      return barrioUpper;
    }
    
    return barrioUpper;
  }

  static int obtenerComuna(String barrio) {
    final normalizado = normalizar(barrio);
    return comunaPorBarrio[normalizado] ?? 0;
  }

  static List<String> getBarriosConocidos() {
    return comunaPorBarrio.keys.toList()..sort();
  }

  static int getComunaExacta(String barrio) {
    final barrioUpper = barrio.toUpperCase().trim();
    return comunaPorBarrio[barrioUpper] ?? 0;
  }
}
