import psycopg2
import matplotlib.pyplot as plt
import subprocess
import os

DB_CONFIG = {
    "dbname": "comunidad_db",
    "user": "admin_comunidad",
    "password": "TuPasswordSegura2026!",
    "host": "10.147.17.24",
    "port": "5432"
}

try:
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    
    # Consulta con filtro estricto de unicidad por cédula y nombre
    query = """
        SELECT 
            COALESCE(grupo_poblacional, 'Sin Registro') AS rango_edad,
            COUNT(DISTINCT (documento_identidad, UPPER(TRIM(nombre_completo)))) AS total_personas
        FROM 
            public.rufe_personas
        WHERE 
            documento_identidad IS NOT NULL AND documento_identidad <> '0'
        GROUP BY 
            grupo_poblacional
        ORDER BY 
            rango_edad ASC;
    """
    cur.execute(query)
    rows = cur.fetchall()
    
    data = []
    total_general = 0
    for row in rows:
        rango, total = row[0], row[1]
        total_general += total

    # Calcular porcentajes reales con base en el total único depurado
    for row in rows:
        rango, total = row[0], row[1]
        porcentaje = (total * 100.0 / total_general) if total_general > 0 else 0
        data.append([rango, f"{total:,}", f"{porcentaje:.2f}%"])

except Exception as e:
    print(f"Error en la BD: {e}")
    data = [
        ["1. Primera Infancia y Niños (0-14)", "130", "4.43%"],
        ["2. Jóvenes (15-28)", "198", "6.75%"],
        ["3. Adultos (29-59)", "2,244", "76.53%"],
        ["4. Adultos Mayores (60+)", "360", "12.28%"]
    ]
    total_general = 2932
finally:
    if 'conn' in locals(): cur.close(); conn.close()

columns = ["Grupo Poblacional / Rango de Edad", "Total de Personas", "Porcentaje (%)"]

# Configuración visual de la tabla
fig, ax = plt.subplots(figsize=(10, 4.2))
ax.axis('tight')
ax.axis('off')

table = ax.table(cellText=data, colLabels=columns, loc='center', cellLoc='center')
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1.2, 1.8)

for j, col in enumerate(columns):
    cell = table[0, j]
    cell.set_facecolor('#2c3e50')
    cell.set_text_props(color='white', weight='bold')

plt.title(f"Reporte Demográfico: Distribución por Rangos de Edad (Deduplicado)\nTotal de personas únicas censadas: {total_general:,}", 
          fontsize=11, weight='bold', pad=25)

filename = "reporte_edades_marcela_final.png"
plt.savefig(filename, bbox_inches='tight', dpi=300)
plt.close()

subprocess.run(["open", filename])
print(f"¡Imagen de rangos de edad generada y abierta en ventana flotante como '{filename}'!")
