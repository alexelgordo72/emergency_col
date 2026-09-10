# ETL SGRD - Procesamiento de RUFE

Módulo de **Extracción, Transformación y Carga (ETL)** de los formularios RUFE (Registro Único de Familias en Emergencia) desde PDFs escaneados hacia la base de datos PostgreSQL.

## 🎯 Objetivo

Procesar los PDFs de RUFE que están en `~/Desktop/SGRD 2026/` (organizados por fecha), extraer la información usando **Gemini 3.1 Flash Lite** (visión), y cargarla en las tablas:
- `reportes_comunitarios`
- `rufe_formularios`
- `rufe_personas`

## 📋 Estructura

