# sgrd_final

A new Flutter project.

## Getting Started

This project is a starting point for a Flutter application.

A few resources to get you started if this is your first Flutter project:

- [Learn Flutter](https://docs.flutter.dev/get-started/learn-flutter)
- [Write your first Flutter app](https://docs.flutter.dev/get-started/codelab)
- [Flutter learning resources](https://docs.flutter.dev/reference/learning-resources)

For help getting started with Flutter development, view the
[online documentation](https://docs.flutter.dev/), which offers tutorials,
samples, guidance on mobile development, and a full API reference.

## 🚀 Versión 3.6.0 (Septiembre 2026)
### Módulo de Reportes Demográficos RUFE
Se integró un pipeline de limpieza y consolidación de datos para la generación de reportes demográficos deduplicados, listos para exportación visual:
* **Limpieza de Género:** Implementación de heurísticas basadas en `parentesco` y diccionarios de nombres para reducir los registros no identificados a casi 0%.
* **Clasificación de Entidades:** Aislamiento de personas jurídicas y empresas.
* **Módulos de Reporte:** Pertenencia Étnica, Rangos de Edad y Población Víctima del Conflicto Armado.
* **Exportación Visual:** Generador de tablas gráficas interactivas vía Python (`matplotlib`) para WhatsApp.
